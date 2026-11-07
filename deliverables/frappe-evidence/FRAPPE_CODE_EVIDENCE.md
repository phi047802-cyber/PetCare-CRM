# BẰNG CHỨNG MÃ NGUỒN PHÁT TRIỂN TRÊN FRAPPE FRAMEWORK

## 1. Thông tin tài liệu

| Thuộc tính | Giá trị |
|---|---|
| Dự án | PetCare CRM |
| Loại sản phẩm | Custom CRM application cho dịch vụ chăm sóc thú cưng |
| Nền tảng mục tiêu | Frappe Framework v15 |
| Tên app | `petcare_crm` |
| Loại bằng chứng | Kiểm tra cấu trúc và mã nguồn tĩnh (code evidence) |
| Phạm vi | App metadata, DocType, controller, ORM, API, RBAC, Workspace, Desk Form Script, Scheduler, Script Report và migration |

> **Tuyên bố phạm vi:** Tài liệu này chứng minh mã nguồn được tổ chức và phát triển theo kiến trúc custom app của Frappe. Tài liệu không thay thế bằng chứng cài đặt và chạy app trên một Frappe site thật. Bằng chứng runtime cần bổ sung bằng `bench --version`, `bench --site ... list-apps`, ảnh Frappe Desk và dữ liệu được lưu thực tế.

---

## 2. Kết luận kiểm tra nhanh

PetCare CRM không phải một website HTML độc lập được gắn nhãn Frappe. Phần backend của dự án sử dụng trực tiếp các cơ chế của Frappe:

- Metadata app và lifecycle hook trong `hooks.py`.
- 15 DocType nghiệp vụ với schema JSON theo chuẩn Frappe.
- Controller Python kế thừa `frappe.model.document.Document`.
- Frappe ORM/Document API: `frappe.get_doc`, `frappe.get_all`, `frappe.db.get_value`, `insert`, `save`.
- RPC API bằng decorator `@frappe.whitelist()`.
- Role và permission nằm trong DocType JSON và fixture Frappe.
- Workspace chuẩn Frappe Desk.
- Form Script sử dụng `frappe.ui.form.on`, `frm.add_custom_button`, `frappe.call`.
- Scheduler khai báo bằng `scheduler_events`.
- Báo cáo loại `Script Report`.
- Setup/migration tự tạo Role sau khi migrate.

Giao diện portal tùy biến chỉ là lớp trình bày. Dữ liệu, phân quyền, API, báo cáo và tác vụ nền vẫn dựa trên Frappe.

---

## 3. Ma trận bằng chứng mã nguồn

| STT | Đặc trưng Frappe | Bằng chứng trong dự án | Ý nghĩa kiểm chứng |
|:---:|---|---|---|
| 1 | App metadata | [`hooks.py`](../../apps/petcare_crm/petcare_crm/hooks.py#L1) khai báo `app_name = "petcare_crm"`, `app_title`, publisher, license | Đây là entry point cấu hình của một Frappe app |
| 2 | Module Frappe | [`modules.txt`](../../apps/petcare_crm/petcare_crm/modules.txt) khai báo module `PetCare CRM` | Frappe dùng module này để nhóm DocType, Report và Workspace |
| 3 | DocType schema | [`woocommerce_order_sync.json`](../../apps/petcare_crm/petcare_crm/petcare_crm/doctype/woocommerce_order_sync/woocommerce_order_sync.json#L7) có `"doctype": "DocType"`, fields, autoname và permissions | Schema được Frappe migrate thành bảng dữ liệu và metadata |
| 4 | Document Controller | [`woocommerce_order_sync.py`](../../apps/petcare_crm/petcare_crm/petcare_crm/doctype/woocommerce_order_sync/woocommerce_order_sync.py#L9) định nghĩa `class WooCommerceOrderSync(Document)` | Logic validation chạy theo lifecycle của Frappe Document |
| 5 | Frappe ORM | [`woocommerce_service.py`](../../apps/petcare_crm/petcare_crm/utils/woocommerce_service.py#L56) dùng `frappe.db.get_value`, `frappe.get_doc`, `insert`, `save` | Dữ liệu được thao tác qua Frappe ORM, không phải mảng dữ liệu HTML tĩnh |
| 6 | Whitelisted API | [`api.py`](../../apps/petcare_crm/petcare_crm/api.py#L4481) dùng `@frappe.whitelist(allow_guest=True)` cho webhook WooCommerce | Endpoint được Frappe xuất bản tại `/api/method/petcare_crm.api...` |
| 7 | RBAC/Permissions | [`woocommerce_order_sync.json`](../../apps/petcare_crm/petcare_crm/petcare_crm/doctype/woocommerce_order_sync/woocommerce_order_sync.json#L201) khai báo quyền cho System Manager, PetCare Manager, Sales và Analyst | Quyền đọc/ghi/tạo/xóa được thực thi bởi Frappe Permission System |
| 8 | Role fixture | [`hooks.py`](../../apps/petcare_crm/petcare_crm/hooks.py#L15) khai báo fixture `Role` | Role nghiệp vụ được xuất/nhập theo cơ chế fixture của Frappe |
| 9 | Workspace Desk | [`petcare_crm.json`](../../apps/petcare_crm/petcare_crm/petcare_crm/workspace/petcare_crm/petcare_crm.json) có `doctype: Workspace`, liên kết DocType và Report | Workspace được Frappe Desk dựng từ metadata, không phải ảnh mô phỏng |
| 10 | Form Script | [`petcare_lead.js`](../../apps/petcare_crm/petcare_crm/petcare_crm/doctype/petcare_lead/petcare_lead.js#L4) dùng `frappe.ui.form.on`, custom button và `frappe.call` | Hành vi giao diện chạy trong Frappe Desk Form lifecycle |
| 11 | Scheduler | [`hooks.py`](../../apps/petcare_crm/petcare_crm/hooks.py#L42) đăng ký job daily/hourly; [`tasks.py`](../../apps/petcare_crm/petcare_crm/tasks.py#L56) triển khai tác vụ | Frappe Scheduler/worker gọi tác vụ nền theo lịch |
| 12 | Script Report | [`petcare_kpi_overview.json`](../../apps/petcare_crm/petcare_crm/petcare_crm/report/petcare_kpi_overview/petcare_kpi_overview.json#L19) khai báo `Script Report`; [`petcare_kpi_overview.py`](../../apps/petcare_crm/petcare_crm/petcare_crm/report/petcare_kpi_overview/petcare_kpi_overview.py#L10) có `execute(filters)` | Báo cáo được Frappe Report Engine gọi và render trong Desk |
| 13 | Migration hook | [`hooks.py`](../../apps/petcare_crm/petcare_crm/hooks.py#L37) khai báo `after_migrate` | Logic setup được chạy sau `bench --site ... migrate` |
| 14 | Setup Role | [`install.py`](../../apps/petcare_crm/petcare_crm/setup/install.py#L17) dùng `frappe.db.exists`, `frappe.get_doc` và `insert` để tạo Role | Site mới có thể khởi tạo cấu hình nghiệp vụ qua Frappe migration |
| 15 | Patch system | [`patches.txt`](../../apps/petcare_crm/petcare_crm/patches.txt) và [`seed_demo_data.py`](../../apps/petcare_crm/petcare_crm/patches/v1_0/seed_demo_data.py) | Dữ liệu/migration được tổ chức theo cơ chế patch của Frappe |
| 16 | Frappe package | [`pyproject.toml`](../../apps/petcare_crm/pyproject.toml) khai báo package `petcare_crm` | App có thể được Bench cài vào `apps/` và đăng ký trên site |

---

## 4. Dấu vết kỹ thuật đặc trưng

### 4.1. Metadata và lifecycle của app

Tệp [`hooks.py`](../../apps/petcare_crm/petcare_crm/hooks.py) chứa các thành phần đặc trưng của Frappe:

```python
app_name = "petcare_crm"
app_title = "PetCare CRM"
after_migrate = "petcare_crm.setup.install.setup_petcare_crm"

scheduler_events = {
    "daily": ["petcare_crm.tasks.daily_petcare_scan"],
    "hourly": ["petcare_crm.tasks.hourly_workflow_check"],
}
```

Một frontend HTML độc lập không sử dụng `after_migrate`, fixtures hay Frappe Scheduler hooks.

### 4.2. DocType và controller

Ví dụ WooCommerce sử dụng đầy đủ cặp schema/controller của Frappe:

```text
petcare_crm/doctype/woocommerce_order_sync/
├── __init__.py
├── woocommerce_order_sync.json
└── woocommerce_order_sync.py
```

Schema JSON định nghĩa field, unique key, Link tới Contact/Pet/Opportunity và ma trận quyền. Controller kế thừa `Document` và thực hiện validation trước khi Frappe lưu bản ghi.

Các DocType nghiệp vụ khác cũng theo cấu trúc này, ví dụ:

- `PetCare Lead`
- `PetCare Opportunity`
- `Pet`
- `PetCare Appointment`
- `Service Visit`
- `Customer Membership`
- `Membership Transaction`
- `Care Recommendation`
- `WooCommerce Order Sync`

### 4.3. API do Frappe công bố

Webhook WooCommerce được khai báo trong [`api.py`](../../apps/petcare_crm/petcare_crm/api.py#L4481):

```python
@frappe.whitelist(allow_guest=True)
def woocommerce_order_webhook(...):
    ...
```

Theo cơ chế RPC của Frappe, hàm này được gọi qua:

```text
POST /api/method/petcare_crm.api.woocommerce_order_webhook
```

Endpoint xác thực HMAC rồi gọi service. Service tiếp tục sử dụng Frappe Document API để tạo hoặc cập nhật bản ghi CRM.

### 4.4. Giao diện Desk và giao diện tùy biến

Dự án có hai lớp giao diện:

1. **Frappe Desk native:** Workspace, List View, Form View, Script Report và Form Script.
2. **Portal/UI tùy biến:** giao diện phục vụ khách hàng hoặc demo nghiệp vụ.

Việc xây UI tùy biến không làm dự án mất tính chất Frappe. Điều kiện cần kiểm tra là UI phải gọi API Frappe và dữ liệu phải được lưu vào DocType, thay vì chỉ thay đổi dữ liệu JavaScript cục bộ.

> `preview.html`, `desk_preview.html` và `start_preview.py` là bản preview độc lập. Các tệp này hữu ích cho trình diễn giao diện nhưng không được dùng làm bằng chứng duy nhất rằng Frappe runtime đang hoạt động.

---

## 5. Truy vết một quy trình hoàn chỉnh: WooCommerce → Frappe CRM

| Bước | Thành phần | Bằng chứng |
|:---:|---|---|
| 1 | WooCommerce phát sinh hoặc đổi trạng thái đơn | [`class-petcare-woocommerce-sync.php`](../wordpress/petcare-lead-capture/includes/class-petcare-woocommerce-sync.php#L14) đăng ký hook WooCommerce |
| 2 | WordPress ký payload | Plugin tạo HMAC-SHA256 và header `X-WC-Webhook-Signature` |
| 3 | Frappe nhận request | [`woocommerce_order_webhook`](../../apps/petcare_crm/petcare_crm/api.py#L4482) là whitelisted method |
| 4 | Kiểm tra bảo mật | [`WooCommerceWebhookSecurity`](../../apps/petcare_crm/petcare_crm/utils/woocommerce_service.py#L30) dùng constant-time signature comparison |
| 5 | Chống xử lý trùng | Service tạo `external_order_key` theo website + order ID và kiểm tra Delivery ID |
| 6 | Ghi dữ liệu CRM | Service dùng `frappe.get_doc` để tạo Contact, Pet, Opportunity và WooCommerce Order Sync |
| 7 | Quản trị trong Desk | Workspace liên kết tới DocType `WooCommerce Order Sync` |
| 8 | Kiểm thử | [`test_woocommerce_integration.py`](../../apps/petcare_crm/petcare_crm/tests/test_woocommerce_integration.py#L71) kiểm tra HMAC, mapping, idempotency và retry contract |

Chuỗi truy vết này cho thấy WordPress chỉ là nguồn dữ liệu bên ngoài; nơi quản trị và xử lý CRM là custom app Frappe.

---

## 6. Cách giảng viên tự kiểm tra mã nguồn trong 5 phút

1. Mở `apps/petcare_crm/petcare_crm/hooks.py` và kiểm tra `app_name`, fixtures, `after_migrate`, `scheduler_events`.
2. Mở một thư mục trong `petcare_crm/doctype/` và đối chiếu file JSON với controller kế thừa `Document`.
3. Tìm `@frappe.whitelist` trong `api.py`.
4. Tìm `frappe.get_doc`, `frappe.db.get_value`, `.insert()` và `.save()` trong service layer.
5. Mở Workspace JSON và Script Report.
6. Mở một Form Script có `frappe.ui.form.on` và `frappe.call`.
7. Chạy test suite và xem test WooCommerce được master runner thực thi.

Các lệnh kiểm tra nhanh:

```powershell
rg "@frappe\.whitelist" apps/petcare_crm/petcare_crm/api.py
rg "frappe\.ui\.form\.on" apps/petcare_crm/petcare_crm/petcare_crm/doctype -g "*.js"
rg '"doctype": "DocType"' apps/petcare_crm/petcare_crm/petcare_crm/doctype -g "*.json"
python apps/petcare_crm/petcare_crm/tests/run_all_tests.py
```

---

## 7. Bằng chứng runtime cần bổ sung

Để chứng minh app không chỉ đúng cấu trúc mà còn chạy thật, cần ghi lại kết quả:

```bash
bench --version
bench --site petcare.localhost list-apps
bench --site petcare.localhost migrate
bench --site petcare.localhost run-tests --app petcare_crm
```

Ảnh/video tối thiểu:

1. `petcare_crm` xuất hiện trong danh sách installed apps.
2. Workspace PetCare CRM mở trong Frappe Desk.
3. Role Permission Manager hiển thị Role nghiệp vụ.
4. Tạo dữ liệu từ UI hoặc WooCommerce.
5. DevTools hiển thị request tới `/api/method/petcare_crm.api...`.
6. Dữ liệu vừa tạo xuất hiện trong DocType trên Desk.

---

## 8. Trạng thái xác minh

| Hạng mục | Trạng thái |
|---|:---:|
| Cấu trúc custom Frappe app | Đã xác minh từ code |
| DocType và Document Controller | Đã xác minh từ code |
| Frappe ORM và Whitelisted API | Đã xác minh từ code |
| RBAC, Workspace, Form Script | Đã xác minh từ code |
| Scheduler và Script Report | Đã xác minh từ code |
| WooCommerce → Frappe integration | Đã có code và automated tests |
| Bộ kiểm thử Python hiện tại | 99/99 PASS |
| Cài app trên Frappe Bench thật | Chưa có bằng chứng trong repository |
| Kiểm thử WordPress ↔ Frappe live | Chưa có bằng chứng trong repository |

## 9. Kết luận

Mã nguồn cung cấp bằng chứng rõ ràng rằng PetCare CRM được thiết kế dưới dạng custom application cho Frappe Framework: sử dụng metadata, DocType, Document Controller, ORM, Whitelisted API, RBAC, Workspace, Form Script, Scheduler, Script Report và migration hook của Frappe.

Giao diện tùy biến không phủ nhận nền tảng Frappe; nó chỉ thay đổi lớp presentation. Để hoàn thiện hồ sơ nghiệm thu, nhóm cần bổ sung bằng chứng runtime từ một Frappe site thật và không sử dụng bản preview tĩnh làm bằng chứng thay thế.
