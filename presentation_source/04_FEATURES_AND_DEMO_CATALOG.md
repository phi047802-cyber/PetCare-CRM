# PETCARE CRM — DANH MỤC TÍNH NĂNG & KỊCH BẢN THAO TÁC (FEATURES & DEMO CATALOG)

> **Mã hồ sơ**: `CATALOG-DEMO-2026`  
> **Dự án**: PetCare CRM (Hệ thống CRM Dịch vụ Chăm sóc Thú cưng)  
> **Mục tiêu**: Danh mục 10 tính năng tương tác phục vụ trình diễn trước hội đồng chấm đồ án, đối chiếu từng bước thao tác với giao diện và mã nguồn thực tế.  
> **Nguyên tắc an toàn**: Toàn bộ kịch bản sử dụng bộ dữ liệu mẫu thuần Việt có sẵn; không chèn dữ liệu rác vào CSDL trong quá trình demo.

---

## BẢNG TỔNG HỢP 10 TÍNH NĂNG TIÊU BIỂU

```
┌────┬──────────────────────────────────────────────────────────────┬────────────────────────────┬────────────────────────┐
│ STT│ Tên Tính Năng Trình Diễn                                     │ Phân Hệ Nghiệp Vụ          │ Vai Trò Người Thao Tác │
├────┼──────────────────────────────────────────────────────────────┼────────────────────────────┼────────────────────────┤
│ 01 │ Tiếp nhận Lead Đa Kênh & Khử Trùng Lặp Khách Hàng            │ CRM Core & Lead Intake     │ Khách hàng / Sales     │
│ 02 │ Quản lý Cơ Hội Bán Hàng & Phễu Bán Hàng Kanban               │ Sales Pipeline & Deals     │ PetCare Sales          │
│ 03 │ Tra cứu Hồ Sơ Khách Hàng 360 & Gia Đình Đa Thú Cưng          │ Customer 360 & Profiles    │ Lễ tân / CSKH          │
│ 04 │ Đặt Lịch Hẹn Trực Tuyến & Check-in Tiếp Đón Một Chạm         │ Appointments & Scheduling  │ Khách hàng / Lễ tân    │
│ 05 │ Phiếu Dịch Vụ & Cấn Trừ Quyền Lợi Hội Viên Khóa Dòng         │ Service Ops & Memberships  │ Kỹ thuật viên / Thu ngân│
│ 06 │ Sinh Mã Thanh Toán VietQR Động & Webhook Tự Động Đối Soát     │ Payments & Integrations    │ Thu ngân / Hệ thống    │
│ 07 │ Quét Chu Kỳ Chăm Sóc & Đề Xuất Giữ Chân (Due Soon / At Risk) │ Care Intelligence Engine   │ CSKH / Quản lý         │
│ 08 │ Nạp Tiền Ví Trả Trước, Gia Hạn Thẻ & Rollover Bảo Lưu        │ Membership & Wallet        │ Thu ngân / Sales       │
│ 09 │ Tiếp Nhận Khiếu Nại Dịch Vụ & Giám Sát Cảnh Báo SLA          │ Service Recovery & Cases   │ CSKH / Quản lý         │
│ 10 │ Báo Cáo Quản Trị 8 Chỉ Số KPI & Đối Sánh Đa Chi Nhánh         │ Analytics & KPI Reporting  │ Quản lý / Analyst      │
└────┴──────────────────────────────────────────────────────────────┴────────────────────────────┴────────────────────────┘
```

---

## CHI TIẾT TỪNG TÍNH NĂNG & KỊCH BẢN THAO TÁC

### TÍNH NĂNG 01: TIẾP NHẬN LEAD ĐA KÊNH & KHỬ TRÙNG LẶP SỐ ĐIỆN THOẠI

* **Mục tiêu nghiệp vụ**: Thu nhận thông tin khách hàng từ Landing Page/WordPress form, tự động bẫy bot spam, chuẩn hóa số điện thoại Việt Nam và kiểm tra khử trùng lặp khách hàng trước khi tạo mới.
* **Người thao tác (Actor)**: Khách hàng (điền form) và Nhân viên Tư vấn (`PetCare Sales`).
* **Điều kiện trước khi demo**: Máy chủ preview đang chạy (`python start_preview.py` tại cổng 8080) hoặc Desk container sẵn sàng.
* **Các bước thao tác trên giao diện**:
  1. Mở trang Form Lead WordPress: `deliverables/wordpress/petcare_lead_form_standalone.html` (hoặc tab **Kinh Doanh** trên Portal `preview.html`).
  2. Điền thông tin:
     * Họ tên: `Hoàng Gia Bảo`
     * Số điện thoại: `0911223344` (hoặc `+84911223344`)
     * Nhu cầu / Ghi chú: `Cún Husky 4 tháng tuổi cần tư vấn gói tiêm chủng và tắm spa`
  3. Bấm nút **"Gửi Yêu Cầu Tư Vấn"**.
  4. Mở Frappe Desk (`/desk_preview.html` hoặc `/app/petcare-lead`), mở danh sách `PetCare Lead`.
  5. Mở bản ghi vừa tạo, bấm nút hành động **"Convert Lead"** (Chuyển đổi).
* **Kết quả quan sát được**:
  * Form thông báo gửi thành công kèm ID định danh `LEAD-2026-XXXXX`.
  * Số điện thoại được tự động chuẩn hóa về dạng chuẩn quốc gia.
  * Khi bấm Convert, hệ thống tự động sinh 1 bản ghi `Contact` (Hoàng Gia Bảo) và 1 bản ghi `Pet` liên kết. Nếu SĐT đã tồn tại, hệ thống báo "Khách hàng cũ" và chỉ tạo thêm Pet mà không nhân đôi Contact.
* **Màn hình / File liên quan**: [`petcare_lead_form_standalone.html`](file:///c:/Users/pc/Documents/Doan_CRM/deliverables/wordpress/petcare_lead_form_standalone.html), [`petcare_lead.js`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/petcare_crm/doctype/petcare_lead/petcare_lead.js), [`lead_service.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/utils/lead_service.py).
* **Dữ liệu demo sử dụng**: Lead mẫu `Hoàng Gia Bảo` (`0911223344`).
* **Rủi ro & Phương án dự phòng**: Nếu form HTML standalone không kết nối được backend, mở trực tiếp modal "Tạo Lead Nhanh" ngay trên giao diện Desk.

---

### TÍNH NĂNG 02: QUẢN LÝ PHỄU BÁN HÀNG CƠ HỘI (SALES PIPELINE KANBAN)

* **Mục tiêu nghiệp vụ**: Trực quan hóa tiến trình chốt Deal các gói thẻ hội viên giá trị cao qua 6 giai đoạn bán hàng có trọng số; kiểm soát nguyên nhân thất bại (`lost_reason`).
* **Người thao tác**: Nhân viên Kinh doanh (`PetCare Sales`).
* **Điều kiện trước khi demo**: Đã có các bản ghi Opportunity mẫu ở các giai đoạn khác nhau.
* **Các bước thao tác trên giao diện**:
  1. Trên Desk Navbar, chọn **Sales Opportunity** (hoặc mở Drawer trên Desk).
  2. Quan sát bảng Kanban với các cột: Prospecting (10%), Qualification (25%), Proposal (60%), Negotiation (80%), Closed Won (100%), Closed Lost (0%).
  3. Chọn cơ hội của khách hàng `Nguyễn Văn An` (Giá trị: 1.490.000 VNĐ, đang ở cột *Proposal*).
  4. Kéo thả thẻ sang cột **Closed Won**: Hệ thống tự động ghi nhận xác suất 100% và kích hoạt gợi ý khởi tạo thẻ hội viên.
  5. Thử nghiệm kéo một cơ hội khác sang **Closed Lost**: Hệ thống bật hộp thoại bắt buộc nhập lý do thất bại (ví dụ: "Khách chê giá đắt", "Đối thủ giảm giá 20%").
* **Kết quả quan sát được**:
  * Doanh thu dự kiến có trọng số trên thanh tổng kết tự động nhảy số theo thời gian thực.
  * Không thể đóng mất Deal nếu để trống lý do thất bại.
* **Màn hình / File liên quan**: [`petcare_opportunity.js`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/petcare_crm/doctype/petcare_opportunity/petcare_opportunity.js), [`sales_pipeline_service.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/utils/sales_pipeline_service.py).
* **Dữ liệu demo sử dụng**: Cơ hội của khách `Nguyễn Văn An` (1.490.000 VNĐ), `Lê Hoàng Long` (500.000 VNĐ - Lost).
* **Rủi ro & Phương án dự phòng**: Nếu view Kanban chưa hiển thị kịp trên Desk, chuyển sang chế độ List View và mở Form cơ hội để thay đổi trường `Sales Stage`.

---

### TÍNH NĂNG 03: TRA CỨU HỒ SƠ KHÁCH HÀNG 360 & GIA ĐÌNH ĐA THÚ CƯNG (MULTI-PET)

* **Mục tiêu nghiệp vụ**: Lễ tân hoặc bác sĩ tra cứu một chạm số điện thoại của khách hàng để xem toàn cảnh: danh sách các bé thú cưng, thẻ hội viên, số dư ví, các lượt dịch vụ gần nhất và cảnh báo y tế.
* **Người thao tác**: Nhân viên Lễ tân (`PetCare Front Desk`) / Bác sĩ thú y.
* **Điều kiện trước khi demo**: Đã nạp dữ liệu mẫu của khách hàng `Nguyễn Văn An` (sở hữu 2 bé: Corgi Bơ và Poodle Đậu Đậu).
* **Các bước thao tác trên giao diện**:
  1. Mở Cổng Web Portal tại địa chỉ `http://127.0.0.1:8080/` (hoặc mở tab **Tra Cứu Khách Hàng**).
  2. Tại ô tìm kiếm, nhập số điện thoại: `0901234567` (hoặc gõ tên `Nguyễn Văn An`).
  3. Bấm **Tìm Kiếm** (hoặc Enter).
* **Kết quả quan sát được**:
  * Hệ thống hiển thị ngay thẻ thông tin khách hàng `Nguyễn Văn An` kèm nhãn hội viên `Silver Member`.
  * Khối **Danh Sách Thú Cưng (Multi-Pet)** hiển thị đồng thời 2 hồ sơ:
    * Bé 1: `Bơ` (Chó Corgi, 11.5 kg, chu kỳ tắm sấy: Sắp đến hạn).
    * Bé 2: `Đậu Đậu` (Chó Poodle, 4.2 kg, khám sức khỏe: Bình thường).
  * Khối **Thẻ Hội Viên**: Gói Chăm Sóc Bạc, thời hạn còn 30 ngày, quyền lợi còn 1 buổi Grooming miễn phí và 2 lượt Spa giảm 10%.
  * Có sẵn các nút bấm hành động nhanh: *Mở Quầy POS Cho Bé Bơ*, *Nạp Tiền Ví*, *Gia Hạn Thẻ*, *Đặt Lịch Hẹn*.
* **Màn hình / File liên quan**: `preview.html` (`#tab-client`), API `get_customer_portal_details`, [`customer_service.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/utils/customer_service.py).
* **Dữ liệu demo sử dụng**: Khách hàng `Nguyễn Văn An` (`0901234567`).

---

### TÍNH NĂNG 04: ĐẶT LỊCH HẸN TRỰC TUYẾN & CHECK-IN TIẾP ĐÓN TẠI QUẦY

* **Mục tiêu nghiệp vụ**: Chủ nuôi chủ động đặt hẹn trực tuyến; nhân viên lễ tân tiếp đón tại quầy chỉ cần 1 thao tác Check-in để tự động tạo phiếu dịch vụ `Service Visit`.
* **Người thao tác**: Chủ nuôi thú cưng & Lễ tân (`PetCare Front Desk`).
* **Các bước thao tác trên giao diện**:
  1. Trên Web Portal, chuyển sang mục **Lịch Hẹn Dịch Vụ** (`#subview-appts-content`).
  2. Quan sát danh sách các lịch hẹn trong ngày (ví dụ: Lịch hẹn của bé `Bơ` lúc 09:00, bé `Đậu Phộng` lúc 10:30).
  3. Bấm nút **"Đặt Lịch Hẹn Mới"**:
     * Chọn Khách hàng: `Trần Thị Bích Ngọc`
     * Chọn Bé: `Đậu Phộng`
     * Chọn Dịch vụ: `Grooming Toàn Diện`
     * Chọn Giờ hẹn: Ngày hôm nay, 14:00
     * Bấm **Lưu Lịch Hẹn**.
  4. Tại dòng lịch hẹn của bé `Bơ` (trạng thái `Scheduled`), Lễ tân bấm nút **"Check-in Tiếp Đón"**.
* **Kết quả quan sát được**:
  * Trạng thái lịch hẹn lập tức đổi sang `Checked-In`.
  * Hệ thống tự động chuyển thẳng sang màn hình **Quầy POS**, điền sẵn thông tin khách hàng `Nguyễn Văn An`, bé `Bơ`, và dịch vụ tương ứng mà lễ tân không cần gõ lại.
* **Màn hình / File liên quan**: [`petcare_appointment.js`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/petcare_crm/doctype/petcare_appointment/petcare_appointment.js), API `check_in_appointment`.

---

### TÍNH NĂNG 05: PHIẾU DỊCH VỤ & CẤN TRỪ QUYỀN LỢI THẺ HỘI VIÊN (ROW LOCKING)

* **Mục tiêu nghiệp vụ**: Thực hiện dịch vụ cho thú cưng, tự động đối soát quyền lợi hội viên, cấn trừ an toàn chống trừ âm và chống trừ trùng lặp (Pessimistic Row Lock).
* **Người thao tác**: Kỹ thuật viên Spa & Thu ngân.
* **Các bước thao tác trên giao diện**:
  1. Trên màn hình Quầy POS (`#subview-pos-content`), chọn khách `Nguyễn Văn An`, chọn bé `Bơ`.
  2. Tại bảng chọn dịch vụ, nhấp chọn: `Grooming & Tắm Sấy Tiêu Chuẩn` (Đơn giá niêm yết: 350.000 VNĐ).
  3. Quan sát ô **Đối Soát Quyền Lợi Hội Viên**:
     * Hệ thống hiển thị: *Thẻ Bạc phát hiện 1 lượt Grooming miễn phí 100%*.
     * Cột Thành tiền tự động chuyển: `350.000 VNĐ` ➔ **`0 VNĐ (Miễn phí theo Thẻ Bạc)`**.
  4. Nhập trọng lượng bé sau khi tắm: `11.8` kg.
  5. Bấm nút **"Hoàn Tất Dịch Vụ & Cấn Trừ"**.
* **Kết quả quan sát được**:
  * Phiếu `Service Visit` được tạo ở trạng thái `Completed` với `final_price = 0`.
  * Sổ cái `Benefit Redemption Ledger` ghi nhận 1 dòng cấn trừ: Quyền lợi Grooming của thẻ Bạc giảm từ 1 xuống 0.
  * Trọng lượng mới `11.8 kg` tự động cập nhật vào hồ sơ bé Bơ.
  * Thử thao tác lần 2 với cùng dịch vụ: Hệ thống cảnh báo *Hết hạn mức miễn phí*, khôi phục đơn giá gốc `350.000 VNĐ`.
* **Màn hình / File liên quan**: [`service_visit.js`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/petcare_crm/doctype/service_visit/service_visit.js), [`membership_service.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/utils/membership_service.py).

---

### TÍNH NĂNG 06: SINH MÃ THANH TOÁN VIETQR ĐỘNG & WEBHOOK TỰ ĐỘNG ĐỐI SOÁT

* **Mục tiêu nghiệp vụ**: Khách hàng thanh toán qua chuyển khoản ngân hàng không cần gõ số tiền hay nội dung; hệ thống tự động gạch nợ tức thì khi nhận Webhook IPN ngân hàng.
* **Người thao tác**: Thu ngân và Hệ thống Webhook.
* **Các bước thao tác trên giao diện**:
  1. Tạo một phiếu dịch vụ phải thanh toán tiền (ví dụ: Bé `Kem` làm dịch vụ Spa giá `450.000 VNĐ`).
  2. Tại mục Phương Thức Thanh Toán, chọn **"Chuyển Khoản Ngân Hàng (VietQR Napas247)"**.
  3. Bấm **"Tạo Mã Thanh Toán QR"**.
  4. Quan sát cửa sổ Modal hiện ra: Mã QR chuẩn EMVCo kèm thông tin:
     * Số tài khoản nhận: `0901234567` (Ngân hàng TMCP Quân Đội - MB Bank)
     * Số tiền: `450.000 VNĐ`
     * Cú pháp chuyển khoản: `PC-SVC-SV-2026-00008`
  5. Trình diễn giả lập Webhook đối soát: Nhấp nút **"Mô Phỏng Nhận Webhook Ngân Hàng"** trên giao diện demo (hoặc gửi curl có chữ ký HMAC).
* **Kết quả quan sát được**:
  * Màn hình chuyển trạng thái ngay lập tức: Biểu tượng tích xanh **"Đã Nhận Thanh Toán Thành Công 450.000 VNĐ"**.
  * Phiếu dịch vụ đổi trạng thái sang `Completed` và lưu mã giao dịch ngân hàng đối soát.
* **Màn hình / File liên quan**: [`payment_gateway.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/utils/payment_gateway.py), API `payment_webhook`, API `get_service_visit_payment_qr`.

---

### TÍNH NĂNG 07: QUÉT CHU KỲ CHĂM SÓC SINH HỌC & GIỮ CHÂN KHÁCH HÀNG (CARE INTELLIGENCE)

* **Mục tiêu nghiệp vụ**: Tự động phân tích lịch sử thăm khám bằng thuật toán thống kê (EWMA + Tukey IQR + Mùa vụ), phát hiện thú cưng sắp đến hạn hoặc có nguy cơ rời bỏ để chủ động chăm sóc.
* **Người thao tác**: Chuyên viên CSKH & Quản lý phòng khám.
* **Các bước thao tác trên giao diện**:
  1. Mở Cổng Web Portal, chuyển sang tab **Chu Kỳ Chăm Sóc** (`#tab-cycle`).
  2. Bấm nút **"Kích Hoạt Quét Chu Kỳ Chăm Sóc (Care Engine Scan)"**.
  3. Quan sát bảng kết quả phân loại:
     * **Nhóm Sắp Đến Hạn (`DUE_SOON`)**: Bé `Bơ` (Chó Corgi của anh An, chu kỳ chuẩn 30 ngày, đã 27 ngày chưa ghé ➔ còn 3 ngày nữa đến hạn).
     * **Nhóm Nguy Cơ Rời Bỏ (`AT_RISK`)**: Bé `Miu Miu` (Mèo của anh Long, chu kỳ chuẩn 25 ngày, đã vắng mặt 55 ngày ➔ Tỷ lệ vắng mặt $2.2\times$ vượt ngưỡng $1.5\times$).
     * **Nhóm Sắp Hết Hạn Thẻ (`RENEWAL`)**: Bé `Đậu Phộng` (Gói Vàng của chị Ngọc còn 4 ngày nữa hết hạn).
  4. Nhấp nút **"Gọi Nhắc Lịch"** trên dòng bé `Bơ`: Modal ghi nhận cuộc gọi hiện ra, cho phép nhân viên đặt lịch hẹn ngay cho khách.
* **Kết quả quan sát được**:
  * Các đề xuất chăm sóc mới được tạo trong `Care Recommendation`.
  * Các công việc `ToDo` tự động xuất hiện trên danh sách việc cần làm của nhân viên CSKH.
  * Tin nhắn Zalo ZNS nhắc lịch được điều phối an toàn vào hộp thư `Omnichannel Outbox`.
* **Màn hình / File liên quan**: [`care_pattern_service.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/utils/care_pattern_service.py), [`recommendation_service.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/utils/recommendation_service.py).

---

### TÍNH NĂNG 08: NẠP TIỀN VÍ TRẢ TRƯỚC, GIA HẠN THẺ & ROLLOVER BẢO LƯU

* **Mục tiêu nghiệp vụ**: Quản lý dòng tiền thẻ hội viên, nạp thêm tiền vào ví trả trước và kích hoạt cơ chế Rollover bảo lưu số lượt tồn khi khách hàng gia hạn thẻ mới.
* **Người thao tác**: Nhân viên Bán hàng / Thu ngân.
* **Các bước thao tác trên giao diện**:
  1. Trong màn hình Tra cứu 360, chọn khách hàng `Trần Thị Bích Ngọc` (bé `Đậu Phộng`).
  2. Nhấp nút **"Nạp Tiền Ví"**:
     * Nhập số tiền: `1.000.000 VNĐ`
     * Chọn phương thức: `Tiền mặt` (hoặc VietQR)
     * Bấm **Xác Nhận Nạp Tiền**.
  3. Quan sát số dư ví (`balance`) của thẻ nhảy từ `0 VNĐ` lên `1.000.000 VNĐ`; bản ghi `Membership Transaction` được tạo.
  4. Nhấp nút **"Gia Hạn Thẻ Hội Viên"**:
     * Chọn gói mới: `Gói Chăm Sóc Vàng (Gold)`
     * Tích chọn: **"Cho phép Rollover bảo lưu lượt tồn cũ"**
     * Bấm **Thực Hiện Gia Hạn**.
* **Kết quả quan sát được**:
  * Thẻ hội viên cũ của chị Ngọc chuyển trạng thái thành `Renewed`.
  * Thẻ hội viên mới được tạo với thời hạn 365 ngày tiếp theo.
  * Số lượt Grooming còn tồn từ thẻ cũ được cộng dồn nguyên vẹn sang bảng quyền lợi của thẻ mới.
* **Màn hình / File liên quan**: [`customer_membership.js`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/petcare_crm/doctype/customer_membership/customer_membership.js), API `top_up_membership`, API `renew_membership`.

---

### TÍNH NĂNG 09: TIẾP NHẬN PHẢN HỒI KHIẾU NẠI & GIÁM SÁT SLA (SERVICE RECOVERY)

* **Mục tiêu nghiệp vụ**: Ghi nhận các sự cố phát sinh sau dịch vụ, phân loại mức độ khẩn cấp và kích hoạt cảnh báo SLA tự động khi khiếu nại chưa được xử lý kịp thời.
* **Người thao tác**: Nhân viên CSKH & Quản lý phòng khám (`PetCare Manager`).
* **Các bước thao tác trên giao diện**:
  1. Trên Desk Workspace, chọn **Service Cases & Complaints** (hoặc mở Form `PetCare Case`).
  2. Xem bản ghi khiếu nại mẫu của khách `Lê Hoàng Long` (Bé Miu Miu):
     * Chủ đề: *Mèo bị hoảng nhẹ khi sấy lồng*
     * Mức độ ưu tiên: `High`
     * Trạng thái: `Open`
  3. Bác sĩ/Quản lý phòng khám nhập phương án xử lý vào trường `Resolution`: *"Đã gọi điện xin lỗi khách hàng, cam kết từ lần sau chuyển sang sấy tay nhẹ nhàng và tặng 1 voucher giảm giá 20% Spa"*.
  4. Đổi trạng thái sang `Resolved`.
* **Kết quả quan sát được**:
  * Trường thời gian giải quyết (`resolution_date`) được tự động ghi nhận.
  * Nếu Case ở mức `Urgent` bị bỏ quên quá 24h, tác vụ nền `hourly_workflow_check` sẽ gửi cảnh báo đỏ lên Desk Navbar của Quản lý.
* **Màn hình / File liên quan**: [`petcare_case.js`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/petcare_crm/doctype/petcare_case/petcare_case.js), [`workflow_automation.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/utils/workflow_automation.py).

---

### TÍNH NĂNG 10: BÁO CÁO QUẢN TRỊ 8 KPI & ĐỐI SÁNH HIỆU QUẢ ĐA CHI NHÁNH

* **Mục tiêu nghiệp vụ**: Cung cấp bức tranh toàn cảnh về sức khỏe tài chính và vận hành CRM thông qua 8 chỉ số KPI chuẩn và phân bổ doanh thu theo từng chi nhánh.
* **Người thao tác**: Quản lý chuỗi & Chuyên viên Phân tích (`PetCare Analyst`).
* **Các bước thao tác trên giao diện**:
  1. Trên Desk Workspace, mục **Analytics & Reports**, nhấp chọn báo cáo **PetCare KPI Overview**.
  2. Báo cáo dạng Script Report mở ra với bảng số liệu tổng hợp 8 chỉ số.
  3. Chọn bộ lọc ngày bắt đầu (`from_date`) và ngày kết thúc (`to_date`).
  4. Quan sát 3 thẻ tổng kết nhanh (Report Summary Cards):
     * **Lead Win Rate**: Tỷ lệ chuyển đổi Lead thành công (%).
     * **Doanh Thu Thuần**: Tổng tiền thực nhận từ các phiếu dịch vụ sau trừ chiết khấu.
     * **Hội Viên Active**: Số lượng thẻ hội viên đang có hiệu lực.
  5. Mở rộng bảng chi tiết để xem phân bổ doanh thu giữa 4 cơ sở: `CN-TRUNGTAM`, `CN-QUAN1`, `CN-THUDUC`, `CN-BINHTHANH`.
* **Kết quả quan sát được**:
  * Các chỉ số được tính toán chính xác từ các bảng dữ liệu gốc theo đúng công thức nghiệp vụ, phân tách rõ Doanh số niêm yết (Gross) và Doanh thu thực thu (Net).
* **Màn hình / File liên quan**: [`petcare_kpi_overview.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/petcare_crm/report/petcare_kpi_overview/petcare_kpi_overview.py), [`analytics_service.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/utils/analytics_service.py).
