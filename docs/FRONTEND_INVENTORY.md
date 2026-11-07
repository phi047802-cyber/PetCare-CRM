# PETCARE CRM — BẢN ĐỒ VÀ DANH MỤC THÀNH PHẦN FRONTEND
**Tài liệu Khảo sát Giai đoạn 1 (Frontend Inventory)**
*Dự án:* PetCare CRM (Hệ sinh thái Quản lý Phòng khám & Dịch vụ Chăm sóc Thú cưng)
*Nền tảng:* Frappe Framework v15 (Client-side Web Portal, Desk Workspace & Client Scripts)
*Ngày khảo sát:* 04/11/2026
*Nguyên tắc:* Khảo sát thực tế từ repository, bảo toàn 100% backend, schema và business logic.

---

## 1. TỔNG QUAN KIẾN TRÚC FRONTEND HIỆN HỮU

Hệ thống frontend của PetCare CRM hiện tại được cấu thành từ 3 phân hệ giao diện chính:

```
                          ┌──────────────────────────────────────────────┐
                          │            PETCARE CRM FRONTEND              │
                          └──────────────────────┬───────────────────────┘
                                                 │
          ┌──────────────────────────────────────┼──────────────────────────────────────┐
          │                                      │                                      │
          ▼                                      ▼                                      ▼
┌──────────────────────────┐           ┌───────────────────┐             ┌──────────────────────────┐
│  PORTAL TIẾP NHẬN & POS  │           │   DESK WORKSPACE  │             │   DOCTYPE CLIENT SCRIPTS │
│  (Quầy Lễ Tân & Bác Sĩ)  │           │(Quản Trị Vận Hành)│             │ (Form View & List View)  │
├──────────────────────────┤           ├───────────────────┤             ├──────────────────────────┤
│ • preview.html           │           │ • desk_preview.html│            │ • doctype/*/*.js         │
│ • www/frontend.html      │           │ • workspace/      │             │ • report/*/*.js          │
│ • www/index.html         │           │   petcare_crm.json│             │                          │
└──────────────────────────┘           └───────────────────┘             └──────────────────────────┘
```

1. **Cổng Web Portal Tiếp Nhận, POS & Chăm Sóc Khách Hàng (Customer 360 / POS / Care Cycle)**:
   - Các file triển khai: `preview.html` (chạy độc lập qua máy chủ `start_preview.py`) và `apps/petcare_crm/petcare_crm/www/frontend.html`, `apps/petcare_crm/petcare_crm/www/index.html` (chạy qua routing của Frappe web page).
   - Công nghệ: Vanilla JavaScript ES6+, Tailwind CSS, Font Awesome 6.5.1, SheetJS (XLSX v0.18.5), Google Font `Plus Jakarta Sans`.
   - Cơ chế kết nối: Gọi REST API `/api/method/petcare_crm.api.*` kèm CSRF token; có bộ nhớ đệm giả lập tương tác ngoại tuyến (`MOCK_DB`) khi chạy độc lập không có backend.

2. **Giao Diện Không Gian Làm Việc Quản Trị Frappe Desk Workspace**:
   - Các file triển khai: `desk_preview.html` (xem trước tương tác cho Desk) và cấu hình Desk chuẩn `apps/petcare_crm/petcare_crm/petcare_crm/workspace/petcare_crm/petcare_crm.json`.
   - Đối tượng người dùng: Quản lý phòng khám, Bác sĩ trưởng, Trưởng quầy lễ tân, Kế toán/Kiểm toán viên.
   - Chức năng: Dashboard KPI, Shortcuts điều hướng nhanh đến các danh sách dữ liệu, cấu trúc danh mục 5 phân hệ DocType, Drawer tương tác xem bảng dữ liệu và thực hiện tác vụ nghiệp vụ.

3. **Tập Lệnh Phía Trình Duyệt Của Từng DocType (Frappe Client Scripts)**:
   - Thư mục: `apps/petcare_crm/petcare_crm/petcare_crm/doctype/*/*.js`.
   - Chức năng: Gắn logic giao diện cho Form View (nút bấm chuyển trạng thái, bộ lọc động liên kết quan hệ `frm.set_query`, mở Dialog nhập liệu phụ trợ) và List View (chỉ báo màu trạng thái `get_indicator`, nút lọc nhanh trên thanh công cụ trang).

---

## 2. DANH MỤC CÁC MÀN HÌNH VÀ THÀNH PHẦN THỰC TẾ

### 2.1. Phân hệ Cổng Tiếp Nhận & POS (`preview.html`, `www/frontend.html`, `www/index.html`)

| STT | Tên Màn Hình / Tab | Đối Tượng Sử Dụng | Mục Đích Nghiệp Vụ Cốt Lõi | Thao Tác Chính | API / Nguồn Dữ Liệu |
|:---:|:---|:---|:---|:---|:---|
| 1 | **Tra Cứu Hồ Sơ 360 & Hội Viên** (`#tab-client`) | Lễ tân, Bác sĩ, Tư vấn viên CSKH | Tra cứu toàn diện lịch sử khách hàng theo SĐT/Tên: thông tin liên hệ, hồ sơ từng bé thú cưng, thẻ hội viên (Silver/Gold/VIP), hạn mức dịch vụ còn lại, lịch sử lần ghé gần nhất. | • Tìm kiếm theo SĐT/Tên<br>• Nạp tiền thẻ hội viên<br>• Gia hạn thẻ hội viên<br>• Đăng ký hội viên mới<br>• Đặt lịch hẹn mới<br>• Chuyển sang quầy POS | `get_customer_portal_details`<br>`get_available_plans`<br>`top_up_membership`<br>`renew_membership`<br>`register_membership` |
| 2 | **Quầy Tiếp Nhận Nhanh POS** (`#subview-pos-content`) | Lễ tân, Thu ngân, Bác sĩ/KTV | Tiếp nhận thú cưng vào quầy làm dịch vụ: chọn khách, chọn bé cưng, chọn dịch vụ trong danh mục (Khám, Spa, Tắm, Cắt móng), tự động kiểm tra và cấn trừ quyền lợi thẻ hội viên (miễn phí) hoặc tính tiền theo biểu giá. | • Chọn nhanh khách & bé<br>• Chọn dịch vụ theo danh mục<br>• Tự động đối soát quyền lợi<br>• Chọn PTTT (Tiền mặt, VietQR, Ví, Thẻ)<br>• Check-in hoàn tất phiếu dịch vụ | `get_portal_overview`<br>`get_service_catalog`<br>`get_active_membership`<br>`get_remaining_benefit`<br>`check_in_with_benefit` |
| 3 | **Danh Sách Lịch Hẹn Đặt Trước** (`#subview-appts-content`) | Lễ tân, Quản lý lịch hẹn | Theo dõi các lịch hẹn đặt trước của khách trong ngày/tuần; tiếp đón khách đến đúng hẹn và đưa vào quầy POS phục vụ ngay lập tức. | • Lọc theo trạng thái lịch<br>• Check-in nhanh vào POS<br>• Hủy lịch hẹn kèm lý do<br>• Đặt lịch hẹn mới qua Modal | `get_appointments`<br>`check_in_appointment`<br>`cancel_appointment`<br>`book_appointment` |
| 4 | **Theo Dõi Chu Kỳ & Đề Xuất CSKH** (`#tab-cycle`) | Tư vấn viên CSKH, Quản lý | Theo dõi chu kỳ định kỳ của thú cưng (tắm, tiêm phòng, cắt tỉa), phát hiện thú cưng sắp đến hạn hoặc có nguy cơ rời bỏ; tiếp nhận danh sách đề xuất chăm sóc để liên hệ chủ nuôi. | • Lọc bảng chu kỳ (Tất cả, Sắp đến hạn, Nguy cơ rời bỏ, Cần gia hạn)<br>• Gọi điện / Nhắc hẹn chủ nuôi<br>• Bỏ qua đề xuất<br>• Quét chu kỳ chăm sóc | `get_portal_overview`<br>`update_recommendation_status`<br>`run_care_scan` |
| 5 | **Kinh Doanh & KPI** (`#tab-business`) | Quản lý, Sales, CSKH | Theo dõi pipeline, doanh thu đã chốt, tỷ lệ chuyển đổi Lead và doanh thu dịch vụ; ghi nhận nhanh Lead, Opportunity và Case ngay trong portal. | • Tải pipeline theo giai đoạn<br>• Xem KPI từ Analytics Service<br>• Tạo Lead mới<br>• Tạo Opportunity<br>• Ghi nhận phản hồi/Case | `get_pipeline_summary`<br>`get_kpi_dashboard_metrics`<br>`create_lead`<br>`create_opportunity`<br>`create_service_case` |
| 6 | **Modal Thêm Khách Hàng & Bé Mới** (`#create-cust-overlay`) | Lễ tân | Nhập thông tin nhanh khách hàng mới và thú cưng đầu tiên khi khách ghé quầy lần đầu hoặc đăng ký tại chỗ. | • Điền Họ tên, SĐT, Email<br>• Điền Tên bé, Loài, Giống, Cân nặng<br>• Tùy chọn kích hoạt gói hội viên ngay | `create_customer_with_pet` |
| 7 | **Modal Import Khách Hàng Hàng Loạt** (`#import-cust-overlay`) | Quản trị viên, Quản lý | Tải lên danh sách khách hàng và thú cưng từ file Excel/CSV hoặc sao chép - dán bảng tính; tự động kiểm tra tính hợp lệ và import đồng loạt. | • Tải file mẫu .xlsx/.csv<br>• Kéo thả tệp tin hoặc dán bảng<br>• Xem bảng đối soát lỗi trước khi nhập<br>• Thực thi import hàng loạt | `batch_import_customers`<br>SheetJS client engine |

---

### 2.2. Phân hệ Desk Workspace Quản Trị (`desk_preview.html` & `workspace/petcare_crm.json`)

| Phân Vùng | Thành Phần Giao Diện | Chức Năng Hoạt Động |
|:---|:---|:---|
| **Header & Điều Hướng** | Thanh tiêu đề Desk Navbar, Breadcrumb, Nút thao tác nhanh | Chuyển đổi giữa Desk và Web Portal; mở nhanh Modal Thêm Khách Hàng hoặc Import Excel. |
| **Workspace Banner** | Tiêu đề Không Gian Làm Việc PetCare CRM | Giới thiệu vai trò không gian quản trị vận hành trên Frappe v15. |
| **Shortcuts (Chỉ Số Vận Hành Nhanh)** | 5 thẻ số liệu tương tác: New Leads, Due Soon Pets, At Risk Pets, Active Memberships, Open Cases | Nhấp chuột vào từng thẻ để mở ngay bảng dữ liệu chi tiết của nhóm tương ứng trong Drawer. |
| **Module 1: CRM Core & Leads** | Thẻ liên kết DocTypes: PetCare Lead, Sales Opportunity, Customers & Contacts | Mở danh sách khách tiềm năng, cơ hội chốt hợp đồng và danh bạ khách hàng. |
| **Module 2: Pet & Service Operations** | Thẻ liên kết DocTypes: Pet Profiles, Service Catalog, Service Visits, Service Cases & Complaints | Quản lý hồ sơ thú cưng, danh mục bảng giá dịch vụ, nhật ký khám/spa và khiếu nại khách hàng. |
| **Module 3: Membership & Benefits** | Thẻ liên kết DocTypes: Customer Memberships, Membership Plans, Benefit Redemption Ledger, Membership Transactions | Quản lý thẻ hội viên, cấu hình gói, sổ cái cấn trừ quyền lợi và lịch sử giao dịch ví. |
| **Module 4: Care Intelligence & Automation** | Thẻ liên kết DocTypes: Care Recommendations, CRM Tasks & ToDos | Danh sách đề xuất nhắc hẹn chăm sóc chu kỳ và công việc phân công nhân viên. |
| **Module 5: Analytics & Reports** | Thẻ liên kết Báo cáo: PetCare KPI Overview, Multi-Branch Breakdown | Báo cáo doanh thu gộp, doanh thu thực nhận, tỷ lệ giữ chân và hiệu quả đa chi nhánh. |
| **Slide-out Drawer Component** | `#desk-modal` chứa bảng dữ liệu động tương ứng khi click | Xem danh sách, thực hiện chuyển đổi Lead, nạp tiền ví, gia hạn thẻ, giải quyết Case, đánh dấu Won Opportunity. |

---

### 2.3. Danh mục Client Scripts của DocType

| DocType | File Script | Phạm Vi & Thao Tác UI |
|:---|:---|:---|
| **Customer Membership** | `customer_membership.js`<br>`customer_membership_list.js` | • Form: Nút "Nạp Tiền" mở Dialog nạp ví; nút "Gia Hạn Thẻ" mở Dialog chọn gói gia hạn.<br>• List: Cột chỉ báo màu (Xanh: Active, Cam: Sắp hết hạn trong 7 ngày, Đỏ: Expired, Xám: Cancelled). |
| **Care Recommendation** | `care_recommendation.js`<br>`care_recommendation_list.js` | • Form: Nút "Mark Contacted", "Mark Converted", "Dismiss".<br>• List: Chỉ báo màu (Xanh dương: Due Soon, Đỏ: At Risk, Cam: Renewal) và nút lọc nhanh trên thanh công cụ. |
| **Pet** | `pet.js` | • Form: Cảnh báo y tế dị ứng/bệnh lý bằng thanh thông báo vàng; nút "Đặt Lịch Hẹn Chăm Sóc"; nút "Mở Quầy Tiếp Nhận POS". |
| **Service Visit** | `service_visit.js` | • Form: Lọc Pet và Membership theo Customer đã chọn; tự động điền đơn giá chuẩn từ Service Catalog; nút "Ghi Nhận Khiếu Nại / Case" sau khi hoàn tất dịch vụ.<br>• List: Chỉ báo màu trạng thái Completed (Xanh lá), Draft (Xanh dương), Cancelled (Xám). |
| **PetCare Appointment** | `petcare_appointment.js` | • Form: Lọc Pet theo Customer; nút "Check-in Tiếp Đón" khi ở trạng thái Scheduled/Confirmed; nút "Hủy Lịch Hẹn".<br>• List: Chỉ báo màu Scheduled, Confirmed, Checked-In, Cancelled. |
| **PetCare Lead** | `petcare_lead.js` | • Form: Nút "Chuyển Đổi Lead" mở Prompt tạo Contact và Pet nhanh chóng khi Lead đạt Qualified. |
| **PetCare Opportunity** | `petcare_opportunity.js` | • Form: Lọc Pet theo Customer; nút "Tạo Thẻ Hội Viên" khi đạt trạng thái Closed Won. |
| **PetCare Case** | `petcare_case.js` | • Form: Lọc Pet và Service Visit theo Customer; cảnh báo hồ sơ khẩn cấp (Urgent). |
| **PetCare Service** | `petcare_service.js` | • Form: Nút "Mở Phiếu Dịch Vụ Với Dịch Vụ Này" tạo nhanh Service Visit. |
| **Benefit Redemption Ledger** | `benefit_redemption_ledger.js` | • Form: Cảnh báo thanh kiểm toán chỉ đọc màu đỏ khi giao dịch bị hoàn tác (Reverted). |
| **Membership Plan** | `membership_plan.js` | • Form: Kiểm tra hợp lệ giá trị số chu kỳ và thời hạn trên giao diện. |
| **PetCare KPI Overview** | `report/petcare_kpi_overview/...js` | • Report: Bộ lọc ngày bắt đầu (`from_date`) và ngày kết thúc (`to_date`). |

---

## 3. PHÂN VÙNG FILE: ĐƯỢC PHÉP CHỈNH SỬA VÀ KHÓA CHẶT CHẼ

Tuân thủ nghiêm ngặt Ràng buộc số 1 và Mục 2 của Master Prompt:

### 3.1. Danh Sách File Frontend Được Phép Chỉnh Sửa (Whitelist)
Chỉ chỉnh sửa các tệp trình bày, tương tác giao diện người dùng, styles, và tài liệu:
1. `preview.html`
2. `apps/petcare_crm/petcare_crm/www/frontend.html`
3. `apps/petcare_crm/petcare_crm/www/index.html`
4. `desk_preview.html`
5. Các file client scripts của DocType (chỉ chỉnh sửa nhãn hiển thị, modal styling, khả năng tiếp cận, KHÔNG sửa API signature hay logic nghiệp vụ):
   - `apps/petcare_crm/petcare_crm/petcare_crm/doctype/customer_membership/customer_membership.js`
   - `apps/petcare_crm/petcare_crm/petcare_crm/doctype/customer_membership/customer_membership_list.js`
   - `apps/petcare_crm/petcare_crm/petcare_crm/doctype/care_recommendation/care_recommendation.js`
   - `apps/petcare_crm/petcare_crm/petcare_crm/doctype/care_recommendation/care_recommendation_list.js`
   - `apps/petcare_crm/petcare_crm/petcare_crm/doctype/petcare_appointment/petcare_appointment.js`
   - `apps/petcare_crm/petcare_crm/petcare_crm/doctype/service_visit/service_visit.js`
   - `apps/petcare_crm/petcare_crm/petcare_crm/doctype/pet/pet.js`
   - `apps/petcare_crm/petcare_crm/petcare_crm/doctype/petcare_lead/petcare_lead.js`
   - `apps/petcare_crm/petcare_crm/petcare_crm/doctype/petcare_opportunity/petcare_opportunity.js`
   - `apps/petcare_crm/petcare_crm/petcare_crm/doctype/petcare_case/petcare_case.js`
   - `apps/petcare_crm/petcare_crm/petcare_crm/doctype/petcare_service/petcare_service.js`
   - `apps/petcare_crm/petcare_crm/petcare_crm/doctype/benefit_redemption_ledger/benefit_redemption_ledger.js`
   - `apps/petcare_crm/petcare_crm/petcare_crm/doctype/membership_plan/membership_plan.js`
6. Các file tài liệu hướng dẫn và báo cáo trong thư mục `docs/`.

### 3.2. Danh Sách File Bị Khóa Tuyệt Đối (Blacklist / Protected)
Nghiêm cấm thêm, xóa, đổi tên hoặc sửa đổi bất kỳ nội dung nào:
1. Tất cả file Python backend: `apps/petcare_crm/petcare_crm/*.py` (bao gồm `api.py`, `hooks.py`, `tasks.py`, `install.py`, etc.).
2. Tất cả file Python trong `apps/petcare_crm/petcare_crm/utils/*.py` (`analytics_service.py`, `omnichannel_service.py`, `payment_gateway.py`, `workflow_automation.py`, `customer_service.py`, `frappe_adapters.py`, etc.).
3. Tất cả file DocType JSON: `apps/petcare_crm/petcare_crm/petcare_crm/doctype/*/*.json` (DocType schemas, database column definitions, permissions).
4. Tất cả file kiểm thử backend: `apps/petcare_crm/petcare_crm/tests/*.py`.
5. Tất cả file dữ liệu seed, patch, migration: `apps/petcare_crm/petcare_crm/patches/**/*.py`.
6. Tất cả cấu hình triển khai và dependency: `pyproject.toml`, `requirements.txt`, `setup_git.ps1`, `deploy_clean.ps1`.
7. Các tài liệu nghiệm thu nhóm và cá nhân trong `deliverables/`.
