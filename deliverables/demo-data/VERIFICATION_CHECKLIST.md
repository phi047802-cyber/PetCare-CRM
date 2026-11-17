# CHECKLIST XÁC MINH DATASET DEMO

> Chỉ đánh dấu hoàn thành sau khi có bằng chứng trên Frappe site thật.

## A. Chuẩn bị môi trường

- [ ] `bench --version` chạy thành công.
- [ ] `bench --site petcare.localhost list-apps` có `frappe` và `petcare_crm`.
- [ ] `bench --site petcare.localhost migrate` hoàn thành không lỗi.
- [ ] Không dùng `preview.html` thay cho Frappe Desk.

## B. Nạp và kiểm tra dữ liệu

- [ ] Chạy `petcare_crm.patches.v1_0.seed_demo_data.execute` thành công.
- [ ] Chạy lại seed lần hai vẫn không tăng số lượng demo.
- [ ] Chạy `petcare_crm.patches.v1_0.validate_demo_data.execute` nhận `status: PASS`.
- [ ] `failed_checks` là danh sách rỗng.
- [ ] Lưu log hoặc ảnh terminal vào `02-seed-command-pass.png`.

## C. Kiểm tra dữ liệu quan hệ

- [ ] Contact Nguyễn Văn An liên kết đúng hai Pet: Bơ và Đậu Đậu.
- [ ] Mỗi Service Visit liên kết đúng Contact và Pet.
- [ ] Membership liên kết đúng khách hàng, thú cưng và gói.
- [ ] Recommendation liên kết đúng Contact/Pet/Membership.
- [ ] ToDo tham chiếu đúng Care Recommendation.

## D. Kiểm tra hai module

- [ ] Care Recommendation có DUE_SOON, AT_RISK và RENEWAL.
- [ ] Có dữ liệu NEW, CONTACTED và CONVERTED.
- [ ] `PetCare KPI Overview` mở được và không rỗng.
- [ ] KPI Lead/Opportunity/Revenue/Membership/At-Risk đối chiếu được với List View.

## E. Kiểm tra WooCommerce A4.8

- [ ] Trước demo không có bản ghi sync của order ID sắp gửi.
- [ ] Gửi payload thật qua WordPress/WooCommerce hoặc Postman đúng chữ ký HMAC.
- [ ] Frappe tạo `WooCommerce Order Sync`.
- [ ] Contact, Pet và Opportunity được tạo hoặc tái sử dụng đúng.
- [ ] Gửi lại cùng Delivery ID không tạo bản ghi trùng.
- [ ] Đổi trạng thái đơn cập nhật đúng Sales Pipeline.

## F. Bằng chứng bàn giao

- [ ] Có đủ 11 ảnh theo `DEMO_DATASET_EVIDENCE.md`.
- [ ] Ảnh có tiêu đề Frappe Desk hoặc URL site.
- [ ] Không để lộ mật khẩu, API key, webhook secret hoặc `site_config.json`.
- [ ] Không commit database backup lên Git.
- [ ] Ghi ngày chạy, người thực hiện và commit hash vào báo cáo nhóm.

## Biên bản chạy

| Thông tin | Giá trị |
|---|---|
| Ngày chạy | Chưa thực hiện |
| Người thực hiện | Chưa điền |
| Site | `petcare.localhost` |
| Commit hash | Chưa điền |
| Seed result | Chưa thực hiện |
| Validator result | Chưa thực hiện |
| WooCommerce live result | Chưa thực hiện |
