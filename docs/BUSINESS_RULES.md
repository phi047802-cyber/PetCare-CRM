# QUY TẮC NGHIỆP VỤ HỆ THỐNG (BUSINESS RULES & DOMAIN INVARIANTS)

> **Dự án**: PetCare CRM (CRM Toàn Diện Dịch Vụ Thú Cưng)  
> **Nền tảng**: Frappe Framework v15  
> **Phiên bản tài liệu**: 2.0 (Prompt 10 Final Release)  

---

## 1. Phân Hệ Tiếp Thị & Bán Hàng (CRM Core)

### 1.1. Chuẩn Hóa Số Điện Thoại & Chống Trùng Khách Hàng (Deduplication)
* **Quy chuẩn số điện thoại**: Mọi số điện thoại nhập vào hệ thống bắt buộc qua chuẩn hóa Regex `^(03|05|07|08|09)\d{8}$` (10 chữ số di động Việt Nam). Mọi tiền tố `+84`, `84` hoặc khoảng trắng/dấu gạch nối đều được loại bỏ tự động.
* **Quy tắc gộp trùng (Customer Deduplication Invariant)**:
  * Khi chuyển đổi Lead, việc đối soát khách hàng hiện hữu **CHỈ ĐƯỢC PHÉP** dựa trên **Số điện thoại** hoặc **Email**.
  * **TUYỆT ĐỐI NGHIÊM CẤM** tự động gộp khách hàng chỉ vì trùng họ tên (`first_name`, `last_name`). Trùng tên nhưng khác số điện thoại/email bắt buộc tạo bản ghi khách hàng (`Contact`) độc lập mới.
* **Bảo toàn lịch sử giao tiếp**: Toàn bộ ghi chú, cuộc gọi (`Communication`) phát sinh ở giai đoạn Lead phải được liên kết chuyển tiếp sang hồ sơ `Contact` sau khi chuyển đổi.

### 1.2. Vòng Đời Cơ Hội Bán Hàng (PetCare Opportunity)
* **Các giai đoạn chuẩn (Sales Stages)**: `Prospecting` (10%) $\rightarrow$ `Qualification` (20%) $\rightarrow$ `Proposal` (60%) $\rightarrow$ `Negotiation` (80%) $\rightarrow$ `Closed Won` (100%) hoặc `Closed Lost` (0%).
* **Giá trị kỳ vọng có trọng số (Weighted Expected Value)**:
  $$\text{Weighted Value} = \text{Opportunity Amount} \times \frac{\text{Probability}}{100}$$
* **Lý do thất bại**: Khi chuyển sang trạng thái `Closed Lost`, trường `lost_reason` là bắt buộc.

---

## 2. Phân Hệ Thú Cưng & Vận Hành Dịch Vụ (PetCare Domain & Operations)

### 2.1. Phân Định Chủ Thể & Thụ Hưởng (Customer vs Pet)
* **Khách hàng (`Contact`)**: Là chủ thể pháp lý ký hợp đồng, thanh toán và sở hữu thẻ hội viên. Một khách hàng có thể sở hữu từ 1 đến nhiều thú cưng (`Multi-pet`).
* **Thú cưng (`Pet`)**: Là đối tượng thụ hưởng dịch vụ thực tế. Mỗi bé có loài, giống, cân nặng và tiền sử dị ứng riêng.
* **Ràng buộc cách ly dịch vụ (Pet Isolation Invariant)**: Lịch sử dịch vụ và chu kỳ chăm sóc được tính toán riêng biệt cho từng cặp `(Pet, Service Type)`. Nghiêm cấm dùng lượt thăm của thú cưng này để tính chu kỳ cho thú cưng khác của cùng một khách hàng.

### 2.2. Kiểm Tra Quyền Sở Hữu Chéo (Cross-Entity Ownership Guard)
* **Khách hàng vs Thú cưng**: Khi tạo `Service Visit` hoặc `PetCare Case`, hàm `validate_cross_entity_relationship` bắt buộc xác thực:
  $$\text{Pet.customer} == \text{ServiceVisit.customer}$$
  Nghiêm cấm chọn thú cưng của khách hàng A nhưng xuất hóa đơn cho khách hàng B.
* **Khách hàng vs Thẻ hội viên**:
  $$\text{CustomerMembership.customer} == \text{ServiceVisit.customer}$$
  Nếu thẻ hội viên là gói cá nhân (`pet` có giá trị), bắt buộc $\text{CustomerMembership.pet} == \text{ServiceVisit.pet}$.

---

## 3. Phân Hệ Thẻ Hội Viên & Khấu Trừ Quyền Lợi (Membership & Loyalty)

### 3.1. Thứ Tự Áp Dụng Chiết Khấu & Sàn Giá (Pricing Invariants)
Thứ tự ưu tiên áp dụng quyền lợi khi tính giá dịch vụ:
1. **Quyền lợi miễn phí 100% (FREE Benefit)**: $\text{Discount} = \text{Original Price} \implies \text{Final Price} = 0\text{ VND}$.
2. **Quyền lợi giảm theo phần trăm (PERCENTAGE Discount)**: $\text{Discount} = \text{Original Price} \times \frac{\text{Discount Value}}{100}$.
3. **Quyền lợi giảm số tiền cố định (FIXED Discount)**: $\text{Discount} = \min(\text{Discount Value}, \text{Original Price})$.
4. **Giá niêm yết chuẩn (Normal Price)**: Khi không có thẻ hoặc quyền lợi tương ứng đã dùng hết.
* **Quy tắc sàn giá tuyệt đối (Non-Negative Price Floor)**:
  $$\text{Final Price} = \max(0.0, \text{Original Price} - \text{Discount Amount})$$
  Giá thanh toán cuối cùng không bao giờ được phép âm trong bất kỳ trường hợp nào.

### 3.2. An Toàn Giao Dịch & Trừ Quyền Lợi (Transaction Safety & Idempotency)
* **Khóa bi quan (Pessimistic Locking)**: Khi khấu trừ quyền lợi, bản ghi `Customer Membership` được khóa bằng cú pháp `SELECT ... FOR UPDATE` nhằm ngăn chặn hai quầy thu ngân cùng trừ 1 lượt dịch vụ cuối cùng (Race Condition).
* **Bảo vệ lặp lại Idempotency**: Trường `idempotency_key` trong `Benefit Redemption Ledger` đảm bảo nếu yêu cầu tạo phiếu dịch vụ được gửi lại do mạng chập chờn, hệ thống chỉ trả về kết quả đã ghi nhận trước đó, tuyệt đối không trừ lượt lần 2.
* **Gia hạn & Bảo lưu (Rollover Policy)**: Khi khách hàng gia hạn thẻ trước hoặc đúng hạn, số lượt dịch vụ chưa sử dụng trong thẻ cũ được cộng dồn (rollover) sang thẻ mới theo cấu hình `allow_rollover = True`. Lịch sử các giao dịch cũ không bị ghi đè.

---

## 4. Phân Hệ Trí Tuệ Chăm Sóc Khách Hàng (Care Intelligence & Retention)

> **Nguyên tắc nền tảng**: Toàn bộ thuật toán vận hành theo phương pháp **Rule-based & Thống kê học minh bạch**, không sử dụng hộp đen Machine Learning/Deep Learning nhằm bảo đảm tính giải thích được (Explainability).

### 4.1. Phân Tích Chu Kỳ & Lọc Ngoại Lai (IQR & EWMA)
* **Lọc ngoại lai (Interquartile Range - IQR)**: Với số lượt quan sát $\ge 4$, khoảng cách giữa các lần ghé thăm được lọc ngoại lai theo hàng rào Tukey:
  $$[\text{Lower Fence}, \text{Upper Fence}] = [Q_1 - 1.5 \times \text{IQR}, Q_3 + 1.5 \times \text{IQR}]$$
* **Trọng số chu kỳ gần nhất (EWMA)**: Áp dụng trung bình động hàm mũ với hệ số $\alpha = 0.6$:
  $$\text{EWMA}_t = \alpha \times \Delta_t + (1 - \alpha) \times \text{EWMA}_{t-1}$$

### 4.2. Dự Đoán Ngày Tái Khám & Độ Tin Cậy Định Tính
* **Công thức ngày dự kiến**:
  $$\text{Predicted Date} = \text{Last Visit Date} + \text{round}(\text{Typical Interval})$$
* **Độ tin cậy định tính (Qualitative Confidence)**:
  * 0 - 1 lượt: `NONE` / `INSUFFICIENT` (Chưa đủ căn cứ xác lập chu kỳ).
  * 2 - 3 lượt: `LOW` hoặc `MEDIUM` (Chu kỳ sơ bộ).
  * $\ge 4$ lượt: `HIGH` (Chu kỳ trưởng thành đã qua lọc IQR).
* **Miễn trừ trách nhiệm**: Mọi kết quả dự đoán đều kèm chú thích rõ ràng: *"Dự đoán mang tính chất tham khảo dựa trên tần suất lịch sử, không phải lịch hẹn đã xác nhận"*.

### 4.3. Phân Định Rủi Ro & Khử Trùng Lặp Khuyến Nghị
* **Sắp đến hạn (DUE_SOON)**:
  $$\text{Days Until Due} \le \text{Effective Threshold} \quad (\text{Threshold} = \min(3\text{ days}, 40\% \times \text{Interval}))$$
  *Đặc biệt: Thú cưng vừa ghé thăm trong ngày hôm nay KHÔNG BAO GIỜ bị tính là Due Soon.*
* **Có nguy cơ rời bỏ (AT_RISK)**:
  $$\text{Absence Ratio} = \frac{\text{Days Since Last Visit}}{\text{Typical Interval}} \ge 1.5 \quad \text{hoặc} \quad \text{Days Since Last Visit} \ge 90\text{ ngày}$$
* **Khử trùng lặp tại chỗ (In-Place Deduplication)**: Khi bộ lập lịch chạy định kỳ quét lại khách hàng đã có đề xuất mở (`New` hoặc `Contacted`), hệ thống thực hiện cập nhật tại chỗ (`UPDATED`), **tuyệt đối không sinh thêm bản ghi rác**.

---

## 5. Tự Động Hóa & An Toàn Tác Vụ Nền (Schedulers & Safe Mode)

1. **Idempotent ToDo Allocation**: Hàm `TaskManager.ensure_todo()` chỉ tạo nhiệm vụ công việc mới nếu chưa tồn tại nhiệm vụ trạng thái `Open` cho cùng đối tượng tham chiếu.
2. **Cổng giao tiếp Safe Mode**: Trong chế độ phát triển/demo (`ENABLE_LIVE_COMMUNICATION = False`), mọi email/thông báo đều được giả lập an toàn, ngăn ngừa việc gửi email thật ngoài ý muốn tới hòm thư người dùng thử nghiệm.
3. **Giám sát SLA Khiếu Nại (Service Recovery)**: Tự động phát hiện các khiếu nại (`PetCare Case`) trạng thái `Open` vượt quá 24h đối với mức Urgent hoặc 48h đối với mức High để kích hoạt nhiệm vụ leo thang (Escalation) cho Quản lý.
