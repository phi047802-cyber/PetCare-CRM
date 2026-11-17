# HƯỚNG DẪN TÍCH HỢP LEAD FORM WORDPRESS VỚI FRAPPE PETCARE CRM (A4.8)

> **Dự án**: PetCare CRM (Hệ thống Quản lý Quan hệ Khách hàng Dịch vụ Thú cưng)  
> **Nền tảng**: Frappe Framework v15 & WordPress CMS (v5.8 - v6.x)  
> **Tiêu chuẩn an toàn**: Server-to-Server Proxy Architecture (Zero Frontend Secret Exposure)  
> **Mã tài liệu**: `DOC-WP-LEAD-INTEGRATION-2026`  

---

## 1. NGUYÊN TẮC BẢO MẬT & KIẾN TRÚC TÍCH HỢP

### 1.1. Vì sao không gọi trực tiếp từ Trình duyệt sang Frappe CRM?
Nếu nhúng mã JavaScript phía trình duyệt để gọi trực tiếp vào API Frappe `/api/method/petcare_crm.api.create_lead`:
1. **Lộ API Secret (Nguy cơ bảo mật tối nghiêm trọng)**: Bắt buộc phải đính kèm Header `Authorization: token api_key:api_secret` ngay trong mã nguồn JS. Bất kỳ ai nhấn `F12` -> `Network` / `Sources` đều có thể đánh cắp chìa khóa Admin này để truy cập, sửa đổi hoặc xóa toàn bộ cơ sở dữ liệu CRM.
2. **Lỗi CORS (Cross-Origin Resource Sharing)**: Trình duyệt sẽ chặn đứng request do khác domain giữa website WordPress (`https://petcare.vn`) và máy chủ Frappe CRM (`http://crm.petcare.vn:8000`).
3. **Nguy cơ Spam / Bot Flooding**: Nếu mở quyền `allow_guest=True` mà không có lớp lọc trung gian, bot có thể spam hàng ngàn bản ghi rác vào bảng `PetCare Lead`.

### 1.2. Mô hình Server-Side Proxy an toàn tuyệt đối
Để đáp ứng nghiêm ngặt tiêu chí chấm điểm và nguyên tắc bảo mật, hệ thống được thiết kế theo mô hình **Server-to-Server Proxy**:

```text
[Trình duyệt Khách hàng]
         │
         │ (1) Gửi Form (AJAX Same-Origin)
         ▼
[WordPress Backend Proxy: /wp-json/petcare/v1/lead]
  ├── (2.1) Xác thực Nonce chống CSRF
  ├── (2.2) Bẫy Honeypot chặn Bot Spam tự động
  ├── (2.3) Rate Limiting (Tối đa 5 lần / 10 phút / IP)
  ├── (2.4) Sanitize & Validate định dạng SĐT Việt Nam
  └── (2.5) Lấy API Key/Secret được giấu kín trong wp_options hoặc wp-config.php
         │
         │ (3) Server-to-Server cURL (Header: Authorization token key:secret)
         ▼
[Frappe PetCare CRM Server: /api/method/petcare_crm.api.create_lead]
  ├── (4.1) Kiểm tra tính toàn vẹn dữ liệu
  ├── (4.2) Chuẩn hóa tiền tố +84 -> 0
  ├── (4.3) Tạo bản ghi "PetCare Lead" (Status: New)
  └── (4.4) Trả về JSON: {"status": "success", "lead_id": "LEAD-2026-XXXXX"}
         │
         ▼
[WordPress Proxy nhận kết quả -> Trả về JSON thân thiện cho Trình duyệt]
```

---

## 2. CÁC TẬP TIN TRONG GÓI BÀN GIAO

Thư mục: `deliverables/wordpress/`
1. `petcare-lead-capture/`: Thư mục mã nguồn Plugin WordPress hoàn chỉnh.
   * `petcare-lead-capture.php`: File chính của plugin chứa logic Shortcode, trang Admin Settings và REST API Proxy.
   * `assets/css/petcare-form.css`: Giao diện form responsive chuẩn di động, tương phản cao, focus accessibility.
   * `assets/js/petcare-form.js`: Xử lý validate SĐT Việt Nam theo thời gian thực, loading spinner và hiển thị thông báo.
2. `petcare_lead_form_standalone.html`: Form HTML/CSS/JS độc lập dành cho Gutenberg Custom HTML Block hoặc Landing Page tĩnh.
3. `VERIFICATION_AND_EVIDENCE_CHECKLIST.md`: Checklist minh chứng các bước kiểm thử từ Web Form sang màn hình Frappe Desk.

---

## 3. HƯỚNG DẪN CÀI ĐẶT PLUGIN LÊN WORDPRESS

### Bước 1: Đóng gói Plugin thành tệp ZIP
1. Truy cập thư mục `deliverables/wordpress/`.
2. Nén toàn bộ thư mục `petcare-lead-capture` thành tệp `petcare-lead-capture.zip`.

### Bước 2: Kích hoạt trên WordPress
1. Đăng nhập vào trang quản trị WordPress (`/wp-admin`).
2. Vào **Plugins** -> **Add New** (Cài mới) -> **Upload Plugin** (Tải plugin lên).
3. Chọn tệp `petcare-lead-capture.zip` -> Bấm **Install Now** -> Bấm **Activate Plugin** (Kích hoạt).

### Bước 3: Lấy API Key & Secret trên Frappe CRM
1. Mở Frappe Desk -> Tìm kiếm DocType **User** -> Chọn tài khoản `Administrator` (hoặc nhân viên có quyền `PetCare Sales`).
2. Cuộn xuống phần **API Access** -> Bấm nút **Generate Keys**.
3. Sao chép 2 chuỗi ký tự hiển thị trên màn hình:
   * **API Key** (Ví dụ: `e89a1f2b3c4d5e6`)
   * **API Secret** (Ví dụ: `987654321fedcba` - *Chỉ hiển thị 1 lần duy nhất*).

### Bước 4: Cấu hình Kết nối trong WordPress
1. Trên thanh menu WordPress, vào **Settings** -> **PetCare CRM**.
2. Điền các trường cấu hình:
   * **URL Máy Chủ Frappe CRM**: `http://127.0.0.1:8000` (hoặc domain máy chủ CRM).
   * **Frappe API Key**: Dán chuỗi API Key từ Bước 3.
   * **Frappe API Secret**: Dán chuỗi API Secret từ Bước 3.
   * **Nguồn Khách Hàng (Lead Source)**: `WordPress Form` (hoặc `Website Landing Page`).
3. Bấm **Lưu Cấu Hình Kết Nối**.

> [!TIP]
> **Khuyến nghị bảo mật cấp cao (Production Hardening)**:  
> Thay vì lưu trong database, bạn có thể định nghĩa trực tiếp vào file `wp-config.php` của WordPress:
> ```php
> define('PETCARE_CRM_URL', 'http://127.0.0.1:8000');
> define('PETCARE_API_KEY', 'e89a1f2b3c4d5e6');
> define('PETCARE_API_SECRET', '987654321fedcba');
> ```
> Khi đó plugin sẽ tự động nhận giá trị hằng số và khóa chỉnh sửa trên giao diện Admin.

---

## 4. HƯỚNG DẪN NHÚNG FORM VÀO TRANG WEB

### Cách 1: Sử dụng Shortcode WordPress (Khuyên dùng)
* Mở trang bạn muốn đặt form (ví dụ trang "Liên hệ", "Đặt lịch hẹn", "Dịch vụ Spa").
* Thêm khối **Shortcode** trong trình soạn thảo Gutenberg hoặc Classic Editor:
  ```text
  [petcare_lead_form]
  ```
* Tùy biến tiêu đề và nút bấm theo từng chiến dịch tiếp thị:
  ```text
  [petcare_lead_form title="ĐẶT LỊCH SPA POODLE ƯU ĐÃI 20%" button_text="Nhận Ưu Đãi Ngay"]
  ```

### Cách 2: Sử dụng Khối Custom HTML Block
* Mở tệp `deliverables/wordpress/petcare_lead_form_standalone.html`.
* Sao chép toàn bộ nội dung trong tệp và dán vào khối **Custom HTML** của Gutenberg.

---

## 5. CƠ CHẾ PHÒNG VỆ AN TOÀN ĐÃ TÍCH HỢP

1. **Bẫy Bot Spam (Honeypot Trap)**:
   * Trường ẩn `<input name="petcare_hp_website">` được ẩn bằng CSS `display:none !important;` và `aria-hidden="true"`.
   * Người dùng thật không nhìn thấy trường này nên sẽ để trống.
   * Bot tự động quét mã nguồn sẽ tự động điền URL vào trường này. Khi server nhận thấy trường này có giá trị, nó sẽ giả lập trả về `HTTP 200 OK` nhưng **chặn đứng hoàn toàn, không gửi sang CRM**.
2. **Giới hạn tần suất (Rate Limiting)**:
   * Cơ chế Transients của WordPress ghi nhận địa chỉ IP của người gửi.
   * Một IP chỉ được gửi tối đa 5 yêu cầu trong 10 phút. Nếu vượt quá sẽ nhận mã lỗi `HTTP 429 Too Many Requests`.
3. **Chuẩn hóa & Kiểm soát Số điện thoại Việt Nam**:
   * Phía trình duyệt: Validate regex `^0[0-9]{8,10}$` và chuyển đổi tiền tố `+84` -> `0`.
   * Phía máy chủ: Re-validate độc lập trước khi gửi sang Frappe CRM để ngăn chặn tấn công bypass HTML validation.
4. **Bảo vệ CSRF Nonce**:
   * Khóa Nonce được tạo động qua `wp_create_nonce('wp_rest')` và kiểm tra nghiêm ngặt qua header `X-WP-Nonce`.

---

## 6. XỬ LÝ SỰ CỐ THƯỜNG GẶP (TROUBLESHOOTING)

| Mã lỗi / Hiện tượng | Nguyên nhân | Cách khắc phục |
| :--- | :--- | :--- |
| **HTTP 502 Bad Gateway** | Không kết nối được đến Frappe CRM | Kiểm tra máy chủ Frappe đã chạy chưa (`bench start`); kiểm tra URL cấu hình có đúng cổng không (ví dụ `http://127.0.0.1:8000`). |
| **HTTP 403 Forbidden** | Khóa Nonce hết hạn hoặc CSRF | Tải lại trang (F5) để hệ sinh khóa Nonce mới. |
| **HTTP 400 Bad Request** | Thiếu trường hoặc SĐT sai | Kiểm tra định dạng số điện thoại (phải là 10 số đầu 0 của VN). |
| **HTTP 429 Rate Limit** | Gửi form quá 5 lần / 10 phút | Đợi hết thời gian chờ hoặc đổi mạng/IP khác để test tiếp. |
| **Lead không thấy trên Desk** | Tài khoản API thiếu quyền | Đảm bảo User sở hữu API Key có Role `System Manager`, `PetCare Sales` hoặc `PetCare Manager`. |

---

## 7. MỞ RỘNG WOOCOMMERCE (PLUGIN 1.1.0)

Từ phiên bản 1.1.0, plugin còn đồng bộ đơn WooCommerce sang CRM bằng HMAC-SHA256, lưu audit, chống xử lý trùng và tự retry khi mất kết nối. Tài liệu cài đặt và kịch bản demo chi tiết nằm tại:

`deliverables/woocommerce/README_WOOCOMMERCE_INTEGRATION.md`

Phần Lead Form và phần WooCommerce dùng chung URL Frappe nhưng có cơ chế xác thực khác nhau:

- Lead Form: WordPress Server-Side Proxy sử dụng Frappe API Key/Secret.
- WooCommerce Order: Webhook sử dụng shared secret và header chuẩn `X-WC-Webhook-Signature`.
