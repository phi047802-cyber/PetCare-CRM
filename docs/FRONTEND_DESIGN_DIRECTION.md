# PETCARE CRM — ĐỊNH HƯỚNG THIẾT KẾ & HỆ THỐNG QUY CHUẨN FRONTEND
**Tài liệu Thiết kế Giai đoạn 2 (Frontend Design Direction & Tokens)**
*Dự án:* PetCare CRM
*Phiên bản:* v15-Refined 2.0
*Đối tượng:* Nhóm phát triển sản phẩm & kỹ sư frontend

---

## 1. NGUYÊN TẮC THIẾT KẾ CỐT LÕI (CORE PRINCIPLES)

1. **Phần Mềm Vận Hành Y Tế & Chăm Sóc Đích Thực (Clinical & Operational SaaS)**:
   - Giao diện được thiết kế cho nhân viên quầy, bác sĩ khám bệnh, nhân viên spa/grooming và quản lý vận hành mỗi ngày.
   - Ưu tiên tối đa sự tập trung, tốc độ thao tác, khả năng quét nhanh thông tin (scannability) và độ chính xác dữ liệu.
   - Loại bỏ mọi chi tiết trang trí thừa: không gradient nhiều màu, không bóng đổ (shadow) nặng nề, không thẻ lồng thẻ, không icon trang trí rối mắt.

2. **Trung Thực Với Dữ Liệu & Trạng Thái Hệ Thống (Data Integrity & Honesty)**:
   - Không bịa đặt chỉ số ("88/88 test passed", "99.9%", "bảo mật tuyệt đối", "real-time").
   - Phân biệt minh bạch 3 trạng thái giao diện:
     - *Đang tải (Loading State)*: Spinner tinh gọn, kèm thông báo "Đang xử lý...".
     - *Không có dữ liệu (Empty State)*: Khung xám nhạt viền mảnh, thông báo rõ ràng "Chưa có bản ghi nào", gợi ý hành động khởi tạo phù hợp.
     - *Lỗi truy vấn (Error State)*: Cảnh báo đỏ nhạt viền đỏ, ghi rõ mã lỗi HTTP hoặc nguyên nhân xác thực, không âm thầm gán về 0.

3. **Tương Phản & Khả Năng Tiếp Cận Cao (High Accessibility & Contrast)**:
   - Tuân thủ độ tương phản văn bản WCAG AA (tối thiểu 4.5:1 với văn bản thường và 3:1 với văn bản lớn).
   - Mọi nút bấm, trường nhập liệu, hộp chọn đều có trạng thái `:focus-visible` viền rõ nét (outline 2px Teal-600).
   - Hỗ trợ phím tắt chuẩn mực (`Escape` để đóng ngay mọi hộp thoại, `Enter` để kích hoạt tìm kiếm).

---

## 2. BẢNG DESIGN TOKENS CHUẨN HÓA

### 2.1. Bảng Màu (Color Tokens)

| Token | Giá Trị HEX | Ứng Dụng Trong Hệ Thống |
|:---|:---:|:---|
| **Background (Nền trang)** | `#F8FAFC` (Slate-50) | Nền tổng thể toàn bộ màn hình Desk và Web Portal |
| **Surface (Bề mặt thẻ/khối)** | `#FFFFFF` (White) | Thẻ hồ sơ, hàng bảng dữ liệu, nền form nhập liệu |
| **Surface Subdued (Bề mặt phụ)** | `#F1F5F9` (Slate-100) | Header của bảng dữ liệu, thanh tóm tắt chỉ số |
| **Border Default (Viền chuẩn)** | `#E2E8F0` (Slate-200) | Đường ngăn cách hàng, viền thẻ card, viền modal |
| **Border Focus / Hover** | `#CBD5E1` (Slate-300) | Trạng thái hover của thẻ card, phân định khối |
| **Text Primary (Chữ chính)** | `#0F172A` (Slate-900) | Tiêu đề, tên khách hàng, tên thú cưng, số tiền |
| **Text Secondary (Chữ phụ)** | `#475569` (Slate-600) | Nhãn trường, mô tả chi tiết, thời gian, mã bản ghi |
| **Text Muted (Chữ mờ)** | `#94A3B8` (Slate-400) | Placeholder, biểu tượng phụ trợ, breadcrumb divider |
| **Primary Accent (Màu nhấn chính)** | `#0D9488` (Teal-600) | Nút hành động chính, viền focus, icon nhận diện thương hiệu |
| **Primary Accent Hover** | `#0F766E` (Teal-700) | Trạng thái hover của nút chính, tab đang hoạt động |
| **Primary Accent Light** | `#F0FDFA` (Teal-50) | Nền mục được chọn, dòng highlight, badge thông báo nhẹ |

### 2.2. Màu Sắc Trạng Thái Nghiệp Vụ (Semantic Status Colors)

| Trạng Thái Nghiệp Vụ | Mã Màu Nền | Mã Màu Chữ | Mã Màu Viền | Trường Hợp Sử Dụng |
|:---|:---:|:---:|:---:|:---|
| **Hoạt động / Hoàn tất (Active/Success)** | `#ECFDF5` (Emerald-50) | `#065F46` (Emerald-800) | `#A7F3D0` (Emerald-200) | Thẻ hội viên Active, Lịch hẹn Checked-in, Phiếu khám Completed, Lead Converted |
| **Sắp đến hạn / Cảnh báo (Due/Warning)** | `#FFFBEB` (Amber-50) | `#92400E` (Amber-800) | `#FDE68A` (Amber-200) | Bé sắp đến chu kỳ (Due Soon), Thẻ sắp hết hạn, Lịch hẹn chờ khám (Scheduled) |
| **Nguy cơ / Đã hủy (Risk/Danger)** | `#FEF2F2` (Red-50) | `#991B1B` (Red-800) | `#FECACA` (Red-200) | Thú cưng nguy cơ rời bỏ (At Risk), Thẻ hết hạn (Expired), Lịch hẹn Hủy |
| **Đang xử lý / Tiềm năng (Info/Draft)** | `#EFF6FF` (Blue-50) | `#1E40AF` (Blue-800) | `#BFDBFE` (Blue-200) | Phiếu khám Draft, Lead mới tiếp nhận (Qualified), Cơ hội mở (Opportunity) |
| **Đóng / Vô hiệu (Inactive/Neutral)** | `#F8FAFC` (Slate-50) | `#475569` (Slate-600) | `#E2E8F0` (Slate-200) | Hồ sơ lưu trữ, Case đã đóng (Resolved), Giao dịch đã tất toán |

---

## 3. TYPOGRAPHY & SPACING SCALE

- **Font Family:** `'Plus Jakarta Sans', system-ui, -apple-system, sans-serif`
- **Tỷ lệ chữ & Trọng số:**
  - *Tiêu đề trang (Page Title - H1):* `font-extrabold text-xl (20px) / leading-tight text-slate-900`
  - *Tiêu đề khối (Section Title - H2):* `font-bold text-base (16px) / leading-snug text-slate-900`
  - *Tiêu đề bảng / thẻ (Card Title - H3):* `font-bold text-sm (14px) / leading-normal text-slate-800`
  - *Văn bản làm việc chính (Body Text):* `font-medium text-xs (12px) / leading-relaxed text-slate-700`
  - *Nhãn phụ & Chú thích (Caption/Meta):* `font-medium text-[11px] / leading-normal text-slate-500`
  - *Hiển thị số tiền / Tiền tệ:* `font-variant-numeric: tabular-nums; text-align: right; font-bold text-slate-900;`

- **Hệ thống Bo Góc (Border Radius) & Bóng Đổ (Elevation):**
  - Khối thẻ thông tin (Card): `rounded-xl (12px)`, `border border-slate-200`, `shadow-xs` (`box-shadow: 0 1px 2px rgba(15,23,42,0.05)`)
  - Nút bấm & Form inputs: `rounded-lg (8px)`
  - Badge trạng thái: `rounded-full px-2.5 py-0.5 text-[11px] font-bold border`
  - Tuyệt đối không dùng bóng đổ nặng (shadow-xl/shadow-2xl trên màn hình làm việc thông thường).

---

## 4. QUY CHUẨN CÁC COMPONENT DÙNG CHUNG

### 4.1. Nút Bấm (Button Hierarchy)
1. **Primary Button (`btn-teal`)**:
   - `bg-teal-600 text-white font-bold text-xs px-3.5 py-2 rounded-lg hover:bg-teal-700 shadow-xs transition`
   - Dùng cho: Thao tác chính duy nhất trên màn hình (Check-in, Tra cứu, Lưu hồ sơ, Xác nhận nạp tiền).
2. **Secondary Button (`btn-white`)**:
   - `bg-white text-slate-700 border border-slate-300 font-semibold text-xs px-3.5 py-2 rounded-lg hover:bg-slate-50 shadow-2xs transition`
   - Dùng cho: Thao tác phụ (Hủy bỏ, Đóng hộp thoại, Đặt lại form, Xuất file).
3. **Accent Action Button (Thao tác nhanh trên bảng)**:
   - Nạp ví: `bg-amber-500 hover:bg-amber-600 text-white text-xs px-2.5 py-1 rounded-md font-bold`
   - Check-in POS: `bg-teal-600 hover:bg-teal-700 text-white text-xs px-2.5 py-1 rounded-md font-bold`
   - Hủy: `bg-rose-50 hover:bg-rose-100 text-rose-700 border border-rose-300 text-xs px-2.5 py-1 rounded-md font-bold`

### 4.2. Bảng Dữ Liệu (Data Tables)
- Khung bảng: viền `border border-slate-200 rounded-xl overflow-hidden bg-white`.
- Header: `bg-slate-100 text-slate-600 text-[11px] font-bold uppercase tracking-wider py-2.5 px-3 border-b border-slate-200`.
- Hàng: `text-xs text-slate-700 hover:bg-slate-50/80 transition divide-y divide-slate-100`.
- Căn lề chuẩn:
  - Cột mã bản ghi, họ tên, dịch vụ: Căn trái (`text-left`).
  - Cột ngày giờ, trạng thái, SĐT: Căn giữa (`text-center`) hoặc căn trái có phân định rõ.
  - Cột đơn giá, số tiền thanh toán, số dư: Căn phải (`text-right`) kèm thuộc tính `font-variant-numeric: tabular-nums`.
  - Cột hành động: Căn phải (`text-right`).

### 4.3. Hộp Thoại (Modals & Drawers)
- Lớp nền mờ (Backdrop): `fixed inset-0 bg-slate-900/50 backdrop-blur-xs z-50 flex items-center justify-center p-4`.
- Header hộp thoại: Nền phẳng `bg-slate-50` viền dưới `border-b border-slate-200`, tiêu đề đậm rõ ràng kèm nút đóng X góc phải.
- Xử lý bàn phím: Bắt buộc đóng ngay khi người dùng nhấn phím `Escape`.
- Xử lý click ngoài: Đóng hộp thoại khi click vào vùng backdrop (trừ khi đang submit form).

### 4.4. Thẻ Thông Báo Nổi (Toast Notifications)
- Nằm cố định ở góc trên bên phải (`fixed top-16 right-6 z-50`).
- Tự động đóng sau 4 giây, có thể đóng thủ công.
- Kiểu viền bên trái dày 4px phân biệt rõ:
  - Thành công: Viền xanh lục `border-l-emerald-600`, icon checkmark.
  - Cảnh báo: Viền vàng `border-l-amber-500`, icon tam giác chấm than.
  - Lỗi: Viền đỏ `border-l-rose-600`, icon chấm than tròn.
  - Thông tin: Viền xanh ngọc `border-l-teal-600`, icon info tròn.

---

## 5. MAPPING THÀNH PHẦN THEO TỪNG MÀN HÌNH

| Màn Hình | Typography / Header | Bảng / Danh Sách | Form & Input | Button Áp Dụng | Modal / Drawer Áp Dụng |
|:---|:---|:---|:---|:---|:---|
| **Tra Cứu Hồ Sơ 360** | H1 "Tra Cứu Hồ Sơ & Quyền Lợi Hội Viên" | Bảng Lịch Sử Lần Ghé (tabular-nums, right-aligned) | Input tra cứu SĐT kích thước lớn, focus teal rõ nét | Primary "Tra Cứu", Secondary "Xóa" | Modal Nạp Tiền, Modal Gia Hạn, Modal Đăng Ký Mới |
| **Quầy POS Check-in** | H2 "Quầy Tiếp Nhận Nhanh POS" | Thẻ chọn Dịch vụ radio-card; Hộp đối soát quyền lợi 3 lớp giá | Dropdown chọn Bé, Dropdown dịch vụ, Radio PTTT | Primary "Hoàn Tất Tiếp Nhận", Secondary "Làm Lại" | Modal Đặt Lịch Hẹn Chăm Sóc |
| **Quản Lý Lịch Hẹn** | H2 "Danh Sách Lịch Hẹn Đặt Trước" | Bảng Lịch Hẹn (cột ngày giờ mono, cột trạng thái badge) | Bộ lọc trạng thái lịch hẹn | Action "Check-in POS", Action "Hủy Lịch" | Modal Đặt Lịch Hẹn Mới |
| **Chu Kỳ Chăm Sóc** | H2 "Theo Dõi Chu Kỳ & Đề Xuất CSKH" | Bảng Chu Kỳ Thú Cưng; Khối Card đề xuất CSKH | Bộ lọc 4 tab (Tất cả, Sắp đến hạn, Nguy cơ, Gia hạn) | Action "Nhắc Hẹn", Action "Bỏ Qua", "Quét Chu Kỳ" | — |
| **Desk Workspace** | Banner Quản Trị Frappe v15 | Lưới 5 Thẻ Shortcuts; Lưới 5 Modules DocTypes | Ô tìm kiếm nhanh DocType | Button "+ Thêm Khách Hàng", "Import Data", "KPI Dashboard" | Slide-out Drawer xem chi tiết từng DocType |
| **Batch Import** | H2 "Nhập Liệu & Import Dữ Liệu Khách Hàng" | Bảng Đối Soát Xem Trước (Preview Table) với đếm bản ghi hợp lệ / lỗi | Khu vực Kéo thả file + Khung Dán văn bản | Primary "Thực Thi Import", Secondary "Đóng" | Modal Toàn Màn Hình Khép Kín |
