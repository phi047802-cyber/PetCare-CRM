# PetCare CRM v1.0-demo Release Notes

## 🐾 Tổng Quan
Phiên bản **v1.0-demo** hoàn thành 100% (56/56 tasks) theo kế hoạch WBS của Dự án **PetCare CRM**.  
Hệ thống được phát triển trên nền tảng **Frappe Framework v15** tích hợp sâu với **FrappeCRM**, vận hành container hóa hoàn chỉnh trên Docker Compose.

---

## 🚀 Các Tính Năng Đã Triển Khai

### 1. Module 1: Membership & Benefit Management (WBS T01–T21)
- **DocTypes**: `Membership Plan`, `Plan Benefit`, `Customer Membership`, `Membership Benefit`.
- **API Whitelisted**:
  - `get_active_membership(customer, pet, check_date)`: Truy vấn gói hội viên hiện hành.
  - `get_remaining_benefit(membership_name, service_type)`: Kiểm tra quyền lợi còn lại.
  - `record_benefit_usage(membership_name, service_type, count)`: Trừ lượt quyền lợi với cơ chế atomic, tuyệt đối không cho phép âm lượt.
  - `check_membership_renewal(customer, pet)`: Tự động cảnh báo hội viên sắp hết hạn trong 7 ngày.

### 2. Module 2: Care Pattern Engine (WBS T01–T21)
- **DocTypes**: `Pet`, `Service Visit`, `Care Recommendation`.
- **Thuật toán thông minh**:
  - Tính chu kỳ chăm sóc bằng Exponentially Weighted Moving Average (EWMA) và lọc ngoại lai (IQR Outlier Filtering).
  - Phân loại trạng thái: `DUE_SOON` (sắp tới chu kỳ trong 5 ngày), `AT_RISK` (vắng mặt vượt tỷ lệ 1.5), `INSUFFICIENT_DATA` (dưới 3 lượt khám).
- **API Whitelisted**:
  - `get_care_status(pet_name, service_type, check_date)`: Xác định trạng thái chăm sóc.
  - `predict_next_service(pet_name, service_type)`: Dự đoán chính xác ngày quay lại tiếp theo.

### 3. Tích Hợp & Daily Scheduler Automation (WBS T22–T42)
- **Recommendation Engine (`frappe_recommendation_engine.py`)**: Tự động sinh đề xuất kèm thông tin quyền lợi gói hội viên để cá nhân hóa thông điệp CSKH.
- **Deduplication Window**: Cơ chế cửa sổ 14 ngày chống trùng lặp khuyến nghị.
- **Frappe Scheduler (`hooks.py` + `tasks.py`)**: `daily_petcare_scan()` tự động quét hàng ngày các thú cưng đến hạn, có nguy cơ rời bỏ hoặc gói hội viên sắp hết hạn.

### 4. Dữ Liệu Demo & UI List Views (WBS T43–T56)
- **Seed Patch**: `seed_demo_data.py` nạp tức thì 5 Pet, 2 Gói hội viên, 8 Lịch sử dịch vụ phục vụ diễn tập 3 Demo Flows.
- **List Views**: Tùy biến cột, hiển thị badge màu trạng thái và quick filter buttons trên Frappe Desk.

---

## 🧪 Kết Quả Kiểm Thử (Unit Tests & QA)
- **Automated Tests**: 15/15 tests PASS (`bench run-tests --app petcare_crm`).
- **Regression Tests & Demo Flows**: 100% PASS trên tất cả 3 luồng kiểm thử chính.
- **Release Tag**: `v1.0-demo`
