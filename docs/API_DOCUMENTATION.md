# TÀI LIỆU KỸ THUẬT GIAO DIỆN LẬP TRÌNH ỨNG DỤNG (API SPECIFICATION)

> **Dự án**: PetCare CRM (CRM Toàn Diện Dịch Vụ Thú Cưng)  
> **Nền tảng**: Frappe Framework v15  
> **Giao thức**: REST API & Whitelisted RPC Endpoints  
> **Định dạng dữ liệu**: `application/json` (UTF-8)  

---

## 1. Tổng Quan & Cơ Chế Xác Thực (Authentication & Security)

### 1.1. Cấu Trúc Endpoint Chuẩn
Mọi API trong PetCare CRM được đăng ký qua decorator `@frappe.whitelist()` của Frappe Framework:
```text
POST /api/method/petcare_crm.api.[function_name]
GET  /api/method/petcare_crm.api.[function_name]
```

### 1.2. Cơ Chế Xác Thực
1. **Qua Session Cookie (Desk UI / Trình duyệt)**: Khi người dùng đã đăng nhập vào Frappe Desk, cookie `sid` được tự động đính kèm theo header request.
2. **Qua API Key / Secret (Hệ thống bên thứ ba / Tích hợp)**:
   ```http
   Authorization: token api_key:api_secret
   Content-Type: application/json
   ```

### 1.3. Định Dạng Phản Hồi Chuẩn (Standard Response Envelope)
* **Thành công (Success Response)**:
  ```json
  {
    "message": {
      "success": true,
      "data": { ... }
    }
  }
  ```
* **Lỗi có cấu trúc (Structured Error Response)**:
  ```json
  {
    "exception": "petcare_crm.utils.exceptions.ValidationError",
    "exc_type": "ValidationError",
    "_server_messages": "[\"{\\\"message\\\": \\\"Thú cưng không thuộc sở hữu của khách hàng.\\\"}\"]"
  }
  ```

---

## 2. Chi Tiết Các Endpoints Vận Hành & Tích Hợp

### 2.1. Phân Hệ Phân Tích & Quản Trị (KPI Dashboard & Access Verification)

#### `get_kpi_dashboard_metrics`
Trích xuất toàn bộ 8 chỉ số KPI vận hành CRM và Giữ chân khách hàng.
* **Method**: `GET` / `POST`
* **Quyền yêu cầu**: `System Manager`, `PetCare Manager`, `PetCare Analyst`
* **Tham số**:
  * `from_date` *(tùy chọn, string `YYYY-MM-DD`)*: Ngày bắt đầu lọc báo cáo.
  * `to_date` *(tùy chọn, string `YYYY-MM-DD`)*: Ngày kết thúc lọc báo cáo.
* **Phản hồi mẫu**:
  ```json
  {
    "message": {
      "success": true,
      "data": {
        "kpi_1_lead_conversion": {
          "total_leads": 12,
          "converted_leads": 5,
          "conversion_rate_pct": 41.67
        },
        "kpi_2_sales_pipeline": {
          "total_pipeline_value": 4430000.0,
          "weighted_pipeline_value": 2658000.0
        },
        "kpi_3_active_memberships": {
          "active_memberships_count": 8,
          "total_remaining_benefits": 14
        },
        "kpi_4_membership_expiring_soon": {
          "expiring_soon_count": 2
        },
        "kpi_5_service_visits_and_revenue": {
          "total_visits": 28,
          "gross_revenue": 9800000.0,
          "net_revenue": 8750000.0
        },
        "kpi_6_due_soon": {
          "due_soon_count": 3
        },
        "kpi_7_at_risk": {
          "at_risk_count": 2
        },
        "kpi_8_care_recommendations": {
          "total_recommendations": 10,
          "conversion_rate_pct": 50.0
        }
      }
    }
  }
  ```

#### `verify_customer_pet_access`
Kiểm tra ràng buộc sở hữu chéo giữa Khách hàng, Thú cưng và Thẻ hội viên.
* **Method**: `POST`
* **Tham số**:
  * `customer_id` *(bắt buộc, string)*: Mã khách hàng (`Contact`).
  * `pet_id` *(tùy chọn, string)*: Tên hoặc mã thú cưng (`Pet`).
  * `membership_id` *(tùy chọn, string)*: Mã thẻ hội viên (`Customer Membership`).
* **Phản hồi mẫu**:
  ```json
  {
    "message": {
      "valid": true,
      "error_message": null
    }
  }
  ```

---

### 2.2. Phân Hệ CRM Tiếp Thị & Bán Hàng (Lead & Customer Conversion)

#### `convert_lead`
Chuyển đổi khách hàng tiềm năng thành Khách hàng chính thức, Thú cưng và Cơ hội bán hàng.
* **Method**: `POST`
* **Quyền yêu cầu**: `PetCare Sales`, `PetCare Manager`, `System Manager`
* **Tham số**:
  * `lead_name` *(bắt buộc, string)*: Mã định danh Lead (ví dụ: `LEAD-2026-00010`).
* **Phản hồi mẫu**:
  ```json
  {
    "message": {
      "status": "success",
      "lead_id": "LEAD-2026-00010",
      "contact_id": "CONT-00102",
      "pet_id": "PET-00054",
      "opportunity_id": "OPP-00032",
      "message": "Chuyển đổi Lead thành công."
    }
  }
  ```

---

### 2.3. Phân Hệ Vận Hành Dịch Vụ & Hội Viên (Service Visit & Membership)

#### `calculate_service_pricing`
Tính toán chiết khấu và giá dịch vụ dự kiến dựa trên thẻ hội viên khả dụng.
* **Method**: `POST`
* **Tham số**:
  * `customer` *(bắt buộc, string)*: Mã khách hàng.
  * `pet` *(bắt buộc, string)*: Tên thú cưng.
  * `service_type` *(bắt buộc, string)*: Mã hoặc tên dịch vụ.
  * `membership_id` *(tùy chọn, string)*: Mã thẻ hội viên cụ thể.
* **Phản hồi mẫu**:
  ```json
  {
    "message": {
      "original_price": 350000.0,
      "discount_amount": 350000.0,
      "final_price": 0.0,
      "benefit_type": "FREE",
      "remaining_after": 0
    }
  }
  ```

#### `record_pet_service_visit`
Tiếp nhận thú cưng làm dịch vụ, tính giá và cấn trừ quyền lợi thẻ hội viên (kèm Idempotency key).
* **Method**: `POST`
* **Quyền yêu cầu**: `PetCare Technician`, `PetCare Manager`, `System Manager`
* **Tham số**:
  * `pet` *(bắt buộc, string)*: Tên thú cưng.
  * `service_identifier` *(bắt buộc, string)*: Mã dịch vụ (ví dụ: `SRV-GROOM`).
  * `visit_date` *(tùy chọn, string `YYYY-MM-DD`)*: Ngày làm dịch vụ (mặc định hôm nay).
  * `technician` *(tùy chọn, string)*: Kỹ thuật viên phụ trách.
  * `weight_kg` *(tùy chọn, float)*: Cân nặng ghi nhận thực tế.
  * `membership_id` *(tùy chọn, string)*: Thẻ hội viên áp dụng.
* **Phản hồi mẫu**:
  ```json
  {
    "message": {
      "status": "success",
      "visit_id": "VISIT-2026-00120",
      "customer": "CONT-00102",
      "pet": "Bơ",
      "service_type": "Grooming Toàn Diện",
      "original_price": 350000.0,
      "discount_amount": 350000.0,
      "final_price": 0.0,
      "membership_used": "MEM-SILVER-01",
      "benefit_used": "Grooming"
    }
  }
  ```

#### `renew_membership`
Gia hạn thẻ hội viên với chính sách Rollover bảo lưu số lượt tồn.
* **Method**: `POST`
* **Quyền yêu cầu**: `PetCare Sales`, `PetCare Manager`, `System Manager`
* **Tham số**:
  * `membership_name` *(bắt buộc, string)*: Mã thẻ hội viên cũ.
  * `new_end_date` *(bắt buộc, string `YYYY-MM-DD`)*: Ngày hết hạn mới.
  * `allow_rollover` *(tùy chọn, boolean, mặc định `true`)*.
* **Phản hồi mẫu**:
  ```json
  {
    "message": {
      "status": "success",
      "membership": "MEM-SILVER-01",
      "new_end_date": "2027-10-26",
      "rollover_benefits_count": 2,
      "message": "Gia hạn gói hội viên thành công."
    }
  }
  ```

---

### 2.4. Phân Hệ Phản Hồi Dịch Vụ & Xử Lý Sự Cố (Case Management)

#### `create_service_case`
Ghi nhận khiếu nại, phản hồi hoặc yêu cầu hỗ trợ sau khi sử dụng dịch vụ.
* **Method**: `POST`
* **Tham số**:
  * `customer` *(bắt buộc, string)*: Mã khách hàng.
  * `subject` *(bắt buộc, string)*: Tiêu đề phản hồi.
  * `description` *(bắt buộc, string)*: Nội dung chi tiết.
  * `pet` *(tùy chọn, string)*: Thú cưng liên quan.
  * `service_visit` *(tùy chọn, string)*: Phiếu dịch vụ liên quan.
  * `priority` *(tùy chọn, string: `Low`, `Medium`, `High`, `Urgent`)*.
* **Phản hồi mẫu**:
  ```json
  {
    "message": {
      "status": "success",
      "case_id": "CASE-2026-00015",
      "message": "Ghi nhận phản hồi thành công."
    }
  }
  ```
