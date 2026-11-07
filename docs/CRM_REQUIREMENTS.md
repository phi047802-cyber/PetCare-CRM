# YÊU CẦU NGHIỆP VỤ HỆ THỐNG (CRM REQUIREMENTS SPECIFICATION)
## HỆ THỐNG PETCARE CRM TOÀN DIỆN CHO DOANH NGHIỆP DỊCH VỤ THÚ CƯNG

> **Dự án**: PetCare CRM  
> **Nền tảng**: Frappe Framework v15  
> **Phiên bản tài liệu**: 2.0  
> **Mã tài liệu**: REQ-PETCARE-CRM-2026  

---

## 1. DANH MỤC CÁC YÊU CẦU NGHIỆP VỤ CHỨC NĂNG (FUNCTIONAL REQUIREMENTS)

### PHÂN HỆ 1: QUẢN LÝ LEAD & TIẾP NHẬN TIỀM NĂNG (MARKETING & LEAD)

#### REQ-LEAD-01: Ghi nhận thông tin Khách hàng tiềm năng (Lead Intake)
* **Mô tả**: Hệ thống cho phép nhân viên ghi nhận khách hàng tiềm năng đến từ nhiều nguồn khác nhau.
* **Chi tiết dữ liệu**:
  * Tên Lead (`lead_name` - Bắt buộc).
  * Số điện thoại (`phone` - Bắt buộc, kiểm tra định dạng số điện thoại Việt Nam 10 chữ số).
  * Email (`email` - Tùy chọn, kiểm tra tính hợp lệ nếu có nhập).
  * Nguồn tiếp cận (`lead_source`: `Facebook Ads`, `Zalo`, `Hotline`, `Khách ghé qua`, `Được giới thiệu`, `Website`).
  * Người phụ trách (`lead_owner`: Liên kết đến người dùng `User` trong hệ thống).
  * Thông tin thú cưng ban đầu (`initial_pet_info`: Ghi chú về loài, giống, nhu cầu sơ bộ ví dụ: "Cún Poodle 4 tháng cần tiêm phòng").
  * Mức độ ưu tiên (`priority`: `Thấp`, `Trung bình`, `Cao`).
* **Tiêu chí nghiệm thu (Acceptance Criteria)**:
  * Không cho phép lưu Lead nếu thiếu Tên hoặc Số điện thoại.
  * Tự động gán người tạo làm `lead_owner` nếu chưa chỉ định.

#### REQ-LEAD-02: Quản lý vòng đời và trạng thái Lead (Lifecycle Status)
* **Mô tả**: Lead phải chuyển dịch trạng thái có kiểm soát:
  * `New` (Mới tạo): Chưa có tương tác nào.
  * `Contacted` (Đã liên hệ): Nhân viên đã gọi điện hoặc nhắn tin trao đổi.
  * `Qualified` (Đủ điều kiện): Khách hàng có nhu cầu thực tế và phù hợp với dịch vụ của cơ sở.
  * `Unqualified` (Không tiềm năng): Khách từ chối, sai số, hoặc nằm ngoài khu vực phục vụ (yêu cầu nhập lý do).
  * `Converted` (Đã chuyển đổi): Khách hàng đồng ý sử dụng dịch vụ hoặc đặt lịch.
* **Tiêu chí nghiệm thu**:
  * Khi chuyển trạng thái sang `Unqualified`, bắt buộc phải có nội dung giải trình trong trường `unqualified_reason`.
  * Không thể sửa đổi thông tin Lead sau khi đã chuyển sang trạng thái `Converted`.

#### REQ-LEAD-03: Chuyển đổi Lead thành Khách hàng & Thú cưng (Lead Conversion)
* **Mô tả**: Khi Lead ở trạng thái `Qualified`, nhân viên có thể thực hiện thao tác "Chuyển Đổi Lead" (Convert Lead).
* **Quy tắc chuyển đổi**:
  * Hệ thống tự động tạo mới một bản ghi `Contact` (Khách hàng) với tên, số điện thoại, email từ Lead.
  * Nếu có thông tin thú cưng sơ bộ, hệ thống hỗ trợ tạo nhanh bản ghi `Pet` tương ứng gán quyền sở hữu cho Contact vừa tạo.
  * Cho phép tùy chọn tạo ngay một Cơ hội bán hàng (`PetCare Opportunity`) nếu khách đang quan tâm đến gói dịch vụ hoặc combo spa.
  * Cập nhật trạng thái của Lead sang `Converted` và lưu liên kết tham chiếu tới `Contact` vừa tạo.

---

### PHÂN HỆ 2: QUẢN LÝ KHÁCH HÀNG & HỒ SƠ THÚ CƯNG (CUSTOMER & MULTI-PET)

#### REQ-CUST-01: Hồ sơ Khách hàng chuẩn hóa (Unified Customer / Contact)
* **Mô tả**: Tận dụng DocType chuẩn `Contact` của Frappe Framework để quản lý thông tin khách hàng cá nhân.
* **Chi tiết dữ liệu**:
  * Họ và tên đầy đủ (`first_name`, `last_name`).
  * Số điện thoại chính, số điện thoại phụ, địa chỉ liên lạc.
  * Phân hạng khách hàng (`customer_tier`: `Chuẩn`, `Thân thiết`, `VIP`, `VVIP`).
  * Tổng chi tiêu tích lũy (`total_spent`) và tổng số lượt dịch vụ đã hoàn thành (`total_visits`).
  * Dòng thời gian lịch sử tương tác tổng hợp (Timeline) hiển thị đầy đủ cuộc gọi, ghi chú, giao dịch và lịch sử thú cưng.

#### REQ-PET-01: Quản lý Hồ sơ Thú cưng đa đối tượng (Multi-Pet Management)
* **Mô tả**: Một khách hàng (`Contact`) có thể sở hữu một hoặc nhiều thú cưng (`Pet`).
* **Chi tiết dữ liệu thú cưng**:
  * Tên thú cưng (`pet_name` - Bắt buộc, hiển thị nhận diện).
  * Chủ sở hữu (`customer` - Liên kết bắt buộc tới DocType `Contact`).
  * Loài (`species`: `Chó`, `Mèo`, `Thỏ`, `Khác` - Bắt buộc).
  * Giống loài (`breed`: Ví dụ: Poodle, Corgi, Mèo Anh lông ngắn, Husky...).
  * Ngày sinh hoặc Ngày ước tính (`birth_date`), Giới tính (`gender`: `Đực`, `Cái`, `Đã triệt sản`).
  * Cân nặng hiện tại (`weight_kg` - Cập nhật liên tục sau mỗi lần dịch vụ).
  * Tiền sử y tế, tình trạng dị ứng hóa chất, đặc tính hung dữ/nhát người (`medical_notes`).
* **Tiêu chí nghiệm thu**:
  * Khi mở hồ sơ khách hàng, phải xem được danh sách tất cả các thú cưng trực thuộc.
  * Khi mở hồ sơ thú cưng, phải xem được đầy đủ lịch sử tất cả các lần sử dụng dịch vụ (`Service Visit`) của riêng bé đó.

---

### PHÂN HỆ 3: QUẢN LÝ CƠ HỘI BÁN HÀNG & PHỄU KINH DOANH (SALES PIPELINE)

#### REQ-OPP-01: Quản lý Cơ hội bán hàng (PetCare Opportunity)
* **Mô tả**: Quản lý các cơ hội kinh doanh các gói dịch vụ lớn (khách sạn dài ngày, combo làm đẹp toàn diện, thẻ hội viên định kỳ, khóa huấn luyện).
* **Chi tiết dữ liệu**:
  * Tiêu đề cơ hội (`opportunity_title`).
  * Khách hàng (`customer` - Liên kết tới `Contact`).
  * Thú cưng liên quan (`pet` - Tùy chọn).
  * Giai đoạn bán hàng (`stage`: `Prospecting` -> `Qualification` -> `Proposal` -> `Negotiation` -> `Closed Won` -> `Closed Lost`).
  * Giá trị kỳ vọng (`expected_amount`: VNĐ).
  * Xác suất thành công (`probability`: 10% đến 100%).
  * Doanh thu dự kiến (`weighted_amount` = `expected_amount` * `probability` / 100).
  * Người phụ trách (`sales_person`: User).
  * Ngày dự kiến chốt (`expected_closing_date`).
* **Tiêu chí nghiệm thu**:
  * Khi chuyển sang `Closed Won`: Hệ thống cho phép mở nhanh phiếu mua thẻ hội viên (`Customer Membership`) hoặc mở phiếu tiếp nhận dịch vụ (`Service Visit`).
  * Khi chuyển sang `Closed Lost`: Bắt buộc phải chọn lý do thất bại (`lost_reason`: `Giá quá cao`, `Chọn đối thủ khác`, `Không còn nuôi thú cưng`, `Chuyển chỗ ở`, `Khác`) và ghi chú chi tiết.

---

### PHÂN HỆ 4: VẬN HÀNH DỊCH VỤ & TIẾP NHẬN TẠI QUẦY (SERVICE OPERATIONS)

#### REQ-SERV-01: Danh mục Dịch vụ chuẩn hóa (PetCare Service Catalog)
* **Mô tả**: Quản lý danh mục các dịch vụ mà cơ sở cung cấp thay vì nhập văn bản tự do.
* **Chi tiết dữ liệu**:
  * Mã dịch vụ (`service_code` - Mã duy nhất).
  * Tên dịch vụ (`service_name`: Tắm vệ sinh tiêu chuẩn, Cắt tỉa tạo kiểu, Tẩy bọ chét - ve rận, Nhuộm lông thời trang, Khách sạn thú cưng...).
  * Phân loại (`service_category`: `Grooming & Spa`, `Y tế & Vệ sinh`, `Khách sạn & Lưu trú`, `Huấn luyện`).
  * Áp dụng cho loài (`species_applicability`: `Tất cả`, `Chỉ dành cho Chó`, `Chỉ dành cho Mèo`).
  * Đơn giá tiêu chuẩn (`standard_price`: VNĐ).
  * Thời lượng thực hiện ước tính (`estimated_duration_minutes`: phút).
  * Trạng thái kinh doanh (`is_active`: 1 / 0).

#### REQ-SERV-02: Phiếu tiếp nhận Dịch vụ thực tế (Service Visit Record)
* **Mô tả**: Ghi nhận mỗi lần thú cưng được đưa đến cơ sở để sử dụng dịch vụ.
* **Quy tắc tính giá và cấn trừ quyền lợi**:
  * Chọn thú cưng (`pet`): Hệ thống tự động truy xuất chủ nuôi (`customer`) tương ứng.
  * Chọn dịch vụ (`service_type` hoặc `service`): Tự động điền đơn giá gốc (`original_price`).
  * Kiểm tra Thẻ hội viên (`Customer Membership`):
    * Nếu khách có thẻ hội viên còn hiệu lực và còn quyền lợi cho dịch vụ tương ứng:
      * Nếu quyền lợi là `FREE`: Đơn giá thực thu (`final_price`) = 0; tự động giảm 1 lượt còn lại trong thẻ.
      * Nếu quyền lợi là `PERCENTAGE`: `final_price` = `original_price` * (1 - `discount_value` / 100).
      * Nếu quyền lợi là `FIXED`: `final_price` = max(0, `original_price` - `discount_value`).
    * Nếu không có thẻ hoặc quyền lợi đã hết: `final_price` = `original_price`.
  * Sau khi hoàn tất phiếu dịch vụ, hệ thống cập nhật cân nặng mới nhất của thú cưng vào hồ sơ `Pet` và tự động kích hoạt tính toán lại chu kỳ chăm sóc.

---

### PHÂN HỆ 5: QUẢN LÝ THẺ HỘI VIÊN, QUYỀN LỢI & VÍ NẠP (MEMBERSHIP & WALLET)

#### REQ-MEM-01: Cấu hình Gói hội viên (Membership Plan & Plan Benefits)
* **Mô tả**: Cho phép người quản trị định nghĩa các gói hội viên linh hoạt.
* **Chi tiết dữ liệu**:
  * Tên gói (`plan_name`: Gói Đồng / Bạc / Vàng / Kim Cương / Spa Định Kỳ 10 Lượt...).
  * Giá bán gói (`price`: VNĐ).
  * Thời hạn hiệu lực (`validity_days`: ví dụ 30 ngày, 90 ngày, 365 ngày).
  * Bảng con quyền lợi (`Plan Benefit`):
    * Loại dịch vụ áp dụng (`benefit_type`).
    * Tổng số lượt cấp (`total_quantity`: ví dụ 10 lượt tắm, 5 lượt cắt tỉa).
    * Cơ chế giảm giá (`discount_type`: `FREE` - Miễn phí 100%, `PERCENTAGE` - Giảm theo %, `FIXED` - Giảm số tiền cố định).
    * Giá trị giảm (`discount_value`).

#### REQ-MEM-02: Vòng đời Thẻ hội viên khách hàng (Customer Membership Lifecycle)
* **Mô tả**: Quản lý từng thẻ hội viên thực tế được phát hành cho khách hàng.
* **Quy tắc vận hành**:
  * Trạng thái thẻ: `Active` (Đang hoạt động), `Expired` (Hết hạn), `Exhausted` (Đã dùng hết quyền lợi), `Cancelled` (Đã hủy).
  * Kiểm tra thời hạn: Nếu `today() > end_date`, thẻ tự động chuyển trạng thái sang `Expired`.
  * Chính sách Thẻ gia đình (Multi-pet Family Plan): Nếu trường `pet` để trống, thẻ có thể dùng chung cho tất cả các thú cưng của cùng chủ nuôi đó. Nếu trường `pet` có chọn bé cụ thể, thẻ chỉ được phép trừ quyền lợi cho đúng bé đó.
  * Số dư ví trả trước (`balance`): Cho phép khách hàng nạp trước tiền vào thẻ để cấn trừ tiền dịch vụ tiện lợi không dùng tiền mặt.

#### REQ-MEM-03: Giao dịch Tài chính Ví hội viên (Membership Transaction)
* **Mô tả**: Mọi biến động số dư ví phải được ghi nhận qua phiếu giao dịch an toàn (Audit Trail).
* **Loại giao dịch (`transaction_type`)**:
  * `Top Up` (Nạp tiền): Tăng số dư thẻ, ghi nhận hình thức thanh toán (Tiền mặt, Chuyển khoản, Thẻ ngân hàng), mã đối soát.
  * `Deduct` (Trừ tiền thanh toán dịch vụ): Giảm số dư thẻ tương ứng với `final_price` của `Service Visit`.
  * `Refund` (Hoàn tiền): Hoàn trả lại số dư khi hủy phiếu dịch vụ hợp lệ.
* **Ràng buộc an toàn**: Số dư `balance` của thẻ hội viên tuyệt đối không được phép âm (`balance >= 0`).

#### REQ-MEM-04: Quy trình Gia hạn thẻ & Kế thừa quyền lợi (Renewal & Rollover)
* **Mô tả**: Khi khách hàng đồng ý gia hạn thẻ hội viên cũ sang chu kỳ mới:
  * Hệ thống cho phép người dùng lựa chọn:
    1. **Bảo lưu và cộng dồn lượt tồn (Rollover Remaining Benefits)**: Chuyển toàn bộ số lượt dịch vụ chưa dùng hết từ thẻ cũ sang thẻ mới.
    2. **Xóa bỏ lượt tồn (Forfeit Remaining Benefits)**: Thẻ mới chỉ nhận đủ số lượt nguyên bản của gói.
  * Số dư ví tài khoản cũ (`balance`) luôn được tự động chuyển 100% sang thẻ mới.
  * Thẻ cũ được đánh dấu trạng thái `Renewed` và lưu liên kết tham chiếu tới thẻ mới.

---

### PHÂN HỆ 6: ĐỘNG CƠ DỰ BÁO CHU KỲ & GIỮ CHÂN KHÁCH HÀNG (CARE PATTERN ENGINE)

#### REQ-CARE-01: Thuật toán Thống kê Chu kỳ Chăm sóc (EWMA + IQR)
* **Mô tả**: Tự động phân tích lịch sử đến làm dịch vụ của từng thú cưng để tìm ra chu kỳ chăm sóc chuẩn xác, loại bỏ nhiễu thống kê.
* **Quy tắc toán học**:
  * Điều kiện tối thiểu: Phải có từ 2 lần làm dịch vụ trở lên để tính khoảng cách giữa các lần (deltas). Nếu dưới 2 lần, trạng thái chu kỳ là `INSUFFICIENT_DATA`.
  * **Lọc ngoại lệ (Outlier Filtering via IQR)**: Khi có từ 4 khoảng cách trở lên, tính $Q_1$, $Q_3$, $IQR = Q_3 - Q_1$. Chỉ giữ lại các khoảng cách nằm trong hàng rào $[Q_1 - 1.5 \times IQR, Q_3 + 1.5 \times IQR]$.
  * **Chu kỳ trung bình có trọng số (EWMA - Exponentially Weighted Moving Average)**: Gán hệ số $\alpha = 0.6$ ưu tiên cao hơn cho các khoảng cách thời gian gần đây nhất:
    $$EWMA_t = \alpha \times \Delta_t + (1 - \alpha) \times EWMA_{t-1}$$
  * Chu kỳ dự báo được làm tròn thành số nguyên ngày (`average_interval_days`).

#### REQ-CARE-02: Phân loại Trạng thái Chu kỳ & Phát hiện Nguy cơ (Pattern Classification)
* Dựa trên số ngày kể từ lần ghé thăm gần nhất (`days_since_last_visit`):
  * **STABLE (Ổn định)**: Thú cưng chưa đến kỳ chăm sóc kế tiếp.
  * **DUE_SOON (Sắp đến hạn)**: Thú cưng nằm trong khoảng ngưỡng báo trước (ví dụ còn $\le 3$ ngày là đến hạn hoặc trễ không quá 3 ngày so với chu kỳ). Nếu khách vừa làm dịch vụ trong ngày (`days_since == 0`), không được đánh dấu `DUE_SOON`.
  * **OVERDUE / AT_RISK (Có nguy cơ rời bỏ)**: Thú cưng đã quá hạn chu kỳ từ 1.5 lần trở lên mà chủ chưa đưa quay lại cơ sở.

#### REQ-CARE-03: Khởi tạo & Theo dõi Đề xuất Chăm sóc (Care Recommendation Lifecycle)
* **Mô tả**: Tự động tạo bản ghi `Care Recommendation` cho mỗi thú cưng rơi vào trạng thái `DUE_SOON` hoặc `OVERDUE`.
* **Trạng thái đề xuất**:
  * `NEW` (Mới tạo): Scheduler vừa sinh ra, đang chờ nhân viên CSKH xử lý.
  * `CONTACTED` (Đã liên hệ): Nhân viên đã gọi điện / nhắn tin nhắc lịch cho chủ nuôi.
  * `BOOKED` (Đã đặt lịch / Hoàn thành): Khách hàng đồng ý đưa bé đến làm dịch vụ, tạo liên kết trực tiếp tới `Service Visit`.
  * `DISMISSED` (Bỏ qua / Từ chối): Khách từ chối với lý do cụ thể (Bé đang ốm, Đi công tác xa, Đã làm dịch vụ ở nơi khác...).

---

### PHÂN HỆ 7: TỰ ĐỘNG HÓA, BÁO CÁO & KHÔNG GIAN LÀM VIỆC (AUTOMATION & ANALYTICS)

#### REQ-AUTO-01: Tác vụ Quét hàng ngày (Daily PetCare Scan)
* **Mô tả**: Tự động kích hoạt hàng đêm qua Scheduler cron job của Frappe (`petcare_crm.tasks.daily_petcare_scan`).
* **Nội dung thực thi**:
  1. Quét toàn bộ hồ sơ thú cưng, tính toán chu kỳ EWMA, tạo/cập nhật `Care Recommendation`.
  2. Quét toàn bộ `Customer Membership` đang hoạt động: Chuyển sang `Expired` nếu quá `end_date`, gửi cảnh báo nếu còn 7 ngày nữa là hết hạn.
  3. Tự động sinh `ToDo` nhắc việc cho nhân viên CSKH đối với các khách hàng `At Risk`.

#### REQ-DASH-01: PetCare CRM Workspace & Dashboard Số liệu Thời gian thực
* Xây dựng Không gian làm việc (Workspace) chuẩn Desk tích hợp:
  * **Lead Conversion Funnel**: Tỷ lệ chuyển đổi Lead -> Contact qua các nguồn tiếp cận.
  * **Sales Pipeline Chart**: Tổng giá trị cơ hội phân bổ theo từng giai đoạn.
  * **Membership Overview Number Cards**: Số thẻ Active, Số thẻ sắp hết hạn trong tháng, Doanh thu thẻ.
  * **Retention & At-Risk List**: Danh sách thú cưng cần gọi chăm sóc khẩn cấp trong ngày.
