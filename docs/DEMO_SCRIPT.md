# KỊCH BẢN TRÌNH DIỄN ĐỒ ÁN (DEMO SCRIPT & PRESENTATION FLOW)

> **Dự án**: PetCare CRM (Hệ Thống CRM Dịch Vụ Chăm Sóc Thú Cưng)  
> **Nền tảng**: Frappe Framework v15 (Desk Native)  
> **Thời lượng khuyến nghị**: 15 – 20 phút  
> **Tài khoản demo**: `Administrator` / `admin123`  

---

## 🎬 TỔNG QUAN 3 CÂU CHUYỆN DEMO CỐT LÕI

Hệ thống được thiết kế để trình diễn trọn vẹn vòng đời khách hàng qua 3 câu chuyện liền mạch:
1. **Câu chuyện 1 (Tiếp thị & Bán hàng)**: Tiếp nhận Lead từ Facebook Ads, tương tác tư vấn, chuyển đổi thành Khách hàng, Thú cưng và Cơ hội bán hàng trong Sales Pipeline.
2. **Câu chuyện 2 (Dịch vụ & Vận hành Thẻ Hội Viên)**: Khách hàng sở hữu nhiều Pet (Multi-pet), tham gia gói hội viên, sử dụng dịch vụ Grooming được miễn phí 100%, bảo vệ số dư không bị trừ âm khi quyền lợi đã hết.
3. **Câu chuyện 3 (Trí tuệ Chăm sóc & Giữ chân Khách hàng)**: Thuật toán Rule-based phân tích lịch sử ghé thăm, phát hiện thú cưng sắp đến hạn (`DUE_SOON`) và khách hàng có nguy cơ rời bỏ (`AT_RISK`), tự động tạo khuyến nghị và giao việc cho nhân viên CSKH chốt đơn.

---

## 📌 CÂU CHUYỆN 1: LEAD TO CUSTOMER & SALES OPPORTUNITY
**Vai trò thao tác**: `PetCare Sales` (Nhân viên tư vấn bán hàng)  
**Thời lượng**: 5 phút  

### Bước 1: Tiếp nhận Lead mới
1. Đăng nhập vào Frappe Desk, truy cập Workspace **PetCare CRM**.
2. Trên thẻ chỉ số, nhấn vào **"Lead Cần Xử Lý"** hoặc mở danh sách **PetCare Lead**.
3. Xem Lead mẫu: **"Hoàng Gia Bảo"** (Nguồn: `Facebook Ads`, Điện thoại: `0911223344`, Nhu cầu: *Cún Husky 4 tháng tuổi cần tư vấn tiêm chủng*).

### Bước 2: Ghi nhận hoạt động tương tác (Follow-up)
1. Mở chi tiết Lead `Hoàng Gia Bảo`.
2. Tại thanh công cụ bên phải, nhấn **Add Comment / Communication**:
   * *Nội dung*: *"Đã gọi điện tư vấn gói tiêm phòng 7 bệnh và gói tắm khử mùi cho cún con. Khách đồng ý ghé phòng khám cuối tuần."*
3. Trạng thái Lead tự động chuyển từ `New` sang `Contacted`.

### Bước 3: Chuyển đổi Lead thành Khách hàng & Cơ hội
1. Trên form Lead, nhấn nút hành động **"Chuyển Đổi Lead"** (Action Button).
2. Hộp thoại chuyển đổi xuất hiện:
   * **Tên thú cưng**: Nhập `Tuyết Trắng`.
   * **Loài / Giống**: Chọn `Dog` / `Husky`.
   * **Tạo cơ hội bán hàng**: Tích chọn `Có`.
   * **Giá trị cơ hội**: Nhập `1,500,000 VND`.
3. Nhấn **Xác Nhận Chuyển Đổi**:
   * Hệ thống tự động kiểm tra chống trùng số điện thoại.
   * Tạo khách hàng mới `Contact` (Hoàng Gia Bảo).
   * Tạo hồ sơ `Pet` (Tuyết Trắng) liên kết với chủ nuôi.
   * Tạo cơ hội bán hàng `PetCare Opportunity` (1,500,000 VND).
   * Lead được đánh dấu `Converted`, liên kết đầy đủ các mã tham chiếu.

### Bước 4: Quản lý Sales Pipeline
1. Vào menu **PetCare Opportunity**, chuyển sang chế độ xem Kanban hoặc List View.
2. Tìm cơ hội của anh Bảo, kéo chuyển giai đoạn từ `Qualification` $\rightarrow$ `Proposal` $\rightarrow$ `Closed Won`.
3. Báo cáo tỷ lệ chuyển đổi và giá trị phễu tự động cập nhật.

---

## 📌 CÂU CHUYỆN 2: MULTI-PET, MEMBERSHIP & DEDUCTION ENGINE
**Vai trò thao tác**: `PetCare Technician` / Thu ngân  
**Thời lượng**: 6 phút  

### Bước 1: Hồ sơ khách hàng sở hữu nhiều thú cưng (Multi-Pet)
1. Vào danh sách **Contact**, chọn khách hàng **Nguyễn Văn An** (`0901234567`).
2. Xem mục liên kết thú cưng: Anh An sở hữu **2 bé cún**:
   * Bé **Bơ** (Corgi, 11.5 kg, vàng trắng).
   * Bé **Đậu Đậu** (Shiba Inu, 9.2 kg, nâu đỏ).
3. Chứng minh hệ thống hỗ trợ 100% quan hệ $1:N$ giữa Khách hàng và Thú cưng.

### Bước 2: Tham gia Gói Hội Viên & Quản lý Quyền Lợi
1. Vào menu **Customer Membership**, xem thẻ hội viên của anh An (`MEM-SILVER-01`):
   * Gói: `Gói Chăm Sóc Bạc (Silver)`.
   * Trạng thái: `Active`.
   * Quyền lợi còn lại: `1 lượt Grooming Toàn Diện (FREE)` và `2 lượt Spa giảm 10%`.

### Bước 3: Tạo Phiếu Dịch Vụ & Khấu Trừ Ưu Đãi Tự Động
1. Vào danh sách **Service Visit**, nhấn **+ Add Service Visit**:
   * **Khách hàng**: Chọn `Nguyễn Văn An`.
   * **Thú cưng**: Nhấn trường `pet`, bộ lọc query thông minh **chỉ hiển thị 2 bé Bơ và Đậu Đậu** (không hiển thị thú cưng của khách khác).
   * Chọn thú cưng: `Bơ`.
   * **Dịch vụ**: Chọn `SRV-GROOM` ("Grooming Toàn Diện").
   * Hệ thống tự động điền đơn giá niêm yết: `350,000 VND`.
   * **Thẻ hội viên**: Chọn `MEM-SILVER-01`.
2. Quan sát cơ chế cấn trừ:
   * `Original Price`: `350,000 VND`
   * `Discount Amount`: `350,000 VND` (Quyền lợi FREE 100%)
   * `Final Price`: `0 VND`
3. Nhấn **Save**: Phiếu dịch vụ được ghi nhận thành công.

### Bước 4: Kiểm tra An Toàn Số Dư & Xử Lý Khi Hết Quyền Lợi
1. Mở lại thẻ hội viên `MEM-SILVER-01`:
   * Quyền lợi Grooming đã cập nhật: `used_quantity = 1`, `remaining_quantity = 0`.
   * Một dòng lịch sử được ghi nhận trong sổ cái **Benefit Redemption Ledger**.
2. Thử tạo phiếu Grooming thứ 2 cho bé `Đậu Đậu`:
   * Hệ thống tự động nhận diện quyền lợi Grooming miễn phí đã hết (`remaining = 0`).
   * Chiết khấu tự động về `0 VND`, giá thanh toán giữ nguyên giá gốc `350,000 VND`.
   * Chứng minh hệ thống kiểm soát số dư chặt chẽ, tuyệt đối không bị trừ âm.

---

## 📌 CÂU CHUYỆN 3: CARE INTELLIGENCE, DUE SOON / AT RISK & CSKH
**Vai trò thao tác**: `PetCare Manager` (Quản lý phòng khám) & Nhân viên CSKH  
**Thời lượng**: 6 phút  

### Bước 1: Kích hoạt Phân tích Chu kỳ Tự động (Care Engine)
1. Trên giao diện Workspace, kiểm tra Number Cards:
   * **Thú Cưng Sắp Đến Chu Kỳ**: Hiển thị `3` bé.
   * **Hội Viên Sắp Hết Hạn**: Hiển thị `2` hội viên.
2. Bộ lập lịch Frappe Scheduler chạy định kỳ mỗi đêm (hoặc kích hoạt thủ công qua script / Desk button).

### Bước 2: Khám phá Thuật toán Rule-based minh bạch
1. **Trường hợp DUE_SOON (Bé Bơ - Corgi)**:
   * Mở chi tiết `Care Recommendation` của bé Bơ.
   * *Lý do*: Lịch sử 3 lần tắm trước cách đều 30 ngày. Lần gần nhất là 27 ngày trước $\implies$ Còn **3 ngày nữa đến hạn**.
   * *Độ tin cậy*: `HIGH` (Đã qua lọc ngoại lai IQR).
   * *Tích hợp Thẻ*: Nhắc nhở anh An thẻ Bạc sắp hết hạn sau 30 ngày.
2. **Trường hợp AT_RISK (Bé Miu Miu - Mèo Anh)**:
   * Mở chi tiết `Care Recommendation` của bé Miu Miu.
   * *Lý do*: Chu kỳ thông thường là 25 ngày, nhưng bé đã **vắng mặt 55 ngày** (Tỷ lệ vắng mặt $\text{absence\_ratio} = 2.2 \ge 1.5$).
   * *Mức độ ưu tiên*: `Urgent` kèm đề xuất tặng voucher giảm giá để win-back khách hàng.
3. **Trường hợp RENEWAL WARNING (Bé Đậu Phộng)**:
   * Cảnh báo gói hội viên của chị Bích Ngọc sẽ hết hạn sau **4 ngày**.

### Bước 3: Nhân viên CSKH tiếp nhận nhiệm vụ (ToDo Task)
1. Mở danh sách **ToDo**:
   * Hệ thống đã tự động phân bổ nhiệm vụ: *"CSKH: Bé Bơ sắp đến chu kỳ tắm sấy (còn 3 ngày)"*.
   * Nhiệm vụ được giao đích danh kèm hạn xử lý rõ ràng.
2. Nhân viên gọi điện cho anh An:
   * Anh An đồng ý đặt lịch làm dịch vụ.
   * Đổi trạng thái Care Recommendation từ `New` sang `Contacted` $\rightarrow$ `Converted`.
3. Kiểm tra tính **Idempotent (Chống sinh rác)**:
   * Scheduler chạy lại lần 2: Không tạo thêm nhiệm vụ ToDo nào trùng lặp. Đề xuất cũ được cập nhật tại chỗ (`UPDATED`).

### Bước 4: Xem Báo Cáo Quản Trị Tổng Quan (KPI Overview)
1. Mở báo cáo **PetCare KPI Overview** (`petcare_kpi_overview`):
   * Tỷ lệ chuyển đổi Lead: `41.7%`
   * Doanh số phễu kỳ vọng có trọng số: `2,658,000 VND`
   * Tổng số lượt dịch vụ và Doanh thu thực tế (Net Revenue)
   * Tỷ lệ chuyển đổi đề xuất chăm sóc: `50.0%`
2. Kết luận: Hệ thống PetCare CRM vận hành trọn vẹn, khép kín từ khâu thu hút khách hàng tiềm năng đến chăm sóc, tái giữ chân và gia tăng giá trị trọn đời (LTV).
