# PETCARE CRM — GIỚI HẠN HIỆN TẠI & LỘ TRÌNH PHÁT TRIỂN (LIMITATIONS & FUTURE WORK)

> **Mã hồ sơ**: `LIMITS-ROADMAP-2026`  
> **Dự án**: PetCare CRM (Hệ thống CRM Dịch vụ Chăm sóc Thú cưng)  
> **Góc nhìn thẩm định**: Evidence Auditor & Academic Reviewer  
> **Ngày cập nhật**: 07/11/2026  
> **Tuyên ngôn trung thực học thuật**: Một đồ án tốt nghiệp xuất sắc là một đồ án dũng cảm nhìn nhận đúng ranh giới năng lực kỹ thuật của hệ thống, không che giấu lỗi và không thổi phồng thành quả vượt quá các bằng chứng có thể kiểm chứng trong repository.

---

## 1. BẢNG PHÂN LOẠI GIỚI HẠN KỸ THUẬT HIỆN TẠI (HONEST AUDIT TABLE)

| STT | Lĩnh Vực | Hiện Trạng Đã Đạt Được (Verified Reality) | Giới Hạn Kỹ Thuật Trung Thực (Honest Limitation) | Lý Do Khách Quan & Biện Pháp Giảm Thiểu |
|:---:|---|---|---|---|
| **01** | **Cổng Giao Tiếp Đa Kênh (Zalo ZNS / SMS)** | Đã hiện thực hóa kiến trúc Adapter đa kênh, mẫu tin nhắn ZNS, và cơ chế gửi tin qua [`omnichannel_service.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/utils/omnichannel_service.py). | Hoạt động ở **Chế độ Hộp Thư Đi An Toàn (Safe Mode Outbox)**; chưa nạp tiền cước viễn thông thật để gửi SMS/ZNS thực tế tới điện thoại. | Tránh phát sinh chi phí cước dịch vụ viễn thông không cần thiết trong quá trình làm đồ án và thử nghiệm của sinh viên. |
| **02** | **Cổng Thanh Toán & Webhook Ngân Hàng** | Đã hoàn thiện bộ sinh mã VietQR Napas247 động, xác thực chữ ký HMAC-SHA256 và cơ chế chống tấn công gửi lại (Replay Guard). | Webhook chạy ở **Chế độ Mô phỏng Kiểm thử (Sandbox Simulation)**; chưa ký hợp đồng tích hợp trực tiếp với cổng thanh toán NAPAS hoặc cổng trung gian thương mại (như PayOS, VNPay). | Các ngân hàng thương mại yêu cầu giấy phép kinh doanh của pháp nhân doanh nghiệp để cấp API kết nối trực tiếp. |
| **03** | **Môi Trường Kiểm Thử Tự Động (Testing)** | 88 bài test độc lập (10 Suites) đạt **100% PASS** trong thời gian ~2.34s qua bộ chạy `run_all_tests.py`. | 88 tests hiện tại chạy ở tầng **Pure Python Mock Adapter** trên Windows Host; các bài test live Frappe ORM (`test_crm_core.py`, v.v.) yêu cầu môi trường Docker Linux backend. | Frappe Framework v15 không hỗ trợ cài đặt native trên hệ điều hành Windows mà phải chạy qua WSL2 hoặc Docker. |
| **04** | **Thuật Toán Trí Tuệ Chăm Sóc (Care Engine)** | Thuật toán thống kê thực thụ (Tukey IQR + EWMA $\alpha=0.6$ + Hệ số mùa/tuổi) hoạt động chính xác và có thể giải thích toán học. | **Không sử dụng Machine Learning hay Deep Learning**; các ngưỡng phân loại (ví dụ: vắng $\ge 1.5\times$ là At Risk) là tham số cố định (Rule-Based Invariants). | Kích thước dữ liệu mẫu của đồ án (vài chục bản ghi) không đủ lớn để huấn luyện mạng nơ-ron; mô hình thống kê giải thích được phù hợp hơn với thực tế. |
| **05** | **Số Liệu Kinh Doanh & Báo Cáo Tài Chính** | Báo cáo 8 KPI chuẩn trên Desk UI và mô hình bảng tính chuyên sâu [`CLV_ABC_Model.xlsx`](file:///c:/Users/pc/Documents/Doan_CRM/deliverables/finance/CLV_ABC_Model.xlsx). | Các thông số như *Doanh thu 7,2 tỷ, Churn giảm từ 35% về 12%, CLV tăng 38%* là **Kịch bản mô phỏng tài chính (Simulation Scenario)**, không phải số liệu kế toán pháp nhân đã kiểm toán. | Đồ án tốt nghiệp đại học không thể có số liệu kinh doanh sổ sách thật của một doanh nghiệp thương mại hoạt động nhiều năm. |
| **06** | **Ứng Dụng Di Động Cho Chủ Nuôi (Mobile App)** | Đã cung cấp đầy đủ 6 REST APIs chuyên biệt bảo vệ BOLA/IDOR và giao diện Web Responsive xem trước trên di động. | **Chưa đóng gói thành ứng dụng di động Native (APK / iOS IPA)** trên chợ ứng dụng Google Play / App Store. | Nằm ngoài phạm vi của đồ án chuyên ngành CRM (yêu cầu trọng tâm là hệ thống CRM và các giao diện web desk/portal). |

---

## 2. CHUYỂN HÓA GIỚI HẠN THÀNH LỢI THẾ KHI BẢO VỆ ĐỒ ÁN

Khi gặp các câu hỏi từ hội đồng về các giới hạn trên, sinh viên hoàn toàn có thể biến điểm yếu thành điểm cộng về sự thấu đáo trong thiết kế kỹ thuật:

1. **Về Safe Mode Outbox**:
   * *Lập luận*: *"Việc cài đặt chế độ Safe Mode mặc định là một best practice trong kỹ nghệ phần mềm doanh nghiệp. Khi phát triển và chạy test hàng ngày, nếu hệ thống tự động bắn SMS/Zalo thật ra ngoài thì sẽ làm phiền đến khách hàng thật và gây lãng phí tài chính. Safe Mode Outbox giúp nhóm em kiểm tra chính xác 100% nội dung và cú pháp tin nhắn trước khi bật cờ chuyển sang môi trường Production."*
2. **Về Thuật toán Rule-Based thống kê thay vì Deep Learning**:
   * *Lập luận*: *"Nhóm em chủ động lựa chọn mô hình thống kê minh bạch (Explainable Statistics) vì tính ứng dụng thực tế. Với một chuỗi phòng khám thú y, việc giải thích được cho nhân viên CSKH hiểu 'tại sao hệ thống lại gợi ý khách này' quan trọng hơn rất nhiều so với một mô hình AI hộp đen khó hiểu. Thuật toán EWMA và Tukey IQR hoàn toàn đáp ứng được tính chính xác mà tiêu tốn cực ít tài nguyên máy chủ."*
3. **Về Bộ kiểm thử Mock Adapter chạy trên Windows**:
   * *Lập luận*: *"Nhóm em đã tốn rất nhiều tâm huyết để xây dựng tầng Adapter `frappe_adapters.py`. Nhờ tầng trừu tượng này, bất kỳ thầy cô nào trong hội đồng sử dụng máy tính Windows cá nhân chỉ cần cài Python là có thể chạy nghiệm thu toàn bộ 88 bài test trong 2 giây mà không cần cài đặt Docker hay cấu hình cụm máy chủ MariaDB phức tạp."*

---

## 3. LỘ TRÌNH PHÁT TRIỂN TƯƠNG LAI (STRATEGIC ROADMAP)

Dự án được định hướng phát triển thương mại hóa qua **3 giai đoạn chiến lược**:

```
[ LỘ TRÌNH NÂNG CẤP PETCARE CRM (2026 - 2028) ]
│
├── GIAI ĐOẠN 1: PRODUCTION READY & FINTECH (Q1 - Q2/2027)
│    ├── Ký kết hợp đồng đối soát tự động với PayOS / VNPay qua cổng thanh toán thật.
│    ├── Đăng ký Zalo Official Account (OA) có tích xanh và tích hợp Zalo ZNS thực tế.
│    └── Triển khai kiến trúc Multi-Tenant SaaS cho phép nhiều chuỗi phòng khám dùng chung.
│
├── GIAI ĐOẠN 2: OMNICHANNEL & NATIVE MOBILE APP (Q3 - Q4/2027)
│    ├── Đóng gói ứng dụng di động PetCare Owner Portal bằng Flutter (iOS & Android).
│    ├── Tích hợp tổng đài ảo VoIP Cloud (nhận diện cuộc gọi khách hàng và mở pop-up 360).
│    └── Tích hợp camera AI nhận diện khuôn mặt thú cưng tự động check-in tại quầy lễ tân.
│
└── GIAI ĐOẠN 3: IOT VETERINARY & CLINICAL INTELLIGENCE (2028)
     ├── Kết nối chuẩn HL7 / DICOM với máy xét nghiệm máu và máy siêu âm thú y tại phòng khám.
     ├── Ứng dụng mô hình Machine Learning dự đoán nguy cơ béo phì và bệnh ngoài da dựa trên lịch sử cân nặng.
     └── Mở rộng module quản trị chuỗi cung ứng thuốc thú y và vật tư tiêu hao kết nối với ERPNext.
```
