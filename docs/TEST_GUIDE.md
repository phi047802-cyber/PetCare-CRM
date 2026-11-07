# HƯỚNG DẪN KIỂM THỬ HỆ THỐNG (TESTING GUIDE & VERIFICATION)

> **Dự án**: PetCare CRM  
> **Nền tảng**: Frappe Framework v15  
> **Tổng số kịch bản kiểm thử**: **58 tests** (Tỷ lệ Pass hiện tại: **100%**)  

---

## 1. Triết Lý & Chiến Lược Kiểm Thử (Testing Strategy)

Hệ thống PetCare CRM áp dụng chiến lược kiểm thử đa tầng (Test Pyramid) nghiêm ngặt:
1. **Kiểm thử độc lập không phụ thuộc Daemon (Pure Python Mock Architecture)**: Toàn bộ 58 kịch bản kiểm thử có thể chạy trực tiếp trên bất kỳ máy trạm có cài Python 3.10+ mà không bắt buộc khởi động container Docker hay MariaDB server.
2. **Nguyên tắc "Chạy Thật — Không Làm Yếu Assertion"**:
   * Không đánh dấu Pass nếu test chưa thực sự chạy và in kết quả.
   * Khi gặp lỗi, truy tìm nguyên nhân gốc rễ (Root Cause) để sửa code logic, tuyệt đối không xóa bỏ assert hoặc hạ thấp tiêu chuẩn kiểm thử.
3. **Phân định 4 trạng thái kiểm thử rõ ràng**:
   * `PASS`: Kịch bản chạy thành công, toàn bộ điều kiện logic và dữ liệu khớp chính xác.
   * `FAIL`: Logic trả về kết quả sai khác so với quy tắc nghiệp vụ thiết kế.
   * `ERROR`: Lỗi cú pháp, ngoại lệ không được bắt (unhandled exception) hoặc lỗi import.
   * `SKIPPED / BLOCKED`: Bị bỏ qua hoặc bị chặn do thiếu điều kiện tiền quyết.

---

## 2. Cấu Trúc Các Bộ Kiểm Thử (Test Suites Structure)

Thư mục kiểm thử: [`apps/petcare_crm/petcare_crm/tests/`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/tests/)

| Tên File Kiểm Thử | Số Tests | Tầng Kiến Trúc | Nội Dung Trọng Tâm |
|---|:---:|---|---|
| [`test_crm_core_mock.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/tests/test_crm_core_mock.py) | 4 | Unit & Integration | Kiểm tra số điện thoại, quy trình Lead, chuyển đổi không gộp trùng khách hàng, các giai đoạn Opportunity. |
| [`test_service_operations_mock.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/tests/test_service_operations_mock.py) | 4 | Unit & Integration | Danh mục dịch vụ chuẩn, tính giá dịch vụ, cấn trừ quyền lợi 100% FREE, kiểm tra hồ sơ Pet. |
| [`test_membership_lifecycle_mock.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/tests/test_membership_lifecycle_mock.py) | 8 | Domain & Transaction | Thẻ Active/Expired, cấn trừ quyền lợi, bảo vệ Idempotency chống trừ trùng lặp khi retry, rollover gia hạn thẻ. |
| [`test_care_intelligence_mock.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/tests/test_care_intelligence_mock.py) | 11 | Intelligence & Retention | Thuật toán lọc ngoại lai IQR, trung bình động EWMA, dự đoán ngày ghé thăm, phát hiện Due Soon/At Risk, khử trùng lặp đề xuất. |
| [`test_workflow_automation_mock.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/tests/test_workflow_automation_mock.py) | 9 | Automation & Scheduler | Tác vụ nền định kỳ: nhắc Lead quá 24h, tự động hết hạn thẻ, cảnh báo gia hạn 7 ngày, giám sát SLA khiếu nại, Safe Mode. |
| [`test_security_and_reporting_mock.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/tests/test_security_and_reporting_mock.py) | 11 | Security & Analytics | Phân quyền vai trò RBAC (Sales, Tech, Analyst, Manager), xác thực sở hữu chéo, khử khuẩn đầu vào, 8 chỉ số KPI chuẩn. |
| [`test_e2e_scenarios_mock.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/tests/test_e2e_scenarios_mock.py) | 11 | End-to-End Scenarios | 6 kịch bản E2E toàn diện (A: Lead->Khách hàng, B: Dịch vụ->360, C: Hội viên->Redemption, D: Care Intelligence, E: RBAC, F: Idempotent Scheduler). |

---

## 3. Lệnh Thực Thi Kiểm Thử

### 3.1. Chạy Toàn Bộ Bộ Kiểm Thử Bằng Master Runner (Khuyến Nghị)
```powershell
python apps/petcare_crm/petcare_crm/tests/run_all_tests.py
```
*Thời gian chạy*: ~1.5 giây cho toàn bộ 58 tests.

### 3.2. Chạy Riêng Lẻ Từng Suite Cụ Thể
```powershell
# Chạy Suite End-to-End Scenarios
python apps/petcare_crm/petcare_crm/tests/test_e2e_scenarios_mock.py

# Chạy Suite Security & RBAC
python apps/petcare_crm/petcare_crm/tests/test_security_and_reporting_mock.py

# Chạy Suite Care Intelligence
python apps/petcare_crm/petcare_crm/tests/test_care_intelligence_mock.py
```

### 3.3. Chạy Trong Môi Trường Container Frappe Bench
```bash
docker exec -it petcare-backend-1 bench --site petcare.localhost run-tests --app petcare_crm
```
