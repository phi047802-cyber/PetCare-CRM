# Checklist xác minh trên Frappe Bench thật

Thực hiện trên site thử nghiệm trước khi merge/deploy production. Không đưa secret thật vào Git.

Với `deploy_clean.ps1`, đặt trước bốn biến môi trường: `PETCARE_ADMIN_PASSWORD`, `PETCARE_OWNER_PORTAL_SECRET`, `PETCARE_VIETQR_WEBHOOK_SECRET`, `PETCARE_WOOCOMMERCE_WEBHOOK_SECRET`.

## 1. Cấu hình bắt buộc

Trong `sites/<site>/site_config.json`, cấu hình hai secret ngẫu nhiên, mỗi secret tối thiểu 32 ký tự:

```json
{
  "owner_portal_secret": "<random-secret-min-32-characters>",
  "vietqr_webhook_secret": "<random-secret-min-32-characters>",
  "woocommerce_webhook_secret": "<woocommerce-shared-secret>"
}
```

## 2. Migrate và build

```bash
bench --site <site> backup
bench --site <site> migrate
bench build --app petcare_crm
bench --site <site> clear-cache
```

Kỳ vọng: migrate tạo các field thanh toán mới trên Service Visit, unique index cho gateway transaction/reference number và cập nhật quyền role không lỗi.

## 3. Chạy test runtime

```bash
bench --site <site> run-tests --app petcare_crm
python apps/petcare_crm/petcare_crm/tests/run_all_tests.py
```

Lưu ảnh/log: tổng số test, thời gian, commit SHA và tên site.

## 4. Smoke test theo role

- `PetCare Front Desk`: tạo Lead, Pet, Appointment; check-in; xem Membership/Case.
- `PetCare Sales`: tạo/cập nhật Lead và Opportunity; không được sửa catalog dịch vụ.
- `PetCare Technician`: cập nhật Pet/Service Visit; không truy cập Lead/Opportunity.
- `PetCare Analyst`: chỉ đọc/report/export; thử ghi dữ liệu phải bị từ chối.
- Guest: chỉ gọi đúng 8 public endpoint; endpoint nội bộ phải trả 401/403.

## 5. Smoke test nghiệp vụ quan trọng

- Owner Portal: token hợp lệ, token sai, token hết hạn, đặt lịch tương lai, từ chối lịch quá khứ.
- Appointment: check-in tạo đúng một Service Visit có `original_price` từ catalog.
- Membership: không dùng được thẻ của customer/pet khác.
- VietQR: signature đúng/sai; top-up tăng đúng balance; gửi lại cùng transaction ID không cộng lần hai.
- Service Visit payment: trạng thái `Paid`, `paid_amount`, `paid_at`, `gateway_transaction_id` được lưu.
- WooCommerce: webhook đúng secret tạo/cập nhật đúng một sync record khi retry.

## 6. Điều kiện được merge

- `bench migrate` thành công trên bản sao dữ liệu.
- Tất cả test pass và không có traceback trong Error Log.
- Smoke test role và bốn luồng Owner Portal/Appointment/Membership/Payment đều đạt.
- Không có secret thật, file backup hoặc database dump trong Git diff.
