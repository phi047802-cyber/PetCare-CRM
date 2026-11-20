# PETCARE CRM — PRESENTATION SOURCE DOSSIER (BỘ HỒ SƠ NGUỒN BẢO VỆ ĐỒ ÁN)

> **Dự án**: PetCare CRM — Nền tảng Quản trị Quan hệ Khách hàng Chuyên biệt cho Chuỗi Dịch vụ Chăm sóc Thú cưng  
> **Nền tảng công nghệ**: Frappe Framework v15 (Python 3.10+, MariaDB 11.x, Desk Native & Dual-Stack Preview Engine)  
> **Phiên bản hồ sơ**: 2.0 (Verified Final Release)  
> **Đơn vị thẩm định**: Interdisciplinary Review Board (CRM Solution Architect, Frappe Technical Analyst, Business Analyst, Academic Researcher, Evidence Auditor)  
> **Ngày lập hồ sơ**: 07/11/2026  
> **Trạng thái thẩm định**: 100% đối chiếu trực tiếp từ mã nguồn thực tế, schema cơ sở dữ liệu và kết quả thực thi kiểm thử.

---

## 1. MỤC ĐÍCH & Ý NGHĨA CỦA BỘ HỒ SƠ NGUỒN

Bộ hồ sơ nguồn **Presentation Source Dossier** được xây dựng nhằm cung cấp một kho dữ liệu minh chứng có cấu trúc, chuẩn xác và trung thực tuyệt đối, phục vụ cho việc:
1. **Thiết kế Slide Báo cáo & Thuyết trình**: Cung cấp cấu trúc Storyline 13 slide chính + phụ lục, từng thông điệp cốt lõi, bullet points ngắn gọn, sơ đồ trực quan và trích dẫn bằng chứng cụ thể.
2. **Kịch bản Trình diễn Phần mềm (Live Demo Script)**: Hướng dẫn chi tiết từng bước thao tác theo 3 câu chuyện xuyên suốt, chuẩn bị dữ liệu mẫu và phương án dự phòng khi gặp sự cố.
3. **Bộ Câu hỏi & Trả lời Phản biện (Defense Q&A)**: Cung cấp lập luận kỹ thuật, căn cứ nghiệp vụ và bằng chứng mã nguồn để giải đáp các câu hỏi hóc búa từ hội đồng chấm đồ án.
4. **Kiểm toán Minh chứng (Evidence Audit)**: Truy vết mọi tuyên bố về chức năng, số liệu kiểm thử, API và DocType về đúng file, hàm và dòng code trong repository.

---

## 2. THỨ TỰ ĐỌC VÀ CẤU TRÚC HỒ SƠ

Để nắm bắt toàn diện dự án theo từng góc nhìn, người dùng nên đọc các tài liệu theo thứ tự được khuyến nghị dưới đây:

```
[ THỨ TỰ KHÁM PHÁ HỒ SƠ NGUỒN ]
│
├── BƯỚC 1: TỔNG QUAN VÀ ĐỊNH VỊ
│    ├── 00_PROJECT_EXECUTIVE_BRIEF.md       (Bản tóm lược điều hành 2 trang, thang đo giá trị cốt lõi)
│    └── 01_PROJECT_FACTS_AND_EVIDENCE.md     (Bảng tổng mục minh chứng, kiểm toán số liệu thực tế)
│
├── BƯỚC 2: NGHIỆP VỤ & KIẾN TRÚC KỸ THUẬT
│    ├── 02_BUSINESS_AND_CRM_ANALYSIS.md     (Customer Lifecycle, chân dung người dùng, 10 phân hệ nghiệp vụ)
│    └── 03_TECHNICAL_ARCHITECTURE.md        (Clean Architecture 8 tầng, Data Model 14 DocTypes, 53 APIs, Bảo mật)
│
├── BƯỚC 3: VẬN HÀNH, BÁO CÁO & DEMO
│    ├── 04_FEATURES_AND_DEMO_CATALOG.md     (Danh mục chi tiết 10 tính năng demo thực tế)
│    ├── 05_DASHBOARD_KPI_AND_BUSINESS_INSIGHTS.md (8 chỉ số KPI chuẩn, báo cáo đa chi nhánh & mô hình CLV/ABC)
│    └── 07_DEMO_AND_QA_SCRIPT.md            (Kịch bản demo 3 câu chuyện & 12 câu hỏi phản biện bảo vệ)
│
├── BƯỚC 4: THIẾT KẾ SLIDE & TÀI SẢN TRỰC QUAN
│    ├── 06_SLIDE_STORYLINE_AND_OUTLINE.md   (Kịch bản 13 slide thuyết trình chuẩn 10-12 phút)
│    └── 08_VISUAL_ASSET_INVENTORY.md        (Bản kiểm kê sơ đồ BPMN có sẵn và Shot List cần chụp)
│
└── BƯỚC 5: TRUNG THỰC HỌC THUẬT & TRA CỨU SÂU
     ├── 09_LIMITATIONS_AND_FUTURE_WORK.md   (Giới hạn kỹ thuật, phân tách Real vs Mock, lộ trình tương lai)
     └── 10_APPENDIX_TECHNICAL_QA.md         (Bảng tra cứu 14 DocTypes, 53 APIs, ma trận phân quyền RBAC & thuật ngữ)
```

---

## 3. QUY ƯỚC MÃ ĐỊNH DANH MINH CHỨNG (CLAIM ID CONVENTION)

Mọi tuyên bố trong bộ hồ sơ đều được gán mã định danh duy nhất (Claim ID) để phục vụ việc truy vết chéo giữa Slide thuyết trình, Báo cáo và Mã nguồn:

| Tiền tố mã | Nhóm lĩnh vực | Ví dụ | Ý nghĩa |
|:---:|---|---|---|
| `CRM-xxx` | Nghiệp vụ CRM & Vòng đời khách hàng | `CRM-001` | Tính toàn vẹn của hồ sơ khách hàng và thú cưng (Multi-Pet) |
| `TECH-xxx` | Kiến trúc kỹ thuật & Framework Frappe | `TECH-002` | Kiến trúc Clean Architecture 8 tầng và DocType Controller |
| `DATA-xxx` | Mô hình dữ liệu & Cơ sở dữ liệu MariaDB | `DATA-001` | Khóa ngoại $1:N$ giữa Contact và Pet |
| `API-xxx` | Giao diện lập trình whitelisted & Webhook | `API-003` | Xác thực chữ ký HMAC-SHA256 trên Payment Webhook |
| `CARE-xxx` | Trí tuệ chăm sóc & Giữ chân khách hàng | `CARE-001` | Thuật toán lọc ngoại lai Tukey IQR kết hợp trung bình động EWMA |
| `MEM-xxx` | Hội viên, Thẻ trả trước & Sổ cái quyền lợi | `MEM-002` | Khóa dòng Pessimistic Row Lock (`FOR UPDATE`) chống trừ trùng lặp |
| `TEST-xxx` | Kiểm thử tự động & Báo cáo QA | `TEST-001` | Bộ kiểm thử tự động 88/88 tests PASS 100% trong ~2.3s |
| `FIN-xxx` | Quản trị tài chính, CLV & Giá thành ABC | `FIN-001` | Bảng phân bổ 4 Cost Pools và chiết khấu dòng tiền DCF |

---

## 4. BẢNG TỔNG KẾT TRẠNG THÁI KIỂM TOÁN MINH CHỨNG (AUDIT STATUS SUMMARY)

| Hạng mục kiểm toán | Con số trong tài liệu cũ | Hiện trạng thực tế đã kiểm chứng | Trạng thái xác minh | File minh chứng gốc |
|---|:---:|:---:|:---:|---|
| **Tổng số DocTypes** | 11 hoặc 13 | **14 DocTypes** (12 Regular + 2 Child Tables) | `VERIFIED` | [`apps/petcare_crm/petcare_crm/petcare_crm/doctype/`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/petcare_crm/doctype/) |
| **Whitelisted API Endpoints** | 47 hoặc 48 | **53 Whitelisted Functions** | `VERIFIED` | [`apps/petcare_crm/petcare_crm/api.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/api.py) |
| **Số bài kiểm thử tự động** | 58 hoặc 68 | **88 / 88 Tests PASS (100.0%)** | `VERIFIED` | [`apps/petcare_crm/petcare_crm/tests/run_all_tests.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/tests/run_all_tests.py) |
| **Thời gian thực thi Test** | 1.6s | **2.34s** (trên máy chủ Windows hiện tại) | `VERIFIED` | Chạy lệnh `python run_all_tests.py` |
| **Số vai trò người dùng (Roles)** | 5 vai trò | **7 Vai trò chuẩn Frappe** (6 Desk + 1 Portal) | `VERIFIED` | [`apps/petcare_crm/petcare_crm/setup/install.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/setup/install.py) |
| **Chỉ số KPI Quản trị** | 8 KPI | **8 Chỉ số KPI chuẩn + Phân tích Đa chi nhánh** | `VERIFIED` | [`apps/petcare_crm/petcare_crm/utils/analytics_service.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/utils/analytics_service.py) |
| **Tích hợp Webhook & VietQR** | Ý tưởng/Đề xuất | **Đã triển khai đầy đủ với HMAC & Idempotency** | `VERIFIED` (Logic/Mock) | [`apps/petcare_crm/petcare_crm/utils/payment_gateway.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/utils/payment_gateway.py) |
| **Đề xuất khác biệt Care Intelligence** | AI / Machine Learning | **Thống kê Rule-Based (EWMA + Tukey IQR + Mùa vụ)** | `VERIFIED` | [`apps/petcare_crm/petcare_crm/utils/care_pattern_service.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/utils/care_pattern_service.py) |
| **Dữ liệu kinh doanh sổ sách** | Tăng trưởng 38%, v.v. | **Dữ liệu Seed Demo & Kịch bản Mô phỏng Tài chính** | `SIMULATION` | [`patches/v1_0/seed_demo_data.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/patches/v1_0/seed_demo_data.py) & [`CLV_ABC_Model.xlsx`](file:///c:/Users/pc/Documents/Doan_CRM/deliverables/finance/CLV_ABC_Model.xlsx) |

---

## 5. CAM KẾT VỀ TÍNH CHÂN THỰC VÀ BẢO TOÀN MÃ NGUỒN

1. **Bảo toàn sản phẩm**: Toàn bộ mã nguồn, schema cơ sở dữ liệu và cấu hình hệ thống không bị chỉnh sửa hay làm sai lệch trong quá trình lập hồ sơ.
2. **Không bịa đặt số liệu**: Tuyệt đối không tự suy diễn các số liệu về tỷ lệ chuyển đổi, doanh thu thực tế hoặc tuyên bố bảo mật tuyệt đối. Các số liệu minh họa tài chính đều được dán nhãn `KỊCH BẢN MÔ PHỎNG (Simulation)`.
3. **Minh bạch về giới hạn**: Công khai rõ ràng ranh giới giữa kiểm thử Mock độc lập (chạy được ngay trên Windows) và kiểm thử Frappe Live (yêu cầu Docker container), cũng như cơ chế Safe Mode Outbox cho các cổng giao tiếp bên ngoài (Zalo ZNS, SMS, Webhook ngân hàng).
