# 📋 DANH SÁCH TÀI KHOẢN KHÁCH HÀNG & THÚ CƯNG (PETCARE CRM)

Dưới đây là danh sách đầy đủ **8 tài khoản khách hàng thực tế**, thông tin thú cưng, thẻ hội viên và thông tin đăng nhập được quản lý trong hệ thống **PetCare CRM**.

---

## 🔑 1. THÔNG TIN ĐĂNG NHẬP CHUNG

- **Cổng Web Portal (Khách hàng & Lễ tân)**: [http://localhost:8080/portal](http://localhost:8080/portal) (Tra cứu nhanh bằng SĐT / Tên)
- **Cổng Quản trị Frappe Desk**: [http://localhost:8080/app](http://localhost:8080/app) (Đăng nhập bằng Email & Mật khẩu)
- **Mật khẩu mặc định cho tất cả khách hàng**: `Customer@123`
- **Tài khoản Quản trị viên (Admin)**: `Administrator` / `admin123`

---

## 🐶 2. BẢNG CHI TIẾT 8 TÀI KHOẢN KHÁCH HÀNG & THÚ CƯNG

| STT | Khách Hàng & SĐT | Email Đăng Nhập | Mật Khẩu | Bé Cưng & Giống | Gói Hội Viên & Quyền Lợi | Trạng Thái Chăm Sóc & Kịch Bản Demo |
| :---: | :--- | :--- | :---: | :--- | :--- | :--- |
| **1** | **Nguyễn Văn An**<br>📞 `0901234567`<br>📍 Q.1, TP.HCM | `an.nguyen@gmail.com` | `Customer@123` | 🐶 **Bơ**<br>• Corgi (Đực, 2T)<br>• Vàng trắng, 11.5kg | **Gói Chăm Sóc Bạc (Silver)**<br>• Trạng thái: **Active**<br>• Grooming: **1/1 lượt**<br>• Nail Care: 1/1 lượt | ⏰ **`DUE_SOON`** *(Còn 3 ngày tới hạn Grooming)*<br>👉 **Demo Flow 1**: Trừ 1 lượt & Chặn âm lượt.<br>👉 **Demo Flow 2**: Gắn ưu đãi thẻ Bạc vào đề xuất. |
| **2** | **Trần Thị Bích Ngọc**<br>📞 `0912345678`<br>📍 Bình Thạnh, TP.HCM | `ngoc.tran@gmail.com` | `Customer@123` | 🐩 **Đậu Phộng**<br>• Poodle (Cái, 1.5T)<br>• Nâu đỏ xoăn, 4.2kg | **Gói Chăm Sóc Vàng (Gold)**<br>• Trạng thái: **Active**<br>• Grooming: **1/3 lượt**<br>• Spa: 1/2 lượt<br>• Vaccine: 1/1 lượt | ⏰ **`DUE_SOON`** + 💳 **`RENEWAL`**<br>👉 Sắp đến lịch Grooming (2 ngày).<br>👉 **Cảnh báo gia hạn**: Gói hết hạn sau 4 ngày. |
| **3** | **Lê Hoàng Long**<br>📞 `0983456789`<br>📍 Q.7, TP.HCM | `long.le@gmail.com` | `Customer@123` | 🐱 **Miu Miu**<br>• Mèo Anh lông ngắn (3T)<br>• Xám Silver, 4.8kg | **Gói Spa Mèo Quý Tộc**<br>• Trạng thái: **Expired (Hết hạn)**<br>• Grooming: 0/2 lượt | 🚨 **`AT_RISK`** *(Vắng 55 ngày / Chu kỳ 25 ngày)*<br>👉 Tỷ lệ vắng mặt $2.20 \ge 1.5$.<br>👉 **Demo Flow 3a**: Đề xuất Urgent gửi tin nhắn Win-back. |
| **4** | **Phạm Minh Đức**<br>📞 `0974567890`<br>📍 Cầu Giấy, Hà Nội | `duc.pham@gmail.com` | `Customer@123` | 🐶 **Gấu Trúc**<br>• Phốc Sóc (Đực, 2T)<br>• Trắng tuyết, 3.0kg | **Gói Chăm Sóc Bạc (Silver)**<br>• Trạng thái: **Exhausted (Hết lượt)**<br>• Grooming: 0/1 lượt<br>• Nail Care: 0/1 lượt | 🟠 **`OVERDUE`** *(Quá hạn Spa 10 ngày)*<br>👉 Chu kỳ Spa 30 ngày, đã 40 ngày chưa tái khám. |
| **5** | **Hoàng Mai Anh**<br>📞 `0936789012`<br>📍 Hải Châu, Đà Nẵng | `anh.hoang@gmail.com` | `Customer@123` | 🦮 **Kem**<br>• Golden Retriever (3T)<br>• Vàng kim, 29.5kg | **Gói Kim Cương VIP (Diamond)**<br>• Trạng thái: **Active**<br>• Grooming: **4/6 lượt**<br>• Spa: 6/6 lượt<br>• Vaccine: 2/2 lượt | ⚪ **`NORMAL`** *(An toàn)*<br>👉 Chu kỳ Spa 14 ngày, vừa đi 4 ngày trước (còn 10 ngày) $\rightarrow$ Hệ thống không spam đề xuất. |
| **6** | **Vũ Tuấn Kiệt**<br>📞 `0947890123`<br>📍 TP. Thủ Đức, TP.HCM | `kiet.vu@gmail.com` | `Customer@123` | 🐶 **Mít**<br>• Pug mặt xệ (Đực, 1T)<br>• Vàng đen, 7.8kg | *Khách Vãng Lai*<br>(Chưa đăng ký gói định kỳ) | 🟡 **`INSUFFICIENT_DATA`** *(Khách mới)*<br>👉 Mới có 2 lượt khám ($< 3$ lượt).<br>👉 **Demo Flow 3b**: Hệ thống tự động lọc bỏ. |
| **7** | **Đỗ Thu Thảo**<br>📞 `0965678901`<br>📍 Ba Đình, Hà Nội | `thao.do@gmail.com` | `Customer@123` | 🐈 **Sữa**<br>• Mèo Ba Tư (Cái, 4T)<br>• Trắng muốt xù, 5.2kg | *Khách Vãng Lai*<br>(Chưa đăng ký gói định kỳ) | 🟡 **`INSUFFICIENT_DATA`** *(Chỉ 1 lượt khám)*<br>👉 Tự động lọc bỏ không dự đoán sai lệch. |
| **8** | **Đặng Phương Linh**<br>📞 `0928901234`<br>📍 Hoàn Kiếm, Hà Nội | `linh.dang@gmail.com` | `Customer@123` | 🐈 **Mun**<br>• Mèo Mướp (Đực, 2.5T)<br>• Vằn đen xám, 3.9kg | *Khách Mới Tạo Hồ Sơ* | ⚪ **`NO_VISITS`** *(Chưa có lịch sử)*<br>👉 Khách hàng tiềm năng cần tư vấn gói trải nghiệm. |

---

## 🎯 3. HƯỚNG DẪN TRA CỨU NHANH TRÊN GIAO DIỆN

### Cách 1: Sử dụng Cổng Web Portal ([http://localhost:8080/portal](http://localhost:8080/portal))
1. Mở trình duyệt vào [http://localhost:8080/portal](http://localhost:8080/portal).
2. Dán Số điện thoại của bất kỳ khách hàng nào ở bảng trên (VD: `0901234567` hoặc `0912345678`).
3. Bấm **"Tra Cứu"** $\rightarrow$ Hệ thống hiển thị ngay Thẻ Hội Viên Điện Tử, số lượt còn lại, thanh tiến trình và đề xuất chăm sóc AI.

### Cách 2: Sử dụng các nút bấm Kịch Bản Demo 1-Chạm
Ngay trên thanh Top Bar màu đen của Web Portal, bạn có thể click trực tiếp:
- `[🐶 Flow 1: Bé Bơ]` $\rightarrow$ Nạp ngay tài khoản của Nguyễn Văn An.
- `[⏰ Flow 2: Bé Bơ]` $\rightarrow$ Xem đề xuất Due Soon 3 ngày.
- `[🚨 Flow 3a: Bé Miu Miu]` $\rightarrow$ Nạp ngay tài khoản Lê Hoàng Long (At Risk).
- `[🟡 Flow 3b: Bé Mít]` $\rightarrow$ Nạp ngay tài khoản Vũ Tuấn Kiệt (Khách mới).
- `[💳 Gia Hạn: Bé Đậu Phộng]` $\rightarrow$ Nạp ngay tài khoản Bích Ngọc (Cảnh báo hết hạn).
