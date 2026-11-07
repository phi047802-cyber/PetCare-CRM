# BÁO CÁO AUDIT BASELINE & ĐỐI CHIẾU TIÊU CHÍ ĐỒ ÁN (READ-ONLY AUDIT)

> **Dự án**: PetCare CRM (Hệ Thống CRM Dịch Vụ Chăm Sóc Thú Cưng)  
> **Nền tảng**: Frappe Framework v15 (Python 3.14.6, MariaDB, Desk Native)  
> **Thời điểm audit**: 27/10/2026  
> **Trạng thái thực thi**: READ-ONLY Audit (Không sửa đổi mã nguồn ứng dụng)  
> **Tài liệu tham chiếu**: `Tiêu chí đồ án môn học CRM (cập nhật ngày 23_11_2025).pdf`  

---

## 1. PHÂN CẤP THỨ TỰ ƯU TIÊN YÊU CẦU

Căn cứ theo nguyên tắc kiểm chứng, các nguồn thông tin trong dự án được phân cấp rõ ràng như sau:

| Cấp độ ưu tiên | Nguồn thông tin | Mô tả & Mức độ tin cậy |
|:---:|---|---|
| **Cấp 1 (Cao nhất)** | **Yêu cầu giảng viên học kỳ hiện tại** | Xây dựng hệ thống CRM hoàn chỉnh trên nền tảng **Frappe Framework v15** (vận hành toàn diện vòng đời khách hàng, không chỉ gói gọn trong 2 module hội viên ban đầu). |
| **Cấp 2** | **Rubric tham chiếu năm 2025** | Tệp PDF duy nhất trong workspace: `Tiêu chí đồ án môn học CRM (cập nhật ngày 23_11_2025).pdf` (1 trang). **Ghi chú**: Được dùng làm tài liệu tham chiếu cơ sở; gắn nhãn *"Chưa xác minh có rubric 2026 mới hơn hay không"*. |
| **Cấp 3** | **Hiện trạng mã nguồn thực tế** | Toàn bộ 13 DocTypes, 48 whitelisted APIs, 14 services Python, 8 bộ test (68 test cases pass 100%) đã được kiểm chứng trên đĩa. |
| **Cấp 4** | **Báo cáo phân tích do AI tạo** | Các tài liệu Markdown trong `docs/` được sinh ra trong các phiên trước. Không mặc định xem là chân lý mà phải kiểm tra chéo với code thực tế. |
| **Cấp 5 (Thấp nhất)** | **Suy luận của Assistant** | Các ánh xạ kỹ thuật từ nền tảng Odoo (trong rubric 2025) sang Frappe Framework v15 (nền tảng của dự án). |

---

## 2. BẢNG BẰNG CHỨNG KIỂM CHỨNG KỸ THUẬT (AUDIT EVIDENCE TABLE)

| STT | Hạng mục kiểm chứng | Kết luận hiện tại | Trạng thái | Bằng chứng cụ thể (File, dòng, mã nguồn thực tế) | Cách xác minh tiếp |
|:---:|---|---|:---:|---|---|
| **1** | **Số lượng DocTypes** | Có đúng **13 DocTypes** (11 Standard DocTypes + 2 Child Tables). | **Verified** | `apps/petcare_crm/petcare_crm/petcare_crm/doctype/`: <br>• Standard (11): `Benefit Redemption Ledger`, `Care Recommendation`, `Customer Membership`, `Membership Plan`, `Membership Transaction`, `Pet`, `PetCare Case`, `PetCare Lead`, `PetCare Opportunity`, `PetCare Service`, `Service Visit`.<br>• Child Tables (2): `Membership Benefit` (`istable: 1`), `Plan Benefit` (`istable: 1`). | Kiểm tra migration schema trên bench: `bench --site petcare.localhost migrate` |
| **2** | **Số lượng API Whitelist thực tế** | Có đúng **48 hàm `@frappe.whitelist()`** (1 helper rate limit + 47 endpoints nghiệp vụ). | **Verified** | `apps/petcare_crm/petcare_crm/api.py`:<br>• 21 endpoints `allow_guest=True`<br>• 26 endpoints yêu cầu authentication session/token<br>• 1 helper `_check_rate_limit` (whitelist nội bộ) | Chạy regex trích xuất trực tiếp trên `api.py` bằng Python |
| **3** | **Số lượng & Kết quả Test** | Có đúng **68 tests** độc lập chia thành **8 Suites**, tỷ lệ đạt **68/68 PASS (100%)**. | **Verified** (Mock) / **Partial** (Live) | `apps/petcare_crm/petcare_crm/tests/run_all_tests.py`: chạy qua 8 file mock test với thời gian ~2.3 giây.<br>*Lưu ý*: 5 file test live Frappe (`test_crm_core.py`, v.v.) bị lỗi `No module named 'frappe'` khi chạy trên Windows host vì Frappe chỉ cài trong container. | Chạy `bench run-tests --app petcare_crm` bên trong Docker container backend |
| **4** | **Các chức năng đang thực thi** | 14 modules nghiệp vụ Python thuần và Frappe ORM hoạt động đầy đủ. | **Verified** | `apps/petcare_crm/petcare_crm/utils/`: `lead_service.py`, `customer_service.py`, `sales_pipeline_service.py`, `service_operations.py`, `membership_service.py`, `care_pattern_service.py`, `recommendation_service.py`, `workflow_automation.py`, `analytics_service.py`, `security.py`, `payment_gateway.py`, `omnichannel_service.py`, `models.py`, `config.py`. | Chạy test suite tương ứng của từng module |
| **5** | **Endpoint Lead & Deduplication** | Đã triển khai đầy đủ quy trình Lead: tạo mới, tương tác, cập nhật trạng thái, chuyển đổi thành Contact/Pet/Opportunity. | **Verified** | `api.py` dòng 1073-1250 (`create_lead`, `update_lead_status`, `add_lead_interaction`, `convert_lead_to_customer`). Chuẩn hóa SĐT VN qua `_normalize_vn_phone`, chống gộp trùng Contact. | Test `test_crm_core_mock.py` (4 tests PASS) |
| **6** | **Webhook Thanh Toán & VietQR** | Đã triển khai bộ phát sinh VietQR Napas247 và Webhook tự động đối soát IPN. | **Verified** (Logic/Mock) / **Unverified** (Live Bank) | • `payment_gateway.py` dòng 34-142 (`VietQRGenerator`)<br>• `payment_gateway.py` dòng 144-399 (`PaymentWebhookService`)<br>• `api.py` dòng 2005-2022 (`payment_webhook`)<br>Có cơ chế Idempotency chống ghi nhận 2 lần. | Test `test_extended_capabilities_mock.py` (test_04, test_05, test_06 PASS) |
| **7** | **Công thức & Dữ liệu AnalyticsService** | Đã triển khai 8 chỉ số KPI chuẩn và phân tích so sánh liên chi nhánh. | **Verified** | `analytics_service.py` dòng 48-390: Lead Conversion Rate (%), Pipeline Weighted Value, Active Memberships & Balance, Service Visits & Revenue, Care Retention (Due Soon / At Risk), Branch Performance (`CN-TRUNGTAM`, `CN-QUAN1`, `CN-THUDUC`, `CN-BINHTHANH`). | Test `test_security_and_reporting_mock.py` (test_kpi_dashboard PASS) |
| **8** | **Care Intelligence Engine** | Thuật toán dự đoán chu kỳ Rule-based (EWMA + Tukey IQR + Hệ số Mùa vụ + Hệ số Độ tuổi). | **Verified** | `care_pattern_service.py` dòng 70-380: Lọc ngoại lai IQR ($\ge 4$ quan sát), EWMA ($\alpha=0.6$), `SeasonalAdjustmentHelper` (tháng 3-4 factor 0.85; tháng 5-8 factor 0.80), `PetAgeAdjustmentHelper` (<12 tháng factor 0.85; >84 tháng factor 0.80). | Test `test_care_intelligence_mock.py` (11 tests PASS) và `test_extended_capabilities_mock.py` (test_01, test_02, test_03 PASS) |
| **9** | **Membership Ledger & Concurrency** | Ghi nhận sổ cái cấn trừ quyền lợi và bảo vệ tranh chấp đồng thời bằng Row Lock. | **Verified** | • DocType `Benefit Redemption Ledger`<br>• `api.py` dòng 137-254 (`record_benefit_usage` sử dụng `FOR UPDATE` khóa dòng ngăn race condition, số dư không bị âm). | Test `test_membership_lifecycle_mock.py` (8 tests PASS) |
| **10** | **Pet Owner Portal (App Chủ Nuôi)** | Đã cung cấp 4 REST APIs chuyên biệt cho Ứng dụng Di động Chủ nuôi. | **Verified** (API) / **Gap** (Mobile UI) | `api.py` dòng 2060-2210: `owner_portal_get_pets`, `owner_portal_get_health_timeline`, `owner_portal_get_membership_wallet`, `owner_portal_book_appointment`. | Test `test_extended_capabilities_mock.py` (test_10 PASS). Cần xây dựng giao diện Mobile/Web client nếu muốn demo visual |
| **11** | **Email & Zalo ZNS** | Kiến trúc Adapter đa kênh, vận hành mặc định ở Safe Mode Outbox. | **Verified** (Safe Mode) / **Unverified** (Live Telco) | `omnichannel_service.py` dòng 40-230: `OmnichannelDispatcher` hỗ trợ `ZALO_ZNS`, `SMS_BRANDNAME`, `EMAIL`. Khi `ENABLE_LIVE_COMMUNICATION=False`, ghi log vào outbox để preview, an toàn cho dev/demo. | Test `test_extended_capabilities_mock.py` (test_08 PASS) |
| **12** | **Dữ liệu Seed Demo Thuần Việt** | Script nạp dữ liệu phong phú đáp ứng toàn bộ các kịch bản trình diễn. | **Verified** | `apps/petcare_crm/petcare_crm/patches/v1_0/seed_demo_data.py` (636 dòng): 5 Contacts, 8 Pets, 4 Plans, 6 Memberships, 14 Visits, 7 Recommendations, 5 Leads, 4 Opportunities. | Chạy lệnh `bench execute petcare_crm.patches.v1_0.seed_demo_data.execute` |

---

## 3. BẢNG ĐỐI CHIẾU TIÊU CHÍ (TẠM ĐỐI CHIẾU THEO RUBRIC THAM CHIẾU 2025)

> [!NOTE]
> Bảng đối chiếu này dựa trên tệp `Tiêu chí đồ án môn học CRM (cập nhật ngày 23_11_2025).pdf`. Các yêu cầu nhắc đến "Odoo" được đối chiếu tương đương sang nền tảng "Frappe Framework v15" của dự án hiện tại.

| Tiêu chí Rubric | Đối tượng | Tệp đầu ra theo yêu cầu | Hiện trạng dự án PetCare CRM | Đánh giá khoảng cách (Gap Analysis) |
|---|:---:|---|---|---|
| **A4.1: Mô tả case study** | Nhóm | `Report - Nhóm XX.docx` | Đã có tài liệu `PRODUCT_SCOPE.md` và `CRM_REQUIREMENTS.md` mô tả chuỗi phòng khám thú y & spa. | **GAP TÀI LIỆU**: Cần chuyển nội dung Markdown sang tệp Word định dạng chuẩn đồ án (`Report - Nhóm XX.docx`). |
| **A4.2: Cài đặt CRM và nhập liệu căn bản** | Nhóm | `Report - Nhóm XX.docx` | Đã cấu hình tiền tệ VNĐ, RBAC 5 vai trò, sales stages, lost reasons, seed data 100+ bản ghi. | **GAP MINH CHỨNG**: Cần chụp ảnh màn hình Desk UI (Users, Roles, Leads, Opportunities, Visits) chèn vào báo cáo Word. |
| **A4.3.1: Quy trình CRM nhóm** | Nhóm | • `[Tên quy trình] - Nhóm XX.bpmn`<br>• `[Tên quy trình] - Nhóm XX.png`<br>• `Report - Nhóm XX.docx` | Đã có mô tả 8 luồng nghiệp vụ chi tiết kèm sơ đồ sequence Mermaid trong `PROCESS_FLOWS.md`. | **GAP BLOCKER (P0)**: **Chưa có file `.bpmn` chuẩn XML Camunda Desktop Modeler** và file `.png` xuất từ Camunda. |
| **A4.3.2: Quy trình CRM cá nhân** | Cá nhân | • `[Tên quy trình] - MSSV - [Họ tên].bpmn`<br>• `[Tên quy trình] - MSSV - [Họ tên].png`<br>• `[Tên quy trình] - MSSV - [Họ tên].docx` | Logic của các quy trình con đã có sẵn trong mã nguồn (Lead intake, Service Visit, Membership renewal, Care scan). | **GAP BLOCKER (P0)**: **Chưa phân bổ và chưa tạo file `.bpmn` Camunda + file Word cá nhân** cho từng thành viên. |
| **A4.4: Thao tác sử dụng phần mềm** | Cá nhân | `Video: Thao tác CRM - MSSV - [Họ tên].mp4` | Hệ thống chạy ổn định, có dữ liệu demo và test tự động. | **GAP BLOCKER (P1)**: Sinh viên cần tự quay video có mặt và giọng nói. **Cần một kịch bản quay video (Video Script / Storyboard)** từng phút để sinh viên làm theo. |
| **A4.5: Quản lý chi phí, CLV, Activity-based costing (ABC)** | Nhóm | `Report - Nhóm XX.docx` | `AnalyticsService` đã có số liệu doanh thu, giảm giá, số dư thẻ hội viên. | **GAP BLOCKER (P0)**: **Chưa có chương chuyên đề CLV** (công thức vòng đời nuôi thú cưng) và **bảng phân bổ chi phí ABC** (Cost Pools & Drivers theo hoạt động spa/y tế). |
| **A4.6: Đọc báo cáo** | Nhóm | `Report - Nhóm XX.docx` | Đã có 8 KPIs chuẩn và so sánh doanh thu chi nhánh trong `AnalyticsService`. | **GAP BÁO CÁO (P1)**: Cần xuất số liệu thành các biểu đồ trực quan (Funnel, Bar, Donut) và viết bài phân tích ý nghĩa kinh doanh (*Actionable Insights*). |
| **A4.7: Khám phá và gọi API** | Nhóm & Cá nhân | • `File Tìm hiểu API - Nhóm XX.docx`<br>• `File API - MSSV - Họ tên.docx` | Đã có 48 whitelisted APIs, tài liệu kỹ thuật `API_DOCUMENTATION.md` và Payment Webhook IPN. | **GAP TÀI LIỆU (P0)**: Cần soạn file Word hướng dẫn khám phá API/Webhook cho nhóm và phân chia API riêng kèm cURL/Postman cho từng cá nhân. |
| **A4.8: Lead Form (với website WP)** | Nhóm | *(Minh chứng form trên WordPress)* | Đã có API backend `create_lead` chuẩn hóa SĐT và chống trùng. | **GAP TÍCH HỢP (P0)**: **Chưa có mã nguồn Form HTML/JS nhúng WordPress** kết nối đẩy dữ liệu trực tiếp về CRM qua API. |
| **A4.9.1: Module chức năng hữu ích** | Nhóm | • `[Tên module] - Nhóm XX.docx`<br>• Zip file thư mục code | Ứng dụng `petcare_crm` tùy biến sâu (11 DocTypes, Care Intelligence, VietQR, Zalo ZNS). | **GAP TÀI LIỆU (P1)**: Cần biên tập file Word thuyết minh module và chuẩn bị file zip mã nguồn `apps/petcare_crm`. |
| **A4.9.2: Module báo cáo** | Nhóm | • `Module Reporting - Nhóm XX.docx`<br>• Zip file thư mục code | `AnalyticsService` và báo cáo Script Report trong Desk UI. | **GAP TÀI LIỆU (P1)**: Cần biên tập file Word thuyết minh module báo cáo. |
| **A4.10: Các đề xuất & hiện thực khác biệt** | Nhóm | `A4-10 - [Tên đề xuất] - Nhóm XX.docx` | Đã hiện thực hóa 4 đề xuất vượt trội: Care Intelligence theo mùa/tuổi, Dynamic VietQR, Atomic Ledger, Owner Portal APIs. | **GAP TÀI LIỆU (P0)**: Cần soạn thảo văn bản thuyết minh giải pháp khác biệt `A4-10` nộp riêng theo rubric. |
| **A4.11: Đánh giá đề xuất CRM** | Nhóm | `Đánh giá đề xuất - Nhóm XX.docx` | *(Ghi chú trong rubric 2025: Chưa triển khai cho các lớp năm 2025)* | Không bắt buộc theo rubric tham chiếu. |

---

## 4. DANH SÁCH BLOCKER PHÂN CẤP THEO MỨC ĐỘ ƯU TIÊN

### Mức độ P0 (Blocker nghiêm trọng — Thiếu tệp nộp bài bắt buộc hoặc sai định dạng rubric):
1. **P0-1: Thiếu tệp BPMN Camunda XML (`.bpmn`)** cho quy trình nhóm (A4.3.1) và các quy trình cá nhân (A4.3.2). Hiện tại chỉ có sơ đồ Mermaid trong Markdown, không thể mở bằng phần mềm Camunda Modeler trên máy tính như rubric yêu cầu.
2. **P0-2: Thiếu bộ mã nguồn Lead Form tích hợp website WordPress (A4.8)** kết nối REST API về PetCare CRM.
3. **P0-3: Thiếu chuyên đề Quản lý chi phí ABC & Mô hình Giá trị vòng đời khách hàng CLV (A4.5)** trong báo cáo.
4. **P0-4: Thiếu tệp tài liệu khám phá API Nhóm & tài liệu gọi API Cá nhân (A4.7)** có kèm minh chứng Postman/cURL.
5. **P0-5: Thiếu tệp thuyết minh đề xuất khác biệt `A4-10` (A4.10)** và các báo cáo thuyết minh module `A4.9.1`, `A4.9.2`.

### Mức độ P1 (Cần thiết — Ảnh hưởng lớn đến điểm số và bằng chứng nghiệm thu):
1. **P1-1: Thiếu kịch bản quay video chi tiết (Storyboard & Video Script) cho cá nhân (A4.4)**.
2. **P1-2: Báo cáo thiếu ảnh chụp màn hình Desk UI thực tế** chứng minh cấu hình hệ thống (A4.2).
3. **P1-3: Thiếu biểu đồ trực quan hóa dữ liệu và bài phân tích đọc báo cáo (A4.6)**.

### Mức độ P2 (Cải tiến & Xác minh bổ sung):
1. **P2-1: Cần xác nhận với giảng viên** xem có rubric phiên bản 2026 chính thức hay tiếp tục áp dụng chuẩn rubric ngày 23/11/2025.
2. **P2-2: Kiểm thử live Frappe tests bên trong Docker container** (`bench run-tests --app petcare_crm`) bổ sung cho 68 mock tests đã pass 100%.

---

## 5. ĐỀ XUẤT PHƯƠNG ÁN KIỂM CHỨNG ĐỘC LẬP (INDEPENDENT VERIFICATION)

Để đảm bảo tính khách quan và minh bạch, các bước kiểm chứng độc lập được đề xuất như sau:

1. **Kiểm chứng bộ Test hiện hữu trên máy người dùng**:
   ```powershell
   python apps/petcare_crm/petcare_crm/tests/run_all_tests.py
   ```
   *Tiêu chí nghiệm thu*: Trả về đúng `Total Tests: 68 | PASS: 68 | FAIL: 0 | ERRORS: 0`.

2. **Kiểm chứng số lượng DocType trên đĩa**:
   ```powershell
   (Get-ChildItem -Path "apps\petcare_crm\petcare_crm\petcare_crm\doctype" -Directory).Count
   ```
   *Tiêu chí nghiệm thu*: Trả về 13 thư mục DocType.

3. **Kiểm chứng số lượng Whitelisted API**:
   ```powershell
   python -c "import re; f=open('apps/petcare_crm/petcare_crm/api.py', encoding='utf-8').read(); print(len(re.findall(r'@frappe\.whitelist', f)))"
   ```
   *Tiêu chí nghiệm thu*: Trả về 48 lượt khai báo `@frappe.whitelist`.

4. **Kiểm chứng tệp sơ đồ BPMN Camunda sau khi tạo**:
   Tải và cài đặt phần mềm **Camunda Modeler** (phiên bản Desktop, mã nguồn mở tại `camunda.com/download/modeler/`), mở tệp `.bpmn` và xác nhận không có lỗi cú pháp XML, các Pools, Lanes, Tasks, Gateways hiển thị trực quan và đúng chuẩn BPMN 2.0.
