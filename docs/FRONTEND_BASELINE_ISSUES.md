# PETCARE CRM — BÁO CÁO VẤN ĐỀ GIAO DIỆN HIỆN TRẠNG (BASELINE ISSUES)
**Tài liệu Kiểm tra Hiện trạng Giai đoạn 1**
*Dự án:* PetCare CRM
*Ngày lập:* 04/11/2026
*Phương pháp:* Rà soát mã nguồn thực tế từng dòng, đối chiếu với Master Prompt và tiêu chuẩn thiết kế CRM vận hành thực tế.

---

## 1. TỔNG HỢP VẤN ĐỀ THEO MỨC ĐỘ NGHIÊM TRỌNG

| Mức Độ | Số Lượng | Nhóm Vấn Đề Chính |
|:---|:---:|:---|
| **Cao (Critical / High)** | 4 | Lỗi lặp thẻ HTML & vỡ cấu trúc DOM; Hiển thị thông số kỹ thuật/test developer trong giao diện người dùng cuối; Bẫy bàn phím (Escape key không đóng hết modal); Nút thử nghiệm developer xuất hiện trên quầy lễ tân. |
| **Trung Bình (Medium)** | 5 | Tuyên bố tiếp thị thiếu bằng chứng ("thời gian thực"); Sử dụng dải gradient nhiều màu trên header modal; Số tiền chưa căn phải đồng nhất (`tabular-nums`); Thiếu phân cấp thông tin rõ ràng tại khối cấn trừ quyền lợi POS. |
| **Thấp (Low / Polish)** | 3 | Trộn lẫn thuật ngữ tiếng Anh và tiếng Việt không cần thiết; Tương phản màu sắc ở một số badge trạng thái chưa tối ưu; Thiếu chỉ báo trạng thái rỗng (empty state) khi không có dữ liệu lịch hẹn/đề xuất. |

---

## 2. CHI TIẾT CÁC VẤN ĐỀ ĐƯỢC XÁC MINH CÓ DẪN CHỨNG FILE & DÒNG

### 2.1. Lỗi Cấu Trúc HTML & Trùng Lặp Thẻ Head (Mức Độ: Critical)
- **Tập tin bị ảnh hưởng:**
  - `preview.html` (Dòng 1 đến 125)
  - `apps/petcare_crm/petcare_crm/www/frontend.html` (Dòng 1 đến 125)
  - `apps/petcare_crm/petcare_crm/www/index.html` (Dòng 1 đến 125)
- **Dẫn chứng mã nguồn:**
  ```html
  <!-- Dòng 1-63: Khai báo đầy đủ head và mở body -->
  <!DOCTYPE html>
  <html lang="vi">
  <head>
    <title>PetCare Clinic & Spa ...</title>
    ...
  </head>
  <body class="bg-slate-50 ... min-h-screen">
  <!-- Dòng 65: Văn bản thô bị rò rỉ ngay trong body -->
  PetCare Clinic & Spa — Quản Lý Tiếp Nhận & Quyền Lợi Hội Viên Thú Cưng<meta name="csrf-token" content="{{ frappe.session.csrf_token }}">
    <script>window.frappe_csrf_token = "{{ frappe.session.csrf_token }}";</script>
    <!-- Dòng 69-122: Trùng lặp hoàn toàn thẻ Tailwind, FontAwesome, Google Fonts, tailwind.config và style block -->
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="...font-awesome...">
    <style>body, html { ... }</style>
  ```
- **Hệ quả thực tế:**
  1. Dòng chữ `PetCare Clinic & Spa — Quản Lý Tiếp Nhận & Quyền Lợi Hội Viên Thú Cưng` bị in trực tiếp lên đỉnh màn hình dưới dạng văn bản thô không định dạng, đè lên thanh navbar.
  2. Trình duyệt tải tệp CSS và font 2 lần, tăng thời gian phân tích DOM và tiêu tốn bộ nhớ không cần thiết.

---

### 2.2. Trưng Bày Chỉ Số Kiểm Thử & Tuyên Bố Kỹ Thuật Developer Trên Giao Diện Vận Hành (Mức Độ: High)
- **Tập tin bị ảnh hưởng:** `desk_preview.html`
- **Dẫn chứng mã nguồn:**
  - *Dòng 95-98:*
    ```html
    <span class="inline-flex items-center gap-1.5 bg-emerald-50 text-emerald-800 text-xs px-3 py-1.5 rounded-lg border border-emerald-200 font-bold shadow-2xs">
      <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
      88/88 Test Cases PASS (100%)
    </span>
    ```
  - *Dòng 355:*
    ```html
    <div class="text-xs text-slate-400">
      PetCare CRM v2.0 • Hoàn tất nghiệm thu 100% (88/88 Test Cases) • Khởi chạy trên Frappe Framework v15
    </div>
    ```
- **Vi phạm tiêu chuẩn:**
  - Vi phạm trực tiếp Mục 3.2 ("Các dãy thống kê trang trí như 99.9%, 10K+, 24/7, 100% Secure, 88/88 tests passed khi không phải dữ liệu nghiệp vụ được xác minh và có ngữ cảnh").
  - Vi phạm Mục 3.3 ("Không để thông tin kỹ thuật dành cho developer xuất hiện trong giao diện người dùng cuối. Không đưa số lượng test, số endpoint, số DocType, tỷ lệ pass, benchmark hoặc tuyên bố kiến trúc vào dashboard nếu chúng không phục vụ một tác vụ CRM cụ thể").
  - Vi phạm Mục 6 - Điều số 6 ("Không hiển thị số test, phần trăm hoàn thành hoặc badge 'verified' trong UI cho người dùng CRM").

---

### 2.3. Tuyên Bố Tiếp Thị Thiếu Cơ Sở Kỹ Thuật & Thông Báo Giả Lập Sai Thực Tế (Mức Độ: High)
- **Tập tin bị ảnh hưởng:** `desk_preview.html` và `preview.html`
- **Dẫn chứng mã nguồn:**
  - *desk_preview.html dòng 109 & preview.html dòng 748:*
    `<i class="fa-solid fa-bolt text-teal-600"></i> Dữ liệu tự động đồng bộ thời gian thực`
    Tuyên bố "thời gian thực" (real-time) mà không có kết nối WebSocket/Server-Sent Events được kiểm chứng (vi phạm Mục 3.3).
  - *desk_preview.html dòng 1964-1967:*
    ```javascript
    function testWebhookFromDesk() {
      showToast(`HMAC Webhook Gateway: Đã xác thực chữ ký SHA-256 an toàn và bảo mật cho luồng VietQR IPN!`, 'success');
    }
    ```
    Tạo thông báo bảo mật thành công giả lập khi người dùng nhấn nút, vi phạm Mục 3.3 và Mục 6 - Điều 5.
  - *desk_preview.html dòng 691:*
    `showToast('Đã nạp ... đ cho ...! Biên lai đã gửi Mailtrap Sandbox!', 'success');`
    Người dùng quầy tiếp tân hoặc kế toán không nên thấy thông báo nhắc đến công cụ debug nội bộ "Mailtrap Sandbox".

---

### 2.4. Công Cụ Debug Developer Đặt Lẫn Vào Màn Hình Tiếp Đón Quầy (Mức Độ: Medium)
- **Tập tin bị ảnh hưởng:** `preview.html` (Dòng 331-334, 442-446)
- **Dẫn chứng mã nguồn:**
  - Thanh header có nút tím nổi bật:
    `<button onclick="sendTestEmail()" ...><i class="fa-solid fa-envelope text-purple-600"></i> Gửi Mailtrap Test</button>`
  - Khối phím tắt nhanh có thẻ:
    `<div class="font-extrabold text-xs text-purple-900">Kiểm Tra Mailtrap</div>`
- **Đánh giá:**
  Nhân viên lễ tân phòng khám thú cưng tra cứu thông tin khách hàng không có nhu cầu bấm "Gửi Mailtrap Test". Nút này làm nhiễu không gian làm việc và gây nhầm lẫn với tác vụ nghiệp vụ gửi xác nhận thực tế cho khách.

---

### 2.5. Lỗi Bẫy Bàn Phím (Escape Key Không Đóng Toàn Bộ Modal) (Mức Độ: Medium)
- **Tập tin bị ảnh hưởng:** `preview.html` (Dòng 3259-3266)
- **Dẫn chứng mã nguồn:**
  ```javascript
  window.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      document.getElementById('renew-overlay')?.remove();
      document.getElementById('reg-overlay')?.remove();
      document.getElementById('appt-modal-overlay')?.remove();
    }
  });
  ```
- **Hệ quả thực tế:**
  Listener chỉ bắt và xóa 3 modal (`renew-overlay`, `reg-overlay`, `appt-modal-overlay`). Khi người dùng mở Modal "Thêm Khách Hàng & Thú Cưng Mới" (`#create-cust-overlay`) hoặc Modal "Import Dữ Liệu Excel/CSV" (`#import-cust-overlay`) hoặc các modal quick-topup, nhấn phím `Escape` hoàn toàn không có tác dụng, gây ức chế và vi phạm quy chuẩn thao tác bàn phím (WCAG Accessibility Keyboard trap).

---

### 2.6. Lạm Dụng Gradient Màu Mè Trong Hộp Thoại Chức Năng (Mức Độ: Medium)
- **Tập tin bị ảnh hưởng:** `preview.html` (Dòng 3537)
- **Dẫn chứng mã nguồn:**
  `class="p-4 px-6 border-b border-slate-200 flex justify-between items-center bg-gradient-to-r from-emerald-50 to-teal-50"`
- **Vi phạm tiêu chuẩn:**
  Vi phạm Mục 3.2 ("Gradient nhiều màu, nền phát sáng, neon... phải tránh"). Cần chuẩn hóa về nền phẳng (Flat surface) trắng tinh hoặc Slate/Teal đồng nhất, viền xám mảnh chuẩn y tế.

---

### 2.7. Bố Cục Quầy POS Chưa Tối Ưu Phân Cấp Giá & Quyền Lợi Cấn Trừ (Mức Độ: Medium)
- **Tập tin bị ảnh hưởng:** `preview.html` (Dòng 560-630)
- **Hiện trạng:**
  Khối hiển thị quyền lợi cấn trừ (`#pos-benefit-status-box`) và tổng tiền thanh toán (`#pos-final-price-display`) được bố trí nhưng thiếu độ nổi bật trực quan về sự so sánh giữa:
  1. Đơn giá tiêu chuẩn ban đầu (Original Price).
  2. Mức quyền lợi thẻ hội viên được cấn trừ (Miễn phí 100% hoặc giảm % theo gói).
  3. Số tiền còn lại thu từ khách (0 đ nếu miễn phí, hoặc số tiền sau giảm).
  Nhân viên thu ngân cần nhìn thấy ngay trong 1 giây mà không phải nhẩm tính.

---

### 2.8. Tính Nhất Quán Về Thuật Ngữ Nghiệp Vụ & Định Dạng Số (Mức Độ: Low)
- **Tập tin bị ảnh hưởng:** `desk_preview.html` và `preview.html`
- **Hiện trạng:**
  - Bảng số liệu trong một số Drawer chưa áp dụng thuộc tính `font-variant-numeric: tabular-nums` và `text-align: right`, dẫn đến các hàng số tiền bị lệch trục dọc khi số chữ số khác nhau.
  - Các nhãn trên Desk Shortcuts sử dụng tiếng Anh pha tạp ("New Leads", "Due Soon Pets", "At Risk Pets", "Active Memberships", "Open Cases") trong khi toàn bộ hệ thống đang phục vụ vận hành phòng khám tại Việt Nam. Cần chuẩn hóa nhãn tiếng Việt chuẩn mực, giữ kèm mã/thuật ngữ chuyên môn nếu cần.
