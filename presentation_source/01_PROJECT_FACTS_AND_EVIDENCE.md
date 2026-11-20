# PETCARE CRM — BẢNG TỔNG MỤC MINH CHỨNG & KIỂM TOÁN DỮ LIỆU (PROJECT FACTS & EVIDENCE LEDGER)

> **Mã hồ sơ**: `LEDGER-EVIDENCE-2026`  
> **Dự án**: PetCare CRM (Hệ thống CRM Dịch vụ Chăm sóc Thú cưng)  
> **Đơn vị kiểm toán**: Evidence Auditor & Technical Review Board  
> **Ngày cập nhật**: 07/11/2026  
> **Quy ước trạng thái minh chứng**:  
> • `IMPLEMENTED`: Đã có triển khai logic trong mã nguồn.  
> • `VERIFIED`: Đã được kiểm tra qua test tự động hoặc thao tác có thể tái hiện 100%.  
> • `DEMONSTRATED`: Có ảnh sơ đồ thật, UI tương tác hoặc video kiểm chứng.  
> • `SIMULATION`: Dữ liệu mô phỏng / kịch bản kinh doanh mẫu, không phải số liệu sổ sách thực.  
> • `DOCUMENTED_ONLY`: Chỉ xuất hiện trong tài liệu cũ, không khớp với mã nguồn thực tế.  
> • `UNVERIFIED`: Chưa đủ dữ kiện để khẳng định.  
> • `NOT_FOUND`: Đã tìm kiếm hợp lý nhưng không tồn tại trong repository.  

---

## 1. DANH SÁCH CON SỐ BỊ CẤM HOẶC CẦN ĐÍNH CHÍNH (PROHIBITED & RECTIFIED NUMBERS)

> [!CAUTION]
> **CẢNH BÁO KIỂM TOÁN ĐẶC BIỆT DÀNH CHO NGƯỜI LÀM SLIDE & THUYẾT TRÌNH**  
> Dưới đây là các con số từng xuất hiện trong các bản thảo báo cáo cũ hoặc lời đồn đoán. Sinh viên **TUYỆT ĐỐI KHÔNG ĐƯỢC ĐƯA LÊN SLIDE NHƯ SỰ THẬT HIỆN TẠI** nếu không đi kèm lời đính chính kỹ thuật:

| Con số cũ / Tuyên bố cũ | Hiện trạng thực tế đã kiểm chứng | Lý do mâu thuẫn & Hướng dẫn sử dụng trên Slide | Trạng thái kiểm toán |
|---|---|---|:---:|
| **"Hệ thống có đúng 11 DocTypes"** | Hệ thống hiện có **14 DocTypes** (12 Regular DocTypes + 2 Child Tables). | Ban đầu chỉ có 11 Standard DocTypes và 2 Child Tables (tổng 13). Sau đợt vá lỗi kiểm toán (Finding-11), DocType `PetCare Appointment` được bổ sung để hoàn thiện chức năng đặt lịch. Tổng cộng là **14 DocTypes**. | `RECTIFIED` (Dùng số 14) |
| **"Có 47 (hoặc 48) whitelisted APIs"** | Hệ thống hiện có **53 hàm `@frappe.whitelist()`** trong `api.py`. | Các báo cáo cũ đếm 47 hoặc 48 endpoints. Trong phiên bản hoàn thiện, 5 endpoints mới được bổ sung: `generate_portal_token`, `create_appointment`, `get_appointments`, `check_in_appointment`, `cancel_appointment`. Tổng chính xác là **53 endpoints**. | `RECTIFIED` (Dùng số 53) |
| **"Đạt 58/58 (hoặc 68/68) test pass"** | Hệ thống hiện đạt **88 / 88 Tests PASS (100.0%)** chia thành **10 Suites**. | Ban đầu có 58 tests (Suites 1–7), sau mở rộng thành 68 tests (Suite 8), sau đó bổ sung Suite 9 (WordPress Lead Form - 6 tests) và Suite 10 (Audit Remediation - 14 tests). Tổng số test hiện tại là **88 tests**, chạy trong **~2.34s**. | `RECTIFIED` (Dùng số 88) |
| **"Hệ thống có 5 vai trò (Roles)"** | Hệ thống có **7 vai trò người dùng chuẩn Frappe** (6 Desk + 1 Portal). | Các tài liệu cũ gộp vai trò hoặc chỉ liệt kê 5 vai trò Desk. File [`install.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/setup/install.py) và [`hooks.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/hooks.py) định nghĩa rõ ràng 7 roles: Front Desk, Veterinarian, Groomer, Manager, Sales, Analyst, Customer Portal. | `RECTIFIED` (Dùng số 7) |
| **"Tăng trưởng doanh thu 38%, tỷ lệ churn giảm từ 35% về 12%"** | Đây là **Kịch bản mô phỏng tài chính (Simulation Scenario)** trong mô hình CLV & ABC. | Không được trình bày như kết quả kinh doanh thực tế của một doanh nghiệp có thật. Phải ghi rõ *"Số liệu minh họa từ mô hình định giá trị tài chính CLV"*. | `SIMULATION` (Ghi rõ nhãn) |
| **"Care Intelligence là thuật toán Trí tuệ Nhân tạo / Machine Learning AI"** | Đây là **Thuật toán thống kê Rule-Based minh bạch** (Tukey IQR + EWMA + Hệ số mùa/tuổi). | Mã nguồn không sử dụng thư viện Machine Learning (như PyTorch/TensorFlow) mà dùng công thức toán thống kê giải thích được (*Explainable Mathematics*). Không được quảng cáo là AI/ML để tránh bị hội đồng trừ điểm học thuật. | `RECTIFIED` (Mô tả đúng) |
| **"Hệ thống bảo mật 100%, chống gian lận tuyệt đối"** | Hệ thống sử dụng **HMAC-SHA256, Idempotency Replay Guard, BOLA Guard và Row Lock**. | Không có hệ thống nào bảo mật 100%. Phải trình bày cụ thể các cơ chế phòng vệ có bằng chứng trong code. | `PROHIBITED` (Cấm nói 100%) |

---

## 2. BẢNG TỔNG MỤC MINH CHỨNG CHI TIẾT (MASTER EVIDENCE LEDGER)

### 2.1. Nhóm Nghiệp Vụ CRM & Vòng Đời Khách Hàng (CRM Core)

| Claim ID | Tuyên bố nghiệp vụ | Trạng thái | Nguồn kiểm chứng (File & Symbol) | Phương pháp kiểm chứng | Ghi chú & Giới hạn |
|:---:|---|:---:|---|---|---|
| **CRM-001** | Chuẩn hóa số điện thoại Việt Nam (+84, 09x về 84xxx), ngăn ngừa sai lệch định dạng. | `VERIFIED` | [`petcare_crm/utils/lead_service.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/utils/lead_service.py#L35): `_normalize_vn_phone` | Chạy Test Suite 1 & Suite 9 | Hỗ trợ các đầu số di động 10 số hiện hành tại Việt Nam. |
| **CRM-002** | Bẫy bot Honeypot trên Lead Form, ngăn chặn spam tự động từ internet mà không cần Captcha cồng kềnh. | `VERIFIED` | [`petcare_crm/api.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/api.py): `submit_website_lead` (kiểm tra `hp_field`) | Chạy Test Suite 9 (test_honeypot_trap_blocks_bot) | Nếu bot điền trường ẩn `hp_field`, hệ thống âm thầm trả về thành công giả lập và không ghi DB. |
| **CRM-003** | Khử trùng lặp khách hàng (Deduplication): Tìm kiếm Contact theo SĐT trước khi tạo mới. | `VERIFIED` | [`petcare_crm/utils/lead_service.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/utils/lead_service.py#L90): `LeadConversionCoordinator.convert_lead` | Chạy Test Suite 1 (test_03_lead_deduplication) | Nếu đã tồn tại Contact trùng SĐT, hệ thống tái sử dụng Contact và gán Pet mới. |
| **CRM-004** | Chuyển đổi Lead 1 chạm thành Contact, Pet và Opportunity trong cùng một giao dịch ACID. | `VERIFIED` | [`petcare_crm/api.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/api.py): `convert_lead_to_customer` | Chạy Test Suite 7 (Scenario A: E2E Lead to Customer) | Đảm bảo tính toàn vẹn, rollback nếu một trong các bước thất bại. |
| **CRM-005** | Quản lý Phễu bán hàng (Sales Pipeline) 6 giai đoạn với tỷ lệ xác suất có trọng số. | `VERIFIED` | [`petcare_crm/utils/sales_pipeline_service.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/utils/sales_pipeline_service.py): `OPPORTUNITY_STAGES` | Đọc code & Test Suite 1 (test_04_sales_pipeline_stages) | Prospecting (10%), Qualification (25%), Proposal (60%), Negotiation (80%), Closed Won (100%), Closed Lost (0%). |
| **CRM-006** | Bắt buộc nhập lý do thất bại (`lost_reason`) khi chuyển cơ hội sang Closed Lost. | `VERIFIED` | [`petcare_crm/utils/sales_pipeline_service.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/utils/sales_pipeline_service.py): `update_stage` | Chạy Test Suite 1 (test_04_pipeline) | Ném ngoại lệ `ValidationError` nếu thiếu `lost_reason`. |

---

### 2.2. Nhóm Vận Hành Dịch Vụ & Hồ Sơ Thú Cưng (Pet & Service Ops)

| Claim ID | Tuyên bố nghiệp vụ | Trạng thái | Nguồn kiểm chứng (File & Symbol) | Phương pháp kiểm chứng | Ghi chú & Giới hạn |
|:---:|---|:---:|---|---|---|
| **OPS-001** | Hỗ trợ hộ gia đình đa thú cưng (Multi-Pet Household, quan hệ $1:N$ giữa Contact và Pet). | `VERIFIED` | Schema [`pet.json`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/petcare_crm/doctype/pet/pet.json) trường `customer` (Link -> Contact) | Test Suite 2 & dữ liệu mẫu khách hàng An (2 pets: Bơ & Đậu Đậu) | Cho phép theo dõi lịch sử độc lập cho từng bé. |
| **OPS-002** | Cập nhật cân nặng lâm sàng sau mỗi lần thực hiện dịch vụ vào hồ sơ thú cưng. | `VERIFIED` | [`petcare_crm/utils/service_operations.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/utils/service_operations.py): `ServiceOperationsService.record_visit` | Test Suite 2 (test_01_service_visit_creation) | Trường `weight_kg` trên Pet tự động nhận giá trị mới nhất từ Service Visit. |
| **OPS-003** | Khởi tạo lịch hẹn (`PetCare Appointment`) và hỗ trợ Check-in tại quầy sinh phiếu Service Visit. | `VERIFIED` | [`petcare_crm/api.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/api.py): `create_appointment`, `check_in_appointment` | Test Suite 10 (Finding-11 Remediation Test) | Lễ tân check-in sẽ tự động đổi trạng thái lịch hẹn thành `Checked-In` và tạo `Service Visit`. |
| **OPS-004** | Quản lý sự cố sau dịch vụ (`PetCare Case`) kết nối với phiếu Service Visit và giám sát SLA. | `VERIFIED` | [`petcare_crm/api.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/api.py): `create_service_case`, `update_case_status` | Test Suite 5 (test_04_sla_monitoring) | Cảnh báo khiếu nại quá hạn SLA qua Hourly Workflow Task. |

---

### 2.3. Nhóm Thẻ Hội Viên & Sổ Cái Quyền Lợi (Membership & Loyalty)

| Claim ID | Tuyên bố nghiệp vụ | Trạng thái | Nguồn kiểm chứng (File & Symbol) | Phương pháp kiểm chứng | Ghi chú & Giới hạn |
|:---:|---|:---:|---|---|---|
| **MEM-001** | Cấn trừ quyền lợi thẻ hội viên (100% FREE hoặc chiết khấu %) tự động khi làm dịch vụ. | `VERIFIED` | [`petcare_crm/utils/membership_service.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/utils/membership_service.py): `MembershipService.redeem_benefit` | Test Suite 3 (8 tests PASS) | Khấu trừ số lượt còn lại (`remaining_quantity`), ghi nhật ký BRL. |
| **MEM-002** | Cơ chế khóa dòng dữ liệu (`FOR UPDATE`) ngăn ngừa trừ trùng lặp (Race Condition) khi thao tác đồng thời. | `VERIFIED` | [`petcare_crm/api.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/api.py#L180): `record_benefit_usage` | Code audit & Test Suite 3 (test_05_concurrency_lock) | Sử dụng Pessimistic Locking trên hàng của bảng `tabCustomer Membership`. |
| **MEM-003** | Bảo vệ Idempotency bằng `idempotency_key`, ném lỗi nếu client gửi trùng request cấn trừ. | `VERIFIED` | [`petcare_crm/utils/membership_service.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/utils/membership_service.py): `BenefitRedemptionLedger.check_idempotency` | Test Suite 3 (test_04_idempotent_redemption) | Ngăn chặn trừ 2 lần khi mạng chập chờn hoặc nhân viên bấm đúp chuột. |
| **MEM-004** | Ngăn chặn số dư âm và số lượt âm (`remaining_quantity >= 0`, `balance >= 0`). | `VERIFIED` | [`petcare_crm/utils/membership_service.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/utils/membership_service.py): Invariant assertions | Test Suite 3 (test_02_insufficient_benefits) | Ném ngoại lệ `InsufficientBenefitsException` nếu không đủ lượt. |
| **MEM-005** | Hỗ trợ gia hạn thẻ và bảo lưu lượt tồn (Benefit Rollover) sang chu kỳ thẻ mới. | `VERIFIED` | [`petcare_crm/api.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/api.py): `renew_membership` với tham số `allow_rollover=1` | Test Suite 3 (test_06_membership_rollover) | Số lượt chưa dùng của thẻ cũ được cộng dồn vào thẻ mới kích hoạt. |

---

### 2.4. Nhóm Trí Tuệ Chăm Sóc & Giữ Chân Khách Hàng (Care Intelligence)

| Claim ID | Tuyên bố nghiệp vụ | Trạng thái | Nguồn kiểm chứng (File & Symbol) | Phương pháp kiểm chứng | Ghi chú & Giới hạn |
|:---:|---|:---:|---|---|---|
| **CARE-001** | Lọc dữ liệu ngoại lai bằng khoảng tứ phân vị (Tukey IQR) cho chuỗi lịch sử $\ge 4$ lần thăm khám. | `VERIFIED` | [`petcare_crm/utils/care_pattern_service.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/utils/care_pattern_service.py#L85): `CarePatternAnalyzer._filter_outliers_iqr` | Test Suite 4 (test_02_iqr_outlier_filtering) | Loại bỏ các khoảng cách bất thường do chủ nuôi đi công tác đột xuất. |
| **CARE-002** | Tính toán chu kỳ trung bình có trọng số thời gian bằng Trung bình động hàm mũ (EWMA, $\alpha=0.6$). | `VERIFIED` | [`petcare_crm/utils/care_pattern_service.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/utils/care_pattern_service.py#L115): `CarePatternAnalyzer._calculate_ewma` | Test Suite 4 (test_03_ewma_calculation) | Ưu tiên các khoảng cách ghé thăm gần nhất phản ánh đúng thói quen hiện tại. |
| **CARE-003** | Điều chỉnh chu kỳ theo hệ số biến thiên Mùa vụ (Seasonal Factor) và Độ tuổi (Age Factor). | `VERIFIED` | [`petcare_crm/utils/care_pattern_service.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/utils/care_pattern_service.py): `SeasonalAdjustmentHelper`, `PetAgeAdjustmentHelper` | Test Suite 8 (Tests 1, 2, 3 PASS) | Mùa nóng rút ngắn chu kỳ tắm sấy (0.80-0.85); chó con/già có hệ số riêng. |
| **CARE-004** | Phân loại trạng thái sinh học: `STABLE`, `DUE_SOON` ($\le 3$ ngày đến hạn) và `AT_RISK` ($\ge 1.5\times$ chu kỳ). | `VERIFIED` | [`petcare_crm/utils/care_pattern_service.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/utils/care_pattern_service.py): `RiskDetectionService.evaluate_status` | Test Suite 4 (test_04_status_classification) | Tự động cập nhật vào bản ghi `Care Recommendation`. |
| **CARE-005** | Khử trùng lặp đề xuất chăm sóc: Gating 7 ngày không tạo khuyến nghị trùng cho cùng một thú cưng. | `VERIFIED` | [`petcare_crm/utils/recommendation_service.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/utils/recommendation_service.py): `CareRecommendationCoordinator.generate_recommendations` | Test Suite 4 (test_08_anti_duplicate_gating) | Tránh làm phiền khách hàng khi nhân viên chạy scan nhiều lần trong tuần. |

---

### 2.5. Nhóm Thanh Toán, Webhook & Tích Hợp Đa Kênh (Integrations)

| Claim ID | Tuyên bố nghiệp vụ | Trạng thái | Nguồn kiểm chứng (File & Symbol) | Phương pháp kiểm chứng | Ghi chú & Giới hạn |
|:---:|---|:---:|---|---|---|
| **INT-001** | Sinh mã VietQR động theo chuẩn Napas247 chứa mã phiếu `PC-SVC-*` hoặc mã thẻ `PC-MEM-*`. | `VERIFIED` | [`petcare_crm/utils/payment_gateway.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/utils/payment_gateway.py): `VietQRGenerator` | Test Suite 8 (Test 4 PASS) | Sinh chuỗi payload EMVCo và URL ảnh QR hiển thị tại quầy thu ngân POS. |
| **INT-002** | Webhook ngân hàng tự động đối soát IPN, gạch nợ phiếu Service Visit hoặc nạp tiền ví trả trước. | `VERIFIED` | [`petcare_crm/api.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/api.py): `payment_webhook` | Test Suite 8 (Tests 5, 6, 7 PASS) | Bắt buộc đối soát đúng số tiền (`amount_mismatch_guard`), sai lệch sẽ báo lỗi. |
| **INT-003** | Xác thực chữ ký số HMAC-SHA256 trên Webhook ngân hàng chống giả mạo gói tin thanh toán. | `VERIFIED` | [`petcare_crm/utils/payment_gateway.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/utils/payment_gateway.py): `PaymentWebhookService._verify_hmac_signature` | Test Suite 8 (Test 5: invalid signature returns 401) | Sử dụng `hmac.compare_digest` chống tấn công đo thời gian (Timing Attack). |
| **INT-004** | Chống tấn công gửi lại (Replay Attack Guard) trên Webhook bằng bảng kiểm toán giao dịch. | `VERIFIED` | [`petcare_crm/utils/payment_gateway.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/utils/payment_gateway.py): `_is_transaction_processed` | Test Suite 8 (Test 6: replay transaction returns 200 ignored) | Giao dịch đã xử lý sẽ bỏ qua an toàn, không nạp tiền lần 2. |
| **INT-005** | Bộ điều phối tin nhắn đa kênh (Zalo ZNS / SMS Brandname) với chế độ Safe Mode Outbox. | `VERIFIED` | [`petcare_crm/utils/omnichannel_service.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/utils/omnichannel_service.py): `OmnichannelDispatcher` | Test Suite 8 (Test 8 PASS) | Mặc định không gửi tin thật đến nhà mạng; ghi log vào Outbox để dev/demo an toàn. |
| **INT-006** | Phòng vệ BOLA / IDOR trên Cổng Chủ Nuôi bằng Signed Portal Token. | `VERIFIED` | [`petcare_crm/api.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/api.py#L4150-L4195): `_verify_owner_portal_access` | Test Suite 10 (Finding P0 Remediation Test) | Khách vãng lai không có token hợp lệ bị chặn 403 khi cố xem hồ sơ người khác. |

---

### 2.6. Nhóm Báo Cáo KPI & Quản Trị Tài Chính (Analytics & Finance)

| Claim ID | Tuyên bố nghiệp vụ | Trạng thái | Nguồn kiểm chứng (File & Symbol) | Phương pháp kiểm chứng | Ghi chú & Giới hạn |
|:---:|---|:---:|---|---|---|
| **KPI-001** | Báo cáo Script Report 8 chỉ số KPI chuẩn trong Frappe Desk UI. | `VERIFIED` | [`petcare_crm/petcare_crm/report/petcare_kpi_overview/`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/petcare_crm/report/petcare_kpi_overview/) | Test Suite 6 (test_kpi_dashboard) & xem trong Desk | Lead Win Rate, Pipeline Value, Active Memberships, Service Revenue, Due Soon, At Risk, Retention Rate. |
| **KPI-002** | Phân tích hiệu quả hoạt động đối sánh đa chi nhánh (`CN-TRUNGTAM`, `CN-QUAN1`, `CN-THUDUC`, `CN-BINHTHANH`). | `VERIFIED` | [`petcare_crm/utils/analytics_service.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/utils/analytics_service.py#L370): `get_branch_comparison_metrics` | Test Suite 6 (test_branch_performance) | Tách bạch doanh thu niêm yết, doanh thu thực nhận và số lượt phục vụ từng cơ sở. |
| **FIN-001** | Bảng tính mô hình Giá thành Hoạt động (Activity-Based Costing - ABC) 4 Cost Pools. | `VERIFIED` (Mô hình) | [`deliverables/finance/CLV_ABC_Model.xlsx`](file:///c:/Users/pc/Documents/Doan_CRM/deliverables/finance/CLV_ABC_Model.xlsx) & Report Word | Mở file Excel kiểm tra công thức tính | Bóc tách chi phí Bác sĩ/KTV, vật tư y tế, khấu hao máy móc và quản lý chung. |
| **FIN-002** | Mô hình Định giá trị Vòng đời Khách hàng (Customer Lifetime Value - CLV) chiết khấu dòng tiền DCF. | `SIMULATION` | [`deliverables/finance/PetCare_CRM_CLV_ABC_Report.md`](file:///c:/Users/pc/Documents/Doan_CRM/deliverables/finance/PetCare_CRM_CLV_ABC_Report.md) | Đối chiếu công thức tài chính DCF | Dựa trên giả định kinh tế minh họa: vòng đời nuôi thú cưng 10 năm, lãi suất chiết khấu 10%/năm. |

---

### 2.7. Nhóm Kiểm Thử & Đảm Bảo Chất Lượng (Quality Assurance)

| Claim ID | Tuyên bố kỹ thuật | Trạng thái | Nguồn kiểm chứng (File & Symbol) | Phương pháp kiểm chứng | Ghi chú & Giới hạn |
|:---:|---|:---:|---|---|---|
| **QA-001** | Bộ kiểm thử tự động đạt 88/88 test cases PASS (100.0%) không có lỗi cú pháp hoặc runtime. | `VERIFIED` | [`petcare_crm/tests/run_all_tests.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/tests/run_all_tests.py) | Chạy lệnh `python run_all_tests.py` | 10 Suites độc lập bao phủ CRM Core, Ops, Membership, Care Engine, Automation, Security, E2E, Extensions, WordPress và Audit Remediation. |
| **QA-002** | Thời gian thực thi toàn bộ 88 bài test hoàn tất trong khoảng 2.3 – 2.5 giây. | `VERIFIED` | Đầu ra thực tế từ lệnh chạy test | Đo bằng `time.perf_counter()` trong runner | Thời gian cực nhanh do sử dụng Pure Python Adapter cách ly không phụ thuộc mạng/DB. |
| **QA-003** | Khả năng chạy kiểm thử độc lập mà không bắt buộc cài đặt MariaDB hay Frappe Bench. | `VERIFIED` | [`petcare_crm/utils/frappe_adapters.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/utils/frappe_adapters.py) | Chạy trực tiếp trên Windows Host | Đảm bảo tính tái lập (Reproducibility) cao khi chấm đồ án trên mọi máy tính. |
