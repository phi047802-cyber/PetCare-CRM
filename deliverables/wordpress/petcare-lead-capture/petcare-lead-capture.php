<?php
/**
 * Plugin Name: PetCare CRM Lead Capture
 * Plugin URI:  https://github.com/petcare-crm
 * Description: Tích hợp Form Đặt Lịch & Tư Vấn Chăm Sóc Thú Cưng cho WordPress kết nối bảo mật qua Server-Side Proxy với Frappe PetCare CRM.
 * Version:     1.1.0
 * Author:      PetCare CRM Development Team
 * License:     GPL-2.0+
 * Text Domain: petcare-lead-capture
 */

if (!defined('ABSPATH')) {
    exit; // Chặn truy cập trực tiếp
}

define('PETCARE_LEAD_VERSION', '1.1.0');
define('PETCARE_LEAD_PLUGIN_DIR', plugin_dir_path(__FILE__));
define('PETCARE_LEAD_PLUGIN_URL', plugin_dir_url(__FILE__));

class PetCare_Lead_Capture {

    private static $instance = null;

    public static function get_instance() {
        if (self::$instance === null) {
            self::$instance = new self();
        }
        return self::$instance;
    }

    private function __construct() {
        // Đăng ký Shortcode
        add_shortcode('petcare_lead_form', [$this, 'render_lead_form']);

        // Đăng ký Assets (CSS/JS)
        add_action('wp_enqueue_scripts', [$this, 'register_assets']);

        // Đăng ký REST API Endpoint Proxy
        add_action('rest_api_init', [$this, 'register_rest_routes']);

        // Màn hình cài đặt Admin
        if (is_admin()) {
            add_action('admin_menu', [$this, 'add_admin_menu']);
            add_action('admin_init', [$this, 'register_settings']);
        }

        // WooCommerce order synchronization (inactive when WooCommerce is absent).
        require_once PETCARE_LEAD_PLUGIN_DIR . 'includes/class-petcare-woocommerce-sync.php';
        new PetCare_WooCommerce_Sync();
    }

    /**
     * Đăng ký CSS và JS
     */
    public function register_assets() {
        wp_register_style(
            'petcare-form-style',
            PETCARE_LEAD_PLUGIN_URL . 'assets/css/petcare-form.css',
            [],
            PETCARE_LEAD_VERSION
        );

        wp_register_script(
            'petcare-form-script',
            PETCARE_LEAD_PLUGIN_URL . 'assets/js/petcare-form.js',
            [],
            PETCARE_LEAD_VERSION,
            true
        );
    }

    /**
     * Render Shortcode [petcare_lead_form]
     */
    public function render_lead_form($atts) {
        wp_enqueue_style('petcare-form-style');
        wp_enqueue_script('petcare-form-script');

        // Truyền tham số bảo mật Nonce & REST URL vào JS
        wp_localize_script('petcare-form-script', 'PetCareConfig', [
            'rest_url' => esc_url_raw(rest_url('petcare/v1/lead')),
            'nonce'    => wp_create_nonce('wp_rest'),
        ]);

        $atts = shortcode_atts([
            'title'       => 'ĐẶT LỊCH HẸN & TƯ VẤN CHĂM SÓC THÚ CƯNG',
            'subtitle'    => 'Để lại thông tin để nhận tư vấn chuyên môn và ưu đãi dịch vụ từ đội ngũ Bác sĩ & Chuyên viên PetCare.',
            'button_text' => 'Gửi Thông Tin Đặt Lịch Ngay',
        ], $atts, 'petcare_lead_form');

        ob_start();
        ?>
        <div class="petcare-lead-container" id="petcare-lead-wrapper">
            <div class="petcare-lead-header">
                <div class="petcare-lead-badge">🐾 PetCare Care Intelligence</div>
                <h3 class="petcare-lead-title"><?php echo esc_html($atts['title']); ?></h3>
                <p class="petcare-lead-subtitle"><?php echo esc_html($atts['subtitle']); ?></p>
            </div>

            <!-- Khung thông báo phản hồi (Accessibility ARIA Live) -->
            <div id="petcare-form-alert" class="petcare-alert petcare-hidden" role="alert" aria-live="assertive"></div>

            <form id="petcare-lead-form" class="petcare-form" novalidate>
                <!-- BẪY BOT SPAM (HONEYPOT) - Ẩn hoàn toàn với người dùng thật -->
                <div class="petcare-hp-wrap" aria-hidden="true" style="display:none !important;">
                    <label for="petcare_hp_website">Website URL (Leave blank)</label>
                    <input type="text" id="petcare_hp_website" name="petcare_hp_website" tabindex="-1" autocomplete="off">
                </div>

                <div class="petcare-form-grid">
                    <!-- Họ tên chủ nuôi -->
                    <div class="petcare-form-group">
                        <label for="petcare_lead_name" class="petcare-label">
                            Họ và Tên Chủ Nuôi <span class="petcare-required" aria-hidden="true">*</span>
                        </label>
                        <input type="text" id="petcare_lead_name" name="lead_name" class="petcare-input" 
                               placeholder="Ví dụ: Nguyễn Văn An" required aria-required="true">
                        <span class="petcare-error-text" id="error_lead_name"></span>
                    </div>

                    <!-- Số điện thoại -->
                    <div class="petcare-form-group">
                        <label for="petcare_phone" class="petcare-label">
                            Số Điện Thoại Liên Hệ <span class="petcare-required" aria-hidden="true">*</span>
                        </label>
                        <input type="tel" id="petcare_phone" name="phone" class="petcare-input" 
                               placeholder="Ví dụ: 0912345678" pattern="^0[0-9]{8,10}$" required aria-required="true">
                        <span class="petcare-error-text" id="error_phone"></span>
                    </div>
                </div>

                <div class="petcare-form-grid">
                    <!-- Email -->
                    <div class="petcare-form-group">
                        <label for="petcare_email" class="petcare-label">Địa Chỉ Email (Tùy chọn)</label>
                        <input type="email" id="petcare_email" name="email" class="petcare-input" 
                               placeholder="email@example.com">
                        <span class="petcare-error-text" id="error_email"></span>
                    </div>

                    <!-- Dịch vụ quan tâm -->
                    <div class="petcare-form-group">
                        <label for="petcare_service_type" class="petcare-label">Dịch Vụ Quan Tâm</label>
                        <select id="petcare_service_type" name="service_type" class="petcare-select">
                            <option value="Tắm Spa & Cắt Tỉa Lông Toàn Diện">Tắm Spa & Cắt Tỉa Lông Toàn Diện (Grooming)</option>
                            <option value="Khám Sức Khỏe & Chẩn Đoán Lâm Sàng">Khám Sức Khỏe & Thú Y Lâm Sàng</option>
                            <option value="Tiêm Phòng Vắc-xin & Tẩy Giun Định Kỳ">Tiêm Phòng Vắc-xin & Phòng Bệnh</option>
                            <option value="Khách Sạn Thú Cưng Lưu Trú">Khách Sạn & Trông Giữ Thú Cưng (Pet Hotel)</option>
                            <option value="Tư Vấn Thẻ Hội Viên Tiết Kiệm">Đăng Ký Gói Thẻ Hội Viên VIP / Family Plan</option>
                        </select>
                    </div>
                </div>

                <!-- Thông tin thú cưng & nhu cầu -->
                <div class="petcare-form-group">
                    <label for="petcare_pet_info" class="petcare-label">Thông Tin Bé Cưng & Yêu Cầu Đặc Biệt</label>
                    <textarea id="petcare_pet_info" name="pet_info" class="petcare-textarea" rows="3" 
                              placeholder="Ví dụ: Bé Poodle 2 tuổi, nặng 4.5kg, cần tắm cắt lông tròn kiểu gấu Teddy và bấm móng..."></textarea>
                </div>

                <!-- Nút Submit có trạng thái Loading -->
                <div class="petcare-submit-wrap">
                    <button type="submit" id="petcare-submit-btn" class="petcare-submit-button">
                        <span class="petcare-btn-text"><?php echo esc_html($atts['button_text']); ?></span>
                        <span class="petcare-spinner petcare-hidden" aria-hidden="true"></span>
                    </button>
                </div>

                <div class="petcare-privacy-notice">
                    🔒 <em>Thông tin cá nhân được bảo mật theo tiêu chuẩn PetCare CRM. Chúng tôi cam kết không spam.</em>
                </div>
            </form>
        </div>
        <?php
        return ob_get_clean();
    }

    /**
     * Đăng ký REST API Route Proxy
     */
    public function register_rest_routes() {
        register_rest_route('petcare/v1', '/lead', [
            'methods'             => 'POST',
            'callback'            => [$this, 'handle_lead_submission'],
            'permission_callback' => '__return_true', // Kiểm tra qua Nonce, Honeypot & Rate-limit bên trong
        ]);
    }

    /**
     * Xử lý gửi Form phía Server-Side Proxy
     */
    public function handle_lead_submission(WP_REST_Request $request) {
        // 1. Kiểm tra CSRF Nonce
        $nonce = $request->get_header('X-WP-Nonce');
        if (!wp_verify_nonce($nonce, 'wp_rest')) {
            return new WP_REST_Response([
                'success' => false,
                'message' => 'Phiên làm việc đã hết hạn. Vui lòng tải lại trang và thử lại.',
            ], 403);
        }

        // 2. Kiểm tra Bẫy Bot Honeypot
        $hp_field = $request->get_param('petcare_hp_website');
        if (!empty($hp_field)) {
            // Trả về thành công giả lập để đánh lừa bot tự động, không ghi vào CRM
            return new WP_REST_Response([
                'success' => true,
                'message' => 'Cảm ơn bạn đã liên hệ. Đội ngũ PetCare sẽ phản hồi sớm nhất!',
                'lead_id' => 'LEAD-BOT-TRAPPED',
            ], 200);
        }

        // 3. Giới hạn tần suất gửi (Rate Limiting: tối đa 5 lần / 10 phút / IP)
        $client_ip = sanitize_text_field($_SERVER['REMOTE_ADDR'] ?? '127.0.0.1');
        $transient_key = 'petcare_rl_' . md5($client_ip);
        $request_count = get_transient($transient_key);

        if ($request_count !== false && (int)$request_count >= 5) {
            return new WP_REST_Response([
                'success' => false,
                'message' => 'Bạn đã gửi yêu cầu quá nhiều lần. Vui lòng đợi 10 phút trước khi gửi lại.',
            ], 429);
        }

        // 4. Thu thập & Làm sạch dữ liệu đầu vào (Sanitization)
        $lead_name    = sanitize_text_field($request->get_param('lead_name'));
        $phone        = sanitize_text_field($request->get_param('phone'));
        $email        = sanitize_email($request->get_param('email'));
        $service_type = sanitize_text_field($request->get_param('service_type'));
        $pet_info     = sanitize_textarea_field($request->get_param('pet_info'));

        // 5. Server-Side Validation nghiêm ngặt
        if (empty($lead_name)) {
            return new WP_REST_Response([
                'success' => false,
                'message' => 'Vui lòng nhập họ và tên của bạn.',
            ], 400);
        }

        if (empty($phone)) {
            return new WP_REST_Response([
                'success' => false,
                'message' => 'Vui lòng nhập số điện thoại liên hệ.',
            ], 400);
        }

        // Chuẩn hóa & kiểm tra số điện thoại Việt Nam
        $cleaned_phone = preg_replace('/[\s\-\.]/', '', $phone);
        if (strpos($cleaned_phone, '+84') === 0) {
            $cleaned_phone = '0' . substr($cleaned_phone, 3);
        }

        if (!preg_match('/^0[0-9]{8,10}$/', $cleaned_phone)) {
            return new WP_REST_Response([
                'success' => false,
                'message' => 'Số điện thoại không hợp lệ. Vui lòng nhập số điện thoại di động Việt Nam (ví dụ: 0912345678).',
            ], 400);
        }

        // 6. Lấy cấu hình kết nối Frappe CRM (ưu tiên hằng số trong wp-config.php)
        $crm_url    = defined('PETCARE_CRM_URL') ? PETCARE_CRM_URL : get_option('petcare_crm_url', 'http://127.0.0.1:8000');
        $api_key    = defined('PETCARE_API_KEY') ? PETCARE_API_KEY : get_option('petcare_api_key', '');
        $api_secret = defined('PETCARE_API_SECRET') ? PETCARE_API_SECRET : get_option('petcare_api_secret', '');
        $source     = get_option('petcare_lead_source', 'WordPress Form');

        $crm_url = rtrim($crm_url, '/');

        if (empty($crm_url)) {
            return new WP_REST_Response([
                'success' => false,
                'message' => 'Hệ thống CRM chưa được cấu hình. Vui lòng liên hệ quản trị viên website.',
            ], 500);
        }

        // Tổng hợp thông tin thú cưng & ghi chú
        $initial_pet_info = '';
        if (!empty($service_type)) {
            $initial_pet_info .= "Dịch vụ quan tâm: {$service_type}. ";
        }
        if (!empty($pet_info)) {
            $initial_pet_info .= "Ghi chú: {$pet_info}";
        }
        $initial_pet_info = trim($initial_pet_info);

        // 7. Chuẩn bị Payload gửi sang Frappe CRM (Server-to-Server cURL)
        $frappe_payload = [
            'lead_name'        => $lead_name,
            'phone'            => $cleaned_phone,
            'email'            => !empty($email) ? $email : null,
            'lead_source'      => $source,
            'priority'         => 'Medium',
            'initial_pet_info' => !empty($initial_pet_info) ? $initial_pet_info : null,
        ];

        $frappe_endpoint = $crm_url . '/api/method/petcare_crm.api.create_lead';

        $headers = [
            'Content-Type' => 'application/json',
            'Accept'       => 'application/json',
        ];

        // Nếu có API Key & Secret thì gắn Authorization header
        if (!empty($api_key) && !empty($api_secret)) {
            $headers['Authorization'] = 'token ' . $api_key . ':' . $api_secret;
        }

        // Gọi HTTP POST máy chủ-tới-máy chủ
        $response = wp_remote_post($frappe_endpoint, [
            'method'      => 'POST',
            'headers'     => $headers,
            'body'        => wp_json_encode($frappe_payload),
            'timeout'     => 15,
            'sslverify'   => false, // Hỗ trợ dev local self-signed SSL
        ]);

        // 8. Xử lý lỗi kết nối hạ tầng
        if (is_wp_error($response)) {
            return new WP_REST_Response([
                'success' => false,
                'message' => 'Không thể kết nối đến máy chủ PetCare CRM. Vui lòng gọi trực tiếp hotline để được hỗ trợ tức thì.',
                'debug'   => WP_DEBUG ? $response->get_error_message() : null,
            ], 502);
        }

        $http_code = wp_remote_retrieve_response_code($response);
        $body      = wp_remote_retrieve_body($response);
        $data      = json_decode($body, true);

        if ($http_code >= 200 && $http_code < 300) {
            // Tăng đếm rate limit sau khi gửi thành công
            set_transient($transient_key, ($request_count ? (int)$request_count + 1 : 1), 600);

            $lead_id = $data['message']['lead_id'] ?? 'LEAD-NEW';
            return new WP_REST_Response([
                'success' => true,
                'lead_id' => $lead_id,
                'message' => "Đăng ký thành công! Mã hồ sơ tư vấn của bạn là [{$lead_id}]. Bác sĩ/Tư vấn viên PetCare sẽ liên hệ trong ít phút.",
            ], 200);
        } else {
            // Bắt lỗi từ Frappe và làm sạch thông điệp an toàn cho khách hàng
            $error_message = 'Đã có lỗi xảy ra khi ghi nhận hồ sơ. Vui lòng kiểm tra lại thông tin hoặc liên hệ hotline.';
            if (isset($data['message']) && is_string($data['message'])) {
                $error_message = $data['message'];
            } elseif (isset($data['exc_type']) && $data['exc_type'] === 'ValidationError') {
                $error_message = 'Thông tin gửi lên không hợp lệ hoặc số điện thoại đã có hồ sơ đang xử lý.';
            }

            return new WP_REST_Response([
                'success' => false,
                'message' => $error_message,
            ], 400);
        }
    }

    /**
     * Màn hình quản trị cấu hình Admin (Settings -> PetCare CRM)
     */
    public function add_admin_menu() {
        add_options_page(
            'Cấu Hình PetCare CRM',
            'PetCare CRM',
            'manage_options',
            'petcare-crm-settings',
            [$this, 'render_admin_settings_page']
        );
    }

    public function register_settings() {
        register_setting('petcare_crm_options', 'petcare_crm_url', 'esc_url_raw');
        register_setting('petcare_crm_options', 'petcare_api_key', 'sanitize_text_field');
        register_setting('petcare_crm_options', 'petcare_api_secret', 'sanitize_text_field');
        register_setting('petcare_crm_options', 'petcare_lead_source', 'sanitize_text_field');
        register_setting('petcare_crm_options', 'petcare_wc_sync_enabled', 'absint');
        register_setting('petcare_crm_options', 'petcare_wc_webhook_secret', 'sanitize_text_field');
    }

    public function render_admin_settings_page() {
        $using_constants = defined('PETCARE_CRM_URL') && defined('PETCARE_API_KEY');
        ?>
        <div class="wrap">
            <h1>🐾 Cấu Hình Kết Nối PetCare CRM (Frappe Framework)</h1>
            <p>Thiết lập thông số kết nối Server-to-Server an toàn. Khóa bảo mật (Secret) được lưu trữ phía máy chủ WordPress và <strong>tuyệt đối không bị rò rỉ ra trình duyệt</strong>.</p>

            <?php if ($using_constants): ?>
                <div class="notice notice-info">
                    <p><strong>Lưu ý bảo mật:</strong> Hệ thống đang sử dụng cấu hình cố định thông qua hằng số bảo mật trong tệp <code>wp-config.php</code>.</p>
                </div>
            <?php endif; ?>

            <form method="post" action="options.php">
                <?php settings_fields('petcare_crm_options'); ?>
                <table class="form-table" role="presentation">
                    <tr>
                        <th scope="row"><label for="petcare_crm_url">URL Máy Chủ Frappe CRM</label></th>
                        <td>
                            <input name="petcare_crm_url" type="url" id="petcare_crm_url" 
                                   value="<?php echo esc_attr(defined('PETCARE_CRM_URL') ? PETCARE_CRM_URL : get_option('petcare_crm_url', 'http://127.0.0.1:8000')); ?>" 
                                   class="regular-text" <?php echo $using_constants ? 'readonly' : ''; ?> required>
                            <p class="description">Ví dụ: <code>http://127.0.0.1:8000</code> hoặc <code>https://crm.petcare.vn</code> (Không có dấu gạch chéo cuối).</p>
                        </td>
                    </tr>
                    <tr>
                        <th scope="row"><label for="petcare_api_key">Frappe API Key</label></th>
                        <td>
                            <input name="petcare_api_key" type="text" id="petcare_api_key" 
                                   value="<?php echo esc_attr(defined('PETCARE_API_KEY') ? '••••••••••••••••' : get_option('petcare_api_key', '')); ?>" 
                                   class="regular-text" <?php echo $using_constants ? 'readonly' : ''; ?> required>
                            <p class="description">Lấy trong Frappe Desk -> User -> Administrator -> API Access -> API Key.</p>
                        </td>
                    </tr>
                    <tr>
                        <th scope="row"><label for="petcare_api_secret">Frappe API Secret</label></th>
                        <td>
                            <input name="petcare_api_secret" type="password" id="petcare_api_secret" 
                                   value="<?php echo esc_attr(defined('PETCARE_API_SECRET') ? '••••••••••••••••' : get_option('petcare_api_secret', '')); ?>" 
                                   class="regular-text" <?php echo $using_constants ? 'readonly' : ''; ?> required>
                            <p class="description">Khóa bí mật API Secret chỉ sinh một lần trong Frappe Desk.</p>
                        </td>
                    </tr>
                    <tr>
                        <th scope="row"><label for="petcare_lead_source">Nguồn Khách Hàng (Lead Source)</label></th>
                        <td>
                            <input name="petcare_lead_source" type="text" id="petcare_lead_source" 
                                   value="<?php echo esc_attr(get_option('petcare_lead_source', 'WordPress Form')); ?>" 
                                   class="regular-text">
                            <p class="description">Mặc định: <code>WordPress Form</code> hoặc <code>Website Landing Page</code>.</p>
                        </td>
                    </tr>
                    <tr>
                        <th scope="row">Đồng Bộ Đơn WooCommerce</th>
                        <td>
                            <label>
                                <input name="petcare_wc_sync_enabled" type="hidden" value="0">
                                <input name="petcare_wc_sync_enabled" type="checkbox" value="1"
                                       <?php checked(1, (int)get_option('petcare_wc_sync_enabled', 0)); ?>>
                                Tự động gửi đơn mới và thay đổi trạng thái sang PetCare CRM
                            </label>
                        </td>
                    </tr>
                    <tr>
                        <th scope="row"><label for="petcare_wc_webhook_secret">WooCommerce Webhook Secret</label></th>
                        <td>
                            <input name="petcare_wc_webhook_secret" type="password" id="petcare_wc_webhook_secret"
                                   value="<?php echo esc_attr(defined('PETCARE_WC_WEBHOOK_SECRET') ? '••••••••••••••••' : get_option('petcare_wc_webhook_secret', '')); ?>"
                                   class="regular-text" <?php echo defined('PETCARE_WC_WEBHOOK_SECRET') ? 'readonly' : ''; ?>>
                            <p class="description">Phải trùng với <code>woocommerce_webhook_secret</code> trong <code>site_config.json</code> của Frappe. Khuyến nghị khai báo hằng <code>PETCARE_WC_WEBHOOK_SECRET</code> trong <code>wp-config.php</code>.</p>
                        </td>
                    </tr>
                </table>
                <?php if (!$using_constants) submit_button('Lưu Cấu Hình Kết Nối'); ?>
            </form>

            <hr>
            <h3>Hướng Dẫn Nhúng Form Vào Giao Diện</h3>
            <p>Sử dụng Shortcode sau để chèn form vào bất kỳ Bài viết (Post), Trang (Page) hoặc Widget nào:</p>
            <code>[petcare_lead_form]</code>
            <p>Tùy biến tiêu đề bằng tham số:</p>
            <code>[petcare_lead_form title="ĐĂNG KÝ SPA CHO BÉ CƯNG" button_text="Đặt Lịch Hôm Nay"]</code>
        </div>
        <?php
    }
}

// Khởi chạy Plugin
add_action('plugins_loaded', ['PetCare_Lead_Capture', 'get_instance']);
