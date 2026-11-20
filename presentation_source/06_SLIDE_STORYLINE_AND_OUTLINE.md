# PETCARE CRM — KỊCH BẢN THUYẾT TRÌNH & ĐẶC TẢ SLIDE (SLIDE STORYLINE & OUTLINE)

> **Mã hồ sơ**: `SLIDES-STORYLINE-2026`  
> **Dự án**: PetCare CRM (Hệ thống CRM Dịch vụ Chăm sóc Thú cưng)  
> **Thời lượng báo cáo**: **10 – 12 phút** (Đồ án tốt nghiệp / Đồ án chuyên ngành CRM)  
> **Quy mô trình chiếu**: **13 Slide nội dung chính + 4 Slide phụ lục kỹ thuật**  
> **Nguyên tắc thiết kế**: Tiêu đề hướng kết luận, tối đa 3–5 bullet points ngắn, ưu tiên sơ đồ/ảnh minh chứng, tách bạch dữ liệu thật vs. mô phỏng.

---

## BẢNG TỔNG QUAN KỊCH BẢN 13 SLIDE CHÍNH

```
┌───────┬────────────────────────────────────────────────────────────────────────┬─────────────┬──────────────────────────────┐
│ Slide │ Tiêu Đề Kết Luận Của Slide                                             │ Thời Lượng  │ Tài Sản Trực Quan Khuyên Dùng│
├───────┼────────────────────────────────────────────────────────────────────────┼─────────────┼──────────────────────────────┤
│ 01    │ Giới thiệu PetCare CRM: Nền tảng CRM Chuyên biệt cho Chuỗi Thú Cưng    │ 0:45        │ Logo PetCare & Mockup Desk   │
│ 02    │ Thách thức Quản trị: Khi Chăm sóc Thú cưng Đòi hỏi CRM Chuyên biệt    │ 1:00        │ Sơ đồ 4 Pain Points lớn      │
│ 03    │ Mục tiêu Đồ án: Số hóa Trọn vẹn Vòng đời Khách hàng (Customer Life)    │ 0:45        │ Bảng đối chiếu mục tiêu      │
│ 04    │ Kiến trúc Tổng thể: Clean Architecture 8 Tầng trên Frappe Framework v15│ 1:00        │ Sơ đồ khối 8 Tầng Kiến trúc  │
│ 05    │ Vòng đời Khách hàng End-to-End: Kết nối Tiếp thị, Bán hàng & Dịch vụ   │ 1:15        │ Sơ đồ BPMN 2.0 Group Camunda │
│ 06    │ Quản lý Gia đình Đa Thú cưng (Multi-Pet) & Bán hàng Phễu Pipeline      │ 1:00        │ Giao diện Khách hàng 360     │
│ 07    │ Điểm sáng Vận hành: Cấn trừ Quyền lợi Hội viên An toàn (Atomic Ledger) │ 1:15        │ Giao diện Quầy POS & Sổ BRL  │
│ 08    │ Khác biệt Nổi bật: Động cơ Trí tuệ Chăm sóc Chu kỳ Sinh học Thú cưng   │ 1:15        │ Đồ thị EWMA & Giao diện Cycle│
│ 09    │ Tích hợp Số: Cổng Thanh toán VietQR Động & Đối soát Webhook Ngân hàng   │ 1:00        │ Mã VietQR & Sơ đồ Luồng HMAC │
│ 10    │ Quản trị Điều hành: Dashboard 8 Chỉ số KPI & So sánh Đa Chi nhánh      │ 1:00        │ Báo cáo Script Report KPI    │
│ 11    │ Chuyên đề Tài chính: Phân bổ Giá thành ABC & Định giá trị Vòng đời CLV │ 1:00        │ Bảng 4 Cost Pools & Đồ thị   │
│ 12    │ Kiểm thử Tự động & Bảo mật: 88/88 Tests PASS & Ma trận Phân quyền RBAC │ 0:45        │ Bảng kết quả 10 Test Suites  │
│ 13    │ Đánh giá Nghiệm thu, Giới hạn Hệ thống & Lộ trình Tương lai            │ 0:45        │ Bảng Tự đánh giá trung thực  │
├───────┼────────────────────────────────────────────────────────────────────────┼─────────────┼──────────────────────────────┤
│ TỔNG  │ 13 Slide Chính                                                         │ ~11:40      │ Sẵn sàng cho phần Demo & Q&A │
└───────┴────────────────────────────────────────────────────────────────────────┴─────────────┴──────────────────────────────┘
```

---

## CHI TIẾT ĐẶC TẢ TỪNG SLIDE THUYẾT TRÌNH

---

### SLIDE 01: GIỚI THIỆU ĐỀ TÀI & ĐỊNH VỊ SẢN PHẨM
* **Tiêu đề slide**: **PetCare CRM: Nền Tảng Quản Trị Quan Hệ Khách Hàng Chuyên Biệt Cho Chuỗi Phòng Khám & Spa Thú Cưng**
* **Mục tiêu slide**: Giới thiệu tên đề tài, nhóm thực hiện, giảng viên hướng dẫn và định vị sản phẩm ngay trong 45 giây đầu tiên.
* **Key Message**: PetCare CRM không phải phần mềm POS bán lẻ đơn thuần, mà là giải pháp CRM toàn diện vận hành trọn vẹn vòng đời khách hàng và chăm sóc thú cưng định kỳ.
* **Nội dung xuất hiện trên slide (Bullet points)**:
  * **Nền tảng công nghệ**: Frappe Framework v15 (Python 3.10+, MariaDB 11.x, Desk Native Architecture).
  * **Định vị sản phẩm**: Vertical CRM chuyên sâu cho ngành dịch vụ thú cưng (Veterinary Clinic & Pet Spa Chain).
  * **Phạm vi hỗ trợ**: Hội sở trung tâm và chuỗi 4 chi nhánh vận hành tập trung.
  * **Mức độ hoàn thiện**: 14 DocTypes, 53 Whitelisted APIs, 100% kiểm thử tự động (88/88 Tests PASS).
* **Hình ảnh trực quan**: Logo PetCare CRM kết hợp hình ảnh giao diện Desk Workspace và Portal.
* **Nguồn minh chứng**: [`README.md`](file:///c:/Users/pc/Documents/Doan_CRM/README.md), Claim `TECH-001`.
* **Lời thuyết trình gợi ý (Speaker Notes - 45s)**:
  > *"Kính thưa quý thầy cô trong Hội đồng chấm đồ án, hôm nay nhóm chúng em xin phép được báo cáo đề tài: Xây dựng hệ thống PetCare CRM toàn diện cho chuỗi phòng khám và spa thú cưng trên nền tảng Frappe Framework v15. Ngành dịch vụ thú cưng đang tăng trưởng bùng nổ, tuy nhiên phần lớn các phòng khám hiện nay chỉ sử dụng phần mềm bán hàng đơn giản, dẫn đến việc mất dấu lịch sử chăm sóc và thất thoát hội viên. PetCare CRM được chúng em thiết kế nhằm số hóa trọn vẹn vòng đời khách hàng, gắn liền với chu kỳ sinh học của từng bé thú cưng."*
* **Câu chuyển tiếp**: *"Để hiểu rõ lý do tại sao ngành dịch vụ thú cưng bắt buộc phải có một CRM chuyên biệt, chúng em xin đi vào các bài toán đau đầu nhất trong thực tế vận hành."*
* **Ghi chú trung thực**: Nêu rõ đây là sản phẩm xây dựng trên Frappe v15, không phải Odoo như rubric mẫu ban đầu.

---

### SLIDE 02: THÁCH THỨC QUẢN TRỊ TRONG NGÀNH CHĂM SÓC THÚ CƯNG
* **Tiêu đề slide**: **Thách Thức Nghiệp Vụ: Khi CRM Truyền Thống Thất Bại Trước Hành Vi Nuôi Thú Cưng**
* **Mục tiêu slide**: Chỉ ra 4 nỗi đau (pain points) lớn của mô hình phòng khám/spa thú cưng mà các phần mềm CRM phổ thông không giải quyết thuận tiện.
* **Key Message**: Khách hàng không mua dịch vụ cho bản thân họ mà mua cho thú cưng; quản lý theo đầu người sẽ làm mất dấu chu kỳ chăm sóc.
* **Nội dung xuất hiện trên slide**:
  * **Bài toán Hộ Đa Thú Cưng (Multi-Pet)**: 40% hộ gia đình nuôi từ 2 bé trở lên; mỗi bé có giống loài, cân nặng và tiền sử dị ứng riêng biệt.
  * **Khách hàng rời bỏ âm thầm (Churn 35–40%)**: Thú cưng cần tắm/tiêm định kỳ nhưng chủ nuôi hay quên; phòng khám chỉ chờ khách tự ghé mà không chủ động nhắc hẹn.
  * **Thất thoát quyền lợi thẻ trả trước**: Quản lý gói thẻ (Silver/Gold/VIP) bằng sổ sách dễ bị trừ âm số dư hoặc tranh chấp khi nhiều quầy thao tác cùng lúc.
  * **Dữ liệu phân mảnh đa chi nhánh**: Không kiểm soát được tỷ lệ chuyển đổi Lead và doanh thu thực nhận sau chiết khấu giữa các cơ sở.
* **Hình ảnh trực quan**: Sơ đồ 4 khối Pain Points minh họa mối quan hệ 1 Chủ nuôi $\rightarrow$ Nhiều Thú cưng.
* **Nguồn minh chứng**: [`docs/PRODUCT_SCOPE.md`](file:///c:/Users/pc/Documents/Doan_CRM/docs/PRODUCT_SCOPE.md), Claim `CRM-001`.
* **Lời thuyết trình gợi ý (Speaker Notes - 60s)**:
  > *"Trong ngành chăm sóc thú cưng, người trả tiền là chủ nuôi nhưng đối tượng phục vụ trực tiếp lại là các bé thú cưng. Nếu một phòng khám dùng CRM phổ thông để quản lý, khi một khách hàng như anh An nuôi cả một chú Corgi và một chú Poodle, hệ thống sẽ gộp chung vào một hồ sơ và không thể biết bé nào đã đến kỳ tiêm vắc-xin hay cắt tỉa lông. Bên cạnh đó, các gói thẻ trả trước trị giá hàng triệu đồng nếu không được khóa đồng thời sẽ rất dễ bị nhân viên trừ nhầm hoặc thất thoát. Đây chính là những khoảng trống nghiệp vụ mà PetCare CRM tập trung giải quyết triệt để."*
* **Câu chuyển tiếp**: *"Xuất phát từ những trăn trở đó, mục tiêu tổng thể của đồ án đã được xác lập như thế nào?"*

---

### SLIDE 03: MỤC TIÊU VÀ PHẠM VI HỆ THỐNG
* **Tiêu đề slide**: **Mục Tiêu Đồ Án: Số Hóa Khép Kín Vòng Đời Khách Hàng Từ Tiếp Cận Đến Giữ Chân**
* **Mục tiêu slide**: Trình bày rõ ràng phạm vi hệ thống đã hiện thực hóa, cam kết hoàn thành đồ án theo chuẩn Rubric đại học.
* **Key Message**: Chuyển đổi từ một module hội viên đơn lẻ thành một hệ sinh thái CRM toàn diện vận hành khép kín trên dữ liệu thực tế.
* **Nội dung xuất hiện trên slide**:
  * **Marketing & Bán hàng**: Tiếp nhận Lead đa kênh, bẫy bot Honeypot, chuẩn hóa SĐT Việt Nam và quản lý phễu Kanban 6 giai đoạn.
  * **Vận hành Chuyên môn**: Hồ sơ thú cưng, danh mục bảng giá chuẩn, lịch hẹn check-in và phiếu dịch vụ tích hợp cân nặng.
  * **Két sắt Thẻ Hội viên**: Cấp thẻ, nạp ví, cấn trừ an toàn tuyệt đối với khóa dòng dữ liệu (`FOR UPDATE`) và bảo lưu lượt tồn (Rollover).
  * **Trí tuệ Chăm sóc (Care Retention)**: Thuật toán thống kê dự đoán chu kỳ chăm sóc, phát hiện `DUE_SOON` và `AT_RISK` tự động.
  * **Tích hợp Số & Quản trị**: Mã VietQR động, Webhook ngân hàng tự động đối soát, và Dashboard báo cáo 8 chỉ số KPI.
* **Hình ảnh trực quan**: Bảng ma trận 5 mục tiêu tương ứng với các tiêu chí Rubric A4.1 – A4.10.
* **Nguồn minh chứng**: [`docs/FINAL_IMPLEMENTATION_REPORT.md`](file:///c:/Users/pc/Documents/Doan_CRM/docs/FINAL_IMPLEMENTATION_REPORT.md), Claim `TECH-002`.
* **Lời thuyết trình gợi ý (Speaker Notes - 45s)**:
  > *"Mục tiêu của nhóm em không dừng lại ở việc tạo ra các bảng nhập liệu đơn giản, mà là xây dựng một hệ thống CRM khép kín đáp ứng trọn vẹn định nghĩa hoàn thành (Definition of Done). Hệ thống phải đảm bảo 5 trụ cột: Tiếp cận khách hàng chuẩn hóa, Quản lý hồ sơ đa thú cưng, Két sắt quyền lợi hội viên an toàn tuyệt đối, Động cơ dự đoán chăm sóc định kỳ, và Báo cáo quản trị đa chi nhánh. Tất cả đều được hiện thực hóa qua mã nguồn Frappe v15 có thể kiểm thử độc lập."*
* **Câu chuyển tiếp**: *"Để hiện thực hóa 5 mục tiêu này, kiến trúc hệ thống đã được thiết kế như thế nào?"*

---

### SLIDE 04: KIẾN TRÚC TỔNG THỂ CLEAN ARCHITECTURE 8 TẦNG
* **Tiêu đề slide**: **Kiến Trúc Hệ Thống: Clean Architecture 8 Tầng Đảm Bảo Phân Tách Trách Nhiệm**
* **Mục tiêu slide**: Thuyết phục hội đồng về tính chuyên nghiệp trong thiết kế phần mềm, tính độc lập của tầng nghiệp vụ và khả năng kiểm thử cao.
* **Key Message**: Tầng nghiệp vụ (Domain Layer) được viết bằng Python OOP thuần túy, hoàn toàn không phụ thuộc vào framework Frappe hay cơ sở dữ liệu.
* **Nội dung xuất hiện trên slide**:
  * **Tầng 6 (Presentation)**: Workspace Desk Native, DocType Client Scripts (`*.js`), Web Portal Responsive.
  * **Tầng 5 (API Controller)**: 53 Whitelisted Endpoints, kiểm soát phiên đăng nhập, Rate Limiting và chữ ký HMAC.
  * **Tầng 4 & 3 (Application & Domain)**: Các Coordinators điều phối và các Services OOP thuần túy (`CarePatternAnalyzer`, `PricingEngine`, `BenefitRedemptionLedger`).
  * **Tầng 2 & 1 (DocType & Infrastructure)**: Frappe ORM, MariaDB 11.x (ACID & Row Lock), Redis Cache/Queue.
  * **Tầng 7 & 8 (Automation & Testing)**: Background Scheduler định kỳ và Bộ kiểm thử tự động 88 tests.
* **Hình ảnh trực quan**: Sơ đồ Mermaid 8 tầng kiến trúc (đã có trong tài liệu kỹ thuật).
* **Nguồn minh chứng**: [`apps/petcare_crm/petcare_crm/utils/`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/utils/), Claim `TECH-003`.
* **Lời thuyết trình gợi ý (Speaker Notes - 60s)**:
  > *"Về mặt kỹ thuật, PetCare CRM tuân thủ nghiêm ngặt mô hình Clean Architecture 8 tầng. Điểm đặc sắc nhất trong kiến trúc của chúng em là tầng Domain (Tầng 3): toàn bộ logic cốt lõi như thuật toán lọc nhiễu chu kỳ, công thức định giá hay sổ cái cấn trừ đều là mã nguồn Python thuần túy. Điều này giúp hệ thống đạt tính phân tách trách nhiệm tối đa, và cho phép chúng em xây dựng bộ Adapter để chạy toàn bộ 88 bài test độc lập ngay trên máy Windows chỉ trong hơn 2 giây mà không cần khởi động toàn bộ cụm máy chủ Frappe cồng kềnh."*
* **Câu chuyển tiếp**: *"Trên nền kiến trúc vững chắc đó, luồng quy trình nghiệp vụ khách hàng thực tế diễn ra như thế nào?"*

---

### SLIDE 05: QUY TRÌNH CRM END-TO-END (BPMN 2.0 GROUP PROCESS)
* **Tiêu đề slide**: **Quy Trình Nghiệp Vụ End-to-End: Kết Nối Liền Mạch 5 Phân Làn Vận Hành**
* **Mục tiêu slide**: Minh chứng quy trình CRM nhóm chuẩn mực (Tiêu chí Rubric A4.3.1), có sự tham gia của nhiều phòng ban từ Marketing, Sales, Lễ tân đến Bác sĩ và Hệ thống tự động.
* **Key Message**: Quy trình được mô hình hóa bằng chuẩn quốc tế BPMN 2.0 XML tương thích Camunda Modeler, gắn kết chặt chẽ với các endpoint API thực tế.
* **Nội dung xuất hiện trên slide**:
  * **5 Phân làn (Swimlanes)**: Khách hàng (Chủ nuôi) $\rightarrow$ Sales $\rightarrow$ Lễ tân $\rightarrow$ Bác sĩ/KTV $\rightarrow$ Hệ thống CRM Engine.
  * **Giai đoạn 1**: Tiếp nhận Lead từ Web, bẫy Honeypot, chuẩn hóa SĐT và khử trùng lặp khách hàng.
  * **Giai đoạn 2**: Tư vấn bán hàng qua phễu Kanban; chuyển đổi Lead 1 chạm thành Contact & Pet.
  * **Giai đoạn 3**: Check-in lịch hẹn, kiểm tra thể trạng, ghi nhận cân nặng và thực hiện dịch vụ.
  * **Giai đoạn 4**: Cấn trừ quyền lợi thẻ hội viên (Row Lock), thanh toán VietQR động và đối soát IPN.
  * **Giai đoạn 5**: Tự động hóa Care Intelligence quét chu kỳ chăm sóc, phát hiện Due Soon/At Risk và gửi Zalo ZNS.
* **Hình ảnh trực quan**: Ảnh sơ đồ quy trình xuất từ Camunda: [`PetCare_CRM_End_to_End_Group.png`](file:///c:/Users/pc/Documents/Doan_CRM/deliverables/bpmn/group/PetCare_CRM_End_to_End_Group.png).
* **Nguồn minh chứng**: Tệp BPMN XML [`PetCare_CRM_End_to_End_Group.bpmn`](file:///c:/Users/pc/Documents/Doan_CRM/deliverables/bpmn/group/PetCare_CRM_End_to_End_Group.bpmn), Claim `BPMN-001`.
* **Lời thuyết trình gợi ý (Speaker Notes - 75s)**:
  > *"Trên màn hình là sơ đồ quy trình nghiệp vụ End-to-End của nhóm em được vẽ trên phần mềm Camunda Modeler chuẩn BPMN 2.0. Quy trình được phân bổ qua 5 làn bơi rõ ràng. Điểm bắt đầu là khi khách hàng điền form trên website; hệ thống sẽ tự động chuẩn hóa số điện thoại và kiểm tra trùng lặp. Nhân viên Sales tư vấn và chuyển đổi Lead thành Contact và Pet chỉ bằng một thao tác. Khi khách mang thú cưng đến, lễ tân Check-in lịch hẹn, bác sĩ thực hiện dịch vụ và cập nhật cân nặng mới. Cuối cùng, hệ thống tự động cấn trừ thẻ hội viên hoặc sinh mã VietQR để khách quét thanh toán, trước khi tự động kích hoạt chu trình chăm sóc định kỳ cho lần ghé tiếp theo."*
* **Câu chuyển tiếp**: *"Hãy cùng nhìn sâu hơn vào cách hệ thống quản lý gia đình đa thú cưng và phễu bán hàng tại các bước đầu tiên."*

---

### SLIDE 06: QUẢN LÝ GIA ĐÌNH ĐA THÚ CƯNG & BÁN HÀNG PHỄU PIPELINE
* **Tiêu đề slide**: **CRM Tiếp Thị & Bán Hàng: Giải Bài Toán Đa Thú Cưng & Quản Trị Cơ Hội Bán Hàng**
* **Mục tiêu slide**: Chứng minh năng lực của CRM Core: không nhân đôi dữ liệu khách hàng, quản lý quan hệ 1:N và trực quan hóa cơ hội chốt thẻ hội viên.
* **Key Message**: Một khách hàng có thể sở hữu nhiều thú cưng độc lập; phễu Kanban 6 giai đoạn giúp tăng tỷ lệ chốt các gói thẻ hội viên giá trị cao.
* **Nội dung xuất hiện trên slide**:
  * **Khử trùng lặp thông minh (Deduplication)**: Kiểm tra Contact theo SĐT trước khi tạo mới; liên kết nhiều Pet vào chung một chủ nuôi.
  * **Hồ sơ Khách hàng 360**: Hiển thị tổng quan các bé cưng, thẻ hội viên, lịch sử thăm khám và tổng giá trị chi tiêu (LTV).
  * **Sales Pipeline Kanban**: 6 giai đoạn từ Prospecting (10%) đến Closed Won (100%), tự động tính toán doanh thu có trọng số.
  * **Ràng buộc nghiệp vụ (Invariants)**: Chuyển sang Closed Lost bắt buộc phải nhập nguyên nhân thất bại (`lost_reason`) để phục vụ cải tiến kinh doanh.
* **Hình ảnh trực quan**: Ảnh chụp màn hình Tra cứu Khách hàng 360 (Khách hàng Nguyễn Văn An nuôi bé Bơ & bé Đậu Đậu) và Bảng Kanban Opportunity.
* **Nguồn minh chứng**: [`lead_service.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/utils/lead_service.py), [`sales_pipeline_service.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/utils/sales_pipeline_service.py), Claim `CRM-003`, `CRM-005`.
* **Lời thuyết trình gợi ý (Speaker Notes - 60s)**:
  > *"Đây là giao diện Tra cứu 360 của khách hàng Nguyễn Văn An. Quý thầy cô có thể thấy, anh An sở hữu đồng thời 2 bé: chú Corgi Bơ và chú Poodle Đậu Đậu. Mỗi bé có một thẻ hồ sơ sinh học riêng với lịch sử cân nặng và chu kỳ dịch vụ độc lập. Khi anh An quan tâm đến việc mua Gói Hội Viên Kim Cương trị giá 8 triệu đồng, cơ hội này được đưa vào phễu bán hàng Kanban. Nhân viên tư vấn có thể theo dõi từng bước đàm phán, và hệ thống sẽ tự động nhân giá trị gói với xác suất từng cột để dự báo chính xác dòng tiền bán hàng trong tháng."*
* **Câu chuyển tiếp**: *"Khi khách hàng đã đưa thú cưng đến phòng khám sử dụng dịch vụ, hệ thống xử lý quyền lợi thẻ hội viên như thế nào để đảm bảo tuyệt đối không thất thoát?"*

---

### SLIDE 07: KÉT SẮT THẺ HỘI VIÊN & CẤN TRỪ AN TOÀN (ATOMIC BENEFIT LEDGER)
* **Tiêu đề slide**: **Vận Hành Dịch Vụ: Cơ Chế Khóa Dòng & Sổ Cái Quyền Lợi Hội Viên Bất Biến**
* **Mục tiêu slide**: Làm nổi bật năng lực kiến trúc giao dịch tài chính: chống Race Condition, chống trừ trùng lặp (Idempotency) và bảo lưu lượt tồn (Rollover).
* **Key Message**: Số dư thẻ hội viên được bảo vệ như một tài khoản ngân hàng; mọi biến động đều được kiểm toán qua sổ cái bất biến `Benefit Redemption Ledger`.
* **Nội dung xuất hiện trên slide**:
  * **Cấn trừ tự động tại quầy POS**: Tự động nhận diện quyền lợi miễn phí 100% hoặc chiết khấu % theo gói thẻ (Silver, Gold, VIP).
  * **Khóa dòng dữ liệu (Pessimistic Row Lock)**: Lệnh `SELECT ... FOR UPDATE` trên hàng thẻ hội viên ngăn chặn 2 quầy thu ngân trừ đồng thời.
  * **Bảo vệ Idempotency**: Khóa giao dịch bằng `idempotency_key`, ngăn trừ trùng lặp khi mạng chập chờn hoặc nhân viên bấm đúp chuột.
  * **Bảo lưu quyền lợi (Benefit Rollover)**: Khi gia hạn thẻ mới, toàn bộ số lượt dịch vụ chưa dùng hết của thẻ cũ được cộng dồn nguyên vẹn.
* **Hình ảnh trực quan**: Giao diện Quầy POS cấn trừ dịch vụ về 0 VNĐ và Bảng Sổ cái `Benefit Redemption Ledger`.
* **Nguồn minh chứng**: [`membership_service.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/utils/membership_service.py), [`api.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/api.py#L180), Claim `MEM-001`, `MEM-002`, `MEM-005`.
* **Lời thuyết trình gợi ý (Speaker Notes - 75s)**:
  > *"Điểm cốt lõi trong phân hệ dịch vụ của PetCare CRM chính là Két sắt quyền lợi hội viên (Atomic Benefit Ledger). Khi bé Bơ làm dịch vụ Grooming giá 350.000 VNĐ, quầy POS tự động đối soát thấy thẻ Bạc còn 1 buổi miễn phí và trừ số tiền thanh toán về đúng 0 VNĐ. Để ngăn ngừa gian lận hoặc lỗi hệ thống khi chuỗi có nhiều cơ sở thao tác cùng lúc, chúng em áp dụng cơ chế khóa dòng Pessimistic Row Lock trong cơ sở dữ liệu MariaDB. Số dư và lượt quyền lợi được bảo đảm không bao giờ bị âm. Đặc biệt, khi thẻ hết hạn, nếu khách hàng gia hạn gói mới, hệ thống cho phép Rollover bảo lưu toàn bộ số lượt tồn, giúp tăng tính gắn kết của khách hàng với thương hiệu."*
* **Câu chuyển tiếp**: *"Sau khi hoàn tất dịch vụ, làm sao để giữ chân khách hàng quay lại đúng hẹn? Đó là lúc Động cơ Trí tuệ Chăm sóc Care Intelligence phát huy tác dụng."*

---

### SLIDE 08: ĐỘNG CƠ TRÍ TUỆ CHĂM SÓC THEO CHU KỲ (CARE INTELLIGENCE)
* **Tiêu đề slide**: **Đề Xuất Khác Biệt: Trí Tuệ Chăm Sóc Dự Đoán Chu Kỳ Sinh Học & Tự Động Giữ Chân**
* **Mục tiêu slide**: Trình bày đề xuất khác biệt có giá trị cao nhất (Tiêu chí A4.10) với cơ sở toán học thống kê minh bạch, giải thích được.
* **Key Message**: Kết hợp bộ lọc ngoại lai Tukey IQR, trung bình động EWMA và hệ số mùa vụ/độ tuổi để phát hiện chính xác khách hàng sắp đến hạn hoặc có nguy cơ rời bỏ.
* **Nội dung xuất hiện trên slide**:
  * **Lọc nhiễu ngoại lai (Tukey IQR)**: Loại bỏ các khoảng cách ghé thăm bất thường khi lịch sử $\ge 4$ lần ghé ($[Q_1 - 1.5 \times IQR, Q_3 + 1.5 \times IQR]$).
  * **Trung bình động hàm mũ (EWMA, $\alpha=0.6$)**: Đặt trọng số cao hơn cho các lần ghé gần nhất phản ánh đúng thói quen hiện tại của thú cưng.
  * **Hệ số Mùa vụ & Độ tuổi**: Rút ngắn chu kỳ tắm sấy vào mùa nóng (tháng 3–8 factor 0.8–0.85); điều chỉnh riêng cho chó con dưới 1 tuổi.
  * **Phân loại hành động tự động**:
    * `DUE_SOON` ($\le 3$ ngày đến hạn): Tự động nhắc lịch qua Zalo ZNS / SMS và giao việc cho nhân viên CSKH.
    * `AT_RISK` ($\ge 1.5\times$ chu kỳ): Cảnh báo nguy cơ mất khách, đề xuất tặng voucher kích hoạt lại.
* **Hình ảnh trực quan**: Đồ thị minh họa công thức EWMA kết hợp bộ lọc IQR và Giao diện Danh sách Đề xuất Chăm sóc (`Care Recommendation`).
* **Nguồn minh chứng**: [`care_pattern_service.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/utils/care_pattern_service.py), Claim `CARE-001`, `CARE-002`, `CARE-003`.
* **Lời thuyết trình gợi ý (Speaker Notes - 75s)**:
  > *"Thưa thầy cô, đây là điểm khác biệt lớn nhất của PetCare CRM so với các CRM thông thường: Động cơ Care Intelligence. Nhóm em không quảng cáo công nghệ bằng các thuật ngữ AI mơ hồ, mà xây dựng một thuật toán thống kê thực thụ có thể giải thích được toán học. Hệ thống dùng khoảng tứ phân vị Tukey IQR để loại bỏ các điểm ngoại lai — ví dụ như đợt chủ nuôi đi công tác xa khiến khoảng cách bị dãn đột xuất. Sau đó, công thức EWMA với hệ số alpha 0.6 sẽ tính ra chu kỳ sinh hoạt thực tế, kết hợp với hệ số mùa hè nóng bức. Kết quả là hệ thống phát hiện chính xác bé Bơ còn 3 ngày nữa đến hạn tắm sấy (Due Soon), và bé Miu Miu đã 55 ngày chưa quay lại (At Risk), từ đó tự động giao việc cho nhân viên gọi điện chăm sóc kèm tin nhắn Zalo ZNS."*
* **Câu chuyển tiếp**: *"Bên cạnh tự động hóa chăm sóc, khâu thanh toán không tiền mặt đã được tích hợp thông minh như thế nào?"*

---

### SLIDE 09: CỔNG THANH TOÁN VIETQR & ĐỐI SOÁT WEBHOOK NGÂN HÀNG
* **Tiêu đề slide**: **Tích Hợp Số: Cổng Thanh Toán VietQR Động & Tự Động Đối Soát Qua Webhook IPN**
* **Mục tiêu slide**: Minh chứng khả năng lập trình tích hợp cổng thanh toán hiện đại (Tiêu chí A4.7) kèm các biện pháp bảo mật an toàn giao dịch.
* **Key Message**: Tự động sinh mã VietQR Napas247 chứa mã phiếu; Webhook ngân hàng kiểm tra chữ ký HMAC-SHA256 tự động gạch nợ tức thời.
* **Nội dung xuất hiện trên slide**:
  * **Mã VietQR động chuẩn EMVCo**: Tự động nhúng số tiền thực thu và cú pháp đối soát `PC-SVC-{visit_id}` hoặc `PC-MEM-{membership_id}`.
  * **Webhook IPN đối soát tự động**: Ngân hàng bắn tín hiệu biến động số dư $\rightarrow$ CRM tự động gạch nợ phiếu hoặc nạp tiền ví thẻ mà không cần thu ngân gõ tay.
  * **Bảo mật Chữ ký số HMAC-SHA256**: Bắt buộc kiểm tra chữ ký mật mã trên header `X-Signature`, ngăn chặn kẻ xấu giả lập thông báo nạp tiền.
  * **Chống tấn công gửi lại (Replay Attack Guard)**: Bảng kiểm toán lưu trữ `transaction_id`, từ chối xử lý trùng lặp khi webhook bị retry.
* **Hình ảnh trực quan**: Mẫu mã VietQR Napas247 động sinh từ hệ thống và Sơ đồ luồng xác thực chữ ký HMAC-SHA256.
* **Nguồn minh chứng**: [`payment_gateway.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/utils/payment_gateway.py), API `payment_webhook`, Claim `INT-001`, `INT-003`, `INT-004`.
* **Lời thuyết trình gợi ý (Speaker Notes - 60s)**:
  > *"Tại quầy thu ngân, PetCare CRM giải quyết triệt để sự cố khách chuyển nhầm số tiền hoặc thu ngân mất thời gian mở app ngân hàng kiểm tra. Khi bấm thanh toán, hệ thống phát sinh ngay một mã VietQR động chuẩn Napas247. Khách quét mã là toàn bộ số tiền và cú pháp phiếu dịch vụ được điền tự động. Khi giao dịch thành công, Webhook của ngân hàng sẽ gửi thông báo tức thời về CRM. Nhóm em đã cài đặt thuật toán băm HMAC-SHA256 để kiểm tra tính toàn vẹn gói tin, kiểm tra đối khớp số tiền và chống gửi lại giao dịch. Phiếu dịch vụ được đổi trạng thái Hoàn tất ngay trên màn hình trong chưa đầy 1 giây."*
* **Câu chuyển tiếp**: *"Toàn bộ các giao dịch và hoạt động chăm sóc trên được tổng hợp lên bàn làm việc của ban giám đốc ra sao?"*

---

### SLIDE 10: BÁO CÁO QUẢN TRỊ 8 KPI & ĐỐI SÁNH ĐA CHI NHÁNH
* **Tiêu đề slide**: **Phân Tích Quản Trị: Dashboard 8 Chỉ Số KPI Chuẩn & Đối Sánh Hiệu Quả Đa Chi Nhánh**
* **Mục tiêu slide**: Thể hiện năng lực lập trình module báo cáo (Tiêu chí A4.6 & A4.9.2), cung cấp góc nhìn kinh doanh sâu sắc cho nhà quản trị chuỗi.
* **Key Message**: 8 chỉ số KPI chuẩn được tính toán trực tiếp từ cơ sở dữ liệu Frappe, phân tách rõ Doanh số niêm yết (Gross) và Doanh thu thực thu (Net).
* **Nội dung xuất hiện trên slide**:
  * **8 Chỉ số KPI cốt lõi**:
    1. Tỷ lệ chuyển đổi Lead (%) | 2. Doanh thu phễu có trọng số | 3. Thẻ hội viên Active & Số dư ví
    4. Thẻ sắp hết hạn (7d & 30d) | 5. Doanh thu thuần & Ưu đãi cấn trừ | 6. Thú cưng Due Soon
    7. Khách hàng At Risk | 8. Tỷ lệ giữ chân khách hàng thực tế (Retention Rate %)
  * **Báo cáo Script Report Desk Native**: Tích hợp bộ lọc thời gian và xuất dữ liệu Excel chuẩn xác.
  * **Phân tích đối sánh 4 chi nhánh**: So sánh hiệu quả vận hành giữa Cơ sở Trung Tâm, Quận 1, Thủ Đức và Bình Thạnh.
* **Hình ảnh trực quan**: Ảnh chụp giao diện Báo cáo Script Report `PetCare KPI Overview` với các thẻ tóm tắt màu sắc.
* **Nguồn minh chứng**: [`petcare_kpi_overview.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/petcare_crm/report/petcare_kpi_overview/petcare_kpi_overview.py), [`analytics_service.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/utils/analytics_service.py), Claim `KPI-001`, `KPI-002`.
* **Lời thuyết trình gợi ý (Speaker Notes - 60s)**:
  > *"Đây là giao diện Báo cáo quản trị PetCare KPI Overview được chúng em xây dựng bằng Frappe Script Report. Báo cáo cung cấp 8 chỉ số sức khỏe quan trọng nhất của doanh nghiệp. Điểm đặc biệt là báo cáo phân định rất rạch ròi giữa Doanh số niêm yết và Doanh thu thực nhận, giúp ban giám đốc thấy được chính xác bao nhiêu phần trăm doanh thu đang được dùng để tri ân cấn trừ cho hội viên. Qua bảng phân tích 4 chi nhánh, chúng em nhận thấy cơ sở Quận 1 và Trung Tâm có tỷ lệ cấn trừ hội viên lên tới 30%, chứng minh mức độ trung thành của khách hàng ở khu vực này rất cao, trong khi các cơ sở mới mở chủ yếu là khách vãng lai cần đẩy mạnh bán thẻ."*
* **Câu chuyển tiếp**: *"Để chứng minh tính hiệu quả tài chính ở tầm nhìn chiến lược, nhóm em đã xây dựng mô hình chuyên đề giá thành ABC và giá trị vòng đời CLV như thế nào?"*

---

### SLIDE 11: CHUYÊN ĐỀ TÀI CHÍNH ABC COSTING & ĐỊNH GIÁ TRỊ VÒNG ĐỜI (CLV)
* **Tiêu đề slide**: **Chuyên Đề Tài Chính: Tính Giá Thành Hoạt Động (ABC) & Định Giá Trị Vòng Đời (CLV)**
* **Mục tiêu slide**: Hoàn thành xuất sắc Tiêu chí Rubric A4.5; chứng minh tư duy quản trị tài chính hiện đại kết nối trực tiếp với đòn bẩy CRM.
* **Key Message**: Khắc phục hiện tượng trợ giá chéo bằng 4 Cost Pools và chứng minh hiệu quả giữ chân khách hàng giúp tăng trưởng CLV đến 58.7%.
* **Nội dung xuất hiện trên slide**:
  * **Tính giá thành theo hoạt động (ABC)**: Phân bổ 4 Cost Pools (Nhân công Bác sĩ/KTV, Vật tư tiêu hao, Khấu hao máy móc, Quản lý chung).
  * **Bóc tách Tỷ suất Lợi nhuận biên ($CM\%$)**: Tiêm phòng vắc-xin đạt $CM\% = 50\%$ (biên lợi nhuận cao); Grooming đạt $CM\% = 30\%$ (thâm dụng nhân công).
  * **Mô hình Định giá trị Vòng đời Khách hàng (CLV)**: Áp dụng phương pháp chiết khấu dòng tiền DCF theo cấp độ Hộ gia đình ($1:N$ thú cưng).
  * **So sánh 3 kịch bản kinh doanh**:
    * Chưa có CRM (Churn 35%, f = 6 lần/năm) $\rightarrow$ $\text{CLV} \approx 4,82 \text{ triệu VNĐ}$.
    * Có PetCare CRM (Churn 18%, f = 9 lần/năm) $\rightarrow$ $\text{CLV} \approx 7,65 \text{ triệu VNĐ}$ (**Tăng trưởng $+58.7\%$**).
* **Hình ảnh trực quan**: Sơ đồ 4 Cost Pools ABC và Biểu đồ so sánh cột CLV giữa 3 kịch bản kinh doanh.
* **Nguồn minh chứng**: Tệp bảng tính [`deliverables/finance/CLV_ABC_Model.xlsx`](file:///c:/Users/pc/Documents/Doan_CRM/deliverables/finance/CLV_ABC_Model.xlsx) và Báo cáo chuyên đề Word A4.5, Claim `FIN-001`, `FIN-002`.
* **Lời thuyết trình gợi ý (Speaker Notes - 60s)**:
  > *"Để đáp ứng tiêu chí A4.5, nhóm em đã xây dựng mô hình bảng tính chuyên sâu kết nối dữ liệu vận hành CRM với bài toán tài chính quản trị. Bằng phương pháp ABC, chúng em bóc tách chi phí vào 4 trung tâm hoạt động để tránh hiện tượng trợ giá chéo giữa các dịch vụ. Từ tỷ suất đóng góp biên thực tế, nhóm em áp dụng mô hình chiết khấu dòng tiền DCF theo vòng đời 10 năm của thú cưng. Kết quả mô phỏng cho thấy: nhờ có Care Intelligence kéo giảm tỷ lệ khách rời bỏ từ 35% xuống 18% và nhắc khách đi spa đúng hẹn, Giá trị vòng đời của một hộ nuôi cún tăng vọt từ 4,8 triệu lên 7,6 triệu đồng, tức tăng trưởng gần 59% mà không cần tốn thêm ngân sách quảng cáo."*
* **Câu chuyển tiếp**: *"Toàn bộ hệ thống phức tạp này đã được bảo đảm chất lượng và kiểm soát an toàn bằng những công cụ kiểm thử nào?"*

---

### SLIDE 12: KIỂM THỬ TỰ ĐỘNG & BẢO VỆ PHÂN QUYỀN RBAC
* **Tiêu đề slide**: **Bảo Đảm Chất Lượng: 88/88 Tests Tự Động PASS 100% & Ma Trận Phân Quyền 7 Vai Trò**
* **Mục tiêu slide**: Đưa ra bằng chứng kiểm thử vững chắc, không thể chối cãi về độ tin cậy và an toàn của hệ thống trước hội đồng phản biện.
* **Key Message**: 10 Test Suites bao phủ từ Unit, Integration, E2E đến Bảo mật và Tích hợp bên ngoài; thực thi 100% PASS trong 2.34 giây.
* **Nội dung xuất hiện trên slide**:
  * **Master Test Runner**: Chạy tự động 10 Suites độc lập bằng lệnh `python run_all_tests.py`.
  * **Kết quả nghiệm thu thực tế**: **Tổng số test: 88 | PASS: 88 (100.0%) | FAIL: 0 | ERRORS: 0 | Thời gian: ~2.34s**.
  * **Bao phủ kiểm thử**: CRM Core, Service Ops, Két sắt Thẻ hội viên, Thuật toán Care Engine, Background Jobs, Bảo mật RBAC, E2E Scenarios, Cổng thanh toán VietQR, Lead Form WordPress và Vá lỗi Kiểm toán.
  * **Ma trận Phân quyền 7 Roles**: Front Desk, Veterinarian, Groomer, Manager, Sales, Analyst, Customer Portal; phòng vệ BOLA/IDOR bằng Signed Token.
* **Hình ảnh trực quan**: Ảnh chụp màn hình Console đầu ra của lệnh `python run_all_tests.py` màu xanh lá cây 100% PASS.
* **Nguồn minh chứng**: [`run_all_tests.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/tests/run_all_tests.py), Claim `TEST-001`, `QA-001`.
* **Lời thuyết trình gợi ý (Speaker Notes - 45s)**:
  > *"Chất lượng của PetCare CRM được bảo chứng bởi bộ kiểm thử tự động toàn diện gồm 88 test cases chia làm 10 Suites. Tất cả các kịch bản cấn trừ thẻ, khóa dòng chống race condition, tính toán IQR lọc nhiễu hay xác thực chữ ký HMAC webhook đều có bài kiểm thử tương ứng. Khi chạy Master Test Runner, toàn bộ 88 bài test đều đạt tỷ lệ Pass tuyệt đối 100% trong thời gian chỉ 2.34 giây. Về mặt bảo mật, hệ thống thiết lập 7 vai trò người dùng chuẩn Frappe kết hợp cơ chế kiểm tra sở hữu chéo, bảo đảm nhân viên không can thiệp trái thẩm quyền và khách hàng không thể xem trộm hồ sơ của nhau."*
* **Câu chuyển tiếp**: *"Nhìn lại toàn bộ chặng đường thực hiện đồ án, nhóm em tự đánh giá những thành quả đạt được và những điểm giới hạn trung thực như thế nào?"*

---

### SLIDE 13: ĐÁNH GIÁ NGHIỆM THU, GIỚI HẠN & HƯỚNG PHÁT TRIỂN
* **Tiêu đề slide**: **Đánh Giá Nghiệm Thu: Thành Quả Đạt Được, Giới Hạn Thực Tế & Lộ Trình Phát Triển**
* **Mục tiêu slide**: Thể hiện thái độ trung thực học thuật, dũng cảm công khai các giới hạn kỹ thuật và vạch ra lộ trình mở rộng thương mại hóa rõ ràng.
* **Key Message**: PetCare CRM đã hoàn thành xuất sắc mục tiêu đồ án tốt nghiệp, sẵn sàng triển khai thử nghiệm thực tế tại các chuỗi phòng khám thú cưng.
* **Nội dung xuất hiện trên slide**:
  * **Thành quả nổi bật**: Đạt chuẩn 100% các tiêu chí Rubric A4.1 – A4.10; mã nguồn sạch chuẩn Clean Architecture; giao diện Desk Native hoàn chỉnh.
  * **Giới hạn kỹ thuật trung thực**:
    * Các cổng Zalo ZNS / SMS và Webhook ngân hàng hiện vận hành ở **Safe Mode Sandbox / Outbox** an toàn để demo, chưa nạp tiền cước viễn thông thật.
    * 88 bài test chạy ở tầng Mock Adapter trên Windows; kiểm thử Live ORM yêu cầu môi trường Docker.
    * Số liệu tài chính CLV/ABC là mô hình mô phỏng học thuật, chưa phải số liệu kế toán pháp nhân.
  * **Lộ trình phát triển**: Đóng gói Mobile App chuyên dụng cho chủ nuôi (React Native/Flutter), kết nối API máy xét nghiệm máu thú y tự động.
* **Hình ảnh trực quan**: Bảng tổng kết đối chiếu Rubric & Roadmap 3 giai đoạn mở rộng.
* **Nguồn minh chứng**: [`docs/KNOWN_LIMITATIONS.md`](file:///c:/Users/pc/Documents/Doan_CRM/docs/KNOWN_LIMITATIONS.md), Claim `LIMIT-001`.
* **Lời thuyết trình gợi ý (Speaker Notes - 45s)**:
  > *"Để tổng kết, PetCare CRM đã đáp ứng trọn vẹn và vượt mức các yêu cầu của đồ án chuyên ngành CRM. Chúng em tự hào đã xây dựng được một sản phẩm thực tế, có kiến trúc bài bản và tư duy giải quyết bài toán ngành thú cưng sâu sắc. Nhóm em cũng hoàn toàn trung thực ghi nhận rằng các cổng giao tiếp như Zalo ZNS hay Webhook ngân hàng hiện đang chạy ở chế độ Safe Mode Outbox để đảm bảo an toàn thử nghiệm. Trong tương lai, nhóm em hướng tới việc đóng gói ứng dụng di động cho chủ nuôi và tích hợp trực tiếp với các thiết bị xét nghiệm thú y. Em xin chân thành cảm ơn quý thầy cô đã lắng nghe và rất mong nhận được những góp ý quý báu từ Hội đồng!"*
* **Câu chuyển tiếp**: *"Sau đây, nhóm chúng em xin kính mời Hội đồng theo dõi phần Demo trực tiếp các tính năng trên phần mềm!"*

---

## 4. CÁC SLIDE PHỤ LỤC KỸ THUẬT DỰ PHÒNG (BACKUP APPENDIX SLIDES)

* **Appendix 01: Danh Mục 14 DocTypes & Quan Hệ Khóa Ngoại**: Bảng tra cứu 12 Regular DocTypes và 2 Child Tables.
* **Appendix 02: Bảng Phân Loại 53 Whitelisted API Endpoints**: Phân nhóm 53 endpoints theo 8 phân hệ và cơ chế bảo vệ.
* **Appendix 03: Ma Trận Phân Quyền RBAC 7 Vai Trò Chi Tiết**: Quyền CRUD chi tiết của từng Role trên các DocType cốt lõi.
* **Appendix 04: Công Thức Toán Học Chi Tiết Của Care Engine & CLV**: Chi tiết giải thuật lọc Tukey IQR, trung bình động EWMA ($\alpha=0.6$), công thức chiết khấu dòng tiền DCF và phân bổ 4 Cost Pools ABC.
