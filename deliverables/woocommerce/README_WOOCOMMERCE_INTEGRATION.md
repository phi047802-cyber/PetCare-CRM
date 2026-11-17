# TÍCH HỢP ĐƠN HÀNG WOOCOMMERCE VỚI PETCARE CRM

## 1. Mục tiêu

Module đồng bộ đơn hàng WooCommerce vào Frappe PetCare CRM, hoàn thiện phần “hứng đơn hàng từ WooCommerce” của tiêu chí A4.8.

Luồng chính:

```text
WooCommerce Order
  -> WordPress tạo JSON và chữ ký HMAC-SHA256
  -> POST /api/method/petcare_crm.api.woocommerce_order_webhook
  -> Frappe xác thực chữ ký và Delivery ID
  -> Tìm hoặc tạo Contact
  -> Tìm hoặc tạo Pet nếu checkout có thông tin thú cưng
  -> Tạo/cập nhật PetCare Opportunity
  -> Lưu WooCommerce Order Sync để audit và chống xử lý trùng
```

## 2. Thành phần đã triển khai

- WordPress/WooCommerce hooks:
  - `woocommerce_checkout_order_processed`
  - `woocommerce_order_status_changed`
  - Order Action “Đồng bộ lại sang PetCare CRM”
- HMAC-SHA256 theo chuẩn `X-WC-Webhook-Signature` của WooCommerce.
- Action Scheduler retry tối đa 3 lần khi CRM tạm thời không kết nối được.
- Idempotency theo hai cấp:
  - `X-WC-Webhook-Delivery-ID` ngăn xử lý lại cùng một delivery.
  - `external_order_key = SHA256(site_url + order_id)` ngăn tạo trùng đơn giữa các lần gửi.
- Mapping trạng thái:

| WooCommerce | PetCare Opportunity |
|---|---|
| `pending`, `checkout-draft` | `Proposal` |
| `on-hold` | `Negotiation` |
| `processing`, `completed` | `Closed Won` |
| `cancelled`, `failed`, `refunded`, `trash` | `Closed Lost` |

## 3. Cấu hình Frappe

Chạy trong thư mục Frappe Bench:

```bash
bench --site petcare.localhost set-config woocommerce_webhook_secret "THAY_BANG_CHUOI_BI_MAT_DAI"
bench --site petcare.localhost set-config woocommerce_sales_owner "Administrator"
bench --site petcare.localhost migrate
bench restart
```

`woocommerce_webhook_secret` phải trùng tuyệt đối với secret cấu hình trong WordPress.

Endpoint:

```text
POST https://crm.example.vn/api/method/petcare_crm.api.woocommerce_order_webhook
```

## 4. Cấu hình WordPress

1. Cài WooCommerce.
2. Cài plugin `petcare-lead-capture.zip` phiên bản 1.1.0.
3. Vào `Settings -> PetCare CRM`.
4. Nhập URL máy chủ Frappe.
5. Bật “Đồng Bộ Đơn WooCommerce”.
6. Nhập cùng Webhook Secret đã đặt trên Frappe.

Khuyến nghị không lưu secret trong database WordPress production. Khai báo trong `wp-config.php`:

```php
define('PETCARE_CRM_URL', 'https://crm.example.vn');
define('PETCARE_WC_WEBHOOK_SECRET', 'THAY_BANG_CHUOI_BI_MAT_DAI');
```

## 5. Thông tin thú cưng tại checkout

Module tự nhận ba order meta nếu website có form checkout tùy biến:

```text
_petcare_pet_name
_petcare_pet_species
_petcare_pet_breed
```

Nếu không có `_petcare_pet_name`, CRM vẫn tạo Contact và Opportunity nhưng không tự tạo hồ sơ Pet giả.

## 6. Kiểm thử

Chạy riêng suite WooCommerce:

```powershell
python -m unittest -v apps/petcare_crm/petcare_crm/tests/test_woocommerce_integration.py
```

Chạy toàn bộ hệ thống:

```powershell
python apps/petcare_crm/petcare_crm/tests/run_all_tests.py
```

## 7. Kịch bản demo cá nhân

1. Mở WooCommerce và tạo đơn cho dịch vụ “Gói Spa Toàn Diện”.
2. Nhập tên, số điện thoại và thông tin thú cưng.
3. Hoàn tất checkout.
4. Mở Order Notes để chứng minh CRM trả về `sync_id`.
5. Mở Frappe Desk -> PetCare CRM -> WooCommerce Orders.
6. Mở bản ghi sync và chỉ các liên kết Contact, Pet, Opportunity.
7. Chuyển WooCommerce order sang `Cancelled`.
8. Làm mới Frappe và chứng minh Opportunity chuyển sang `Closed Lost`.
9. Gửi lại cùng Delivery ID trong Postman để chứng minh `duplicate: true`.
10. Sửa một ký tự trong body nhưng giữ signature cũ để chứng minh CRM từ chối request giả mạo.

## 8. Tệp mã nguồn chính

- `deliverables/wordpress/petcare-lead-capture/includes/class-petcare-woocommerce-sync.php`
- `apps/petcare_crm/petcare_crm/utils/woocommerce_service.py`
- `apps/petcare_crm/petcare_crm/api.py`
- `apps/petcare_crm/petcare_crm/petcare_crm/doctype/woocommerce_order_sync/`
- `apps/petcare_crm/petcare_crm/tests/test_woocommerce_integration.py`

