# PetCare CRM v1.0 — Demo Cheat-sheet & Hướng Dẫn Thuyết Trình Kịch Bản
> **Thời lượng demo chuẩn**: 7 – 10 phút  
> **Cổng Giao Diện Web Lễ Tân & Bác Sĩ (Frontend)**: [http://localhost:8080/frontend](http://localhost:8080/frontend) (hoặc [http://localhost:8080/](http://localhost:8080/))  
> **Cổng Quản Trị Hệ Thống Frappe Desk**: [http://localhost:8080/app](http://localhost:8080/app)  
> **Tài khoản Administrator**: `Administrator` | Mật khẩu: `admin123`

---

## ⚡ BƯỚC KHỞI ĐỘNG (SETUP DỮ LIỆU SẠCH BAN ĐẦU)
Nếu trình diễn trên máy mới hoặc muốn reset dữ liệu sạch thuần Việt trước khi bắt đầu:
```powershell
.\deploy_clean.ps1
```
*Script tự động kiểm tra Docker, đồng bộ file, nạp dữ liệu chuẩn và chạy 22/22 unit tests.*

---

## 🌟 PHẦN 1: DEMO TRÊN CỔNG GIAO DIỆN (`http://localhost:8080/frontend`)
Giao diện được thiết kế theo chuẩn **Flat & Clinical Teal** chuyên nghiệp, tươi sáng, 100% không gradient, chia làm 3 không gian tác nghiệp rõ ràng:

---

### 🐶 KHÔNG GIAN 1: TRA CỨU KHÁCH HÀNG 360 (Tab 1: Tra Cứu Khách Hàng)

#### 1. Demo Nghiệp Vụ Hội Viên & Trừ Lượt An Toàn (Bé Bơ - Corgi)
1. Trong ô tìm kiếm, nhập số điện thoại: **`0901234567`** (hoặc gõ chữ **`Bơ`**) $\rightarrow$ Nhấn **"Tra cứu ngay"** (hoặc nhấn nút gợi ý nhanh `[🐶 Bé Bơ (Grooming / Gói Bạc)]`).
2. Màn hình hiển thị toàn bộ chân dung khách hàng 360:
   - Chủ nuôi: **Nguyễn Văn An** | SĐT: `0901234567` | Email: `an.nguyen@gmail.com`.
   - Thông tin thú cưng: Bé **Bơ** (Corgi - 11.5 kg - Ghi chú: *Rất hiếu động, sợ máy sấy nhiệt độ cao*).
   - Thẻ hội viên điện tử: **Gói Chăm Sóc Bạc (Silver)** với **Grooming: 6 lượt**, **Nail Care: 5 lượt**, **Spa: 3 lượt** (Hạn dùng: 1 tháng).
3. **Thao tác Trừ Lượt**:
   - Nhấn nút **`[Cấn Trừ 1 Lượt Grooming]`** trên thẻ.
   - Hệ thống hiển thị Toast xanh: *"✓ Đã cấn trừ 1 lượt Grooming cho bé Bơ thành công."*
   - Thẻ cập nhật ngay: Số lượt còn lại chuyển thành **5/6 lượt** và thanh tiến trình tự động tính toán lại.
   - Có thể thực hiện cấn trừ liên tục nhiều lần thuận tiện cho buổi diễn tập.
4. **Thao tác Chống Âm Lượt Tuyệt Đối**:
   - Khi số lượt của gói về 0 (hoặc thử nghiệm với bé đã hết lượt như Miu Miu thẻ Expired), nhấn nút trừ lượt.
   - Hệ thống chặn ngay lập tức với Toast đỏ: *"Không đủ lượt dịch vụ hoặc thẻ đã hết hiệu lực."*
   - Số lượt không bao giờ bị âm.
   👉 **Điểm nhấn thuyết trình**: Cơ chế khóa dòng `FOR UPDATE` trong giao dịch database ngăn ngừa tuyệt đối lỗi Race Condition khi nhiều nhân viên cùng thao tác.

---

### 🏥 KHÔNG GIAN 2: QUẦY TIẾP NHẬN POS (Tab 2: Quầy Tiếp Nhận POS)

#### 2. Demo Tiếp Nhận Dịch Vụ Nhanh & Tự Động Nhận Diện Quyền Lợi
1. Chuyển sang Tab **"Quầy Tiếp Nhận (POS)"**.
2. Tại danh sách thú cưng, chọn **Bơ (Corgi) — Chủ: Nguyễn Văn An**.
3. Cột bên phải ngay lập tức nạp hồ sơ tóm tắt của bé Bơ: cân nặng 11.5 kg, ghi chú chăm sóc, và tình trạng thẻ hội viên.
4. Nhấp chọn thẻ dịch vụ: **`[Grooming - Tắm & Cắt Tỉa (350.000đ)]`**.
5. Hộp kiểm tra chính sách hiển thị thông báo tích hợp:
   - Nếu thẻ còn lượt: *"Hội viên Gói Chăm Sóc Bạc — Áp dụng Miễn Phí 100% (Giá gốc: 350.000đ ➔ Cần thu: 0đ)"*.
   - Nếu thẻ đã hết lượt: *"Thanh toán giá gốc: 350.000đ (Đã hết lượt ưu đãi trong gói)"*.
6. Nhấn nút **`[✓ Xác Nhận & Mở Phiếu Dịch Vụ]`**:
   - Hệ thống tạo mới `Service Visit` ngay lập tức.
   - **Tự động đóng đề xuất cũ**: Mọi khuyến nghị `NEW` của bé Bơ trước đó đều tự động chuyển thành **`CONVERTED`** (Đã chuyển đổi thành công), giúp bảng điều khiển không còn đề xuất trùng lặp.
   - Trạng thái chu kỳ của bé Bơ chuyển ngay sang **`NOT_DUE`** (Ổn định - Vừa phục vụ hôm nay).

---

### 🤖 KHÔNG GIAN 3: TRỢ LÝ PHÂN TÍCH CHU KỲ (Tab 3: AI Care Engine)

#### 3. Bảng Theo Dõi Chu Kỳ & Bộ Lọc Trạng Thái
1. Chuyển sang Tab **"Trợ Lý Chu Kỳ AI"**.
2. Trên cùng là 4 thẻ KPI tóm tắt:
   - Thú Cưng Quản Lý: **10**
   - Chủ Nuôi Đăng Ký: **8**
   - Gói Hội Viên Kích Hoạt: **5**
   - Lượt Dịch Vụ Đã Phục Vụ: **23**
3. Thử nghiệm **Bộ lọc thông minh** trên bảng danh sách:
   - Bấm **`[Tất Cả]`**: Hiển thị đầy đủ danh sách thú cưng.
   - Bấm **`[Quá Hạn / Rời Bỏ]`**: Lọc ra các bé có nguy cơ cao (Bé Miu Miu vắng 64 ngày, Bé Đậu Phộng vắng 18 ngày, Bé Gấu Trúc vắng 49 ngày).
   - Bấm **`[Ổn Định]`**: Lọc ra các bé vừa sử dụng dịch vụ hoặc chưa đến hạn (Bé Bơ, Bé Kem, Bé Sữa).

#### 4. Bảng Đề Xuất Chăm Sóc Cần Xử Lý (Solid Color Badges)
1. Quan sát lưới các thẻ đề xuất bên dưới:
   - **Thẻ Màu Đỏ Rực (High Priority - Hộp chữ tô màu đặc)**:
     - Bé **Miu Miu**: *"Pet 'Miu Miu' đã quá chu kỳ Grooming (55 ngày vắng, tỷ lệ: 2.20 >= 1.5). Đề xuất: Gửi tin nhắn win-back, nhắc khách hàng quay lại."*
     - Bé **Gấu Trúc**: *"Gói hội viên sắp hết hạn sau 1 ngày."*
   - **Thẻ Màu Cam (Medium Priority - Hộp chữ tô màu đặc)**:
     - Bé **Kem**: *"Sắp đến chu kỳ Spa (còn 5 ngày). Còn 6 lượt Spa ưu đãi chưa dùng."*
2. **Thao Tác Tương Tác Trực Tiếp Ngay Trên Thẻ**:
   - Bấm **`[📞 Đã Gọi Điện]`**: Cập nhật trạng thái khuyến nghị sang `CONTACTED`.
   - Bấm **`[📅 Đặt Lịch POS]`**: Tự động chuyển ngay sang Tab Quầy POS và điền sẵn thông tin bé cưng + dịch vụ cần làm.
   - Bấm **`[✕]`**: Bỏ qua khuyến nghị (`DISMISSED`).

---

## 🖥️ PHẦN 2: DEMO QUẢN TRỊ BACK-OFFICE TRÊN FRAPPE DESK (`http://localhost:8080/app`)

Mở trình duyệt sang [http://localhost:8080/app](http://localhost:8080/app):
1. **DocType `Customer Membership`**:
   - Xem danh sách thẻ thành viên của khách hàng, bảng chi tiết các quyền lợi (`Membership Benefit` child table), số lượt đã dùng và số lượt còn lại.
2. **DocType `Care Recommendation`**:
   - Xem các bản ghi khuyến nghị được sinh tự động từ thuật toán EWMA / Cronjob quét định kỳ mỗi ngày.
   - Kiểm tra các trạng thái: `NEW`, `CONTACTED`, `CONVERTED`.
3. **DocType `Service Visit`**:
   - Xem lịch sử các lượt dịch vụ đã ghi nhận qua quầy POS kèm giá gốc và giá sau khi trừ ưu đãi hội viên.

---

## 🎯 CÁC CÂU HỎI HỘI ĐỒNG THƯỜNG GẶP & CÁCH TRẢ LỜI

| Câu hỏi của Giảng viên / Hội đồng | Câu trả lời trọng tâm |
| :--- | :--- |
| **1. Làm sao tránh trừ âm lượt khi 2 lễ tân cùng thao tác 1 lúc?** | Hệ thống sử dụng khóa hàng `SELECT ... FOR UPDATE` trong transaction của MariaDB. Mọi yêu cầu trừ lượt đồng thời buộc phải xếp hàng, và transaction kiểm tra chặt chẽ `remaining_quantity >= count` trước khi ghi nhận, ngăn chặn hoàn toàn Race Condition. |
| **2. Tại sao sau khi làm dịch vụ, tình trạng của bé lại không còn là "Sắp tới hạn"?** | Khi phát sinh một Service Visit mới, thuật toán tính lại `days_since_last_visit = 0`. Với khoảng cách 0 ngày, hệ thống nhận diện khách vừa phục vụ nên trạng thái chu kỳ tự động chuyển thành `NOT_DUE` (Ổn định). Đồng thời các khuyến nghị cũ cho dịch vụ đó được đánh dấu `CONVERTED`. |
| **3. Thuật toán dự đoán chu kỳ hoạt động như thế nào?** | Thuật toán sử dụng phân tích khoảng cách trung bình (IQR Outlier Filter loại bỏ đột biến), kết hợp ngưỡng nhạy (5-7 ngày cho `DUE_SOON` và tỷ lệ vắng $\ge 1.3 - 1.5$ cho `AT_RISK`). Yêu cầu tối thiểu 3 lượt ghé khám để đảm bảo không tạo cảnh báo rác. |
