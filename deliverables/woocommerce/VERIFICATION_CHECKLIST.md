# CHECKLIST MINH CHỨNG WOOCOMMERCE — A4.8

## Cài đặt

- [ ] Frappe site đã migrate và có DocType `WooCommerce Order Sync`.
- [ ] WordPress đã cài WooCommerce.
- [ ] Plugin PetCare CRM Lead Capture phiên bản 1.1.0 đã kích hoạt.
- [ ] URL CRM và shared secret đã cấu hình ở cả hai hệ thống.
- [ ] Chế độ đồng bộ đơn hàng đã bật.

## Ảnh cần chụp

- [ ] Cấu hình PetCare CRM trong WordPress (che secret).
- [ ] Checkout WooCommerce có thông tin khách hàng và thú cưng.
- [ ] Chi tiết đơn hàng và Order Note “đồng bộ thành công”.
- [ ] Danh sách `WooCommerce Order Sync` trên Frappe Desk.
- [ ] Bản ghi sync có Contact, Pet và Opportunity liên kết.
- [ ] Opportunity phản ánh đúng số tiền và trạng thái đơn.
- [ ] Postman trả `duplicate: true` khi gửi lại cùng Delivery ID.
- [ ] Frappe từ chối chữ ký HMAC sai.
- [ ] Kết quả 11/11 test WooCommerce PASS.

## Bằng chứng quá trình cá nhân

- [ ] GitHub Issue mô tả yêu cầu và tiêu chí nghiệm thu.
- [ ] Nhánh `feature/woocommerce-order-integration`.
- [ ] Commit riêng cho phân tích, backend, plugin, test và tài liệu.
- [ ] Pull Request có mô tả, ảnh và kết quả test.
- [ ] Có ít nhất một lượt review và một commit sửa theo review.
- [ ] Video cá nhân có mặt, giọng nói và thao tác trực tiếp.

## Tình huống phải demo

| Mã | Tình huống | Kết quả mong đợi |
|---|---|---|
| WC-01 | Tạo đơn mới | Tạo Contact/Pet/Opportunity và Sync record |
| WC-02 | Gửi lại cùng delivery | Không tạo thêm dữ liệu, trả `duplicate: true` |
| WC-03 | Đơn chuyển `completed` | Opportunity là `Closed Won` |
| WC-04 | Đơn chuyển `cancelled` | Opportunity là `Closed Lost` |
| WC-05 | Chữ ký sai | Request bị từ chối, không ghi database |
| WC-06 | CRM mất kết nối | WordPress lên lịch retry bằng Action Scheduler |

