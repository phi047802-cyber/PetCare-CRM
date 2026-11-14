# MINH CHỨNG DATASET VÀ DATABASE DEMO PETCARE CRM

> **Phạm vi**: dữ liệu demo phục vụ A4.2.2, Module Care Intelligence và Module PetCare KPI Reporting
> **Nền tảng**: Frappe Framework v15
> **Dataset version**: 2026.11
> **Trạng thái minh chứng**: mã nguồn seed/validator đã có; ảnh và log Frappe runtime phải được nhóm bổ sung sau khi chạy trên site thật

## 1. Mục tiêu

Bộ dữ liệu này chứng minh hệ thống không chỉ có giao diện tĩnh mà có dữ liệu quan hệ và dữ liệu giao dịch thực sự trong database của Frappe. Dữ liệu được tạo hoàn toàn giả lập, không chứa thông tin cá nhân thật.

Dataset bao phủ:

- Master data: khách hàng, thú cưng, dịch vụ và gói hội viên.
- Transactional data: thẻ hội viên, lượt dịch vụ, lịch hẹn, Lead, Opportunity, Care Recommendation, ToDo và Case.
- Dữ liệu theo nhiều trạng thái để báo cáo KPI không bị rỗng.
- Các tình huống `DUE_SOON`, `AT_RISK`, `RENEWAL`, Lead chuyển đổi và Opportunity thắng/thua.

## 2. Thành phần và số lượng kỳ vọng

| DocType | Số lượng demo | Ý nghĩa |
|---|---:|---|
| Contact | 8 | Chủ nuôi ở nhiều tỉnh/thành |
| Address | 8 | Địa chỉ giả lập liên kết động với từng Contact |
| Pet | 9 | Có trường hợp một chủ nuôi nhiều thú cưng |
| PetCare Service | 4 | Grooming, Spa, Vaccine, Health Check |
| Membership Plan | 3 | Silver, Gold và Diamond VIP |
| Customer Membership | 4 | Active, sắp hết hạn, hết quyền lợi và Expired |
| Service Visit | 12 | Tạo lịch sử chu kỳ và doanh thu |
| PetCare Appointment | 7 | Lịch hẹn trong ngày ở nhiều chi nhánh |
| PetCare Lead | 4 | New, Contacted, Converted, Unqualified |
| PetCare Opportunity | 4 | Prospecting, Proposal, Closed Won, Closed Lost |
| Care Recommendation | 4 | DUE_SOON, AT_RISK, RENEWAL và CONVERTED |
| ToDo | 2 | Việc cần xử lý cho khuyến nghị trạng thái NEW |
| PetCare Case | 2 | Một phản hồi mới và một phản hồi đã xử lý |

Danh sách máy đọc được nằm tại [`demo_dataset_manifest.json`](demo_dataset_manifest.json).

## 3. Cách khởi tạo database demo

Chạy trong thư mục Frappe Bench sau khi app `petcare_crm` đã được cài vào site:

```bash
bench --site petcare.localhost migrate
bench --site petcare.localhost execute petcare_crm.patches.v1_0.seed_demo_data.execute
```

Seed script sử dụng tên bản ghi thật do Frappe sinh ra để liên kết Contact → Pet → Visit/Membership/Recommendation. Script dọn đúng phạm vi dữ liệu demo trước khi tạo lại nên có thể chạy lặp lại mà không làm nhân đôi Lead, Opportunity, Case, ToDo hoặc sai KPI.

Không đưa seed demo vào `patches.txt`: dữ liệu giả lập chỉ được nạp chủ động khi demo, không tự động xuất hiện trong môi trường production sau `bench migrate`.

## 4. Kiểm tra database sau khi seed

Chạy validator chỉ đọc:

```bash
bench --site petcare.localhost execute petcare_crm.patches.v1_0.validate_demo_data.execute
```

Kết quả hợp lệ phải có:

```text
"status": "PASS"
"failed_checks": []
```

Validator kiểm tra cả số lượng và phân bố trạng thái, gồm:

- Một chủ nuôi có hai Pet.
- Đủ bốn trạng thái Lead.
- Đủ bốn giai đoạn Opportunity dùng trong demo.
- Ba Membership Active và một Membership Expired.
- Hai DUE_SOON, một AT_RISK và một RENEWAL.
- Hai Recommendation NEW, một CONTACTED và một CONVERTED.

`WooCommerce Order Sync` chỉ là thông tin bổ sung và không phải điều kiện PASS của seed. Bản ghi này phải được tạo trực tiếp khi demo webhook để chứng minh tích hợp A4.8.

## 5. Ba kịch bản demo chính

### Story 1 — Lead đến cơ hội bán hàng

1. Mở Lead `Hoàng Gia Bảo` ở trạng thái New.
2. Chuyển sang Contacted/Qualified hoặc trình bày Lead `Nguyễn Văn An` đã Converted.
3. Mở Opportunity `DEMO - Nâng cấp gói VIP cho Nguyễn Văn An`.
4. Trình bày giá trị kỳ vọng, xác suất và giai đoạn Proposal.

### Story 2 — Dịch vụ và quyền lợi hội viên

1. Mở Contact `Nguyễn Văn An` và hai thú cưng `Bơ`, `Đậu Đậu`.
2. Mở thẻ Silver của bé Bơ.
3. Kiểm tra quyền lợi Grooming còn một lượt.
4. Mở lịch sử Service Visit và giải thích doanh thu/chiết khấu.

### Story 3 — Care Intelligence và Reporting

1. Mở `Bơ` ở tình huống DUE_SOON.
2. Mở `Miu Miu` ở tình huống AT_RISK sau 55 ngày không quay lại.
3. Mở `Đậu Phộng` ở tình huống Membership RENEWAL.
4. Mở Script Report `PetCare KPI Overview` và đối chiếu số liệu với List View.

## 6. Minh chứng phải thu trên Frappe thật

Lưu ảnh vào `deliverables/demo-data/evidence/` theo tên sau:

| Tên file | Nội dung bắt buộc |
|---|---|
| `01-bench-list-apps.png` | Site và app `petcare_crm` đã được cài |
| `02-seed-command-pass.png` | Log seed hoàn thành và validator PASS |
| `03-contact-multipet.png` | Contact Nguyễn Văn An cùng hai Pet |
| `04-lead-statuses.png` | List View Lead có nhiều trạng thái |
| `05-opportunity-pipeline.png` | Opportunity theo nhiều giai đoạn |
| `06-membership-benefits.png` | Thẻ hội viên và quyền lợi còn lại |
| `07-service-visits.png` | Lịch sử dịch vụ có giá và ngày |
| `08-care-recommendations.png` | DUE_SOON, AT_RISK, RENEWAL |
| `09-kpi-report.png` | PetCare KPI Overview có dữ liệu |
| `10-woocommerce-before.png` | WooCommerce Order Sync trước khi gửi đơn |
| `11-woocommerce-after.png` | Bản ghi sync được tạo sau webhook |

Ảnh phải hiển thị thanh địa chỉ hoặc tiêu đề Frappe Desk, không dùng trang `preview.html` làm bằng chứng database.

## 7. Database schema và bản sao lưu

Không cần viết file SQL tạo bảng. Frappe tạo schema từ DocType JSON khi chạy `bench migrate`; đây mới là cách triển khai đúng chuẩn framework.

Nếu cần lưu bản sao trước ngày bảo vệ, có thể chạy:

```bash
bench --site petcare.localhost backup --with-files
```

Không commit database backup, mật khẩu, `site_config.json` hoặc file chứa dữ liệu xác thực lên Git. Seed script và manifest là bản tái tạo dataset dùng để nộp cùng mã nguồn.

## 8. Truy vết mã nguồn

- Seed: `apps/petcare_crm/petcare_crm/patches/v1_0/seed_demo_data.py`
- Validator: `apps/petcare_crm/petcare_crm/patches/v1_0/validate_demo_data.py`
- DocType schemas: `apps/petcare_crm/petcare_crm/petcare_crm/doctype/`
- KPI report: `apps/petcare_crm/petcare_crm/petcare_crm/report/petcare_kpi_overview/`
- WooCommerce sample payload: `deliverables/woocommerce/sample_order_payload.json`
