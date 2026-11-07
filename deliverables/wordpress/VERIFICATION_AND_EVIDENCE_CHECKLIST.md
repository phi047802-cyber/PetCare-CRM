# TÀI LIỆU MINH CHỨNG & CHECKLIST KIỂM THỬ TÍCH HỢP WORDPRESS LEAD FORM (A4.8)

> **Dự án**: PetCare CRM  
> **Nền tảng**: WordPress (Frontend Form & Proxy) <-> Frappe Framework v15 (CRM Core)  
> **Mục tiêu**: Cung cấp bằng chứng kiểm thử từng bước (Step-by-Step Verification) từ thao tác người dùng trên website đến khi bản ghi xuất hiện trên giao diện quản trị Frappe Desk.  
> **Mã tài liệu**: `VERIF-WP-LEAD-2026`  

---

## 1. QUY TRÌNH KIỂM THỬ ĐẦU-CUỐI (END-TO-END VERIFICATION FLOW)

```text
[BƯỚC 1: ĐIỀN FORM WEBSITE]
Khách hàng truy cập website -> Điền thông tin đặt lịch -> Nhấn nút "Gửi Thông Tin"
         │
         ▼
[BƯỚC 2: KIỂM TRA REQUEST MẠNG]
F12 DevTools -> Network Tab -> Xem Request POST /wp-json/petcare/v1/lead
(Kiểm tra: Header có X-WP-Nonce, Body là JSON hợp lệ, KHÔNG có Secret của Frappe)
         │
         ▼
[BƯỚC 3: KIỂM TRA PHẢN HỒI RESPONSE]
Nhận HTTP 200 OK -> JSON: {"success": true, "lead_id": "LEAD-2026-XXXXX", ...}
Giao diện form hiển thị Alert thành công màu xanh
         │
         ▼
[BƯỚC 4: XÁC MINH TRÊN GIAO DIỆN FRAPPE DESK]
Đăng nhập Frappe Desk -> Mở danh sách "PetCare Lead" -> Tìm thấy bản ghi với mã tương ứng
(Kiểm tra: Tên khách hàng, SĐT đã chuẩn hóa, Nguồn WordPress, Chi tiết dịch vụ)
```

---

## 2. CHECKLIST HÌNH ẢNH MINH CHỨNG CẦN THU THẬP KHI BÁO CÁO

> [!IMPORTANT]
> **Quy ước trung thực**: Sinh viên chụp ảnh màn hình thật từ môi trường chạy máy chủ local/demo. Danh sách dưới đây chỉ rõ các góc chụp và thông tin bắt buộc phải xuất hiện trong ảnh minh chứng nộp cho Giảng viên.

| STT | Tên minh chứng | Màn hình cần chụp | Các yếu tố bắt buộc xuất hiện trong ảnh | Trạng thái |
| :---: | :--- | :--- | :--- | :---: |
| **IMG-01** | **Cấu hình Plugin trong WordPress** | `wp-admin` -> `Settings` -> `PetCare CRM` | • URL máy chủ CRM (ví dụ `http://127.0.0.1:8000`)<br>• Trường API Key có giá trị<br>• API Secret được che dạng password<br>• Nguồn: `WordPress Form` | `[CẦN CHỤP KHI DEMO]` |
| **IMG-02** | **Nhúng Form trên Page WordPress** | Trình soạn thảo Gutenberg | • Khối Shortcode `[petcare_lead_form]` hoặc Custom HTML Block trên trang Đặt Lịch | `[CẦN CHỤP KHI DEMO]` |
| **IMG-03** | **Giao diện Form trên Trình duyệt** | Trang web hiển thị trên PC & Điện thoại | • Form đẹp, responsive, có nhãn tiếng Việt rõ ràng<br>• Các ô nhập: Tên, SĐT, Email, Dịch vụ, Bé cưng<br>• Nút bấm gradient nổi bật | `[CẦN CHỤP KHI DEMO]` |
| **IMG-04** | **Thao tác Điền Dữ liệu Mẫu** | Form đã điền đầy đủ dữ liệu | • Họ tên: Nguyễn Văn An<br>• SĐT: `0912345678`<br>• Dịch vụ: Tắm Spa & Cắt Tỉa Lông Toàn Diện<br>• Ghi chú: Bé Poodle 4.5kg cần cạo lông chân | `[CẦN CHỤP KHI DEMO]` |
| **IMG-05** | **F12 DevTools: Request Payload** | `F12` -> Tab `Network` -> Header & Payload | • URL: `/wp-json/petcare/v1/lead`<br>• Request Method: `POST`<br>• Payload JSON chứa đúng các trường<br>• **Chứng minh: Không hề có API Key/Secret của Frappe trong Network** | `[CẦN CHỤP KHI DEMO]` |
| **IMG-06** | **F12 DevTools: Response JSON & UI Success** | Tab `Network` Response + Giao diện Web | • HTTP Status: `200 OK`<br>• Response: `{"success": true, "lead_id": "LEAD-2026-00001", ...}`<br>• Form chuyển sang thông báo màu xanh có mã Lead | `[CẦN CHỤP KHI DEMO]` |
| **IMG-07** | **Xác minh Lead trên Frappe Desk** | Frappe Desk -> `PetCare Lead List` | • Bản ghi mới xuất hiện trên đầu danh sách<br>• ID trùng khớp: `LEAD-2026-00001`<br>• Status: `New`<br>• Lead Source: `WordPress Form` hoặc `Website Landing Page` | `[CẦN CHỤP KHI DEMO]` |
| **IMG-08** | **Chi tiết Hồ sơ Lead trên Desk** | Mở form chi tiết của bản ghi vừa tạo | • Tên: Nguyễn Văn An<br>• SĐT: `0912345678`<br>• Mục `Initial Pet Info` có ghi rõ dịch vụ và thể trạng bé | `[CẦN CHỤP KHI DEMO]` |

---

## 3. CHI TIẾT CÁC BƯỚC THỰC THI & PAYLOAD MẪU

### Kịch bản 1: Gửi thông tin hợp lệ (Happy Path)
* **Dữ liệu nhập**:
  ```json
  {
    "lead_name": "Trần Thị Mai",
    "phone": "0987654321",
    "email": "mai.tran@example.com",
    "service_type": "Tắm Spa & Cắt Tỉa Lông Toàn Diện",
    "pet_info": "Bé Corgi 2 tuổi, nặng 11kg, tắm khử mùi hôi và tỉa phao câu"
  }
  ```
* **Request gửi đi** (`POST /wp-json/petcare/v1/lead`):
  ```http
  POST /wp-json/petcare/v1/lead HTTP/1.1
  Host: petcare-demo.local
  Content-Type: application/json
  X-WP-Nonce: a1b2c3d4e5

  {
    "lead_name": "Trần Thị Mai",
    "phone": "0987654321",
    "email": "mai.tran@example.com",
    "service_type": "Tắm Spa & Cắt Tỉa Lông Toàn Diện",
    "pet_info": "Bé Corgi 2 tuổi, nặng 11kg, tắm khử mùi hôi và tỉa phao câu",
    "petcare_hp_website": ""
  }
  ```
* **Response nhận về từ Server**:
  ```http
  HTTP/1.1 200 OK
  Content-Type: application/json; charset=UTF-8

  {
    "success": true,
    "lead_id": "LEAD-2026-00002",
    "message": "Đăng ký thành công! Mã hồ sơ tư vấn của bạn là [LEAD-2026-00002]. Bác sĩ/Tư vấn viên PetCare sẽ liên hệ trong ít phút."
  }
  ```
* **Kết quả trong Database Frappe**:
  Bản ghi DocType `PetCare Lead` được tạo mới với:
  - `name`: `LEAD-2026-00002`
  - `lead_name`: `Trần Thị Mai`
  - `phone`: `0987654321`
  - `lead_source`: `WordPress Form`
  - `status`: `New`
  - `priority`: `Medium`
  - `initial_pet_info`: `Dịch vụ quan tâm: Tắm Spa & Cắt Tỉa Lông Toàn Diện. Ghi chú: Bé Corgi 2 tuổi, nặng 11kg, tắm khử mùi hôi và tỉa phao câu`

---

### Kịch bản 2: Bắt lỗi Số điện thoại sai định dạng (Validation Failure)
* **Dữ liệu nhập**:
  ```json
  {
    "lead_name": "Lê Văn Test",
    "phone": "1234abc",
    "service_type": "Khám Sức Khỏe"
  }
  ```
* **Phản hồi từ Client JS**: Bị chặn ngay tại trình duyệt, viền ô SĐT chuyển sang màu đỏ kèm thông báo lỗi:
  *"Số điện thoại không hợp lệ (cần là SĐT Việt Nam 10 chữ số, ví dụ 0912345678)."*
* **Nếu bypass JS bằng Postman**: Server WordPress trả về:
  ```http
  HTTP/1.1 400 Bad Request
  Content-Type: application/json

  {
    "success": false,
    "message": "Số điện thoại không hợp lệ. Vui lòng nhập số điện thoại di động Việt Nam (ví dụ: 0912345678)."
  }
  ```

---

### Kịch bản 3: Bẫy Bot Spam qua Honeypot (Bot Trap Trap)
* **Bot gửi request kèm trường ẩn**:
  ```json
  {
    "lead_name": "Bot Casino 88",
    "phone": "0911223344",
    "petcare_hp_website": "http://spam-casino-link.com"
  }
  ```
* **Phản hồi từ Server Proxy**:
  ```http
  HTTP/1.1 200 OK
  Content-Type: application/json

  {
    "success": true,
    "lead_id": "LEAD-BOT-TRAPPED",
    "message": "Cảm ơn bạn đã liên hệ. Đội ngũ PetCare sẽ phản hồi sớm nhất!"
  }
  ```
* **Kết quả kiểm chứng**: Hoàn toàn **KHÔNG CÓ** bất kỳ bản ghi nào được ghi vào cơ sở dữ liệu Frappe CRM. Bot tưởng đã spam thành công trong khi hệ thống sạch 100%.

---

### Kịch bản 4: Giới hạn tần suất gửi (Rate Limiting)
* Một người dùng hoặc script spam gửi liên tục 6 lần trong vòng 2 phút từ cùng 1 địa chỉ IP.
* **Lần thứ 6 nhận được phản hồi**:
  ```http
  HTTP/1.1 429 Too Many Requests
  Content-Type: application/json

  {
    "success": false,
    "message": "Bạn đã gửi yêu cầu quá nhiều lần. Vui lòng đợi 10 phút trước khi gửi lại."
  }
  ```
