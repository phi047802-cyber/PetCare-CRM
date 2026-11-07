# BẢNG MA TRẬN PHÂN QUYỀN (ROLE PERMISSION MATRIX) & BẢO MẬT HỆ THỐNG

> **Dự án**: PetCare CRM (CRM Toàn Diện Dịch Vụ Thú Cưng)  
> **Nền tảng**: Frappe Framework v15 (Desk Native Architecture)  
> **Phiên bản tài liệu**: 2.0 (Prompt 8 Architecture Release)  

---

## 1. Danh Sách Vai Trò (System Roles)

| Mã Vai Trò | Tên Vai Trò Hiển Thị | Đối Tượng Sử Dụng | Trách Nhiệm Nghiệp Vụ Chính |
|---|---|---|---|
| `System Manager` | System Administrator | Quản trị viên hệ thống / Kỹ thuật viên IT | Toàn quyền cấu hình hệ thống, quản lý tài khoản, phân quyền, sao lưu và kiểm toán toàn vẹn dữ liệu. |
| `PetCare Manager` | CRM Manager | Quản lý phòng khám / Trưởng bộ phận CRM & CSKH | Điều phối toàn bộ hoạt động CRM, duyệt chiết khấu, quản lý bảng giá dịch vụ, theo dõi SLA khiếu nại, hủy/điều chỉnh phiếu và phân tích báo cáo doanh thu. |
| `PetCare Sales` | Sales / Customer Care | Nhân viên bán hàng / Lễ tân / CSKH | Tiếp nhận & chuyển đổi Lead, quản lý cơ hội bán hàng, đăng ký thẻ hội viên, nạp tiền ví, gọi điện chăm sóc theo khuyến nghị (Due Soon / At Risk), mở Case khiếu nại. |
| `PetCare Technician` | Service Staff / Kỹ thuật viên | Bác sĩ thú y / Kỹ thuật viên Grooming, Spa | Tiếp nhận thú cưng làm dịch vụ, cập nhật cân nặng & sức khỏe vào hồ sơ Pet, ghi nhận phiếu Service Visit thực tế, phản hồi xử lý kỹ thuật cho các Case liên quan. |
| `PetCare Analyst` | Analyst / Reporting User | Chuyên viên phân tích dữ liệu / Kế toán quản trị | Truy xuất báo cáo phân tích, theo dõi các chỉ số KPI chuyển đổi, phễu bán hàng, tỷ lệ giữ chân khách hàng (Retention) và doanh thu dịch vụ. (Chỉ đọc & xuất báo cáo). |

---

## 2. Ma Trận Phân Quyền Chi Tiết Theo Nhóm DocType

*Ký hiệu: `R` (Read), `C` (Create), `W` (Write/Edit), `D` (Delete), `S` (Submit), `X` (Cancel), `Rep` (Report), `Exp` (Export)*

### 2.1. Phân Hệ CRM Core (Tiếp Thị & Bán Hàng)

| DocType | System Manager | PetCare Manager | PetCare Sales | PetCare Technician | PetCare Analyst |
|---|:---:|:---:|:---:|:---:|:---:|
| `PetCare Lead` | R, C, W, D, Rep, Exp | R, C, W, D, Rep, Exp | R, C, W, Rep | — | R, Rep, Exp |
| `PetCare Opportunity` | R, C, W, D, Rep, Exp | R, C, W, D, Rep, Exp | R, C, W, Rep | — | R, Rep, Exp |
| `Contact` (Khách hàng) | R, C, W, D, Rep, Exp | R, C, W, Rep, Exp | R, C, W, Rep | R | R, Rep, Exp |

### 2.2. Phân Hệ Thú Cưng & Vận Hành Dịch Vụ (PetCare Domain & Service Operations)

| DocType | System Manager | PetCare Manager | PetCare Sales | PetCare Technician | PetCare Analyst |
|---|:---:|:---:|:---:|:---:|:---:|
| `Pet` | R, C, W, D, Rep, Exp | R, C, W, Rep, Exp | R, C, W, Rep | R, W (Cân nặng, sức khỏe) | R, Rep, Exp |
| `PetCare Service` (Bảng giá) | R, C, W, D, Rep, Exp | R, C, W, Rep, Exp | R (Xem giá niêm yết) | R (Xem dịch vụ) | R, Rep, Exp |
| `Service Visit` | R, C, W, D, X, Rep, Exp | R, C, W, X, Rep, Exp | R, C, Rep | R, C, W | R, Rep, Exp |
| `PetCare Case` (Khiếu nại) | R, C, W, D, Rep, Exp | R, C, W, Rep, Exp | R, C, W | R, W (Nội dung kỹ thuật) | R, Rep, Exp |

### 2.3. Phân Hệ Hội Viên & Khách Hàng Thân Thiết (Membership & Loyalty)

| DocType | System Manager | PetCare Manager | PetCare Sales | PetCare Technician | PetCare Analyst |
|---|:---:|:---:|:---:|:---:|:---:|
| `Membership Plan` | R, C, W, D, Rep, Exp | R, C, W, Rep, Exp | R (Tư vấn gói) | R | R, Rep, Exp |
| `Customer Membership` | R, C, W, D, X, Rep, Exp | R, C, W, X, Rep, Exp | R, C (Đăng ký mới) | R (Xem quyền lợi còn) | R, Rep, Exp |
| `Benefit Redemption Ledger` | R, C, W, D, X, Rep, Exp | R, Rep, Exp (Audit) | R (Xem lịch sử) | R | R, Rep, Exp |
| `Membership Transaction` | R, C, W, D, Rep, Exp | R, C (Nạp ví), Rep, Exp | R, C (Nạp ví tiền mặt) | — | R, Rep, Exp |

### 2.4. Phân Hệ Chăm Sóc Khách Hàng Tự Động & Công Việc (Intelligence & Automation)

| DocType | System Manager | PetCare Manager | PetCare Sales | PetCare Technician | PetCare Analyst |
|---|:---:|:---:|:---:|:---:|:---:|
| `Care Recommendation` | R, C, W, D, Rep, Exp | R, C, W, D, Rep, Exp | R, W (Đổi trạng thái CSKH) | R | R, Rep, Exp |
| `ToDo` (Nhiệm vụ nhân viên) | R, C, W, D, Rep, Exp | R, C, W, D, Rep, Exp | R, C, W (Task được giao) | R, W (Task dịch vụ) | R, Rep |
| `Communication` | R, C, W, D, Rep, Exp | R, C, W, Rep, Exp | R, C, W (Ghi nhận trao đổi) | R | R, Rep |

---

## 3. Nguyên Tắc Bảo Mật & Kiểm Soát Quyền Truy Cập Chéo (Cross-Entity Ownership)

### 3.1. Bảo Vệ Tầng Backend (Server-side Enforcement)
* **Không phụ thuộc Frontend**: Việc ẩn nút trên giao diện Desk hoặc Client Script chỉ mang tính chất nâng cao trải nghiệm người dùng (UX), **không được coi là hàng rào bảo mật**. Mọi thao tác đều được kiểm tra thẩm quyền tại Python Controller (`validate()`, `before_insert()`, `on_trash()`) và REST API.
* **Module [`security.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/utils/security.py)** cung cấp hàm kiểm tra quyền tập trung `check_role_permission(doctype, permission_type, user)`.

### 3.2. Kiểm Tra Ràng Buộc Sở Hữu Chéo (Cross-Entity Relationship Guard)
Để ngăn chặn hành vi khai thác ID chéo hoặc ghi nhận sai lệch giữa các khách hàng:
1. **Khách hàng vs Thú cưng**: Khi mở `Service Visit` hoặc `PetCare Case`, hàm `validate_cross_entity_relationship` xác thực `Pet.customer == ServiceVisit.customer`. Nghiêm cấm chọn Pet của khách hàng này nhưng xuất hóa đơn cho khách hàng khác.
2. **Khách hàng vs Thẻ hội viên**: Xác thực `CustomerMembership.customer == ServiceVisit.customer`. Nếu thẻ là gói riêng biệt (`pet` có giá trị), kiểm tra thẻ có khớp với thú cưng nhận dịch vụ hay không.
3. **Thẩm quyền Hủy (Cancel)**: Chỉ `PetCare Manager` hoặc `System Manager` mới có quyền thực hiện thao tác Hủy (`Cancel`) phiếu `Service Visit` hoặc hoàn tác `Benefit Redemption Ledger`.

---

## 4. Chuẩn Hóa Dữ Liệu Đầu Vào & Chống Lộ Lọt Thông Tin

1. **Chuẩn hóa Số Điện Thoại Việt Nam**: Áp dụng Regex `^(03|05|07|08|09)\d{8}$` xác thực độ dài 10 chữ số và đầu số di động hợp lệ.
2. **Khử nhiễm Chuỗi (Sanitization)**: Loại bỏ các thẻ HTML/Script nguy hiểm khỏi các trường văn bản tự do (`notes`, `reason`, `subject`).
3. **Ràng buộc Giá Trị Số**: Các trường tiền tệ, đơn giá và số lượng bắt buộc $\ge 0$, ngăn chặn lỗi số âm làm sai lệch số dư ví và báo cáo doanh thu.
4. **Bảo Mật API Response**: Các API công khai và nội bộ không bao giờ trả về trường nhạy cảm như hash mật khẩu, secret token hoặc API key của bên thứ ba.
