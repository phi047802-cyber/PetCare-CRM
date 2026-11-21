# PETCARE CRM — TÓM LƯỢC ĐIỀU HÀNH DỰ ÁN (PROJECT EXECUTIVE BRIEF)

> **Mã hồ sơ**: `BRIEF-PETCARE-2026`  
> **Dự án**: PetCare CRM (Hệ thống Quản lý Quan hệ Khách hàng Dịch vụ Chăm sóc Thú cưng)  
> **Nền tảng**: Frappe Framework v15 (Desk Native Architecture)  
> **Thời lượng trình bày mục tiêu**: 10 – 12 phút (Đồ án tốt nghiệp / Đồ án chuyên ngành CRM)  
> **Trạng thái thực thi**: 100% Hoàn thành kiểm thử (88/88 Unit/Mock Tests PASS)  

---

## 1. TÊN ĐỀ TÀI & ĐỊNH VỊ SẢN PHẨM

* **Tên đề tài**: **Xây Dựng Hệ Thống PetCare CRM Toàn Diện Cho Chuỗi Phòng Khám & Spa Thú Cưng Trên Nền Tảng Frappe Framework v15**
* **Định vị sản phẩm**: PetCare CRM là một giải pháp CRM chuyên biệt (Vertical CRM) được thiết kế riêng cho ngành dịch vụ thú cưng. Hệ thống vượt qua giới hạn của các phần mềm bán lẻ POS đơn thuần bằng cách số hóa trọn vẹn **Vòng đời Khách hàng (Customer Lifecycle)**: từ khâu tiếp cận đa kênh (Omnichannel Lead Capture), tư vấn bán hàng (Sales Pipeline Kanban), tiếp đón tại quầy & thực hiện dịch vụ, cấn trừ quyền lợi thẻ hội viên (Atomic Benefit Ledger), cho đến tự động phân tích chu kỳ sinh học để nhắc lịch tái khám (Care Intelligence Engine) và phân tích hiệu quả kinh doanh đa chi nhánh.

---

## 2. BỐI CẢNH & CASE STUDY NGHIỆP VỤ

* **Mô hình doanh nghiệp**: Hệ thống phục vụ mô hình **Chuỗi phòng khám thú y, spa và làm đẹp thú cưng** vận hành tập trung với kiến trúc hỗ trợ đa chi nhánh (hệ thống đã cấu hình sẵn 4 cơ sở: `CN-TRUNGTAM`, `CN-QUAN1`, `CN-THUDUC`, `CN-BINHTHANH`).
* **Đặc thù nghiệp vụ ngành Pet Care**:
  1. *Quan hệ 1 Khách hàng - Nhiều Thú cưng (Multi-Pet Household)*: Một chủ nuôi thường sở hữu nhiều thú cưng với giống loài, cân nặng, tiền sử bệnh lý và chu kỳ sinh học hoàn toàn khác nhau.
  2. *Dịch vụ mang tính định kỳ sinh học cao*: Thú cưng cần tắm sấy mỗi 2–3 tuần, cắt tỉa mỗi 4–6 tuần, tiêm phòng mỗi 12 tháng. Nếu không có hệ thống nhắc nhở chủ động, tỷ lệ quên lịch hoặc rời bỏ (churn) lên tới 35% – 40%.
  3. *Mô hình Thẻ hội viên trả trước (Prepaid Memberships)*: Khách hàng mua các gói dịch vụ lớn (Silver, Gold, VIP) để được hưởng ưu đãi miễn phí và chiết khấu. Điều này đòi hỏi hệ thống kiểm soát quyền lợi cực kỳ chặt chẽ, chống thất thoát tài chính và ngăn chặn trừ trùng lặp khi nhiều nhân viên thao tác đồng thời.

---

## 3. VẤN ĐỀ CẦN GIẢI QUYẾT (PAIN POINTS)

| STT | Vấn đề thực tế của phòng khám & Spa thú cưng | Giải pháp giải quyết của PetCare CRM |
|:---:|---|---|
| **1** | **Dữ liệu phân mảnh & Gộp trùng sai lệch**: Tiếp nhận Lead từ Web/Hotline nhưng lưu vào Excel rời rạc; tạo trùng nhiều khách hàng cùng một số điện thoại. | Tự động chuẩn hóa SĐT Việt Nam (+84, 09x), bẫy bot Honeypot trên Lead Form, kiểm tra Deduplication nghiêm ngặt trước khi tạo Contact. |
| **2** | **Quên lịch chăm sóc & Khách hàng rời bỏ âm thầm**: Nhân viên không nhớ lịch nhắc tái khám; chỉ liên hệ thụ động khi khách tự mang thú cưng đến. | **Care Intelligence Engine**: Tự động tính chu kỳ trung bình (EWMA + Tukey IQR), phân loại `DUE_SOON` và `AT_RISK`, tự động giao việc CSKH. |
| **3** | **Thất thoát thẻ hội viên & Tranh chấp đồng thời**: Sử dụng sổ giấy hoặc bảng tính quản lý gói dịch vụ trả trước; nhân viên bấm nhầm gây trừ âm số dư hoặc trừ trùng lặp. | **Atomic Benefit Ledger**: Cơ chế khóa dòng dữ liệu (`FOR UPDATE`), ghi sổ cái kiểm toán bất biến (`BRL`), bảo vệ Idempotency chống double-redeem. |
| **4** | **Quy trình thanh toán chậm & Sai sót đối soát**: Thu ngân gõ sai số tiền chuyển khoản; mất thời gian kiểm tra ứng dụng ngân hàng khi đông khách. | **Dynamic VietQR & IPN Webhook**: Tự động sinh mã VietQR Napas247 chứa cú pháp đối soát; Webhook ngân hàng kiểm tra chữ ký HMAC tự động gạch nợ. |
| **5** | **Thiếu tầm nhìn quản trị tài chính & Giá thành**: Không rõ dịch vụ nào thực sự sinh lời; ảo tưởng doanh thu vòng đời mà không trừ chi phí hoạt động. | **Báo cáo 8 KPI chuẩn** kết hợp **Mô hình ABC (Activity-Based Costing)** và **Định giá trị vòng đời khách hàng (CLV)** theo cấp độ hộ gia đình. |

---

## 4. NHÓM NGƯỜI DÙNG & VAI TRÒ (ROLES)

Hệ thống thiết lập 7 vai trò người dùng chuẩn Frappe (được khai báo trong [`hooks.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/hooks.py) và khởi tạo qua [`install.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/setup/install.py)):
1. **Lễ tân & Thu ngân (`PetCare Front Desk`)**: Tra cứu hồ sơ 360, tiếp nhận tại quầy POS, kiểm tra lịch hẹn, cấn trừ quyền lợi thẻ và xuất phiếu thu.
2. **Bác sĩ thú y (`PetCare Veterinarian`)**: Thăm khám lâm sàng, tiêm phòng, kê đơn, cập nhật diễn tiến cân nặng và hồ sơ bệnh án.
3. **Kỹ thuật viên Spa/Grooming (`PetCare Groomer`)**: Thực hiện tắm sấy, cắt tỉa, vệ sinh lông móng và ghi nhận tình trạng thể chất sau dịch vụ.
4. **Nhân viên Kinh doanh / Telesales (`PetCare Sales`)**: Tiếp nhận Lead, tư vấn cuộc gọi, quản lý phễu cơ hội (Kanban Opportunity) và chốt Deal thẻ hội viên.
5. **Quản lý phòng khám / Chi nhánh (`PetCare Manager`)**: Quản trị danh mục dịch vụ, duyệt giá, xử lý khiếu nại dịch vụ (Case SLA) và giám sát nhân sự.
6. **Chuyên viên Phân tích Quản trị (`PetCare Analyst`)**: Theo dõi 8 chỉ số KPI, hiệu quả chuyển đổi Lead, doanh thu thuần và so sánh hiệu quả đa chi nhánh.
7. **Khách hàng / Chủ nuôi thú cưng (`PetCare Customer Portal`)**: Đặt lịch hẹn trực tuyến, tra cứu lịch sử khám bệnh, theo dõi số dư ví và lượt dịch vụ còn lại qua Portal được bảo vệ bằng Token xác thực.

---

## 5. KIẾN TRÚC & CÔNG NGHỆ TỔNG THỂ

* **Mô hình kiến trúc**: **Clean Architecture 8 Tầng** tuân thủ nguyên tắc phân tách trách nhiệm (Separation of Concerns).
* **Nền tảng ứng dụng**:
  * **Frappe Framework v15** (Desk Native UI, ORM DocType, Role-Based Access Control, Background Scheduler).
  * **Cơ sở dữ liệu**: MariaDB 11.x hỗ trợ giao dịch ACID nghiêm ngặt và khóa dòng Pessimistic Row Lock.
  * **Ngôn ngữ**: Python 3.10+ (Logic OOP thuần túy, không phụ thuộc framework trong tầng Domain).
  * **Frontend**: Frappe Desk Workspace, DocType Client Scripts (`*.js`), tích hợp Web Portal Responsive (Tailwind CSS, Font Awesome, SheetJS).
  * **Máy chủ xem trước độc lập**: Máy chủ kép `start_preview.py` phục vụ giao diện Desk và Portal với độ trễ < 2ms mà không bắt buộc cài đặt MariaDB để chấm điểm hoặc demo.

---

## 6. CÁC PHÂN HỆ NGHIỆP VỤ CỐT LÕI (CORE MODULES)

1. **CRM Tiếp Thị & Bán Hàng (CRM Core)**: Thu nhận Lead đa kênh, chuẩn hóa SĐT, chuyển đổi Lead 1 chạm sang Contact/Pet/Opportunity, quản lý Pipeline Kanban 6 giai đoạn với tỷ lệ xác suất có trọng số.
2. **Hồ Sơ Thú Cưng & Vận Hành Dịch Vụ (Pet & Operations)**: Hồ sơ thú cưng đa quan hệ ($1:N$), danh mục bảng giá niêm yết chuẩn, phiếu dịch vụ `Service Visit` và phiếu khiếu nại `PetCare Case`.
3. **Thẻ Hội Viên & Ví Trả Trước (Membership & Loyalty)**: Quản lý gói thẻ (Bạc, Vàng, VIP), ví trả trước (Top-up balance), cấn trừ quyền lợi tự động (100% FREE hoặc chiết khấu %) với cơ chế kiểm toán bất biến `Benefit Redemption Ledger`.
4. **Trí Tuệ Chăm Sóc & Giữ Chân Khách Hàng (Care Intelligence & Retention)**: Thuật toán Rule-based thống kê minh bạch kết hợp bộ lọc ngoại lai (Tukey IQR), trung bình động hàm mũ (EWMA), hệ số biến thiên theo mùa và độ tuổi thú cưng; tự động phát hiện `DUE_SOON` và `AT_RISK`.
5. **Cổng Tự Phục Vụ & Đa Kênh (Portal, VietQR & Omnichannel)**: Cổng đặt lịch và theo dõi sổ khám cho chủ nuôi, bộ sinh mã VietQR Napas247, Webhook đối soát IPN tự động có chữ ký HMAC-SHA256, và bộ điều phối Zalo ZNS / SMS ở chế độ Safe Mode.
6. **Báo Cáo & Đo Lường Hiệu Quả (Analytics & KPI)**: Báo cáo Script Report 8 chỉ số KPI chuẩn, phân tích đối sánh doanh thu đa chi nhánh và bảng phân bổ chi phí ABC / định giá trị vòng đời CLV.

---

## 7. CÁC ĐIỂM KHÁC BIỆT NỔI BẬT ĐÃ KIỂM CHỨNG (DIFFERENTIATORS)

| Điểm khác biệt | Hiện thực kỹ thuật thực tế | Bằng chứng kiểm chứng |
|---|---|---|
| **1. Trí tuệ chăm sóc theo chu kỳ sinh học** | Thuật toán thống kê thực thụ (EWMA $\alpha=0.6$, Tukey IQR lọc nhiễu, hệ số mùa vụ 0.8–0.85, hệ số tuổi 0.8–0.85); phân loại chính xác `DUE_SOON` và `AT_RISK`. | [`care_pattern_service.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/utils/care_pattern_service.py), Suite 4 (11 tests PASS). |
| **2. Két sắt quyền lợi hội viên (Atomic Benefit Ledger)** | Bảo vệ Idempotency chống trừ lặp; khóa dòng dữ liệu (`FOR UPDATE`); ngăn số dư âm; hỗ trợ bảo lưu lượt tồn (Rollover) khi gia hạn thẻ. | [`membership_service.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/utils/membership_service.py), Suite 3 (8 tests PASS). |
| **3. Thanh toán VietQR & Webhook IPN an toàn** | Chuẩn hóa mã EMVCo; xác thực chữ ký số HMAC-SHA256 trên Webhook; tự động gạch nợ phiếu dịch vụ hoặc nạp ví; cơ chế chống tấn công gửi lại (Replay Guard). | [`payment_gateway.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/utils/payment_gateway.py), Suite 8 (Tests 5, 6, 7 PASS). |
| **4. Cổng Chủ Nuôi bảo vệ BOLA/IDOR** | Cung cấp REST API cho chủ nuôi tra cứu sổ y bạ và đặt lịch; xác thực quyền sở hữu chéo khách hàng - thú cưng (`validate_cross_entity_relationship`); chữ ký Signed Token cho Guest. | [`api.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/api.py) (dòng 4150-4250), Suite 10 (Findings P0-P4 PASS). |

---

## 8. HIỆN TRẠNG TRIỂN KHAI & HẠN CHẾ LỚN (HONEST AUDIT)

* **Hiện trạng triển khai**:
  * 14 DocTypes (12 Regular + 2 Child Tables), 53 whitelisted endpoints, 14 modules Python OOP, 8 chỉ số KPI, 1 Script Report và 1 Workspace Desk Native.
  * Bộ kiểm thử tự động đạt **88 / 88 Tests PASS (100.0%)** trong thời gian thực thi **~2.34 giây**.
  * Dữ liệu mẫu thuần Việt phong phú (8 khách hàng, 9 thú cưng, 3 gói hội viên, 12 lượt dịch vụ, 4 cơ hội, 4 đề xuất chăm sóc) sẵn sàng cho mọi kịch bản demo.
* **Hạn chế kỹ thuật cần nêu rõ**:
  * *Môi trường kiểm thử*: 88 tests hiện tại chạy ở tầng Mock/Pure Python Adapter trên Windows; các file test phụ thuộc Frappe ORM live cần môi trường Docker container backend.
  * *Cổng tích hợp bên ngoài*: Zalo ZNS, SMS Brandname và Webhook Ngân hàng hoạt động ở **Safe Mode Outbox / Sandbox** (mô phỏng an toàn, không tự ý trừ tiền hoặc gửi tin nhắn thật đến nhà mạng).
  * *Số liệu tài chính*: Các chỉ số doanh thu và CLV/ABC là **Kịch bản mô phỏng tài chính (Financial Simulation)** dựa trên schema thực tế, không phải số liệu sổ sách kế toán thật của một pháp nhân đã kiểm toán.
  * *Ứng dụng di động*: Cổng chủ nuôi hiện cung cấp đầy đủ REST API và giao diện Web Responsive xem trước, chưa đóng gói thành ứng dụng native React Native / Flutter trên App Store.

---

## 9. THÔNG ĐIỆP SẢN PHẨM TRONG 25 GIÂY (ELEVATOR PITCH)

> *"PetCare CRM là giải pháp CRM chuyên biệt trên Frappe Framework v15 dành riêng cho chuỗi chăm sóc thú cưng, giải quyết triệt để bài toán giữ chân khách hàng bằng cách kết nối quản lý gia đình đa thú cưng, cấn trừ an toàn quyền lợi thẻ hội viên trả trước, và tự động hóa thuật toán dự đoán chu kỳ chăm sóc sinh học kết hợp tin nhắn nhắc lịch đa kênh, giúp doanh nghiệp tối đa hóa giá trị vòng đời khách hàng và kiểm soát chặt chẽ giá thành dịch vụ."*
