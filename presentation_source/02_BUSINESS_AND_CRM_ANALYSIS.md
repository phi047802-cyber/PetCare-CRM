# PETCARE CRM — PHÂN TÍCH NGHIỆP VỤ & VÒNG ĐỜI KHÁCH HÀNG (BUSINESS & CRM ANALYSIS)

> **Mã hồ sơ**: `ANALYSIS-BUSINESS-2026`  
> **Dự án**: PetCare CRM (Quản lý Quan hệ Khách hàng Dịch vụ Chăm sóc Thú cưng)  
> **Góc nhìn phân tích**: Senior CRM Solution Architect & Business Analyst  
> **Ngày lập hồ sơ**: 07/11/2026  

---

## 1. BỐI CẢNH DOANH NGHIỆP & CASE STUDY NGHIỆP VỤ

### 1.1. Mô hình tổ chức vận hành
PetCare CRM được thiết kế nhằm phục vụ mô hình **Chuỗi phòng khám thú y kết hợp Spa & Khách sạn thú cưng** tại các đô thị lớn. Doanh nghiệp vận hành theo mô hình chuỗi tập trung với các đặc điểm:
* **Hội sở trung tâm & Chi nhánh vận hành**: Quản trị dữ liệu khách hàng, chính sách giá và cấu hình gói hội viên tập trung tại máy chủ trung tâm; vận hành tiếp đón và cung cấp dịch vụ phân tán tại các cơ sở chi nhánh (`CN-TRUNGTAM`, `CN-QUAN1`, `CN-THUDUC`, `CN-BINHTHANH`).
* **Mô hình doanh thu hỗn hợp**:
  1. *Dịch vụ lẻ theo lần ghé*: Khám bệnh, điều trị nội/ngoại trú, tiêm phòng vắc-xin, tắm sấy vệ sinh, cắt tỉa tạo kiểu lông móng.
  2. *Dịch vụ trả trước & Hội viên dài hạn*: Gói chăm sóc định kỳ 6 tháng – 1 năm (Bạc, Vàng, Kim Cương VIP), thu tiền trước và cam kết quyền lợi miễn phí hoặc giảm giá.
  3. *Bán lẻ sản phẩm phụ trợ*: Thức ăn dinh dưỡng, phụ kiện thú cưng, thuốc thú y theo toa.

### 1.2. Thách thức cốt lõi của ngành dịch vụ thú cưng
Khác với các ngành bán lẻ hoặc dịch vụ thông thường, quản trị quan hệ khách hàng trong ngành thú cưng mang những nét đặc thù rất rõ rệt:
* **Mối liên kết tình cảm sâu sắc (Emotional Bond)**: Thú cưng được xem như thành viên trong gia đình ("con cưng / boss"). Chủ nuôi sẵn sàng chi trả cao nếu cảm nhận được sự quan tâm chân thành và dịch vụ chuyên nghiệp, nhưng cũng cực kỳ nhạy cảm và dễ rời bỏ nếu thú cưng gặp sự cố y tế hoặc nhân viên thiếu chu đáo.
* **Bài toán Hộ gia đình Đa Thú Cưng (Multi-Pet Household)**: Khoảng 40% khách hàng nuôi từ 2 thú cưng trở lên (ví dụ: vừa nuôi chó vừa nuôi mèo, hoặc nuôi 2 chú chó khác giống). Mỗi bé có thể trạng, ngày sinh, lịch tiêm phòng và thói quen sinh hoạt khác nhau. CRM thông thường quản lý theo đầu người (`Contact`) sẽ làm mất dấu hồ sơ y bạ của từng thú cưng.
* **Tính chu kỳ lặp lại mang tính bắt buộc sinh học**: Da lông thú cưng liên tục phát triển và tuyến mùi hôi tích tụ theo thời gian. Sau 2–4 tuần, thú cưng bắt buộc phải được tắm vệ sinh và chải chuốt. Nếu phòng khám không chủ động nhắc hẹn, khách hàng sẽ trì hoãn hoặc ghé cơ sở spa đối thủ gần nhà hơn.

---

## 2. CHÂN DUNG NGƯỜI DÙNG & MA TRẬN VAI TRÒ (PERSONAS & ACTORS)

| STT | Tên Vai Trò (Role ID) | Tên Chức Danh Thực Tế | Mục Tiêu & Trách Nhiệm Chính | Nỗi Đau Hàng Ngày Cần CRM Giải Quyết |
|:---:|---|---|---|---|
| **1** | `PetCare Front Desk` | Nhân viên Lễ tân & Thu ngân | Tiếp đón khách hàng tại quầy; tra cứu nhanh lịch sử khách hàng và bé; cấn trừ quyền lợi thẻ hội viên; xuất hóa đơn và thu tiền. | Khách đông phải chờ đợi; mất thời gian lật sổ tìm thông tin thẻ; sợ tính nhầm tiền hoặc trừ trùng thẻ khi khách có nhiều bé. |
| **2** | `PetCare Veterinarian` | Bác sĩ Thú y Chuyên khoa | Khám lâm sàng, chẩn đoán, kê đơn, tiêm phòng và ghi nhận hồ sơ y bạ điện tử của từng thú cưng. | Không có lịch sử tiêm chủng và bệnh lý cũ; không theo dõi được biến thiên cân nặng của bé giữa các lần ghé. |
| **3** | `PetCare Groomer` | Kỹ thuật viên Spa & Làm đẹp | Thực hiện dịch vụ tắm sấy, cắt tỉa lông móng; ghi nhận thể trạng thực tế và phản ứng tâm lý của bé. | Không biết trước thói quen, điểm nhạy cảm hoặc bệnh ngoài da của bé để phục vụ nhẹ nhàng, tránh làm bé hoảng sợ. |
| **4** | `PetCare Sales` | Nhân viên Bán hàng & CSKH | Tiếp nhận Lead đa kênh; gọi điện tư vấn nhu cầu; quản lý cơ hội chốt hợp đồng các gói hội viên giá trị cao. | Lead bị bỏ quên quá 24h; không biết nguồn khách từ đâu hiệu quả; không có công cụ theo dõi phễu bán hàng (Pipeline). |
| **5** | `PetCare Manager` | Quản lý Phòng khám / Chi nhánh | Giám sát vận hành toàn cơ sở; duyệt bảng giá và chính sách ưu đãi; điều phối nhân sự và xử lý khiếu nại dịch vụ. | Báo cáo doanh thu chậm trễ; không kiểm soát được tình trạng khiếu nại quá hạn SLA; thất thoát doanh thu từ thẻ trả trước. |
| **6** | `PetCare Analyst` | Chuyên viên Phân tích Quản trị | Đọc hiểu 8 chỉ số KPI; phân tích tỷ lệ giữ chân khách hàng; so sánh hiệu quả kinh doanh giữa các chi nhánh. | Dữ liệu bị phân mảnh giữa các chi nhánh; thiếu công thức phân bổ giá thành chính xác và không đo lường được giá trị vòng đời CLV. |
| **7** | `PetCare Customer Portal` | Khách hàng / Chủ nuôi thú cưng | Tra cứu hồ sơ y bạ và cân nặng của bé; kiểm tra số dư thẻ hội viên; đặt lịch hẹn dịch vụ trực tuyến. | Mất sổ tiêm giấy; không nhớ ngày cần tiêm phòng nhắc lại; không biết gói thẻ hội viên đã mua còn lại bao nhiêu buổi. |

---

## 3. HÀNH TRÌNH VÒNG ĐỜI KHÁCH HÀNG TOÀN DIỆN (CUSTOMER LIFECYCLE)

Vòng đời khách hàng trong PetCare CRM được chuẩn hóa thành **9 giai đoạn nối tiếp**, đảm bảo không có điểm đứt gãy thông tin giữa các phòng ban:

```
[ SƠ ĐỒ HÀNH TRÌNH VÒNG ĐỜI KHÁCH HÀNG PETCARE CRM ]

 (1) THU HÚT LEAD ────────► (2) TƯ VẤN & BÁN HÀNG ────────► (3) CHUYỂN ĐỔI 360
   • Web Form / Hotline        • Sales Pipeline Kanban        • Tạo Contact & Pet
   • Honeypot Bot Trap         • Qualified / Unqualified      • Chống gộp trùng SĐT
            │                              │                             │
            ▼                              ▼                             ▼
 (4) ĐẶT HẸN & TIẾP ĐÓN ───► (5) THỰC HIỆN DỊCH VỤ ──────► (6) QUYẾT TOÁN & THẺ
   • Lịch hẹn Appointment      • Khám lâm sàng & Cân nặng     • Cấn trừ thẻ (Row Lock)
   • Check-in tại quầy POS     • Thao tác Spa / Grooming      • VietQR / Webhook IPN
            │                              │                             │
            ▼                              ▼                             ▼
 (7) HẬU MÃI & RECOVERY ───► (8) CHĂM SÓC THEO CHU KỲ ────► (9) GIA HẠN HỘI VIÊN
   • Khiếu nại PetCare Case    • Thuật toán EWMA + IQR        • Cảnh báo hết hạn (7d)
   • Quản trị SLA xử lý        • Due Soon / At Risk Alert     • Rollover bảo lưu lượt
```

### Chi tiết từng giai đoạn trong Customer Lifecycle:

#### Giai đoạn 1: Tiếp nhận Khách hàng Tiềm năng Đa Kênh (Lead Intake)
* **Actor chịu trách nhiệm**: Khách hàng (điền form) & Hệ thống tiếp nhận.
* **Trigger / Điều kiện bắt đầu**: Khách hàng điền form đăng ký tư vấn trên Website/Landing Page hoặc gọi điện lên Hotline.
* **Dữ liệu đầu vào**: Họ tên, Số điện thoại, Email, Thông tin ban đầu về thú cưng (loài, giống, nhu cầu), trường ẩn Honeypot (`hp_field`).
* **Hệ thống xử lý**:
  * Kiểm tra Honeypot: Nếu `hp_field` có giá trị ➔ Xác định là Bot tự động, âm thầm loại bỏ, không ghi CSDL.
  * Chuẩn hóa số điện thoại Việt Nam: Chuyển đổi các định dạng `0901234567`, `+84901234567` về chuẩn `84901234567`.
  * Khởi tạo bản ghi `PetCare Lead` ở trạng thái `New`.
* **Business Rule**: Số điện thoại bắt buộc phải đúng định dạng viễn thông Việt Nam (10 chữ số hợp lệ); Họ tên không được để trống.
* **Kết quả / Record tạo ra**: Bản ghi `PetCare Lead` (mã `LEAD-YYYY-#####`).
* **Bộ phận tiếp nhận tiếp theo**: Phòng Kinh doanh / Telesales (`PetCare Sales`).
* **Tự động hóa vs Thủ công**: Tự động hóa 100% khâu tiếp nhận, chuẩn hóa SĐT và bẫy spam; phân công Lead cho nhân viên bán hàng.

#### Giai đoạn 2: Đánh giá Nhu cầu & Quản lý Phễu Cơ hội (Sales Pipeline & Qualification)
* **Actor chịu trách nhiệm**: Nhân viên Bán hàng (`PetCare Sales`).
* **Trigger**: Bản ghi Lead mới xuất hiện trên Desk UI hoặc tác vụ nền cảnh báo Lead chưa liên hệ sau 24h.
* **Dữ liệu đầu vào**: Hồ sơ Lead, thông tin cuộc gọi tư vấn, nhu cầu gói dịch vụ hoặc dịch vụ lẻ.
* **Hệ thống xử lý**:
  * Nhân viên gọi điện tư vấn, ghi lại lịch sử tương tác qua API `add_lead_interaction`.
  * Nếu khách hàng không có nhu cầu: Đổi trạng thái sang `Unqualified`, bắt buộc nhập `unqualified_reason`.
  * Nếu khách có nhu cầu: Đổi trạng thái sang `Qualified`. Nếu khách quan tâm đến các gói thẻ hội viên giá trị cao, tạo bản ghi `PetCare Opportunity` đưa vào phễu Kanban.
* **Business Rule**: Chuyển giai đoạn Opportunity tự động cập nhật xác suất thành công (Prospecting 10% ➔ Closed Won 100%); Đóng mất Deal (`Closed Lost`) bắt buộc phải ghi nhận nguyên nhân thất bại (`lost_reason`).
* **Kết quả tạo ra**: Cập nhật trạng thái Lead; bản ghi `PetCare Opportunity` (mã `OPP-YYYY-#####`).
* **Bộ phận tiếp nhận tiếp theo**: Quầy lễ tân hoặc Tiếp tục chăm sóc phễu.

#### Giai đoạn 3: Chuyển đổi Lead & Thiết lập Hồ sơ Khách hàng 360 (Conversion & Profiling)
* **Actor chịu trách nhiệm**: Nhân viên Bán hàng (`PetCare Sales`) hoặc Lễ tân.
* **Trigger**: Thao tác bấm nút "Chuyển Đổi Lead" (Convert Lead) trên Desk Form hoặc gọi API `convert_lead_to_customer`.
* **Dữ liệu đầu vào**: ID của bản ghi Lead đã Qualified.
* **Hệ thống xử lý**:
  * Kiểm tra đối soát khử trùng lặp (Deduplication): Truy vấn xem số điện thoại của Lead đã tồn tại trong bảng `Contact` hay chưa.
  * Nếu Contact đã tồn tại: Liên kết Lead với Contact cũ, tạo mới hồ sơ thú cưng `Pet` thuộc sở hữu của Contact đó.
  * Nếu Contact chưa tồn tại: Tạo bản ghi `Contact` mới, tạo bản ghi `Pet` mới gắn với Contact.
  * Đổi trạng thái Lead thành `Converted`, đóng liên kết. Toàn bộ chuỗi thao tác được bọc trong một giao dịch cơ sở dữ liệu ACID (Atomic Transaction).
* **Business Rule**: Không bao giờ được tạo 2 Contact có cùng số điện thoại; Một Contact có quyền sở hữu từ 1 đến nhiều thú cưng ($1:N$).
* **Kết quả tạo ra**: Bản ghi `Contact`, bản ghi `Pet` (mã `PET-YYYY-#####`), cập nhật `PetCare Lead` thành `Converted`.
* **Bộ phận tiếp nhận tiếp theo**: Lễ tân quầy dịch vụ (`PetCare Front Desk`).

#### Giai đoạn 4: Đặt Lịch Hẹn & Tiếp Đón Tại Quầy (Appointment & Check-in)
* **Actor chịu trách nhiệm**: Chủ nuôi (qua Cổng Web Portal) hoặc Lễ tân (tại quầy / qua điện thoại).
* **Trigger**: Khách hàng chủ động đặt lịch trước hoặc đưa thú cưng trực tiếp đến phòng khám.
* **Dữ liệu đầu vào**: Khách hàng, Thú cưng, Loại dịch vụ, Chi nhánh, Ngày & Giờ hẹn.
* **Hệ thống xử lý**:
  * Tạo lịch hẹn trong DocType `PetCare Appointment` ở trạng thái `Scheduled`.
  * Khi khách hàng có mặt tại phòng khám, Lễ tân thực hiện thao tác **Check-in một chạm**.
  * Hệ thống tự động chuyển trạng thái lịch hẹn thành `Checked-In` và tự động khởi tạo sẵn một phiếu dịch vụ `Service Visit` tương ứng.
* **Business Rule**: Không được đặt lịch trong quá khứ; Kiểm tra quyền sở hữu giữa khách hàng và thú cưng trước khi đặt.
* **Kết quả tạo ra**: Bản ghi `PetCare Appointment` (mã `APT-YYYY-#####`) và phiếu nháp `Service Visit`.
* **Bộ phận tiếp nhận tiếp theo**: Bác sĩ / Kỹ thuật viên Spa (`PetCare Specialist`).

#### Giai đoạn 5: Thực hiện Chuyên môn & Cập nhật Sinh học (Service Delivery & Health Log)
* **Actor chịu trách nhiệm**: Bác sĩ Thú y (`PetCare Veterinarian`) hoặc Kỹ thuật viên Spa (`PetCare Groomer`).
* **Trigger**: Tiếp nhận thú cưng từ quầy lễ tân sau khi đã check-in.
* **Dữ liệu đầu vào**: Phiếu `Service Visit`, tình trạng thể chất của bé.
* **Hệ thống xử lý**:
  * Cân trọng lượng lâm sàng của bé và kiểm tra da lông, tai móng.
  * Thực hiện dịch vụ kỹ thuật (Tắm sấy, Cắt tỉa, Tiêm chủng, Điều trị).
  * Ghi nhận cân nặng mới và ghi chú phản ứng của bé vào phiếu `Service Visit`.
  * Cân nặng mới tự động đồng bộ vào trường `weight_kg` trên hồ sơ gốc của thú cưng `Pet`.
* **Business Rule**: Trọng lượng thú cưng phải là số dương hợp lệ ($> 0$ kg).
* **Kết quả tạo ra**: Cập nhật thông số kỹ thuật trên `Service Visit` và `Pet`.
* **Bộ phận tiếp nhận tiếp theo**: Quầy Thu ngân / Lễ tân.

#### Giai đoạn 6: Quyết toán, Cấn trừ Thẻ Hội viên & Thanh toán VietQR (Billing & Payments)
* **Actor chịu trách nhiệm**: Lễ tân / Thu ngân (`PetCare Front Desk`) & Hệ thống thanh toán.
* **Trigger**: Thú cưng hoàn thành dịch vụ, khách hàng đến quầy làm thủ tục nhận lại bé và thanh toán.
* **Dữ liệu đầu vào**: Phiếu `Service Visit`, phương thức thanh toán (Tiền mặt, VietQR, Ví thẻ hội viên).
* **Hệ thống xử lý**:
  * **Trường hợp có Thẻ hội viên (`Customer Membership`)**:
    * Hệ thống kích hoạt khóa dòng Pessimistic Row Lock (`FOR UPDATE`) trên bản ghi thẻ để chống race condition.
    * Kiểm tra quyền lợi còn lại (`remaining_quantity`). Nếu dịch vụ được miễn phí 100%, trừ 1 lượt quyền lợi, giảm tiền `final_price = 0`, ghi nhật ký Sổ cái kiểm toán `Benefit Redemption Ledger`.
    * Nếu dịch vụ được giảm giá %, tính toán số tiền chiết khấu và trừ vào số dư ví thẻ nếu khách chọn thanh toán bằng ví.
  * **Trường hợp thanh toán chuyển khoản VietQR**:
    * Hệ thống tự động phát sinh mã VietQR Napas247 động gắn cú pháp `PC-SVC-{visit_id}` và số tiền thực thu.
    * Khách hàng quét mã trên ứng dụng ngân hàng.
    * Khi ngân hàng biến động số dư, Webhook IPN bắn về CRM, xác thực chữ ký HMAC-SHA256, kiểm tra chống gửi lại (Replay Guard) và tự động gạch nợ phiếu dịch vụ thành `Completed`.
* **Business Rule**: Số dư ví và số lượt quyền lợi không bao giờ được phép âm; Khóa tranh chấp đồng thời bắt buộc phải có; Sai lệch số tiền webhook sẽ bị từ chối.
* **Kết quả tạo ra**: Phiếu `Service Visit` chuyển trạng thái `Completed`; Bản ghi `Benefit Redemption Ledger` (mã `BRL-YYYY-#####`); Bản ghi `Membership Transaction` (nếu có trừ tiền ví).
* **Bộ phận tiếp nhận tiếp theo**: Bàn giao thú cưng cho chủ nuôi và chuyển sang chu trình theo dõi sau dịch vụ.

#### Giai đoạn 7: Chăm sóc Sau Dịch vụ & Phục hồi Sự cố (After-Service Care & Service Recovery)
* **Actor chịu trách nhiệm**: Nhân viên CSKH & Quản lý phòng khám (`PetCare Manager`).
* **Trigger**: Khách hàng phản hồi sự cố (ví dụ: bé bị hoảng khi sấy lồng, cắt móng sát tủy) hoặc gọi điện hỏi tư vấn dinh dưỡng sau khám.
* **Dữ liệu đầu vào**: Khách hàng, Thú cưng, Phiếu dịch vụ liên quan, Nội dung phản ánh, Mức độ ưu tiên.
* **Hệ thống xử lý**:
  * Khởi tạo bản ghi `PetCare Case` ở trạng thái `Open`.
  * Tác vụ nền hàng giờ (`hourly_workflow_check`) giám sát thời gian xử lý: Nếu Case mức độ High/Urgent bị bỏ quên quá hạn cam kết SLA, hệ thống gửi cảnh báo đến Quản lý phòng khám.
  * Nhân viên liên hệ xin lỗi, tặng voucher đền bù và ghi nhận phương án giải quyết vào trường `resolution`.
* **Business Rule**: Case giải quyết xong chuyển trạng thái `Resolved` hoặc `Closed` bắt buộc phải có ghi chú xử lý.
* **Kết quả tạo ra**: Bản ghi `PetCare Case` (mã `CASE-YYYY-#####`).
* **Bộ phận tiếp nhận tiếp theo**: Đưa khách hàng trở lại chu trình chăm sóc định kỳ.

#### Giai đoạn 8: Phân tích Chu kỳ Chăm sóc & Nhắc Lịch Tự Động (Care Intelligence & Retention)
* **Actor chịu trách nhiệm**: Động cơ Trí tuệ Chăm sóc (`Care Engine`) & Nhân viên CSKH.
* **Trigger**: Tác vụ quét nền định kỳ hàng ngày (`daily_petcare_scan`) chạy vào ban đêm.
* **Dữ liệu đầu vào**: Toàn bộ lịch sử các lần ghé `Service Visit` của tất cả thú cưng trong hệ thống.
* **Hệ thống xử lý**:
  * Với mỗi thú cưng có từ 2 lần ghé trở lên:
    * Tính toán các khoảng cách giữa các lần ghé liên tiếp (Visit Intervals).
    * Nếu lịch sử $\ge 4$ lần: Áp dụng thuật toán **Tukey IQR** để loại bỏ các điểm ngoại lai bất thường ($[Q_1 - 1.5 \times IQR, Q_3 + 1.5 \times IQR]$).
    * Áp dụng công thức **Trung bình động hàm mũ (EWMA, $\alpha=0.6$)** để tính chu kỳ chuẩn $C_{ewma}$.
    * Nhân với hệ số biến thiên Mùa vụ (tháng 3–8 rút ngắn chu kỳ vì thời tiết nóng bức) và Độ tuổi (thú cưng dưới 1 tuổi cần tắm thường xuyên hơn).
  * So sánh với số ngày kể từ lần ghé gần nhất ($D_{last}$):
    * Nếu ngày dự kiến còn cách $\le 3$ ngày ➔ Phân loại `DUE_SOON` (Sắp đến hạn).
    * Nếu $D_{last} \ge 1.5 \times C_{ewma}$ ➔ Phân loại `AT_RISK` (Khách hàng có nguy cơ rời bỏ).
  * Tạo bản ghi `Care Recommendation` và tự động sinh công việc ToDo gán cho nhân viên CSKH; điều phối tin nhắn Zalo ZNS / SMS nhắc lịch (ở chế độ Safe Mode Outbox).
* **Business Rule**: Cơ chế lọc chống làm phiền (Anti-spam Gating): Không tạo đề xuất trùng lặp trong vòng 7 ngày cho cùng một thú cưng và cùng loại dịch vụ.
* **Kết quả tạo ra**: Bản ghi `Care Recommendation` (mã `REC-YYYY-#####`) và các nhiệm vụ `ToDo`.
* **Bộ phận tiếp nhận tiếp theo**: Nhân viên CSKH liên hệ khách hàng để đặt lịch tái khám (quay lại Giai đoạn 4).

#### Giai đoạn 9: Cảnh báo Hết hạn Thẻ & Tái Tục Quyền Lợi (Membership Renewal & Rollover)
* **Actor chịu trách nhiệm**: Tác vụ nền Scheduler & Nhân viên Bán hàng / CSKH.
* **Trigger**: Tác vụ nền hàng ngày quét các thẻ hội viên có `end_date` sắp đến hạn trong vòng 7 ngày.
* **Dữ liệu đầu vào**: Thẻ hội viên đang hoạt động (`status = 'Active'`).
* **Hệ thống xử lý**:
  * Tự động khởi tạo đề xuất chăm sóc loại `RENEWAL` cảnh báo thẻ sắp hết hạn.
  * Nếu quá ngày `end_date` mà khách chưa gia hạn: Hệ thống tự động chuyển trạng thái thẻ thành `Expired`.
  * Khi khách hàng đồng ý gia hạn: Nhân viên gọi API `renew_membership` với cờ `allow_rollover=1`. Hệ thống tạo thẻ hội viên mới, tự động kế thừa toàn bộ số lượt dịch vụ chưa dùng hết của thẻ cũ sang thẻ mới (Benefit Rollover), và đổi trạng thái thẻ cũ thành `Renewed`.
* **Business Rule**: Thẻ hết hạn không được tiếp tục cấn trừ quyền lợi; Thao tác Rollover chỉ áp dụng khi khách hàng mua gói mới trước hoặc ngay tại thời điểm gia hạn.
* **Kết quả tạo ra**: Bản ghi `Customer Membership` mới, đóng thẻ cũ thành `Renewed`.
* **Bộ phận tiếp nhận tiếp theo**: Duy trì vòng đời khách hàng trung thành dài hạn.

---

## 4. BẢNG MA TRẬN PHÂN HỆ VÀ GIÁ TRỊ NGHIỆP VỤ (MODULE & BUSINESS VALUE MATRIX)

| Phân Hệ / Năng Lực | Vấn Đề Nghiệp Vụ Cần Giải Quyết | Đối Tượng Sử Dụng | Chức Năng Đã Xác Minh (Verified Code) | Dữ Liệu Tạo Ra / Cập Nhật | Bằng Chứng Kiểm Chứng | Trạng Thái Triển Khai |
|---|---|---|---|---|---|:---:|
| **1. Quản lý Lead & Phễu Bán Hàng** | Bỏ sót khách tiềm năng; dữ liệu trùng lặp số điện thoại; phễu bán hàng mơ hồ. | Nhân viên Sales, Telesales, Quản lý | • Chuẩn hóa SĐT Việt Nam (+84, 09x)<br>• Bẫy bot Honeypot trên Lead Form<br>• Khử trùng lặp Contact<br>• Quản lý Pipeline Kanban 6 giai đoạn | `PetCare Lead`<br>`Contact`<br>`Pet`<br>`PetCare Opportunity` | `lead_service.py`<br>`sales_pipeline_service.py`<br>Suite 1, Suite 9 | `VERIFIED` |
| **2. Hồ Sơ Thú Cưng & Dịch Vụ** | Mất dấu hồ sơ y tế; không theo dõi được diễn tiến cân nặng của thú cưng. | Lễ tân, Bác sĩ thú y, Kỹ thuật viên | • Quản lý gia đình đa thú cưng ($1:N$)<br>• Danh mục bảng giá chuẩn<br>• Tự động cập nhật cân nặng sau khám<br>• Check-in lịch hẹn một chạm | `Pet`<br>`PetCare Service`<br>`Service Visit`<br>`PetCare Appointment` | `service_operations.py`<br>`pet.json`<br>Suite 2, Suite 10 | `VERIFIED` |
| **3. Thẻ Hội Viên & Sổ Cái Quyền Lợi** | Thất thoát tài chính từ thẻ trả trước; nhân viên bấm nhầm gây trừ âm hoặc trừ trùng lặp. | Thu ngân, Lễ tân, Quản lý chi nhánh | • Cấn trừ quyền lợi 100% FREE hoặc %<br>• Khóa dòng `FOR UPDATE` chống race condition<br>• Khóa Idempotency chống double-redeem<br>• Rollover bảo lưu lượt tồn khi gia hạn | `Customer Membership`<br>`Membership Plan`<br>`Benefit Redemption Ledger`<br>`Membership Transaction` | `membership_service.py`<br>`api.py` (L180)<br>Suite 3 | `VERIFIED` |
| **4. Trí Tuệ Chăm Sóc & Giữ Chân** | Khách hàng quên lịch chăm sóc; phòng khám bị động để mất khách vào tay đối thủ. | Nhân viên CSKH, Quản lý phòng khám | • Thuật toán thống kê EWMA ($\alpha=0.6$)<br>• Lọc ngoại lai Tukey IQR<br>• Hệ số mùa vụ và độ tuổi<br>• Phân loại Due Soon & At Risk<br>• Khử trùng lặp đề xuất 7 ngày | `Care Recommendation`<br>`ToDo` | `care_pattern_service.py`<br>`recommendation_service.py`<br>Suite 4, Suite 8 | `VERIFIED` |
| **5. Cổng Thanh Toán & Webhook IPN** | Thu ngân gõ sai tiền chuyển khoản; mất thời gian kiểm tra ứng dụng ngân hàng khi đông khách. | Khách hàng, Thu ngân, Kế toán | • Sinh mã VietQR Napas247 động<br>• Webhook ngân hàng kiểm tra chữ ký HMAC-SHA256<br>• Tự động gạch nợ phiếu hoặc nạp ví<br>• Chống tấn công Replay Attack | `Service Visit` (Completed)<br>`Membership Transaction` | `payment_gateway.py`<br>`api.py` (L4030)<br>Suite 8 (Tests 5,6,7) | `VERIFIED` |
| **6. Cổng Tự Phục Vụ Chủ Nuôi (Portal)** | Khách hàng mất sổ tiêm phòng giấy; không biết thẻ hội viên còn bao nhiêu lượt. | Chủ nuôi thú cưng (Pet Owner) | • Tra cứu sổ khám bệnh & cân nặng điện tử<br>• Kiểm tra số dư ví & quyền lợi thẻ<br>• Đặt lịch hẹn trực tuyến<br>• Bảo vệ BOLA/IDOR bằng Signed Token | `PetCare Appointment`<br>`PetCare Case` | `api.py` (L4150-4350)<br>Suite 8, Suite 10 | `VERIFIED` |
| **7. Báo Cáo & Phân Tích Quản Trị** | Không có tầm nhìn số liệu kinh doanh; không so sánh được hiệu quả giữa các chi nhánh. | Quản lý chuỗi, Giám đốc, Chuyên viên phân tích | • Báo cáo 8 KPI chuẩn trên Desk UI<br>• Phân tích đối sánh doanh thu 4 chi nhánh<br>• Mô hình phân bổ giá thành ABC<br>• Định giá trị vòng đời khách hàng CLV | Script Report `petcare_kpi_overview`<br>`CLV_ABC_Model.xlsx` | `analytics_service.py`<br>Suite 6<br>Mô hình Excel | `VERIFIED` (Hệ thống) / `SIMULATION` (CLV/ABC) |

---

## 5. PHÂN QUYỀN, VAI TRÒ & KIỂM SOÁT BẢO MẬT (SECURITY CONTROLS)

Hệ thống phân quyền được bảo vệ theo **3 lớp phòng vệ độc lập**:

```
                              ┌────────────────────────────────────────┐
                              │       3 LỚP PHÒNG VỆ BẢO MẬT           │
                              └───────────────────┬────────────────────┘
                                                  │
         ┌────────────────────────────────────────┼────────────────────────────────────────┐
         │                                        │                                        │
         ▼                                        ▼                                        ▼
┌──────────────────┐                    ┌──────────────────┐                    ┌──────────────────┐
│ LỚP 1: RBAC ORM  │                    │ LỚP 2: BACKEND   │                    │ LỚP 3: CROSS-    │
│  (Frappe DocPerm)│                    │  TOKEN & SESSIONS│                    │  TENANT ISOLATION│
├──────────────────┤                    ├──────────────────┤                    ├──────────────────┤
│ Phân quyền CRUD  │                    │ Phân biệt Guest  │                    │ Ngăn chặn BOLA / │
│ trên từng DocType│                    │ và User có Token │                    │ IDOR khách hàng  │
│ cho 7 Roles      │                    │ Header / Cookie  │                    │ và thú cưng      │
└──────────────────┘                    └──────────────────┘                    └──────────────────┘
```

1. **Lớp 1: Ma trận Phân quyền Frappe ORM (Document Permissions)**:
   * Được khai báo qua schema JSON và Fixtures tại [`hooks.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/hooks.py) và tự động khởi tạo qua [`install.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/setup/install.py).
   * Phân quyền chi tiết quyền Đọc (Read), Tạo (Create), Sửa (Write), Xóa (Delete) và Báo cáo (Report) cho từng vai trò nghiệp vụ. Ví dụ: Kỹ thuật viên Groomer chỉ được đọc thông tin thú cưng và cập nhật cân nặng, không có quyền xóa thẻ hội viên hay sửa bảng giá dịch vụ.
2. **Lớp 2: Kiểm soát Truy cập Tầng API (Whitelisted Security & Session Guards)**:
   * Toàn bộ 53 endpoints trong [`api.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/api.py) được kiểm soát đăng nhập.
   * Các endpoint nhạy cảm (như duyệt thẻ, tạo bảng giá, gạch nợ) bắt buộc phải có phiên đăng nhập của nhân viên có vai trò phù hợp (`PetCare Manager`, `PetCare Sales`, `PetCare Front Desk`).
   * Các endpoint công khai (`allow_guest=True`) phục vụ Webhook và Portal đều được áp dụng cơ chế bảo vệ bổ sung: Rate Limiting, bẫy Honeypot, xác thực chữ ký HMAC-SHA256, hoặc kiểm tra Signed Portal Token.
3. **Lớp 3: Kiểm soát Sở hữu Chéo & Chống Tấn công BOLA / IDOR (Cross-Tenant Isolation)**:
   * Hàm `validate_cross_entity_relationship(customer_id, pet_id)` trong [`security.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/utils/security.py) kiểm tra bắt buộc thú cưng phải thuộc sở hữu của khách hàng đó trong CSDL trước khi cho phép xem sổ y bạ hoặc đặt lịch.
   * Hàm `_verify_owner_portal_access` trong [`api.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/api.py#L4150) kiểm tra chữ ký Token gắn riêng cho từng khách hàng, ngăn chặn hành vi thay đổi `customer_id` trên URL để xem trộm hồ sơ người khác.
