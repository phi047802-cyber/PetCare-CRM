# KẾ HOẠCH BÀN GIAO & MA TRẬN TRACEABILITY ĐỒ ÁN PETCARE CRM

> **Dự án**: PetCare CRM (Hệ Thống CRM Dịch Vụ Chăm Sóc Thú Cưng)  
> **Nền tảng**: Frappe Framework v15  
> **Ngày lập kế hoạch**: 27/10/2026  
> **Tài liệu căn cứ**: `docs/AUDIT_BASELINE.md` & `Tiêu chí đồ án môn học CRM (cập nhật ngày 23_11_2025).pdf`  
> **Trạng thái tài liệu**: Bản kế hoạch hành động chốt để nghiệm thu (Chưa sửa mã nguồn ứng dụng)  

---

## 1. PHÂN LOẠI CÁC NHÓM YÊU CẦU (REQUIREMENT CLASSIFICATION)

Để đảm bảo tính trung thực và không đánh đồng các nguồn thông tin theo Nguyên tắc 3, toàn bộ yêu cầu đồ án được phân chia độc lập thành **3 nhóm riêng biệt**:

### Nhóm I: Bắt buộc đã xác minh (Từ giảng viên học kỳ hiện tại)
* **REQ-M01**: Xây dựng hệ thống CRM hoàn chỉnh, bao quát vòng đời khách hàng từ khâu tiếp cận Lead, Bán hàng, Vận hành dịch vụ, Hội viên đến Chăm sóc giữ chân định kỳ (không chỉ làm 2 module riêng lẻ).
* **REQ-M02**: Vận hành trên nền tảng **Frappe Framework v15** (thay vì Odoo), sử dụng Frappe Desk Native UI, DocTypes, Whitelisted APIs và MariaDB.
* **REQ-M03**: Logic nghiệp vụ được viết theo hướng đối tượng (OOP), có thể kiểm thử độc lập, có cơ chế phân quyền bảo mật (RBAC) và an toàn giao dịch tài chính.

### Nhóm II: Tham chiếu Rubric cũ (Tệp PDF ngày 23/11/2025)
*Ghi chú: Ánh xạ tương đương từ Odoo sang Frappe Framework v15.*
* **REQ-R01 (A4.1)**: Mô tả Case Study chi tiết (bối cảnh, quy mô, chân dung khách hàng, vấn đề nghiệp vụ).
* **REQ-R02 (A4.2)**: Cấu hình CRM & Nhập liệu căn bản (tiền tệ VNĐ, phân quyền Users/Roles, Sales Teams, Pipeline stages, lý do thất bại, chứng minh dùng nhiều).
* **REQ-R03 (A4.3.1)**: Quy trình CRM nhóm điển hình xuyên suốt các phòng ban (file `.bpmn` Camunda + file `.png` + mô tả).
* **REQ-R04 (A4.3.2)**: Quy trình CRM cá nhân độc lập cho từng thành viên (file `.bpmn` Camunda + file `.png` + mô tả).
* **REQ-R05 (A4.4)**: Thao tác sử dụng phần mềm qua Video cá nhân (quay màn hình có mặt và giọng nói, chứng minh tự cài đặt và chạy quy trình).
* **REQ-R06 (A4.5)**: Chuyên đề Quản lý chi phí, Giá trị vòng đời khách hàng (CLV) và Kế toán chi phí theo hoạt động (Activity-based Costing - ABC).
* **REQ-R07 (A4.6)**: Đọc hiểu báo cáo CRM/Sales với các biểu đồ trực quan, phân nhóm theo team/tháng/chi nhánh.
* **REQ-R08 (A4.7)**: Khám phá và gọi API/Webhook (file nhóm khám phá API & Webhook; file cá nhân gọi API riêng biệt có cURL/Postman).
* **REQ-R09 (A4.8)**: Tích hợp Lead Form thu thập khách hàng tiềm năng từ website WordPress về CRM.
* **REQ-R10 (A4.9.1)**: Thuyết minh Module chức năng hữu ích tùy biến chuyên sâu kèm mã nguồn ZIP.
* **REQ-R11 (A4.9.2)**: Thuyết minh Module Báo cáo quản trị kèm mã nguồn ZIP.
* **REQ-R12 (A4.10)**: Thuyết minh Các đề xuất & hiện thực hóa khác biệt mang lại giá trị thực tế cho khách hàng.

### Nhóm III: Khuyến nghị nâng chất lượng (Best Practices đồ án xuất sắc)
* **REQ-Q01**: Bộ kiểm thử tự động toàn diện (Automated Testing) với Master Test Runner đạt tỷ lệ Pass 100% (hiện đã đạt 68/68 tests).
* **REQ-Q02**: Thanh toán mã QR động VietQR theo chuẩn Napas247 QuickLink và Webhook đối soát IPN tự động có khóa Idempotency.
* **REQ-Q03**: Động cơ Trí tuệ chăm sóc (Care Intelligence) có giải thích thuật toán (Explainability) kết hợp hệ số mùa vụ và độ tuổi thú cưng.
* **REQ-Q04**: Điều phối thông báo đa kênh (Omnichannel) hỗ trợ Zalo ZNS, SMS Brandname và Email ở chế độ Safe Mode Outbox Preview an toàn.
* **REQ-Q05**: Bộ REST APIs chuyên biệt phục vụ Ứng dụng Di động Chủ nuôi (Pet Owner Mobile App).

---

## 2. ĐỊNH NGHĨA HOÀN THÀNH CHUNG (DEFINITION OF DONE - DoD)

Một hạng mục chỉ được đánh dấu là **HOÀN THÀNH (DONE)** khi thỏa mãn đầy đủ 6 điều kiện tiên quyết sau:

1. **Có tệp vật lý tồn tại**: Tệp đầu ra phải được tạo đúng đường dẫn và tên tệp quy định trong rubric (không chỉ mô tả bằng lời).
2. **Khả năng mở / thực thi độc lập**:
   * Tệp `.bpmn` phải mở thành công trên phần mềm **Camunda Modeler Desktop** (phiên bản $\ge 5.0$), không lỗi cú pháp XML, hiển thị đầy đủ Pools, Lanes, Tasks, Gateways.
   * Tệp mã nguồn Python/JS phải chạy được, không lỗi cú pháp, vượt qua linter/test runner.
   * Tệp Word/Markdown phải định dạng chuẩn mực, mục lục rõ ràng.
3. **Có minh chứng kiểm chứng**: Có ảnh chụp màn hình thực tế (Desk UI, kết quả chạy lệnh terminal, request/response Postman) hoặc log kiểm thử xác thực.
4. **Không chứa Secret / Dữ liệu nhạy cảm**: Tuyệt đối không hard-code API token bí mật, private key, mật khẩu quản trị hoặc số tài khoản cá nhân.
5. **Số liệu đồng nhất 100% với mã nguồn**: Toàn bộ số DocType (13), số API (48), số kịch bản test (68), tên trường dữ liệu và công thức trong báo cáo phải khớp chính xác với codebase thực tế.
6. **Kiểm tra chéo và nghiệm thu độc lập**: Có lệnh hoặc quy trình cụ thể để người khác có thể tự tái lập kết quả trên máy tính của họ.

---

## 3. MA TRẬN TRACEABILITY (TRUY XUẤT NGUỒN GỐC YÊU CẦU ĐẾN BÀN GIAO)

| Mã Tiêu Chí | Nhóm Yêu Cầu | Nguồn Yêu Cầu + Mục | Hạng Mục Triển Khai | File / Minh Chứng Đầu Ra | Cách Kiểm Tra / Tiêu Chí Nghiệm Thu | Trạng Thái Hiện Tại | Phụ Trách (Placeholder) |
|---|:---:|---|---|---|---|:---:|:---:|
| **A4.1** | Nhóm II | Rubric 2025, Trang 1 | Báo cáo Case Study PetCare CRM | `Report - Nhóm XX.docx` (Chương 1) | Đọc tài liệu: Có bối cảnh ngành thú cưng, quy mô chuỗi phòng khám, 3 buyer personas, ma trận nỗi đau & giải pháp. | **Gap** (Đã có bản MD, chưa có DOCX) | `[Thành viên 1]` |
| **A4.2.1** | Nhóm II | Rubric 2025, Trang 1 | Minh chứng Thiết lập & Cấu hình CRM | `Report - Nhóm XX.docx` (Chương 2) + Ảnh chụp Desk UI | Kiểm tra ảnh chụp: Tiền tệ VNĐ, 5 Roles RBAC, Sales stages, lý do thất bại, email safe mode. | **Gap** (Hệ thống đã có, chưa chụp ảnh) | `[Thành viên 2]` |
| **A4.2.2** | Nhóm II | Rubric 2025, Trang 1 | Nhập liệu mẫu phong phú | `Report - Nhóm XX.docx` (Chương 2) + Dữ liệu DB | Chạy script seed data: có 100+ bản ghi Contacts, Pets, Visits, Memberships, Recs. | **Verified** (Đã có seed script) | `[Thành viên 2]` |
| **A4.3.1** | Nhóm II | Rubric 2025, Trang 1 | Sơ đồ Quy trình CRM Nhóm Điển hình | `deliverables/bpmn/group/PetCare_CRM_End_to_End_Group.bpmn`<br>`deliverables/bpmn/group/PetCare_CRM_End_to_End_Group.png`<br>`deliverables/bpmn/group/PetCare_CRM_End_to_End_Group_Explanation.docx` | Mở file `.bpmn` bằng Camunda Modeler: Có 5 Lanes (Khách, Marketing/Sales, Lễ tân, Bác sĩ/Kỹ thuật, Hệ thống CRM tự động). 100% có BPMN DI. | **ĐÃ HOÀN THÀNH (DONE)** | `[Thành viên 1]` |
| **A4.3.2** | Nhóm II | Rubric 2025, Trang 1 | Sơ đồ Quy trình CRM Cá nhân (4 TV) | `deliverables/bpmn/individual/member_[1-4]/`<br>Mỗi TV: 1 file `.bpmn` + 1 file `.png` + 1 file `.docx` + 1 file `.md` | Mở từng file `.bpmn` trên Camunda: Mỗi bạn 1 quy trình độc lập không trùng lặp (FLOW-01, FLOW-02, FLOW-05, FLOW-07/08). 100% có BPMN DI. | **ĐÃ HOÀN THÀNH (DONE)** | `[Cả 4 Thành viên]` |
| **A4.4** | Nhóm II | Rubric 2025, Trang 1 | Video Thao tác CRM Cá nhân | `Video: Thao tác CRM - MSSV - [Họ tên].mp4` + Storyboard Word | Xem video: 5-7 phút, có mặt và giọng nói, quay trang Admin Desk và thực hiện trọn vẹn quy trình cá nhân. | **Gap Blocker** (P1) (Cần Storyboard) | `[Cả 4 Thành viên]` |
| **A4.5** | Nhóm II | Rubric 2025, Trang 1 | Chuyên đề CLV & Kế toán chi phí ABC | `deliverables/finance/`<br>• `CLV_ABC_Model.xlsx` (5 sheets động)<br>• `PetCare_CRM_CLV_ABC_Report.docx`<br>• `PetCare_CRM_CLV_ABC_Report.md` | Kiểm tra tài liệu & bảng tính: Công thức DCF 5 năm, 4 Cost Pools & Drivers ABC, 3 kịch bản kinh doanh, phân tích độ nhạy 2 chiều, giải quyết hộ đa thú cưng. | **ĐÃ HOÀN THÀNH (DONE)** | `[Thành viên 3]` |
| **A4.6** | Nhóm II | Rubric 2025, Trang 1 | Đọc hiểu Báo cáo Quản trị & Sales | `Report - Nhóm XX.docx` (Chương 5) | Kiểm tra biểu đồ: Phễu Lead, Doanh thu chi nhánh, Cơ cấu gói hội viên, Tỷ lệ tái khám Care Retention kèm bài phân tích hành động. | **Gap** (Đã có KPI code, chưa xuất biểu đồ) | `[Thành viên 4]` |
| **A4.7.1** | Nhóm II | Rubric 2025, Trang 1 | Khám phá API & Webhook (Nhóm) | `deliverables/api/`<br>• `API_INVENTORY.md` (48 APIs)<br>• `PetCare_CRM_API_Specification_Group.docx`<br>• `WEBHOOK_SECURITY_AND_TEST_GUIDE.md`<br>• `PetCare_CRM_API_Collection.postman_collection.json` | Kiểm tra tài liệu: Cơ chế Auth Token/Cookie, đặc tả 48 APIs, giải thích cURL `create_lead` và Webhook IPN VietQR (HMAC-SHA256, Idempotency). | **ĐÃ HOÀN THÀNH (DONE)** | `[Thành viên 1]` |
| **A4.7.2** | Nhóm II | Rubric 2025, Trang 1 | Thực thi Gọi API Cá nhân (4 TV) | `deliverables/api/PetCare_CRM_API_Specification_Individual_Template.docx` và `.md` | Kiểm tra tài liệu cá nhân: 4 API độc lập (`create_lead`, `create_opportunity`, `record_pet_service_visit`, `send_omnichannel_notification`), cURL, JSON body và checklist ảnh Postman. | **ĐÃ HOÀN THÀNH (DONE)** | `[Cả 4 Thành viên]` |
| **A4.8** | Nhóm II | Rubric 2025, Trang 1 | Tích hợp Lead Form WordPress | `deliverables/wordpress/`<br>• Plugin `petcare-lead-capture.zip`<br>• Standalone Form HTML<br>• `README_WORDPRESS_LEAD_FORM.md`<br>• `VERIFICATION_AND_EVIDENCE_CHECKLIST.md` | Điền form trên WordPress/Standalone -> Server-to-Server Proxy cURL -> Frappe CRM tạo Lead thành công. Đã có 6/6 integration tests pass. | **ĐÃ HOÀN THÀNH (DONE)** | `[Thành viên 2]` |
| **A4.9.1** | Nhóm II | Rubric 2025, Trang 1 | Thuyết minh Module Chức năng PetCare | `Module PetCare CRM - Nhóm XX.docx` + `PetCare_CRM_Code.zip` | Đọc tài liệu: Thuyết minh kiến trúc Clean Architecture, 11 DocTypes, tính năng VietQR, Zalo ZNS, Membership Ledger. | **Gap** (Code đã có, cần đóng gói) | `[Thành viên 1]` |
| **A4.9.2** | Nhóm II | Rubric 2025, Trang 1 | Thuyết minh Module Báo cáo KPI | `Module Reporting - Nhóm XX.docx` + `Reporting_Code.zip` | Đọc tài liệu: Thuyết minh `AnalyticsService`, 8 chỉ số KPI, phân tích so sánh đa chi nhánh. | **Gap** (Code đã có, cần đóng gói) | `[Thành viên 4]` |
| **A4.10** | Nhóm II | Rubric 2025, Trang 1 | Thuyết minh Đề xuất Khác biệt | `A4-10 - Giai phap Care Intelligence va VietQR Tu dong - Nhóm XX.docx` | Kiểm tra tài liệu: Lập luận giá trị của Care Intelligence theo mùa vụ/độ tuổi, Dynamic VietQR IPN, và Owner Portal. | **Gap Blocker** (P0) | `[Thành viên 3]` |
| **REQ-M01** | Nhóm I | Giảng viên 2026 | CRM hoàn chỉnh đa phân hệ | Codebase `apps/petcare_crm/` | Chạy 74 tests tự động: Bao quát trọn vẹn Lead, Deal, Visit, Membership, Care Scan, WordPress Integration. | **Verified** (74/74 tests PASS) | `[Cả nhóm]` |
| **REQ-Q01** | Nhóm III | Best Practice | Kiểm thử tự động 100% Pass | `apps/petcare_crm/petcare_crm/tests/run_all_tests.py` | Chạy lệnh `python apps/petcare_crm/petcare_crm/tests/run_all_tests.py`: 74 tests đạt kết quả OK (100% Pass). | **Verified** (100% Pass) | `[Thành viên 1]` |

---

## 4. DANH MỤC TỆP BÀN GIAO DỰ KIẾN (DELIVERABLES INVENTORY)

```
THƯ MỤC BÀN GIAO ĐỒ ÁN (DELIVERY ARTIFACTS):
├── 📄 README_NGHIEM_THU.md                                  # Hướng dẫn chạy và nghiệm thu đồ án độc lập
├── 📁 01_BAO_CAO_CHINH/
│   └── Report - Nhóm XX.docx                                # Báo cáo tổng hợp (A4.1, A4.2, A4.5, A4.6)
├── 📁 02_QUY_TRINH_BPMN_CAMUNDA/
│   ├── Quy trinh CRM Tong the - Nhom XX.bpmn                # Sơ đồ BPMN 2.0 XML nhóm (A4.3.1)
│   ├── Quy trinh CRM Tong the - Nhom XX.png                 # Ảnh xuất nét cao từ Camunda Modeler
│   ├── Quy trinh Tiep nhan Lead - MSSV1 - [Ten TV1].bpmn    # BPMN cá nhân 1 (A4.3.2)
│   ├── Quy trinh Tiep nhan Lead - MSSV1 - [Ten TV1].png     # Ảnh xuất cá nhân 1
│   ├── Quy trinh Tiep nhan Lead - MSSV1 - [Ten TV1].docx    # Mô tả quy trình cá nhân 1
│   ├── Quy trinh Dich vu & Thanh toan - MSSV2 - [Ten TV2].bpmn # BPMN cá nhân 2
│   ├── Quy trinh Dich vu & Thanh toan - MSSV2 - [Ten TV2].png
│   ├── Quy trinh Dich vu & Thanh toan - MSSV2 - [Ten TV2].docx
│   ├── Quy trinh The Hoi vien & Vi - MSSV3 - [Ten TV3].bpmn    # BPMN cá nhân 3
│   ├── Quy trinh The Hoi vien & Vi - MSSV3 - [Ten TV3].png
│   ├── Quy trinh The Hoi vien & Vi - MSSV3 - [Ten TV3].docx
│   ├── Quy trinh Care Intelligence - MSSV4 - [Ten TV4].bpmn    # BPMN cá nhân 4
│   ├── Quy trinh Care Intelligence - MSSV4 - [Ten TV4].png
│   └── Quy trinh Care Intelligence - MSSV4 - [Ten TV4].docx
├── 📁 03_TAI_LIEU_API/
│   ├── File Tim hieu API - Nhom XX.docx                     # Tài liệu khám phá API & Webhook nhóm (A4.7)
│   ├── File API - MSSV1 - [Ten TV1].docx                    # API Cá nhân 1 (create_lead)
│   ├── File API - MSSV2 - [Ten TV2].docx                    # API Cá nhân 2 (record_pet_service_visit)
│   ├── File API - MSSV3 - [Ten TV3].docx                    # API Cá nhân 3 (record_benefit_usage)
│   └── File API - MSSV4 - [Ten TV4].docx                    # API Cá nhân 4 (predict_next_service)
├── 📁 04_LEAD_FORM_WORDPRESS/
│   ├── index.html                                           # Giao diện Form đặt lịch / tư vấn thú cưng (A4.8)
│   ├── style.css                                            # CSS giao diện PetCare chuẩn mobile
│   ├── petcare-lead-connector.js                            # Script AJAX POST kết nối API create_lead
│   └── HUONG_DAN_CAI_DAT_WORDPRESS.docx                     # Hướng dẫn nhúng vào trang WordPress
├── 📁 05_THUYET_MINH_MODULE_VA_DE_XUAT/
│   ├── Module PetCare CRM - Nhom XX.docx                    # Thuyết minh module tùy biến chuyên sâu (A4.9.1)
│   ├── Module Reporting - Nhom XX.docx                      # Thuyết minh module báo cáo KPI (A4.9.2)
│   └── A4-10 - Giai phap Care Intelligence va VietQR Tu dong - Nhom XX.docx # Đề xuất khác biệt (A4.10)
├── 📁 06_KICH_BAN_VIDEO_THAO_TAC/
│   ├── Video_Script_Huong_Dan_Chung.docx                    # Hướng dẫn kỹ thuật quay màn hình chuẩn
│   ├── Storyboard - MSSV1 - [Ten TV1].docx                  # Kịch bản chi tiết từng phút cho TV1 (A4.4)
│   ├── Storyboard - MSSV2 - [Ten TV2].docx                  # Kịch bản chi tiết cho TV2
│   ├── Storyboard - MSSV3 - [Ten TV3].docx                  # Kịch bản chi tiết cho TV3
│   └── Storyboard - MSSV4 - [Ten TV4].docx                  # Kịch bản chi tiết cho TV4
└── 📁 07_MA_NGUON_DONG_GOI_ZIP/
    └── PetCare_CRM_v2_Full_SourceCode.zip                   # Toàn bộ mã nguồn sạch của ứng dụng
```

---

## 5. KẾ HOẠCH TRIỂN KHAI THEO PHỤ THUỘC & ĐỘ KHÓ TƯƠNG ĐỐI

Các công việc được sắp xếp theo thứ tự **ràng buộc phụ thuộc kỹ thuật** (công việc sau dùng dữ liệu/tài liệu của công việc trước):

| STT | Gói Công Việc (Work Package) | Độ Khó (S/M/L) | Điều Kiện Đầu Vào (Inputs) | Rủi Ro & Thách Thức Kỹ Thuật | Phụ Trách (Placeholder) |
|:---:|---|:---:|---|---|:---:|
| **WP1** | **Xây dựng Sơ đồ BPMN Camunda XML (A4.3)**<br>• Tạo 1 BPMN Nhóm + 4 BPMN Cá nhân chuẩn XML.<br>• Xuất 5 ảnh PNG độ phân giải cao.<br>• Tạo 5 file Word (.docx) và Markdown thuyết minh chi tiết. | **M**<br>(Vừa) | Sơ đồ luồng trong `docs/PROCESS_FLOWS.md` | Lỗi cú pháp namespace Camunda nếu vẽ sai chuẩn BPMN 2.0; sơ đồ thiếu tính liên phòng ban (Lanes). *(Đã hoàn thành 100% không lỗi)* | **ĐÃ HOÀN THÀNH**<br>(Deliverables sẵn sàng) |
| **WP2** | **Xây dựng Lead Form nhúng WordPress (A4.8)**<br>• Code Plugin WordPress `petcare-lead-capture.zip` có Shortcode & Proxy REST API.<br>• Form HTML/CSS/JS độc lập, bảo mật Zero Secret và Honeypot.<br>• Bộ test tự động 6 kịch bản integration pass 100%. | **S**<br>(Nhỏ) | Endpoint `create_lead` & `submit_website_lead` trong `api.py` | Lỗi CORS khi gọi API từ domain website khác vào máy chủ Frappe (đã xử lý triệt để qua Server-Side Proxy). | **ĐÃ HOÀN THÀNH**<br>(Deliverables sẵn sàng) |
| **WP3** | **Biên soạn Chuyên đề CLV & Phân bổ Chi phí ABC (A4.5)**<br>• Xây dựng mô hình Excel 5 sheets (`CLV_ABC_Model.xlsx`) với công thức động.<br>• Bóc tách 4 Cost Pools & Drivers ABC cho 4 dịch vụ cốt lõi.<br>• Mô hình hóa DCF 5 năm cho 3 kịch bản, ma trận độ nhạy 2 chiều.<br>• Giải quyết bài toán Hộ gia đình đa thú cưng (Household level aggregation).<br>• Tài liệu báo cáo chi tiết (.docx và .md). | **M**<br>(Vừa) | Khung giá dịch vụ `PetCare Service` và dữ liệu `Contact`/`Pet` | Tránh bịa đặt số liệu kế toán (đã dán nhãn Kịch bản Minh họa rõ ràng); liên kết chuẩn xác với CSDL Frappe. | **ĐÃ HOÀN THÀNH**<br>(Deliverables sẵn sàng) |
| **WP4** | **Soạn thảo Bộ Tài liệu API & Webhook (A4.7)**<br>• Tổng mục 48 API Whitelisted (`API_INVENTORY.md`).<br>• 1 tài liệu API/Webhook Nhóm (.docx & .md).<br>• 1 tài liệu phân bổ 4 API Cá nhân (.docx & .md).<br>• Bộ Postman Collection (31 requests) & Environment JSON.<br>• Hướng dẫn bảo mật Webhook HMAC-SHA256 & Idempotency. | **M**<br>(Vừa) | 48 endpoints trong `api.py` và `test_extended_capabilities_mock.py` | Request thiếu headers xác thực hoặc thiếu mẫu JSON response thực tế. *(Đã xử lý 100% chuẩn xác)* | **ĐÃ HOÀN THÀNH**<br>(Deliverables sẵn sàng) |
| **WP5** | **Biên soạn Thuyết minh Module & Đề xuất Khác biệt (A4.9 & A4.10)**<br>• Thuyết minh Module CRM & Module Reporting.<br>• Báo cáo Đề xuất khác biệt A4-10. | **M**<br>(Vừa) | Codebase `apps/petcare_crm/` và tài liệu kỹ thuật hiện có | Trình bày lý thuyết suông mà không gắn với mã nguồn thực tế (cần trích dẫn class, hàm thực tế). | `[Thành viên 1]` & `[Thành viên 3]` |
| **WP6** | **Xây dựng Storyboard Kịch bản Video Cá nhân (A4.4)**<br>• Soạn 4 kịch bản video từng phút (5-7 phút/bạn).<br>• Lời thoại mẫu và các bước click chuột trên Desk. | **S**<br>(Nhỏ) | 4 quy trình cá nhân từ WP1 và giao diện Desk UI | Sinh viên quay video lúng túng, quên show tài khoản admin cá nhân hoặc vượt quá thời lượng cho phép. | `[Thành viên 2]` |
| **WP7** | **Tổng hợp Báo cáo Chính `Report - Nhóm XX.docx` & Đóng gói ZIP**<br>• Ghép các chương Case Study, Setup, Quy trình, CLV-ABC, Đọc báo cáo.<br>• Đóng gói file ZIP mã nguồn sạch. | **L**<br>(Lớn) | Toàn bộ kết quả từ WP1 đến WP6 | Xung đột định dạng văn bản giữa các thành viên; quên loại bỏ tệp tạm `.pyc` khi nén zip. | `[Thành viên 1]` (Chủ trì) |

---

## 6. PHÂN CÔNG CÔNG VIỆC THEO 4 THÀNH VIÊN (TEAM ALLOCATION)

Giả định cấu trúc nhóm chuẩn gồm **4 thành viên** với vai trò trách nhiệm chuyên môn hóa:

| Thành Viên (Placeholder) | Vai Trò Đảm Trách | Nhiệm Vụ Quy Trình Cá Nhân (A4.3.2 & A4.4) | Nhiệm Vụ API Cá Nhân (A4.7.2) | Nhiệm Vụ Chuyên Đề Nhóm |
|---|---|---|---|---|
| **`[Thành viên 1]`** *(Nhóm trưởng)* | **Kiến trúc & Tích hợp Hệ thống** | **Quy trình 1**: Tiếp nhận Lead Đa kênh & Chuyển đổi Khách hàng (`FLOW-01`) | API `create_lead` & Webhook `payment_webhook` | Chủ trì Báo cáo chính, vẽ BPMN Nhóm, Thuyết minh Module CRM (A4.9.1). |
| **`[Thành viên 2]`** | **Frontend, Sales & Tiếp thị** | **Quy trình 2**: Quản lý Phễu Cơ hội Bán hàng & Chốt Deal (`FLOW-02`) | API `create_opportunity` & `update_opportunity_stage` | Xây dựng Lead Form WordPress (A4.8), chụp ảnh minh chứng Desk UI (A4.2), soạn Kịch bản Video (A4.4). |
| **`[Thành viên 3]`** | **Vận hành Dịch vụ & Tài chính** | **Quy trình 3**: Vận hành Dịch vụ, Cấn trừ Quyền lợi & Thanh toán VietQR (`FLOW-04 & 05`) | API `record_pet_service_visit` & `record_benefit_usage` | Biên soạn Chuyên đề CLV & Kế toán chi phí ABC (A4.5), Thuyết minh Đề xuất Khác biệt A4-10 (A4.10). |
| **`[Thành viên 4]`** | **Trí tuệ Chăm sóc & Báo cáo** | **Quy trình 4**: Động cơ Dự đoán Chu kỳ Chăm sóc & Cứu vãn Khách hàng Rời bỏ (`FLOW-07 & 08`) | API `predict_next_service` & `get_kpi_dashboard_metrics` | Biên soạn Đọc hiểu Báo cáo Quản trị Sales/CRM (A4.6), Thuyết minh Module Reporting (A4.9.2). |

---

## 7. NĂM (05) VIỆC NÊN LÀM ĐẦU TIÊN VÀ LÝ DO

Để đảm bảo giải quyết đúng các **Blocker nghiêm trọng (P0)** và tạo đà thuận lợi cho toàn bộ đồ án, nhóm nên thực hiện 5 việc sau theo đúng thứ tự:

1. **Việc 1: Tạo tệp BPMN 2.0 XML chuẩn Camunda Modeler cho Quy trình Nhóm và 4 Quy trình Cá nhân (WP1)**
   * *Lý do*: Đây là **Blocker P0 lớn nhất**. Rubric yêu cầu bắt buộc tệp `.bpmn` phải mở được bằng phần mềm Camunda cài trên máy tính. Hiện tại repo mới chỉ có mã Mermaid trong markdown. Tạo xong BPMN sẽ có ngay file ảnh `.png` để nhúng vào tất cả các báo cáo sau này.
2. **Việc 2: Xây dựng bộ mã nguồn Lead Form tích hợp website WordPress (WP2)**
   * *Lý do*: Đáp ứng tiêu chí bắt buộc **A4.8**. Đây là sản phẩm có tính tương tác thực tế cao, giúp chứng minh hệ thống CRM kết nối ngoại vi mượt mà. Code HTML/CSS/JS độc lập, làm nhanh trong 1 phiên là nghiệm thu được ngay.
3. **Việc 3: Soạn thảo chuyên đề Giá trị vòng đời khách hàng (CLV) và Bảng phân bổ chi phí ABC (WP3)**
   * *Lý do*: Đáp ứng tiêu chí **A4.5**. Đây là phần nội dung học thuật thường bị trừ điểm nhiều nhất nếu làm sơ sài. Xây dựng sớm bảng tính số liệu kinh tế chuẩn cho ngành thú cưng sẽ làm nâng tầm chất lượng học thuật của toàn bộ đồ án.
4. **Việc 4: Soạn thảo bộ tài liệu Khám phá API Nhóm & Gọi API Cá nhân có kèm mẫu Postman/cURL (WP4)**
   * *Lý do*: Đáp ứng tiêu chí **A4.7**. Mã nguồn API backend đã có đầy đủ 48 endpoints và chạy ổn định. Chỉ cần biên tập dữ liệu mẫu, cURL và chụp ảnh Postman cho 4 bạn là hoàn tất trọn vẹn tiêu chí này.
5. **Việc 5: Biên tập Báo cáo thuyết minh Đề xuất khác biệt A4-10 (WP5)**
   * *Lý do*: Đáp ứng tiêu chí **A4.10**. Dự án PetCare CRM đang nắm giữ lợi thế cạnh tranh tuyệt đối nhờ 4 tính năng vượt trội (Care Intelligence theo mùa/tuổi, VietQR tự động, Ví hội viên atomic, Owner Portal). Cần văn bản hóa ngay thành tệp nộp riêng để ghi điểm tối đa với hội đồng chấm thi.
