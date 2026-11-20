# PETCARE CRM — PHỤ LỤC TRA CỨU KỸ THUẬT & TỪ ĐIỂN CHUYÊN NGÀNH (APPENDIX TECHNICAL QA & GLOSSARY)

> **Mã hồ sơ**: `APPENDIX-TECH-2026`  
> **Dự án**: PetCare CRM (Hệ thống CRM Dịch vụ Chăm sóc Thú cưng)  
> **Mục tiêu**: Kho dữ liệu tra cứu kỹ thuật chi tiết phục vụ phiên phản biện chuyên sâu trước hội đồng chấm đồ án tốt nghiệp.  

---

## 1. BẢNG TRA CỨU CHI TIẾT 14 DOCTYPES THỰC TẾ

| STT | Tên DocType | Loại Thực Thể | Bảng CSDL (Table Name) | Naming Series / Autoname | Số Lượng Trường | Trường Khóa & Quan Hệ Liên Kết (Links / Child Tables) |
|:---:|---|:---:|---|---|:---:|---|
| **01** | `PetCare Lead` | Regular | `tabPetCare Lead` | `LEAD-.YYYY.-.#####` | 15 fields | `converted_contact` (Link -> Contact), `converted_pet` (Link -> Pet), `converted_opportunity` (Link -> PetCare Opportunity). |
| **02** | `Contact` | Regular (Core) | `tabContact` | Auto / `field:first_name` | 28+ fields | Đại diện cho Khách hàng / Chủ nuôi thú cưng; liên kết 1:N với Pet và Customer Membership. |
| **03** | `Pet` | Regular | `tabPet` | `PET-.YYYY.-.#####` | 7 fields | `customer` (Link -> Contact, Bắt buộc), `pet_name`, `species`, `breed`, `weight_kg`, `birth_date`. |
| **04** | `PetCare Service` | Regular | `tabPetCare Service` | `field:service_code` | 10 fields | `service_code`, `service_name`, `category`, `standard_price`, `default_cycle_days`, `target_species`. |
| **05** | `PetCare Appointment` | Regular | `tabPetCare Appointment` | `APT-.YYYY.-.#####` | 13 fields | `customer` (Link -> Contact), `pet` (Link -> Pet), `service` (Link -> PetCare Service), `linked_service_visit` (Link -> Service Visit). |
| **06** | `Service Visit` | Regular | `tabService Visit` | `SV-.YYYY.-.#####` | 16 fields | `customer` (Link -> Contact), `pet` (Link -> Pet), `service` (Link -> PetCare Service), `membership` (Link -> Customer Membership). |
| **07** | `PetCare Opportunity` | Regular | `tabPetCare Opportunity` | `OPP-.YYYY.-.#####` | 14 fields | `customer` (Link -> Contact), `lead` (Link -> PetCare Lead), `pet` (Link -> Pet), `expected_amount`, `sales_stage`. |
| **08** | `Membership Plan` | Regular | `tabMembership Plan` | `field:plan_name` | 5 fields | `plan_name`, `price`, `validity_days`, `benefits` (Table -> Plan Benefit). |
| **09** | `Plan Benefit` | Child Table | `tabPlan Benefit` | Auto Increment | 4 fields | `parent` (Link -> Membership Plan), `benefit_type`, `discount_type`, `total_quantity`. |
| **10** | `Customer Membership` | Regular | `tabCustomer Membership` | `MEM-.YYYY.-.#####` | 9 fields | `customer` (Link -> Contact), `membership_plan` (Link -> Membership Plan), `balance`, `benefits` (Table -> Membership Benefit). |
| **11** | `Membership Benefit` | Child Table | `tabMembership Benefit` | Auto Increment | 6 fields | `parent` (Link -> Customer Membership), `benefit_type`, `total_quantity`, `used_quantity`, `remaining_quantity`. |
| **12** | `Benefit Redemption Ledger` | Regular | `tabBenefit Redemption Ledger` | `BRL-.YYYY.-.#####` | 12 fields | `membership` (Link -> Customer Membership), `service_visit` (Link -> Service Visit), `benefit_type`, `quantity_deducted`. |
| **13** | `Membership Transaction` | Regular | `tabMembership Transaction` | `MT-.YYYY.-.#####` | 14 fields | `membership` (Link -> Customer Membership), `customer` (Link -> Contact), `transaction_type`, `amount`, `balance_after`. |
| **14** | `Care Recommendation` | Regular | `tabCare Recommendation` | `REC-.YYYY.-.#####` | 10 fields | `customer` (Link -> Contact), `pet` (Link -> Pet), `recommendation_type`, `status`, `due_date`, `priority`. |

---

## 2. MA TRẬN PHÂN QUYỀN RBAC 7 VAI TRÒ (ROLE-PERMISSION MATRIX)

Ký hiệu: **C** (Create), **R** (Read), **U** (Update/Write), **D** (Delete), **-** (Không có quyền).

| DocType Cốt Lõi | System Manager | PetCare Manager | PetCare Front Desk | PetCare Veterinarian | PetCare Groomer | PetCare Sales | PetCare Analyst | PetCare Portal (Khách) |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `PetCare Lead` | CRUD | CRUD | R | - | - | CRUD | R | - |
| `Contact` (Customer) | CRUD | CRUD | CRU | R | R | CRU | R | R (Chỉ xem bản thân) |
| `Pet` | CRUD | CRUD | CRU | CRU | RU (Cân nặng) | CRU | R | R (Chỉ xem bé mình) |
| `PetCare Service` | CRUD | CRUD | R | R | R | R | R | R (Xem bảng giá) |
| `PetCare Appointment` | CRUD | CRUD | CRUD | R | R | CRU | R | CR (Chỉ đặt lịch) |
| `Service Visit` | CRUD | CRUD | CRU | CRU | CRU | R | R | R (Chỉ xem lịch sử) |
| `PetCare Opportunity` | CRUD | CRUD | - | - | - | CRUD | R | - |
| `Membership Plan` | CRUD | CRUD | R | - | - | R | R | R (Xem gói) |
| `Customer Membership` | CRUD | CRUD | RU (Nạp/Gia hạn)| R | R | CRU | R | R (Xem số dư) |
| `Benefit Redemption Ledger`| CRUD | R (Kiểm toán) | R | - | - | - | R | - |
| `Membership Transaction` | CRUD | CRUD | CR | - | - | CR | R | R (Xem sao kê) |
| `Care Recommendation` | CRUD | CRUD | RU (Liên hệ) | R | R | RU (CSKH) | R | - |
| `PetCare Case` | CRUD | CRUD | CR | CR | CR | CR | R | CR (Gửi khiếu nại) |

---

## 3. TỔNG HỢP 10 TEST SUITES VÀ 88 BÀI TEST TỰ ĐỘNG

| Suite ID | Tên File Test | Lớp Kiểm Thử (Layer) | Số Bài Test | Trạng Thái Thực Thi | Nội Dung Kiểm Thử Trọng Tâm |
|:---:|---|---|:---:|:---:|---|
| **Suite 1** | `test_crm_core_mock.py` | Unit & Integration | 4 tests | **4/4 PASS** | Chuẩn hóa SĐT VN, Lead Lifecycle, Deduplication chống trùng, Sales Pipeline Kanban stages. |
| **Suite 2** | `test_service_operations_mock.py` | Unit & Integration | 4 tests | **4/4 PASS** | Danh mục dịch vụ chuẩn, tính giá dịch vụ, cấn trừ miễn phí 100%, cập nhật cân nặng Pet. |
| **Suite 3** | `test_membership_lifecycle_mock.py` | Domain & Financial Safety | 8 tests | **8/8 PASS** | Trạng thái Active/Expired, cấn trừ quyền lợi, khóa dòng Row Lock, Idempotency, Rollover bảo lưu. |
| **Suite 4** | `test_care_intelligence_mock.py` | Retention & Mathematics | 11 tests | **11/11 PASS** | Lọc ngoại lai Tukey IQR, tính EWMA, dự đoán ngày ghé tiếp theo, phân loại Due Soon / At Risk. |
| **Suite 5** | `test_workflow_automation_mock.py` | Background Jobs & SLA | 9 tests | **9/9 PASS** | Tác vụ nền định kỳ: nhắc Lead quá 24h, cảnh báo hết hạn thẻ, quét SLA khiếu nại, Safe Mode. |
| **Suite 6** | `test_security_and_reporting_mock.py` | Security & Analytics | 11 tests | **11/11 PASS** | Phân quyền RBAC 7 vai trò, kiểm tra sở hữu chéo, 8 chỉ số KPI chuẩn, báo cáo đa chi nhánh. |
| **Suite 7** | `test_e2e_scenarios_mock.py` | End-to-End Systems | 11 tests | **11/11 PASS** | 6 Kịch bản E2E toàn diện A–F (Lead $\rightarrow$ Khách hàng $\rightarrow$ Dịch vụ $\rightarrow$ Thẻ $\rightarrow$ Care Engine). |
| **Suite 8** | `test_extended_capabilities_mock.py` | Integrations & Fintech | 10 tests | **10/10 PASS** | Hệ số Mùa vụ & Độ tuổi, Dynamic VietQR, Payment Webhook HMAC, Zalo ZNS Safe Mode, Owner Portal. |
| **Suite 9** | `test_wordpress_lead_integration.py` | Web Integration & Security | 6 tests | **6/6 PASS** | Bẫy bot Honeypot, khử trùng lặp khách hàng, chuẩn hóa SĐT, phòng chống spam Web Form. |
| **Suite 10** | `test_audit_remediation.py` | Security Hardening | 14 tests | **14/14 PASS** | Vá lỗi kiểm toán toàn diện P0–P4 (BOLA/IDOR Guard, Appointment Check-in, Rollback an toàn). |
| **TỔNG** | **Master Test Runner** | **Toàn diện 8 Tầng Kiến trúc** | **88 tests** | **88/88 PASS (100.0%)** | Thời gian chạy: **2.340s** trên Windows Host. |

---

## 4. TỪ ĐIỂN THUẬT NGỮ CHUYÊN NGÀNH SONG NGỮ (BILINGUAL GLOSSARY)

| Thuật Ngữ Tiếng Anh | Giải Thích Tiếng Việt & Ngữ Cảnh Trong PetCare CRM |
|---|---|
| **Activity-Based Costing (ABC)** | **Tính giá thành dựa trên hoạt động**: Phương pháp kế toán quản trị bóc tách chi phí vào các nhóm hoạt động (Cost Pools) dựa trên mức tiêu hao tài nguyên thực tế, tránh hiện tượng trợ giá chéo giữa các dịch vụ. |
| **Broken Object Level Authorization (BOLA)** | **Lỗ hổng ủy quyền cấp đối tượng** (hay IDOR): Nguy cơ bảo mật khi người dùng có thể truy cập hồ sơ của người khác chỉ bằng cách thay đổi mã định danh trên request. Trong dự án được phòng vệ bằng `portal_token` và `validate_cross_entity_relationship`. |
| **Customer Lifetime Value (CLV)** | **Giá trị vòng đời khách hàng**: Tổng giá trị lợi nhuận đóng góp biên mà một khách hàng mang lại cho phòng khám trong suốt thời gian họ gắn bó và sử dụng dịch vụ cho các thú cưng của mình. |
| **Customer 360 View** | **Góc nhìn khách hàng 360 độ**: Màn hình tổng hợp toàn bộ lịch sử tương tác, hồ sơ thú cưng, thẻ hội viên, công nợ và khiếu nại của một khách hàng trên một giao diện duy nhất. |
| **Exponentially Weighted Moving Average (EWMA)** | **Trung bình động hàm mũ**: Thuật toán thống kê tính chu kỳ ghé thăm của thú cưng, trong đó các lần ghé gần nhất được gán trọng số thời gian cao hơn các lần ghé cũ. |
| **Idempotency** | **Tính lũy đẳng**: Khả năng của một API xử lý nhiều yêu cầu giống hệt nhau mà chỉ sinh ra một tác động dữ liệu duy nhất. Giúp ngăn chặn việc trừ tiền hoặc trừ quyền lợi 2 lần khi mạng bị lag. |
| **Interquartile Range (IQR - Tukey)** | **Khoảng tứ phân vị**: Phương pháp thống kê xác định khoảng cách giữa phân vị 75% ($Q_3$) và phân vị 25% ($Q_1$) để nhận diện và loại bỏ các điểm dữ liệu ngoại lai (Outliers) bất thường. |
| **Pessimistic Row Lock (`FOR UPDATE`)** | **Khóa dòng dữ liệu bi quan**: Kỹ thuật cơ sở dữ liệu khóa chặt hàng dữ liệu của thẻ hội viên trong suốt thời gian giao dịch đang diễn ra, ngăn không cho tiến trình khác đọc/ghi đè lên số dư ví. |
| **Rollover** | **Bảo lưu quyền lợi tồn**: Tính năng tự động chuyển toàn bộ số lượt dịch vụ chưa dùng hết của thẻ hội viên cũ sang thẻ mới khi khách hàng thực hiện gia hạn. |
| **Sales Pipeline Kanban** | **Phễu bán hàng dạng bảng Kanban**: Bảng trực quan hóa các giai đoạn đàm phán hợp đồng (Prospecting, Proposal, Closed Won...) giúp nhân viên kinh doanh theo dõi và thúc đẩy cơ hội bán thẻ hội viên. |
| **Instant Payment Notification (IPN Webhook)** | **Thông báo thanh toán tức thời**: Cơ chế ngân hàng tự động phát tín hiệu HTTP POST về máy chủ CRM ngay khi tài khoản nhận được tiền, giúp gạch nợ hóa đơn tự động. |
| **Vertical CRM** | **CRM chuyên sâu theo ngành**: Hệ thống CRM được may đo riêng cho một lĩnh vực kinh doanh đặc thù (ngành dịch vụ thú cưng), chứa sẵn các thực thể và quy tắc ngành mà CRM tổng quát không có. |
