# BẢNG PHÂN BỔ & TÀI LIỆU KỸ THUẬT API CÁ NHÂN (RUBRIC A4.7.2)
## HỆ THỐNG PETCARE CRM - KIỂM THỬ GIAO DIỆN LẬP TRÌNH TỪNG THÀNH VIÊN

> **Dự án**: PetCare CRM (Frappe Framework v15)  
> **Quy mô nhóm**: 4 Thành viên  
> **Chuẩn mô tả**: REST API Spec, Postman Collection cURL, Báo cáo kiểm thử cá nhân  
> **Mã tài liệu**: `DOC-API-INDIVIDUAL-2026`  

---

## 1. MA TRẬN PHÂN CHIA API ĐỘC QUYỀN 4 THÀNH VIÊN

> **Nguyên tắc bảo vệ thông tin sinh viên**: Bảng dưới đây sử dụng placeholder `[MSSV] - [HỌ TÊN]`. Mỗi thành viên đảm trách một API nghiệp vụ hoàn toàn khác nhau, có thể chạy độc lập trên Postman và tương ứng với phân hệ BPMN cá nhân đã được phân công.

| STT | Thành viên phụ trách | Vai trò phân hệ | Mã API sở hữu độc quyền | URL Endpoint Frappe | Quyền Frappe RBAC | Mục đích kiểm thử cá nhân | Bộ Test chứng thực |
| :---: | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | `[MSSV1] - [HỌ TÊN 1]` | Phễu Tiếp nhận & Lead | `create_lead` | `POST /api/method/petcare_crm.api.create_lead` | `PetCare Sales`, `PetCare Manager` | Tiếp nhận Lead, chuẩn hóa số điện thoại VN 10 số (+84 -> 0), kiểm tra regex và tạo bản ghi Lead mới. | `test_lead_sales.py`, `test_crm_core_mock.py` |
| **2** | `[MSSV2] - [HỌ TÊN 2]` | Phễu Cơ hội & Sales | `create_opportunity` | `POST /api/method/petcare_crm.api.create_opportunity` | `PetCare Sales`, `PetCare Manager` | Tạo cơ hội bán hàng, kiểm soát điều kiện ngân sách expected_amount > 0, tính xác suất thành công ban đầu. | `test_lead_sales.py`, `test_sales_pipeline.py` |
| **3** | `[MSSV3] - [HỌ TÊN 3]` | Vận hành Dịch vụ & Thẻ | `record_pet_service_visit` | `POST /api/method/petcare_crm.api.record_pet_service_visit` | `PetCare Receptionist`, `Specialist` | Mở phiếu dịch vụ, áp dụng Pessimistic Row Lock cấn trừ lượt thẻ hội viên, tự động tính giá ưu đãi. | `test_service_operations.py`, `test_pricing.py` |
| **4** | `[MSSV4] - [HỌ TÊN 4]` | Giữ chân & Đa kênh | `send_omnichannel_notification` | `POST /api/method/petcare_crm.api.send_omnichannel_notification` | `PetCare Care Specialist`, `Manager` | Phát thông báo chăm sóc cá nhân hóa qua Zalo ZNS / SMS, lưu hộp thư Outbox và cơ chế thử lại. | `test_extended_capabilities_mock.py` |

---

## 2. CHI TIẾT ĐẶC TẢ TỪNG API CÁ NHÂN KÈM POSTMAN CURL

### 2.1. THÀNH VIÊN 1: `[MSSV1] - [HỌ TÊN 1]` — API `create_lead`
* **Mô tả chức năng**: Tiếp nhận thông tin khách hàng tiềm năng, làm sạch khoảng trắng, chuẩn hóa đầu số `+84` thành `0`, kiểm tra regex số điện thoại Việt Nam `^0\d{8,10}$` và lưu vào bảng `PetCare Lead`.
* **Cú pháp cURL mẫu**:
  ```bash
  curl -X POST "{{base_url}}/api/method/petcare_crm.api.create_lead"     -H "Authorization: token {{api_key}}:{{api_secret}}"     -H "Content-Type: application/json"     -d '{
      "lead_name": "Phan Hoàng Yến",
      "phone": "+84933112233",
      "lead_source": "Facebook Ads",
      "email": "hoangyen.phan@example.com",
      "initial_pet_info": "Bé Mèo Anh lông ngắn 1 tuổi, cần tiêm phòng vắc-xin",
      "priority": "High"
    }'
  ```
* **Phản hồi Thành Công (HTTP 200)**:
  ```json
  {
    "message": {
      "status": "success",
      "lead_id": "LEAD-2026-00045",
      "message": "Ghi nhận Lead thành công."
    }
  }
  ```
* **Kịch bản kiểm thử lỗi**:
  * Gửi thiếu `lead_name` hoặc `phone` -> HTTP 400 `ValidationError: Tên khách hàng tiềm năng (lead_name) là bắt buộc`.
  * Gửi số điện thoại chữ cái `090abc123` -> HTTP 400 `ValidationError: Số điện thoại không hợp lệ`.
  * Không gửi Token Authorization -> HTTP 403 `AuthenticationError`.

---

### 2.2. THÀNH VIÊN 2: `[MSSV2] - [HỌ TÊN 2]` — API `create_opportunity`
* **Mô tả chức năng**: Khởi tạo cơ hội bán hàng gói dịch vụ giá trị cao hoặc thẻ hội viên liên kết với hồ sơ khách hàng (`Contact`). Bắt buộc kiểm soát giá trị kỳ vọng dương (`expected_amount > 0`) và ngày chốt dự kiến từ hôm nay trở đi.
* **Cú pháp cURL mẫu**:
  ```bash
  curl -X POST "{{base_url}}/api/method/petcare_crm.api.create_opportunity"     -H "Authorization: token {{api_key}}:{{api_secret}}"     -H "Content-Type: application/json"     -d '{
      "customer": "CONT-00102",
      "title": "Tư vấn Gói Hội Viên Gia Đình VIP 1 Năm cho bé Bơ",
      "expected_amount": 6500000.0,
      "stage": "Prospecting",
      "expected_closing_date": "2026-11-15",
      "pet": "Bơ"
    }'
  ```
* **Phản hồi Thành Công (HTTP 200)**:
  ```json
  {
    "message": {
      "status": "success",
      "opportunity_id": "OPP-2026-00018",
      "stage": "Prospecting",
      "probability": 10.0,
      "message": "Tạo cơ hội bán hàng thành công."
    }
  }
  ```
* **Kịch bản kiểm thử lỗi**:
  * Gửi `expected_amount = -500000` -> HTTP 400 `ValidationError: Giá trị kỳ vọng phải lớn hơn 0`.
  * Chọn `pet` không thuộc quyền sở hữu của `customer` -> HTTP 400 `ValidationError: Thú cưng không thuộc sở hữu của khách hàng`.

---

### 2.3. THÀNH VIÊN 3: `[MSSV3] - [HỌ TÊN 3]` — API `record_pet_service_visit`
* **Mô tả chức năng**: Tiếp nhận thú cưng làm dịch vụ tại quầy, cập nhật thể trạng cân nặng thực tế (kg), áp dụng cơ chế Khóa hàng dòng dữ liệu (**Pessimistic Row Lock** - `SELECT FOR UPDATE`) để cấn trừ lượt thẻ hội viên khả dụng, ghi sổ nhật ký `Benefit Redemption Ledger`.
* **Cú pháp cURL mẫu**:
  ```bash
  curl -X POST "{{base_url}}/api/method/petcare_crm.api.record_pet_service_visit"     -H "Authorization: token {{api_key}}:{{api_secret}}"     -H "Content-Type: application/json"     -d '{
      "pet": "Bơ",
      "service_identifier": "SRV-GROOM-01",
      "visit_date": "2026-10-27",
      "technician": "Nguyễn Kỹ Thuật",
      "weight_kg": 5.4,
      "membership_id": "MEM-GOLD-0001"
    }'
  ```
* **Phản hồi Thành Công (HTTP 200)**:
  ```json
  {
    "message": {
      "status": "success",
      "visit_id": "VISIT-2026-00125",
      "customer": "CONT-00102",
      "pet": "Bơ",
      "service_type": "Tắm Spa & Cắt Tỉa Lông Toàn Diện",
      "original_price": 350000.0,
      "discount_amount": 350000.0,
      "final_price": 0.0,
      "membership_used": "MEM-GOLD-0001",
      "benefit_used": "Tắm Spa"
    }
  }
  ```
* **Kịch bản kiểm thử lỗi**:
  * Thẻ hội viên đã hết hạn hoặc hết số lượt dịch vụ -> Hệ thống giữ nguyên giá bán lẻ `final_price = 350000.0` và ghi chú rõ không áp dụng được ưu đãi.
  * Hai nhân viên cùng thao tác trừ lượt trên 1 thẻ cùng lúc -> Cơ chế `FOR UPDATE` tuần tự hóa giao dịch, triệt tiêu lỗi âm số dư.

---

### 2.4. THÀNH VIÊN 4: `[MSSV4] - [HỌ TÊN 4]` — API `send_omnichannel_notification`
* **Mô tả chức năng**: Phát tin nhắn chăm sóc khách hàng chủ động qua kênh Zalo ZNS hoặc SMS Brandname. Tích hợp chế độ Safe Mode giả lập an toàn, lưu vết toàn bộ thông điệp vào bảng `Omnichannel Outbox` và cơ chế tự động thử lại khi lỗi mạng.
* **Cú pháp cURL mẫu**:
  ```bash
  curl -X POST "{{base_url}}/api/method/petcare_crm.api.send_omnichannel_notification"     -H "Authorization: token {{api_key}}:{{api_secret}}"     -H "Content-Type: application/json"     -d '{
      "channel": "Zalo ZNS",
      "recipient": "0912345678",
      "template_id": "ZNS_CARE_DUE_SOON",
      "template_data": {
        "customer_name": "Anh An",
        "pet_name": "Bé Bơ",
        "service_name": "Tắm Spa Định Kỳ",
        "due_date": "2026-10-30",
        "discount_code": "RETENTION15"
      }
    }'
  ```
* **Phản hồi Thành Công (HTTP 200)**:
  ```json
  {
    "message": {
      "status": "success",
      "outbox_id": "MSG-2026-00088",
      "channel": "Zalo ZNS",
      "recipient": "0912345678",
      "delivery_status": "SENT",
      "message": "Tin nhắn Zalo ZNS đã được chuyển tiếp thành công đến thuê bao."
    }
  }
  ```
* **Kịch bản kiểm thử lỗi**:
  * Truyền kênh không hỗ trợ `channel = "Telegram"` -> HTTP 400 `ValidationError: Kênh gửi tin nhắn không hợp lệ`.
  * Số điện thoại không tồn tại hoặc sai định dạng -> HTTP 400 `ValidationError: Số điện thoại người nhận không hợp lệ`.

---

## 3. CHECKLIST CHỤP ẢNH MINH CHỨNG POSTMAN KHI DEMO

> [!IMPORTANT]
> **Hướng dẫn thực hiện**: Khi môi trường Frappe CRM đang chạy local, sinh viên mở ứng dụng Postman Desktop, import file `PetCare_CRM_API_Collection.postman_collection.json` và `PetCare_CRM_Local.postman_environment.json`. Gửi request thật và chụp ảnh màn hình nộp báo cáo theo checklist:

1. **Ảnh chụp 1 (Thành viên 1)**: Request `POST create_lead` -> Response `HTTP 200 OK` có mã `LEAD-2026-XXXXX`.
2. **Ảnh chụp 2 (Thành viên 2)**: Request `POST create_opportunity` -> Response `HTTP 200 OK` hiển thị `stage: Prospecting` và `probability: 10.0`.
3. **Ảnh chụp 3 (Thành viên 3)**: Request `POST record_pet_service_visit` -> Response `HTTP 200 OK` hiển thị `final_price: 0.0` và `membership_used`.
4. **Ảnh chụp 4 (Thành viên 4)**: Request `POST send_omnichannel_notification` -> Response `HTTP 200 OK` hiển thị `delivery_status: SENT`.
5. **Ảnh chụp 5 (Nhóm)**: Request `POST payment_webhook` -> Response `HTTP 200 OK` hiển thị gạch nợ thành công kèm mã giao dịch ngân hàng.
