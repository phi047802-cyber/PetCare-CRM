<?php
/**
 * WooCommerce -> PetCare CRM order synchronization.
 *
 * Loaded by the PetCare CRM Lead Capture plugin. This file deliberately uses
 * WooCommerce public APIs only, so it remains inactive when WooCommerce is not
 * installed.
 */

if (!defined('ABSPATH')) {
    exit;
}

class PetCare_WooCommerce_Sync {

    private const RETRY_HOOK = 'petcare_retry_woocommerce_order_sync';
    private const MAX_ATTEMPTS = 3;

    public function __construct() {
        add_action('woocommerce_checkout_order_processed', [$this, 'handle_order_created'], 20, 3);
        add_action('woocommerce_order_status_changed', [$this, 'handle_status_changed'], 20, 4);
        add_action(self::RETRY_HOOK, [$this, 'retry_sync'], 10, 3);
        add_filter('woocommerce_order_actions', [$this, 'register_manual_order_action']);
        add_action('woocommerce_order_action_petcare_sync_order', [$this, 'handle_manual_order_action']);
    }

    public function handle_order_created($order_id, $posted_data = [], $order = null) {
        $this->send_order($order ?: $order_id, 'order.created', 1);
    }

    public function handle_status_changed($order_id, $old_status, $new_status, $order) {
        $this->send_order($order ?: $order_id, 'order.updated', 1);
    }

    public function retry_sync($order_id, $topic, $attempt) {
        $this->send_order($order_id, $topic, (int)$attempt);
    }

    public function register_manual_order_action($actions) {
        $actions['petcare_sync_order'] = __('Đồng bộ lại sang PetCare CRM', 'petcare-lead-capture');
        return $actions;
    }

    public function handle_manual_order_action($order) {
        $this->send_order($order, 'order.updated', 1);
    }

    /**
     * Send a normalized order payload to Frappe with native Woo HMAC headers.
     */
    public function send_order($order_or_id, $topic = 'order.updated', $attempt = 1) {
        if (!function_exists('wc_get_order')) {
            return false;
        }

        $order = is_object($order_or_id) ? $order_or_id : wc_get_order($order_or_id);
        if (!$order) {
            return false;
        }

        $crm_url = defined('PETCARE_CRM_URL')
            ? PETCARE_CRM_URL
            : get_option('petcare_crm_url', 'http://127.0.0.1:8000');
        $secret = defined('PETCARE_WC_WEBHOOK_SECRET')
            ? PETCARE_WC_WEBHOOK_SECRET
            : get_option('petcare_wc_webhook_secret', '');
        $enabled = (bool)get_option('petcare_wc_sync_enabled', 0);

        if (!$enabled && !defined('PETCARE_WC_WEBHOOK_SECRET')) {
            return false;
        }
        if (empty($crm_url) || empty($secret)) {
            $order->add_order_note('PetCare CRM: chưa cấu hình URL hoặc WooCommerce webhook secret.');
            return false;
        }

        $payload = $this->build_payload($order);
        $body = wp_json_encode($payload, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
        $signature = base64_encode(hash_hmac('sha256', $body, $secret, true));
        $delivery_id = function_exists('wp_generate_uuid4')
            ? wp_generate_uuid4()
            : uniqid('petcare-', true);

        $endpoint = rtrim($crm_url, '/') . '/api/method/petcare_crm.api.woocommerce_order_webhook';
        $is_local = strpos($crm_url, '127.0.0.1') !== false || strpos($crm_url, 'localhost') !== false;
        $response = wp_remote_post($endpoint, [
            'headers' => [
                'Content-Type'                 => 'application/json; charset=utf-8',
                'Accept'                       => 'application/json',
                'X-WC-Webhook-Signature'       => $signature,
                'X-WC-Webhook-Topic'           => sanitize_text_field($topic),
                'X-WC-Webhook-Delivery-ID'     => $delivery_id,
                'X-WC-Webhook-Source'          => home_url('/'),
                'X-PetCare-Integration-Version'=> PETCARE_LEAD_VERSION,
            ],
            'body'      => $body,
            'timeout'   => 20,
            'sslverify' => apply_filters('petcare_crm_sslverify', !$is_local),
        ]);

        if (is_wp_error($response)) {
            $this->record_failure($order, $topic, $attempt, $response->get_error_message());
            return false;
        }

        $status_code = (int)wp_remote_retrieve_response_code($response);
        $response_body = json_decode(wp_remote_retrieve_body($response), true);
        if ($status_code < 200 || $status_code >= 300) {
            $error = isset($response_body['message']) && is_string($response_body['message'])
                ? $response_body['message']
                : 'HTTP ' . $status_code;
            $this->record_failure($order, $topic, $attempt, $error);
            return false;
        }

        $result = $response_body['message'] ?? [];
        $sync_id = sanitize_text_field($result['sync_id'] ?? 'unknown');
        $duplicate = !empty($result['duplicate']) ? ' (delivery trùng, không ghi lặp)' : '';
        $order->update_meta_data('_petcare_crm_sync_id', $sync_id);
        $order->update_meta_data('_petcare_crm_last_delivery_id', $delivery_id);
        $order->update_meta_data('_petcare_crm_last_synced_at', current_time('mysql', true));
        $order->save();
        $order->add_order_note("PetCare CRM: đồng bộ thành công [{$sync_id}]{$duplicate}.");
        do_action('petcare_crm_order_synced', $order->get_id(), $result);
        return true;
    }

    private function record_failure($order, $topic, $attempt, $error) {
        $safe_error = sanitize_text_field($error);
        $order->add_order_note("PetCare CRM: lần đồng bộ {$attempt} thất bại - {$safe_error}");

        if ($attempt >= self::MAX_ATTEMPTS || !function_exists('as_schedule_single_action')) {
            do_action('petcare_crm_order_sync_failed', $order->get_id(), $safe_error);
            return;
        }

        $next_attempt = $attempt + 1;
        $args = [$order->get_id(), $topic, $next_attempt];
        if (!function_exists('as_has_scheduled_action') || !as_has_scheduled_action(self::RETRY_HOOK, $args, 'petcare-crm')) {
            as_schedule_single_action(
                time() + (60 * $next_attempt),
                self::RETRY_HOOK,
                $args,
                'petcare-crm'
            );
        }
    }

    private function build_payload($order) {
        $line_items = [];
        foreach ($order->get_items() as $item) {
            $product = $item->get_product();
            $line_items[] = [
                'product_id'   => $item->get_product_id(),
                'variation_id' => $item->get_variation_id(),
                'sku'          => $product ? $product->get_sku() : '',
                'name'         => $item->get_name(),
                'quantity'     => $item->get_quantity(),
                'total'        => $item->get_total(),
            ];
        }

        return [
            'id'            => $order->get_id(),
            'number'        => $order->get_order_number(),
            'status'        => $order->get_status(),
            'currency'      => $order->get_currency(),
            'total'         => $order->get_total(),
            'date_created'  => $order->get_date_created() ? $order->get_date_created()->date('c') : null,
            'customer_id'   => $order->get_customer_id(),
            'customer_note' => $order->get_customer_note(),
            'site_url'      => home_url('/'),
            'billing'       => [
                'first_name' => $order->get_billing_first_name(),
                'last_name'  => $order->get_billing_last_name(),
                'email'      => $order->get_billing_email(),
                'phone'      => $order->get_billing_phone(),
            ],
            'line_items' => $line_items,
            'meta_data'  => [
                ['key' => '_petcare_pet_name', 'value' => $order->get_meta('_petcare_pet_name', true)],
                ['key' => '_petcare_pet_species', 'value' => $order->get_meta('_petcare_pet_species', true)],
                ['key' => '_petcare_pet_breed', 'value' => $order->get_meta('_petcare_pet_breed', true)],
            ],
        ];
    }
}

