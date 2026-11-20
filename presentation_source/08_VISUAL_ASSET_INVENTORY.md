# PETCARE CRM — BẢN KIỂM KÊ TÀI SẢN TRỰC QUAN & DANH MỤC SHOT CẦN CHỤP (VISUAL ASSET INVENTORY & SHOT LIST)

> **Mã hồ sơ**: `INVENTORY-VISUAL-2026`  
> **Dự án**: PetCare CRM (Hệ thống CRM Dịch vụ Chăm sóc Thú cưng)  
> **Đơn vị kiểm toán**: Evidence Auditor & Presentation Researcher  
> **Ngày lập hồ sơ**: 07/11/2026  
> **Nguyên tắc minh chứng**: Tuyệt đối không dùng ảnh stock từ internet để giả làm sản phẩm; phân tách rõ ảnh sơ đồ có sẵn và danh mục các ảnh màn hình (screenshots) cần chụp trực tiếp từ giao diện chạy thật.

---

## 1. TÀI SẢN TRỰC QUAN SẴN CÓ ĐÃ XÁC MINH TRONG REPOSITORY

Khảo sát toàn diện hệ thống ghi nhận hiện có **5 tệp hình ảnh sơ đồ BPMN chất lượng cao** được xuất trực tiếp từ phần mềm Camunda Modeler, hoàn toàn hợp lệ để đưa lên Slide thuyết trình:

| STT | Đường Dẫn Tệp Minh Chứng | Quy Trình Được Mô Tả | Phân Làn & Nội Dung Trực Quan Nhìn Thấy | Kích Thước | Độ Phù Hợp Cho Slide | Che Giấu Dữ Liệu (PII / Secrets) |
|:---:|---|---|---|:---:|:---:|:---:|
| **01** | [`deliverables/bpmn/group/PetCare_CRM_End_to_End_Group.png`](file:///c:/Users/pc/Documents/Doan_CRM/deliverables/bpmn/group/PetCare_CRM_End_to_End_Group.png) | **Quy trình CRM Nhóm End-to-End** (A4.3.1) | 5 Phân làn (Khách hàng, Sales, Lễ tân, Bác sĩ/KTV, CRM Engine); luồng xuyên suốt từ Lead Web Form $\rightarrow$ Bán hàng $\rightarrow$ Check-in $\rightarrow$ Cấn trừ thẻ $\rightarrow$ Care Engine $\rightarrow$ Zalo ZNS. | 441 KB | **Rất cao** (Dùng cho Slide 05) | Không chứa thông tin nhạy cảm. |
| **02** | [`deliverables/bpmn/individual/member_1/MSSV1_HoTen1_TiepNhanLead.png`](file:///c:/Users/pc/Documents/Doan_CRM/deliverables/bpmn/individual/member_1/MSSV1_HoTen1_TiepNhanLead.png) | **Quy trình Cá nhân 1: Tiếp Nhận Lead & Chuyển Đổi** (A4.3.2) | 3 Phân làn (Khách hàng, Sales, CRM); chi tiết khâu bẫy bot Honeypot, chuẩn hóa SĐT, kiểm tra trùng lặp Contact và chuyển đổi 1 chạm. | 382 KB | **Cao** (Dùng cho Slide chi tiết Sales) | Không chứa thông tin nhạy cảm. |
| **03** | [`deliverables/bpmn/individual/member_2/MSSV2_HoTen2_QuanLyOpportunity.png`](file:///c:/Users/pc/Documents/Doan_CRM/deliverables/bpmn/individual/member_2/MSSV2_HoTen2_QuanLyOpportunity.png) | **Quy trình Cá nhân 2: Quản Lý Phễu Cơ Hội Bán Hàng** (A4.3.2) | 3 Phân làn (Khách hàng, Sales, CRM); quản lý phễu Kanban 6 giai đoạn, tính xác suất có trọng số, đóng Lost kèm lý do bắt buộc. | 388 KB | **Cao** (Dùng cho Slide Pipeline) | Không chứa thông tin nhạy cảm. |
| **04** | [`deliverables/bpmn/individual/member_3/MSSV3_HoTen3_DichVu_CanTru_VietQR.png`](file:///c:/Users/pc/Documents/Doan_CRM/deliverables/bpmn/individual/member_3/MSSV3_HoTen3_DichVu_CanTru_VietQR.png) | **Quy trình Cá nhân 3: Dịch Vụ, Cấn Trừ Thẻ & VietQR** (A4.3.2) | 4 Phân làn (Khách hàng, Lễ tân, Kỹ thuật viên, CRM); check-in, cấn trừ thẻ khóa dòng Pessimistic Lock, sinh VietQR và đối soát Webhook. | 430 KB | **Cao** (Dùng cho Slide Vận hành/Thẻ) | Không chứa thông tin nhạy cảm. |
| **05** | [`deliverables/bpmn/individual/member_4/MSSV4_HoTen4_CareIntelligence_ZaloZNS.png`](file:///c:/Users/pc/Documents/Doan_CRM/deliverables/bpmn/individual/member_4/MSSV4_HoTen4_CareIntelligence_ZaloZNS.png) | **Quy trình Cá nhân 4: Care Intelligence & Zalo ZNS** (A4.3.2) | 3 Phân làn (CRM Engine, CSKH, Khách hàng); chạy EWMA + Tukey IQR, lọc Due Soon/At Risk, điều phối Zalo ZNS và giao việc ToDo. | 523 KB | **Rất cao** (Dùng cho Slide Khác biệt) | Không chứa thông tin nhạy cảm. |

---

## 2. SƠ ĐỒ KỸ THUẬT MERMAID ĐÃ CHUẨN HÓA SẴN SÀNG KẾT XUẤT

Trong bộ hồ sơ này, 4 sơ đồ kiến trúc và dữ liệu chuẩn đã được xây dựng bằng cú pháp Mermaid, sẵn sàng để xuất ảnh đưa vào Slide:
1. **Sơ đồ Clean Architecture 8 Tầng**: Xem tại [`03_TECHNICAL_ARCHITECTURE.md`](file:///c:/Users/pc/Documents/Doan_CRM/presentation_source/03_TECHNICAL_ARCHITECTURE.md#2-kiến-trúc-tổng-thể-clean-architecture-8-tầng) $\rightarrow$ Khuyên dùng cho **Slide 04**.
2. **Sơ đồ Thực Thể Quan Hệ ERD (14 DocTypes)**: Xem tại [`03_TECHNICAL_ARCHITECTURE.md`](file:///c:/Users/pc/Documents/Doan_CRM/presentation_source/03_TECHNICAL_ARCHITECTURE.md#3-mô-hình-dữ-liệu--quan-hệ-thực-thể-data-model--er-diagram) $\rightarrow$ Khuyên dùng cho **Slide Phụ lục 01**.
3. **Sơ đồ Tác Vụ Nền Scheduler & Tự Động Hóa**: Xem tại [`03_TECHNICAL_ARCHITECTURE.md`](file:///c:/Users/pc/Documents/Doan_CRM/presentation_source/03_TECHNICAL_ARCHITECTURE.md#5-tự-động-hóa--tác-vụ-nền-scheduler--background-jobs) $\rightarrow$ Khuyên dùng cho **Slide 12**.
4. **Sơ đồ Hành Trình Vòng Đời Khách Hàng (Customer Lifecycle 9 Bước)**: Xem tại [`02_BUSINESS_AND_CRM_ANALYSIS.md`](file:///c:/Users/pc/Documents/Doan_CRM/presentation_source/02_BUSINESS_AND_CRM_ANALYSIS.md#3-hành-trình-vòng-đời-khách-hàng-toàn-diện-customer-lifecycle) $\rightarrow$ Khuyên dùng cho **Slide 03**.

---

## 3. DANH MỤC SHOT CẦN CHỤP TRỰC TIẾP TỪ GIAO DIỆN (SCREENSHOT SHOT LIST)

Để hoàn thiện bài slide có sức thuyết phục cao nhất, sinh viên chỉ cần khởi chạy máy chủ xem trước (`python start_preview.py`) và chụp đúng **8 màn hình thực tế** theo danh mục chuẩn dưới đây:

| Mã Shot | Tên Màn Hình Cần Chụp | Địa Chỉ Truy Cập (URL / Tab) | Trạng Thái Giao Diện & Dữ Liệu Cần Hiển Thị | Vị Trí Slide Đề Xuất | Ghi Chú Bảo Mật (PII) |
|:---:|---|---|---|:---:|---|
| **SHOT-01** | **Bàn làm việc Desk Workspace** | `http://127.0.0.1:8080/desk` | Workspace `PetCare CRM` với 5 thẻ chỉ số nhanh (Shortcuts), banner và danh mục 5 phân hệ DocType. | **Slide 01** (Mở đầu) | Không có PII. |
| **SHOT-02** | **Tra cứu Hồ sơ Khách hàng 360** | `http://127.0.0.1:8080/` $\rightarrow$ `#tab-client` | Tìm khách `Nguyễn Văn An` (`0901234567`); hiển thị 2 bé cún (`Bơ` & `Đậu Đậu`) và Thẻ Bạc còn 1 lượt Grooming. | **Slide 06** (Đa thú cưng) | Che 3 số giữa của SĐT (`090***4567`). |
| **SHOT-03** | **Phễu Bán hàng Cơ hội (Kanban)** | Desk $\rightarrow$ `PetCare Opportunity` (Kanban View) | Bảng Kanban 6 cột giai đoạn; hiển thị thẻ của anh An ở cột *Proposal* và thẻ của chị Ngọc ở cột *Closed Won*. | **Slide 06** (Pipeline) | Dữ liệu demo an toàn. |
| **SHOT-04** | **Quầy POS Tiếp Nhận & Cấn Trừ Thẻ** | Web Portal $\rightarrow$ `#subview-pos-content` | Chọn khách An, bé Bơ, dịch vụ Grooming; ô đối soát hiện *Miễn phí theo Thẻ Bạc* và giá tiền nhảy về `0 VNĐ`. | **Slide 07** (Cấn trừ thẻ) | Dữ liệu demo an toàn. |
| **SHOT-05** | **Modal Thanh Toán VietQR Động** | Quầy POS $\rightarrow$ Chọn PTTT VietQR $\rightarrow$ Bấm Tạo QR | Cửa sổ Modal hiển thị mã VietQR Napas247, số tiền `450.000 VNĐ`, cú pháp `PC-SVC-SV-2026-00008`. | **Slide 09** (VietQR) | Số tài khoản demo an toàn. |
| **SHOT-06** | **Bảng Đề Xuất Chu Kỳ Care Intelligence** | Web Portal $\rightarrow$ `#tab-cycle` | Bảng phân loại 3 khối: Due Soon (bé Bơ), At Risk (bé Miu Miu), Renewal (bé Đậu Phộng); nút "Gọi Nhắc Lịch". | **Slide 08** (Care Engine) | Dữ liệu demo an toàn. |
| **SHOT-07** | **Báo Cáo Script Report 8 Chỉ Số KPI** | Desk $\rightarrow$ Report `PetCare KPI Overview` | Bảng báo cáo 8 dòng chỉ số; 3 thẻ màu tóm tắt (Lead Win Rate, Doanh Thu Thuần, Hội Viên Active). | **Slide 10** (Dashboard KPI) | Không có PII. |
| **SHOT-08** | **Console Đầu Ra 88/88 Test PASS** | Cửa sổ PowerShell | Chạy lệnh `python apps/petcare_crm/petcare_crm/tests/run_all_tests.py`; dòng tổng kết `88 / 88 Tests PASS (100.0%)`. | **Slide 12** (Kiểm thử) | Không có secret. |

---

## 4. HƯỚNG DẪN CHỤP ẢNH CHUẨN ĐỒ ÁN (SCREENSHOT BEST PRACTICES)

1. **Độ phân giải chuẩn**: Chụp màn hình ở độ phân giải tối thiểu Full HD (1920x1080) hoặc 2K để khi chiếu trên máy chiếu giảng đường không bị mờ hạt chữ.
2. **Tỷ lệ hiển thị**: Phóng to trình duyệt ở mức 100% hoặc 110% để các con số và nút bấm nổi bật rõ ràng.
3. **Cắt cúp gọn gàng**: Cắt bỏ thanh bookmark trình duyệt và thanh taskbar Windows cá nhân; chỉ lấy từ thanh Navbar của Desk/Portal trở xuống.
4. **Đồng bộ màu sắc thương hiệu**: Sử dụng bộ ảnh có chung giao diện sáng (Light Theme) với tông màu xanh ngọc chủ đạo (`#0d9488` Teal) của PetCare CRM để tạo sự chuyên nghiệp và nhất quán trên slide.
