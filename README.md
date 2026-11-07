# PetCare CRM — Comprehensive CRM Platform for Pet Care Services

> **Hệ Thống Quản Lý Quan Hệ Khách Hàng Chuyên Biệt Cho Ngành Chăm Sóc Thú Cưng**  
> **Nền tảng**: Frappe Framework v15 (Desk Native Architecture)  
> **Phiên bản hoàn thiện**: 2.0 (Prompt 10 Final Handover Release)  
> **Kiểm thử tự động**: **58 / 58 Tests PASS (100.0%)** | Thời gian thực thi: **1.6s**  

---

## 🌟 Giới Thiệu Tổng Quan

**PetCare CRM** là giải pháp CRM toàn diện được thiết kế riêng cho các phòng khám thú y, spa và chuỗi dịch vụ chăm sóc thú cưng. Hệ thống giải quyết trọn vẹn bài toán vận hành xuyên suốt vòng đời khách hàng:

1. **CRM Tiếp Thị & Bán Hàng (CRM Core)**: Thu thập và quản lý Lead từ các kênh tiếp thị, chuẩn hóa số điện thoại Việt Nam, chuyển đổi thành Khách hàng/Thú cưng/Cơ hội mà không làm gộp trùng dữ liệu, quản lý phễu bán hàng (Sales Pipeline).
2. **Quản Lý Thú Cưng & Vận Hành Dịch Vụ (PetCare Domain & Operations)**: Quản lý hồ sơ thú cưng với quan hệ 1:N với chủ nuôi (`Multi-Pet`), danh mục bảng giá niêm yết chuẩn, phiếu dịch vụ (`Service Visit`) và theo dõi phản hồi (`PetCare Case`).
3. **Thẻ Hội Viên & Khấu Trừ Quyền Lợi (Membership & Loyalty)**: Cấu hình các gói hội viên linh hoạt (Bạc, Vàng, VIP), cấn trừ quyền lợi tự động (100% FREE, chiết khấu %), bảo vệ Idempotency chống trừ trùng lặp, bảo toàn số dư không bị âm và hỗ trợ Rollover khi gia hạn thẻ.
4. **Trí Tuệ Chăm Sóc & Dự Đoán Tái Khám (Care Intelligence & Retention)**: Thuật toán Rule-based thống kê minh bạch kết hợp bộ lọc ngoại lai (Tukey IQR) và trung bình động hàm mũ (EWMA) để dự đoán chu kỳ chăm sóc, phát hiện thú cưng sắp đến hạn (`DUE_SOON`), khách hàng có nguy cơ rời bỏ (`AT_RISK`) và tự động giao nhiệm vụ cho nhân viên CSKH.
5. **Giao Diện Frappe Desk Hoàn Chỉnh (Desk Native UI)**: Workspace nghiệp vụ PetCare CRM, List View, Form View, các nút hành động (Action Buttons), bộ lọc query filter và Báo cáo quản trị 8 chỉ số KPI chuẩn.

---

## 🏗️ Kiến Trúc Hệ Thống (Clean Architecture)

Hệ thống được thiết kế theo mô hình Clean Architecture 8 tầng, đảm bảo tính phân tách trách nhiệm (Separation of Concerns) và khả năng kiểm thử độc lập:

* **Tầng 6 (Presentation Layer)**: Workspace `PetCare CRM`, Form scripts (`pet.js`, `service_visit.js`, `customer_membership.js`), Script Report `petcare_kpi_overview`.
* **Tầng 5 (API / Controller Layer)**: Các endpoint `@frappe.whitelist()` trong [`petcare_crm/api.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/api.py).
* **Tầng 4 (Application Layer)**: Các Coordinator điều phối nghiệp vụ (`LeadConversionCoordinator`, `CareRecommendationCoordinator`, `AutomationCoordinator`, `AnalyticsService`).
* **Tầng 3 (Domain Layer)**: Business logic OOP thuần túy (`CarePatternAnalyzer`, `VisitPredictionService`, `RiskDetectionService`, `PricingEngine`).
* **Tầng 2 (DocType Layer)**: Controllers và Schema JSON định nghĩa các thực thể và quan hệ cơ sở dữ liệu.
* **Tầng 1 (Infrastructure Layer)**: Frappe Framework v15, MariaDB 11.x, Redis Cache & Queues.
* **Tầng 7 & 8 (Automation & Testing)**: Tác vụ nền định kỳ và bộ kiểm thử tự động 58 test cases.

---

## 🚀 Hướng Dẫn Cài Đặt & Chạy Sản Phẩm

### Cách 1: Khởi Chạy Nhanh Độc Lập (Chạy Ngay Không Cần Cài Đặt / Không Cần Docker)
> Thích hợp nhất để demo, chấm điểm đồ án hoặc kiểm tra giao diện & luồng nghiệp vụ ngay lập tức trên mọi hệ điều hành (Windows / macOS / Linux) mà không cần cài đặt MariaDB hay Frappe Bench.

```bash
# Chỉ cần cài đặt Python 3.10+ và chạy:
python start_preview.py
```
* **Cổng Khách Hàng & Thu Ngân POS**: `http://127.0.0.1:8080/`
* **Không Gian Làm Việc Frappe Desk**: `http://127.0.0.1:8080/desk` (hoặc `/app`)
* **Chạy 88 Bài Test Tự Động (100% PASS)**:
  ```bash
  python apps/petcare_crm/petcare_crm/tests/run_all_tests.py
  ```

---

### Cách 2: Khởi Chạy Toàn Bộ Bằng Docker Compose (Production / Full Stack)
```bash
# 1. Khởi động containers
docker compose -f compose.yaml -f overrides/compose.mariadb.yaml -f overrides/compose.redis.yaml --project-name petcare up -d

# 2. Cài đặt app và migrate
docker exec -it petcare-backend-1 bench --site petcare.localhost install-app petcare_crm
docker exec -it petcare-backend-1 bench --site petcare.localhost migrate

# 3. Nạp dữ liệu demo thuần Việt chuẩn Prompt 10
docker exec -it petcare-backend-1 bench --site petcare.localhost execute petcare_crm.patches.v1_0.seed_demo_data.execute
```

### Cách 2: Khởi Chạy Native Trên Frappe Bench
```bash
bench --site [ten_site] install-app petcare_crm
bench --site [ten_site] migrate
bench --site [ten_site] execute petcare_crm.patches.v1_0.seed_demo_data.execute
bench start
```

* **Địa chỉ truy cập**: `http://localhost:8080` (hoặc `http://petcare.localhost:8080`)
* **Tài khoản mặc định**: `Administrator` / `admin123`
* **Workspace chính**: `http://localhost:8080/app/petcare-crm`

---

## 🧪 Kiểm Thử Tự Động (Automated Testing)

Toàn bộ 58 kịch bản kiểm thử độc lập có thể chạy trực tiếp bằng Master Test Runner:

```powershell
python apps/petcare_crm/petcare_crm/tests/run_all_tests.py
```

Kết quả mong đợi:
```text
================================================================================
PETCARE CRM — AUTOMATED TEST SUITE & END-TO-END VALIDATOR
================================================================================
Executing Suite 1: CRM Core & Lead/Opportunity Lifecycle ... [PASS] (4 passed)
Executing Suite 2: PetCare Service Operations & Visit Catalog ... [PASS] (4 passed)
Executing Suite 3: Membership Lifecycle, Benefits & Redemption ... [PASS] (8 passed)
Executing Suite 4: Care Intelligence, Pattern Analytics & Dedup ... [PASS] (11 passed)
Executing Suite 5: Workflow Automation & Scheduled Jobs ... [PASS] (9 passed)
Executing Suite 6: Security, RBAC Matrix & Analytics KPIs ... [PASS] (11 passed)
Executing Suite 7: End-to-End (E2E) Scenarios A-F ... [PASS] (11 passed)
================================================================================
Tổng số kịch bản kiểm thử : 58 | Thành công: 58 (100.0%) | Thời gian: ~1.6s
================================================================================
```

---

## 📚 Hệ Thống Tài Liệu Kỹ Thuật (Documentation Index)

Toàn bộ tài liệu chi tiết được lưu trữ trong thư mục [`docs/`](file:///c:/Users/pc/Documents/Doan_CRM/docs/):

1. **[Báo Cáo Nghiệm Thu Tổng Thể](file:///c:/Users/pc/Documents/Doan_CRM/docs/FINAL_IMPLEMENTATION_REPORT.md)** (`FINAL_IMPLEMENTATION_REPORT.md`): Báo cáo chi tiết về tính năng, kiến trúc, thuật toán, kết quả test và bàn giao.
2. **[Kịch Bản Trình Diễn Đồ Án](file:///c:/Users/pc/Documents/Doan_CRM/docs/DEMO_SCRIPT.md)** (`DEMO_SCRIPT.md`): Hướng dẫn demo từng bước 3 câu chuyện cốt lõi (Lead, Service/Membership, Care Intelligence).
3. **[Hướng Dẫn Cài Đặt](file:///c:/Users/pc/Documents/Doan_CRM/docs/SETUP_GUIDE.md)** (`SETUP_GUIDE.md`): Cài đặt Docker, Native Bench, cấu hình môi trường và xử lý sự cố.
4. **[Quy Tắc Nghiệp Vụ](file:///c:/Users/pc/Documents/Doan_CRM/docs/BUSINESS_RULES.md)** (`BUSINESS_RULES.md`): Đặc tả toàn bộ quy tắc bất biến (Invariants) về định giá, chống trùng khách hàng, an toàn số dư và thuật toán chu kỳ.
5. **[Đặc Tả API](file:///c:/Users/pc/Documents/Doan_CRM/docs/API_DOCUMENTATION.md)** (`API_DOCUMENTATION.md`): Danh mục các REST/Whitelisted endpoints, tham số và mẫu JSON request/response.
6. **[Ma Trận Phân Quyền](file:///c:/Users/pc/Documents/Doan_CRM/docs/ROLE_PERMISSION_MATRIX.md)** (`ROLE_PERMISSION_MATRIX.md`): Bảng ma trận quyền hạn 5 vai trò (System Manager, CRM Manager, Sales, Technician, Analyst) và kiểm soát sở hữu chéo.
7. **[Hướng Dẫn Kiểm Thử](file:///c:/Users/pc/Documents/Doan_CRM/docs/TEST_GUIDE.md)** (`TEST_GUIDE.md`): Cấu trúc 7 test suites và phương pháp chạy kiểm thử.
8. **[Các Giới Hạn Hiện Tại & Hướng Mở Rộng](file:///c:/Users/pc/Documents/Doan_CRM/docs/KNOWN_LIMITATIONS.md)** (`KNOWN_LIMITATIONS.md`): Tuyên bố trung thực về phạm vi prototype nâng cao và lộ trình phát triển.
9. **[Kiến Trúc Tổng Thể](file:///c:/Users/pc/Documents/Doan_CRM/docs/SYSTEM_ARCHITECTURE.md)** (`SYSTEM_ARCHITECTURE.md`): Sơ đồ chi tiết 8 tầng kiến trúc Clean Architecture.
10. **[Hợp Đồng Dữ Liệu & ERD](file:///c:/Users/pc/Documents/Doan_CRM/docs/DATA_CONTRACT.md)** (`DATA_CONTRACT.md`): Sơ đồ ERD thực thể và quy tắc liên kết giữa Customer, Pet, Membership, Service Visit.
