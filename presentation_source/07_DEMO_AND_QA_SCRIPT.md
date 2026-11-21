# PETCARE CRM — KỊCH BẢN DEMO THỰC THẾ & BỘ CÂU HỎI PHẢN BIỆN (DEMO & QA SCRIPT)

> **Mã hồ sơ**: `SCRIPT-DEMO-QA-2026`  
> **Dự án**: PetCare CRM (Hệ thống CRM Dịch vụ Chăm sóc Thú cưng)  
> **Thời lượng demo trực tiếp gợi ý**: 3 – 5 phút  
> **Nguyên tắc demo**: Thao tác mạch lạc, dùng dữ liệu thuần Việt có sẵn, không gõ nhầm số liệu, luôn có phương án dự phòng ngoại tuyến.

---

## PHẦN 1: KỊCH BẢN DEMO TRỰC TIẾP (LIVE DEMO STORYBOARD)

Demo được chia làm **3 Câu Chuyện Nghiệp Vụ Cốt Lõi**, phản ánh trọn vẹn Customer Lifecycle từ khách lạ $\rightarrow$ khách quen $\rightarrow$ hội viên trung thành.

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                 3 CÂU CHUYỆN DEMO XUYÊN SUỐT                                     │
├──────────────────────────────────┬───────────────────────────────┬───────────────────────────────┤
│ STORY 1: LEAD TO DEAL WON        │ STORY 2: SERVICE & ATOMIC MEM │ STORY 3: CARE RETENTION SCAN  │
│ Tiếp nhận Lead web, bẫy bot,     │ Check-in tiếp đón tại quầy,   │ Quét chu kỳ sinh học EWMA+IQR,│
│ chuyển đổi 1 chạm & quản lý phễu │ cấn trừ thẻ hội viên khóa dòng│ cảnh báo Due Soon / At Risk,  │
│ cơ hội bán gói hội viên VIP.     │ và thanh toán VietQR động.    │ điều phối Zalo ZNS nhắc lịch. │
└──────────────────────────────────┴───────────────────────────────┴───────────────────────────────┘
```

---

### STORY 1: TỪ KHÁCH TIỀM NĂNG ĐẾN CƠ HỘI BÁN HÀNG THÀNH CÔNG (LEAD TO DEAL WON)

* **Vai trò sử dụng (Role)**: Khách hàng ngoài & Nhân viên Bán hàng (`PetCare Sales`).
* **Đường dẫn màn hình**:
  * Bước 1: Mở trang Web Form: `deliverables/wordpress/petcare_lead_form_standalone.html` (hoặc Cổng Web Portal `http://127.0.0.1:8080/` $\rightarrow$ tab **Kinh Doanh**).
  * Bước 2: Mở Desk Workspace `http://127.0.0.1:8080/desk` $\rightarrow$ **CRM Core & Leads**.
* **Dữ liệu demo sử dụng**: Khách hàng mới `Hoàng Gia Bảo`, SĐT `0911223344`, thú cưng `Cún Husky 4 tháng tuổi`.
* **Trình tự thao tác từng giây (Step-by-Step Actions)**:
  1. *[00:00 - 00:30]* Trên trang Form Landing Page, sinh viên nhập thông tin: Họ tên `Hoàng Gia Bảo`, SĐT `0911223344`, chọn dịch vụ `Tư vấn tiêm phòng & Spa`. Bấm nút **"Gửi Yêu Cầu Tư Vấn"**.
     * *Lời thoại*: *"Em xin bắt đầu bằng việc đóng vai một khách hàng mới đăng ký tư vấn qua website. Form này đã được tích hợp bẫy bot Honeypot và cơ chế kiểm tra chuẩn hóa đầu số di động Việt Nam."*
     * *Kết quả thấy ngay*: Thông báo gửi thành công kèm mã Lead mới.
  2. *[00:30 - 01:00]* Chuyển sang giao diện Desk, mở danh sách `PetCare Lead`. Nhấp vào Lead `Hoàng Gia Bảo`.
     * *Lời thoại*: *"Tại giao diện Desk của nhân viên Sales, Lead lập tức xuất hiện ở trạng thái New. Nhân viên gọi điện tư vấn thể trạng bé xong, chỉ cần bấm nút Convert Lead."*
     * Bấm nút **"Convert Lead"** trên Form Desk.
     * *Kết quả thấy ngay*: Hệ thống tự động tạo 1 bản ghi `Contact` (Hoàng Gia Bảo) và 1 bản ghi `Pet` liên kết.
  3. *[01:00 - 01:30]* Mở mục **Sales Opportunity** trên Desk.
     * *Lời thoại*: *"Khi anh Bảo muốn mua Gói Hội Viên Kim Cương VIP trị giá 8 triệu đồng, cơ hội xuất hiện trên phễu Kanban. Em kéo thẻ cơ hội từ cột Proposal sang Closed Won."*
     * Kéo thả thẻ sang cột **Closed Won**.
     * *Kết quả thấy ngay*: Xác suất nhảy lên 100%, doanh thu phễu được ghi nhận, kích hoạt quy trình cấp thẻ hội viên.
* **Những điều cần tránh**: Không gõ sai định dạng SĐT (ví dụ: gõ thừa hoặc thiếu số); Không bấm F5 liên tục khi modal đang mở.
* **Phương án dự phòng**: Nếu server web form mất kết nối, mở trực tiếp nút "Tạo Lead Mới" có sẵn trên Desk Workspace.

---

### STORY 2: TIẾP ĐÓN DỊCH VỤ, CẤN TRỪ THẺ HỘI VIÊN & THANH TOÁN VIETQR

* **Vai trò sử dụng**: Nhân viên Lễ tân / Thu ngân (`PetCare Front Desk`).
* **Đường dẫn màn hình**: Cổng Web Portal `http://127.0.0.1:8080/` (hoặc `preview.html`) $\rightarrow$ mục **Quầy Tiếp Nhận POS**.
* **Dữ liệu demo sử dụng**: Khách hàng thân thiết `Nguyễn Văn An` (`0901234567`), thú cưng `Bơ` (Corgi), thẻ hội viên `Gói Chăm Sóc Bạc (Silver)` còn 1 buổi Grooming miễn phí.
* **Trình tự thao tác từng giây**:
  1. *[01:30 - 02:00]* Mở tab **Lịch Hẹn Dịch Vụ**. Nhấp nút **"Check-in Tiếp Đón"** tại dòng lịch hẹn của bé `Bơ`.
     * *Lời thoại*: *"Khi khách hàng Nguyễn Văn An đưa bé Corgi Bơ đến cơ sở, lễ tân bấm Check-in một chạm. Màn hình tự động chuyển sang Quầy POS với đầy đủ thông tin khách và bé cưng."*
     * *Kết quả thấy ngay*: Màn hình Quầy POS mở ra, điền sẵn thông tin anh An và bé Bơ.
  2. *[02:00 - 02:45]* Tại Quầy POS, nhấp chọn dịch vụ: `Grooming & Tắm Sấy Tiêu Chuẩn` (350.000 VNĐ).
     * *Lời thoại*: *"Hệ thống ngay lập tức đối soát dữ liệu và phát hiện thẻ Bạc của bé Bơ còn 1 buổi Grooming miễn phí 100%. Số tiền thanh toán tự động nhảy về 0 VNĐ. Cơ chế khóa dòng Row Lock được kích hoạt ngầm để đảm bảo tính an toàn số dư."*
     * Nhập cân nặng sau dịch vụ: `11.8 kg`. Bấm **"Hoàn Tất & Cấn Trừ"**.
     * *Kết quả thấy ngay*: Phiếu `Service Visit` được tạo thành công; quyền lợi Grooming của thẻ Bạc giảm từ 1 về 0; cân nặng 11.8 kg cập nhật vào hồ sơ bé Bơ.
  3. *[02:45 - 03:15]* Chọn tiếp dịch vụ thứ hai phải trả tiền (ví dụ: Mua thêm sữa tắm giá `200.000 VNĐ`). Chọn phương thức thanh toán **"Chuyển Khoản Ngân Hàng (VietQR)"**.
     * *Lời thoại*: *"Với các dịch vụ phát sinh thêm tiền mặt, quầy thu ngân bấm tạo mã VietQR Napas247 động. Mã này đã được nhúng sẵn số tiền và mã phiếu. Khi ngân hàng bắn Webhook đối soát có chữ ký HMAC-SHA256 về, hệ thống tự động gạch nợ thành công."*
     * Nhấp nút **"Mô Phỏng Nhận Webhook"**.
     * *Kết quả thấy ngay*: Màn hình hiện biểu tượng tích xanh báo nhận tiền thành công tức thì.
* **Những điều cần tránh**: Không bấm cấn trừ 2 lần liên tiếp khi mạng chưa phản hồi; không chọn nhầm sang bé Đậu Đậu (vì bé Đậu Đậu chưa có thẻ).
* **Phương án dự phòng**: Nếu modal VietQR không tải được ảnh QR, chỉ vào ô hiển thị chuỗi cú pháp Napas247 chuẩn EMVCo trên giao diện.

---

### STORY 3: TRÍ TUỆ CHĂM SÓC THEO CHU KỲ (CARE INTELLIGENCE) & ĐIỀU PHỐI ĐA KÊNH

* **Vai trò sử dụng**: Chuyên viên Chăm sóc Khách hàng & Quản lý phòng khám.
* **Đường dẫn màn hình**: Web Portal $\rightarrow$ tab **Chu Kỳ Chăm Sóc** (`#tab-cycle`) và Desk $\rightarrow$ **PetCare KPI Overview**.
* **Dữ liệu demo sử dụng**: Bé `Bơ` (Due Soon còn 3 ngày), bé `Miu Miu` (At Risk vắng mặt 55 ngày), bé `Đậu Phộng` (Renewal còn 4 ngày).
* **Trình tự thao tác từng giây**:
  1. *[03:15 - 04:00]* Tại tab Chu Kỳ Chăm Sóc, bấm nút **"Kích Hoạt Quét Chu Kỳ (Care Engine Scan)"**.
     * *Lời thoại*: *"Đây là tính năng Care Intelligence. Thay vì đợi khách tự nhớ, hệ thống chạy thuật toán thống kê EWMA và Tukey IQR để quét toàn bộ lịch sử thăm khám. Như thầy cô thấy trên bảng kết quả: Bé Bơ được phân loại DUE_SOON vì còn 3 ngày nữa đến chu kỳ tắm sấy; trong khi bé Miu Miu của anh Long đã vắng mặt 55 ngày, vượt 2.2 lần chu kỳ bình thường nên bị xếp vào nhóm AT_RISK có nguy cơ rời bỏ."*
     * *Kết quả thấy ngay*: Bảng phân loại hiển thị danh sách 3 nhóm: Due Soon, At Risk, Expiring Renewal.
  2. *[04:00 - 04:30]* Nhấp nút **"Gọi Nhắc Lịch"** trên dòng bé Bơ.
     * *Lời thoại*: *"Nhân viên CSKH chỉ cần bấm nút Gọi nhắc lịch để xác nhận ngày giờ hẹn cho khách, hoặc kích hoạt tin nhắn Zalo ZNS tự động. Thông báo được đưa vào Hộp thư đi an toàn (Outbox) để kiểm tra nội dung trước khi gửi qua nhà mạng."*
  3. *[04:30 - 05:00]* Chuyển sang Desk Workspace, mở báo cáo **PetCare KPI Overview**.
     * *Lời thoại*: *"Toàn bộ kết quả vận hành được tổng hợp theo thời gian thực trên Báo cáo 8 KPI chuẩn và phân bổ đối sánh giữa 4 chi nhánh. Giúp nhà quản lý thấy rõ tỷ lệ giữ chân khách hàng và doanh thu thực nhận của toàn chuỗi."*
* **Những điều cần tránh**: Không bấm "Dismiss" đề xuất khi chưa giải thích lý do; không chọn nhầm khoảng ngày lọc báo cáo sang tương lai.
* **Phương án dự phòng**: Nếu báo cáo Script Report đang tải chậm, mở màn hình tóm tắt KPI nằm ngay tại tab Kinh Doanh của Web Portal.

---

## PHẦN 2: BỘ 12 CÂU HỎI PHẢN BIỆN BẢO VỆ ĐỒ ÁN (DEFENSE Q&A CHEATSHEET)

Dưới đây là 12 câu hỏi hóc búa nhất mà hội đồng giảng viên thường đặt ra, kèm theo câu trả lời chuẩn xác dựa trên bằng chứng kỹ thuật:

---

### CÂU 01: VÌ SAO NHÓM CHỌN FRAPPE FRAMEWORK V15 THAY VÌ ODOO NHƯ RUBRIC MẪU HOẶC TỰ VIẾT BẰNG DJANGO/FLASK?
* **Căn cứ trả lời**: Kiến trúc Desk Native, cơ chế Metadata DocType, và khả năng mở rộng.
* **Câu trả lời chuẩn**:
  > *"Dạ kính thưa thầy cô, ban đầu nhóm có tham khảo rubric mẫu nhắc đến Odoo, nhưng qua khảo sát kỹ thuật, Frappe Framework v15 sở hữu kiến trúc Metadata-driven tiên tiến hơn hẳn: toàn bộ cấu trúc bảng, phân quyền và giao diện Desk đều được định nghĩa qua schema JSON thống nhất. So với việc tự viết bằng Django hay Flask, Frappe cung cấp sẵn hệ thống Phân quyền Role-based Access Control (RBAC), bộ lập lịch tác vụ nền (Scheduler), và cơ chế xác thực phiên an toàn mà không cần 'phát minh lại bánh xe'. Nhờ đó, nhóm có thể tập trung 100% thời gian vào việc phát triển logic nghiệp vụ chuyên sâu cho ngành thú cưng ở tầng Domain bằng Python OOP thuần túy."*

---

### CÂU 02: HỆ THỐNG CỦA CÁC BẠN LÀ MỘT CRM HOÀN CHỈNH HAY CHỈ LÀ PHẦN MỀM QUẢN LÝ PHÒNG KHÁM (HIS / CLINIC POS)?
* **Căn cứ trả lời**: Định nghĩa CRM, Vòng đời khách hàng (Customer Lifecycle), Sales Pipeline và Retention.
* **Câu trả lời chuẩn**:
  > *"Dạ, PetCare CRM là một hệ thống CRM hoàn chỉnh vì trọng tâm thiết kế của hệ thống là **Quản trị mối quan hệ và vòng đời khách hàng**, chứ không chỉ ghi nhận ca khám như một phần mềm HIS đơn thuần. Hệ thống sở hữu đầy đủ 4 trụ cột CRM: (1) Thu hút & Chuyển đổi Lead từ website; (2) Phễu quản lý cơ hội bán hàng Kanban (Sales Pipeline); (3) Hồ sơ Khách hàng 360 độ gắn kết đa thú cưng; và (4) Động cơ giữ chân khách hàng chủ động (Care Intelligence) phân tích chu kỳ tái khám. Phần quản lý phiếu dịch vụ tại quầy chỉ là mắt xích thực thi (Service Delivery) để cung cấp dữ liệu đầu vào cho bài toán giữ chân và tăng giá trị vòng đời khách hàng (CLV)."*

---

### CÂU 03: MA TRẬN PHÂN QUYỀN (RBAC) VÀ PHÒNG VỆ BẢO MẬT BOLA / IDOR ĐƯỢC THỰC THI THẾ NÀO Ở BACKEND?
* **Căn cứ trả lời**: [`install.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/setup/install.py), [`security.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/utils/security.py) và API `_verify_owner_portal_access`.
* **Câu trả lời chuẩn**:
  > *"Dạ, bảo mật của hệ thống được thực thi ở cả 3 lớp:
  > 1. Tại tầng ORM: 7 vai trò (`PetCare Front Desk`, `Veterinarian`, `Groomer`, `Manager`, `Sales`, `Analyst`, `Customer Portal`) được giới hạn quyền CRUD nghiêm ngặt qua schema JSON và file `install.py`. Kỹ thuật viên Spa tuyệt đối không có quyền sửa đơn giá dịch vụ hay xem báo cáo tài chính.
  > 2. Tại tầng API: 53 endpoints đều kiểm soát session. Các thao tác nhạy cảm bắt buộc phải có vai trò phù hợp.
  > 3. Phòng vệ BOLA/IDOR (Broken Object Level Authorization): Trên Cổng Chủ Nuôi, hàm `validate_cross_entity_relationship` trong `security.py` bắt buộc kiểm tra xem thú cưng có thực sự thuộc quyền sở hữu của khách hàng đó hay không. Với khách vãng lai (Guest), hệ thống yêu cầu chữ ký số `portal_token` băm bằng HMAC, ngăn chặn kẻ xấu sửa ID trên URL để đọc trộm bệnh án của người khác."*

---

### CÂU 04: HỆ THỐNG XỬ LÝ RA SAO VỚI TRƯỜNG HỢP MỘT KHÁCH HÀNG NUÔI NHIỀU THÚ CƯNG (MULTI-PET HOUSEHOLD)?
* **Căn cứ trả lời**: Schema `Pet.json` và Quan hệ $1:N$ với `Contact`.
* **Câu trả lời chuẩn**:
  > *"Dạ, đây chính là ưu điểm vượt trội của PetCare CRM so với CRM bán lẻ thông thường. Trong cơ sở dữ liệu, bảng `Contact` đóng vai trò là Hộ gia đình chủ nuôi, liên kết với bảng `Pet` qua quan hệ một-nhiều ($1:N$). Ví dụ trong dữ liệu demo, khách hàng Nguyễn Văn An sở hữu 2 thú cưng: chú Corgi Bơ và chú Poodle Đậu Đậu. Mỗi bé có một hồ sơ sinh học độc lập, mang lịch sử cân nặng, tiền sử dị ứng và chu kỳ dịch vụ hoàn toàn tách biệt. Thẻ hội viên có thể áp dụng chung cho chủ hộ hoặc gắn riêng cho từng bé, giúp thu ngân cấn trừ chính xác mà không bao giờ bị nhầm lẫn."*

---

### CÂU 05: LÀM SAO HỆ THỐNG CHỐNG ĐƯỢC HIỆN TƯỢNG TRỪ TRÙNG LẶP (DOUBLE-SPENDING) HOẶC RACE CONDITION KHI CẤN TRỪ THẺ HỘI VIÊN?
* **Căn cứ trả lời**: Pessimistic Row Lock (`SELECT ... FOR UPDATE`), Idempotency Key, và Invariant checks trong [`membership_service.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/utils/membership_service.py).
* **Câu trả lời chuẩn**:
  > *"Dạ, để bảo vệ quyền lợi thẻ hội viên như một tài khoản tiền tệ, nhóm em triển khai 3 cơ chế an toàn:
  > 1. **Khóa dòng dữ liệu (Pessimistic Row Lock)**: Khi API `record_benefit_usage` được gọi, câu lệnh SQL thực thi lệnh `SELECT ... FOR UPDATE` trên hàng thẻ hội viên trong bảng `tabCustomer Membership`. Nếu hai quầy thu ngân bấm cấn trừ cùng một tích tắc, giao dịch thứ hai bắt buộc phải chờ giao dịch thứ nhất hoàn tất và commit.
  > 2. **Bảo vệ Idempotency**: Mỗi yêu cầu cấn trừ đều đi kèm một `idempotency_key`. Nếu client gửi lại cùng một key do rớt mạng, hệ thống kiểm tra Sổ cái `Benefit Redemption Ledger` và từ chối xử lý lần hai.
  > 3. **Ràng buộc bất biến (Invariants)**: Tầng Domain kiểm tra điều kiện `remaining_quantity >= count` và `balance >= 0`. Nếu không thỏa mãn, hệ thống ném ngoại lệ `InsufficientBenefitsException` và rollback ngay lập tức."*

---

### CÂU 06: CƠ CHẾ ROLLOVER BẢO LƯU QUYỀN LỢI TỒN KHI GIA HẠN THẺ HOẠT ĐỘNG NHƯ THẾ NÀO?
* **Căn cứ trả lời**: Hàm `renew_membership` trong [`membership_service.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/utils/membership_service.py).
* **Câu trả lời chuẩn**:
  > *"Dạ, trong thực tế, khách hàng thường rất bức xúc nếu gói thẻ hội viên hết hạn mà các buổi spa chưa dùng hết bị hủy bỏ vô điều kiện. Do đó, PetCare CRM hỗ trợ tính năng **Benefit Rollover**. Khi nhân viên bấm gia hạn thẻ qua API `renew_membership` với cờ `allow_rollover=1`, hệ thống thực hiện trong một giao dịch ACID: (1) Khởi tạo bản ghi thẻ mới với thời hạn mới; (2) Quét bảng `Membership Benefit` của thẻ cũ để lấy số lượt tồn `remaining_quantity`; (3) Cộng dồn số lượt tồn này vào dòng quyền lợi tương ứng của thẻ mới; và (4) Đóng thẻ cũ thành trạng thái `Renewed`. Nhờ vậy, khách hàng được bảo lưu 100% quyền lợi, tạo động lực to lớn để họ tiếp tục gia hạn gói mới."*

---

### CÂU 07: THUẬT TOÁN CARE INTELLIGENCE CÓ GÌ KHÁC BIỆT VỚI AI/MACHINE LEARNING? TẠI SAO LẠI CHỌN EWMA VÀ TUKEY IQR?
* **Căn cứ trả lời**: Tính giải thích được (*Explainable Math*), kích thước tập dữ liệu nhỏ của một phòng khám, và hiệu năng tính toán.
* **Câu trả lời chuẩn**:
  > *"Dạ thưa thầy cô, nhóm em hoàn toàn trung thực: Care Intelligence không phải là mô hình Deep Learning hay mạng nơ-ron hộp đen phức tạp. Trong bối cảnh một chuỗi phòng khám thú cưng với vài ngàn khách hàng, việc áp dụng Machine Learning phức tạp rất dễ bị quá khớp (overfitting) và không thể giải thích được lý do cho nhân viên CSKH. Thay vào đó, nhóm em chọn **Mô hình thống kê quy tắc minh bạch**:
  > * Dùng **Tukey IQR** để loại bỏ các điểm ngoại lai bất thường (như chủ nuôi đi công tác đột xuất 3 tháng mới cho cún đi tắm một lần).
  > * Dùng **Trung bình động hàm mũ (EWMA, $\alpha=0.6$)** vì thói quen gần nhất của thú cưng có giá trị dự báo cao hơn các lần ghé từ năm ngoái.
  > Thuật toán này chạy cực nhanh, tiêu tốn ít tài nguyên và quan trọng nhất là nhân viên CSKH có thể giải thích rõ ràng với chủ nuôi: 'Dạ em thấy thông thường 20 ngày bé Bơ đi tắm một lần, đợt này đã 27 ngày rồi nên em gọi nhắc lịch cho bé ạ'."*

---

### CÂU 08: HỆ SỐ MÙA VỤ VÀ ĐỘ TUỔI ĐƯỢC TÍNH TOÁN VÀ CAN THIỆP VÀO CHU KỲ NHƯ THẾ NÀO?
* **Căn cứ trả lời**: [`care_pattern_service.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/utils/care_pattern_service.py) (`SeasonalAdjustmentHelper`, `PetAgeAdjustmentHelper`).
* **Câu trả lời chuẩn**:
  > *"Dạ, chu kỳ sinh học của thú cưng biến động rất lớn theo thời tiết và giai đoạn trưởng thành:
  > * **Về mùa vụ**: Vào mùa hè nóng bức (tháng 3 đến tháng 8 tại Việt Nam), lông thú cưng tiết nhiều dầu và dễ bốc mùi hôi hơn. Hệ số `SeasonalAdjustmentHelper` sẽ nhân chu kỳ tắm sấy với hệ số từ `0.80` đến `0.85`, giúp rút ngắn chu kỳ dự đoán để nhắc lịch sớm hơn.
  > * **Về độ tuổi**: Chó con dưới 1 tuổi (Puppy) hiếu động, hay nghịch bẩn và hệ miễn dịch chưa hoàn thiện nên cần tắm và tiêm phòng dày hơn (hệ số `0.85`); ngược lại thú cưng già trên 7 tuổi có thói quen tĩnh tại hơn.
  > Công thức cuối cùng: $\text{Chu kỳ hiệu chỉnh} = \text{Chu kỳ EWMA} \times \text{Factor}_{\text{Mùa}} \times \text{Factor}_{\text{Tuổi}}$."*

---

### CÂU 09: WEBHOOK THANH TOÁN ĐƯỢC BẢO VỆ CHỐNG GIẢ MẠO VÀ CHỐNG GỬI LẠI (REPLAY ATTACK) BẰNG CƠ CHẾ NÀO?
* **Căn cứ trả lời**: [`payment_gateway.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/utils/payment_gateway.py) (`PaymentWebhookService`).
* **Câu trả lời chuẩn**:
  > *"Dạ, Webhook tiếp nhận biến động số dư là cổng mở công khai (`allow_guest=True`), do đó nguy cơ bị hacker giả mạo gói tin chuyển khoản là rất lớn. Nhóm em bảo vệ bằng 4 lớp:
  > 1. **Chữ ký số HMAC-SHA256**: Gói tin gửi về bắt buộc phải có header `X-Signature`. Hệ thống băm payload với `WEBHOOK_SECRET` và so sánh bằng `hmac.compare_digest` để chống tấn công phân tích thời gian (Timing Attack). Sai chữ ký bị chặn ngay ở mã 401.
  > 2. **Chống tấn công gửi lại (Replay Guard)**: Hệ thống ghi nhận mã `transaction_id` của ngân hàng vào sổ kiểm toán. Nếu cùng một giao dịch bị gửi lại lần 2, hệ thống trả về mã 200 'Already processed' và bỏ qua an toàn, tuyệt đối không gạch nợ hay nạp tiền ví lần 2.
  > 3. **Kiểm tra khớp số tiền (Amount Guard)**: Số tiền chuyển khoản bắt buộc phải lớn hơn hoặc bằng số nợ của phiếu dịch vụ.
  > 4. **Bảo vệ bằng Idempotency**: Mọi thao tác gạch nợ đều đi qua transaction có khóa."*

---

### CÂU 10: TẠI SAO BÁO CÁO PHẢI TÁCH BẠCH DOANH SỐ NIÊM YẾT (GROSS) VÀ DOANH THU THỰC NHẬN (NET)?
* **Căn cứ trả lời**: Script Report `petcare_kpi_overview` và Hàm ý cấn trừ quyền lợi hội viên.
* **Câu trả lời chuẩn**:
  > *"Dạ, trong mô hình CRM dịch vụ hội viên, nếu chỉ nhìn vào Doanh số niêm yết (Gross Revenue), nhà quản lý sẽ bị ảo tưởng về dòng tiền thực tế. Ví dụ: một buổi Spa giá niêm yết 450.000 VNĐ nhưng khách dùng thẻ VIP được miễn phí 100%, hoặc giảm giá 10% chỉ thu 405.000 VNĐ. Nếu kế toán ghi nhận doanh thu 450.000 VNĐ thì két tiền sẽ bị thâm hụt so với sổ sách. PetCare CRM tách bạch rõ: Doanh số niêm yết thể hiện **Quy mô năng lực phục vụ**, còn Doanh thu thực nhận (`Net Revenue = Gross - Discounts`) thể hiện **Dòng tiền thực thu**. Khoản chênh lệch chính là **Chi phí tri ân hội viên**, giúp ban giám đốc đánh giá chính xác hiệu quả tài chính của từng chính sách phát hành thẻ."*

---

### CÂU 11: MỐI LIÊN HỆ GIỮA MÔ HÌNH GIÁ THÀNH HOẠT ĐỘNG (ABC) VÀ GIÁ TRỊ VÒNG ĐỜI KHÁCH HÀNG (CLV) LÀ GÌ?
* **Căn cứ trả lời**: Tài liệu chuyên đề A4.5 [`PetCare_CRM_CLV_ABC_Report.md`](file:///c:/Users/pc/Documents/Doan_CRM/deliverables/finance/PetCare_CRM_CLV_ABC_Report.md) và File Excel.
* **Câu trả lời chuẩn**:
  > *"Dạ, hai mô hình này tạo thành một chiếc cầu nối tài chính hoàn chỉnh:
  > * Phương pháp **Activity-Based Costing (ABC)** bóc tách chi phí vào 4 Cost Pools để tính ra Tỷ suất Lợi nhuận đóng góp biên thực tế ($CM\%$) cho từng dịch vụ sau khi trừ chi phí nhân công tay nghề cao và vật tư y tế.
  > * Thay vì tính CLV dựa trên Doanh thu ảo, nhóm em đưa $CM\%$ của mô hình ABC vào công thức chiết khấu dòng tiền DCF của CLV. Khi Care Intelligence của CRM giúp tăng tần suất ghé thăm $f$ và giảm tỷ lệ rời bỏ (Churn), chúng em đo lường được chính xác mức tăng trưởng lợi nhuận biên thực tế của cả vòng đời khách hàng (tăng từ 4,8 triệu lên 7,6 triệu đồng/khách), chứng minh CRM mang lại giá trị thặng dư thực chất cho doanh nghiệp chứ không chỉ làm đẹp số liệu."*

---

### CÂU 12: NHỮNG GIỚI HẠN KỸ THUẬT LỚN NHẤT HIỆN TẠI VÀ HƯỚNG PHÁT TRIỂN TIẾP THEO LÀ GÌ?
* **Căn cứ trả lời**: [`docs/KNOWN_LIMITATIONS.md`](file:///c:/Users/pc/Documents/Doan_CRM/docs/KNOWN_LIMITATIONS.md) và Thái độ trung thực học thuật.
* **Câu trả lời chuẩn**:
  > *"Dạ, nhóm em hoàn toàn trung thực công khai 3 giới hạn lớn nhất của đồ án hiện tại:
  > 1. **Về tích hợp bên ngoài**: Cổng tin nhắn Zalo ZNS / SMS và Webhook ngân hàng hiện đang vận hành ở chế độ **Safe Mode Sandbox / Outbox** để bảo đảm an toàn khi demo và kiểm thử, chưa nạp tiền cước viễn thông thật.
  > 2. **Về môi trường kiểm thử**: 88 bài test tự động hiện chạy qua bộ Pure Python Adapter trên Windows để đảm bảo tốc độ và tính độc lập; các bài test live Frappe ORM cần môi trường Docker Linux.
  > 3. **Về ứng dụng di động**: Cổng chủ nuôi hiện cung cấp đầy đủ REST API bảo vệ BOLA và giao diện Web Responsive xem trước, chưa đóng gói thành ứng dụng native trên Google Play / App Store.
  > Hướng phát triển tiếp theo của nhóm là đóng gói ứng dụng di động Flutter cho chủ nuôi và tích hợp trực tiếp với máy xét nghiệm sinh hóa thú y tại phòng khám."*
