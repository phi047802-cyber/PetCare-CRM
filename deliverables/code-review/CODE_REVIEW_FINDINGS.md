# Báo cáo rà soát và khắc phục mã nguồn PetCare CRM

Ngày rà soát: 15/11/2026  
Nhánh thực hiện: `audit/frappe-runtime-readiness`  
Phạm vi: Frappe API, DocType schema, RBAC, Owner Portal, lịch hẹn, Membership, VietQR và test contract.

## Kết quả hiện tại

- 13 test suite, tổng cộng **123/123 test pass**.
- Python compile, JSON parse và đối chiếu field truy vấn/payload với DocType đều pass.
- Toàn bộ API đăng nhập có authorization guard; guest endpoint được giới hạn bằng allowlist cố định.
- Không còn `frappe.set_user("Administrator")` trong API và không còn secret mặc định trong code.
- Chưa chạy được `bench migrate`/MariaDB thật vì workspace hiện không chứa Frappe site đang hoạt động. Việc này phải hoàn tất theo `LIVE_BENCH_CHECKLIST.md` trước khi merge vào `main`.

## Danh sách phát hiện đã xử lý

| ID | Mức độ | Phát hiện / ảnh hưởng | Khắc phục | Bằng chứng kiểm thử | Trạng thái |
|---|---|---|---|---|---|
| AUD-001 | P0 | Nhiều endpoint thay đổi dữ liệu cho Guest và có luồng tự nâng quyền Administrator. Người ngoài có thể ghi dữ liệu CRM. | Bỏ guest khỏi endpoint nội bộ, bỏ impersonation, thêm RBAC backend cho toàn bộ API authenticated. | Runtime contract `test_05`, audit guest tests. | Đã sửa |
| AUD-002 | P0 | Owner Portal và VietQR dùng secret fallback hardcode; portal token không hết hạn. | Bắt buộc secret tối thiểu 32 ký tự từ site config/env; token chứa expiry và kiểm tra HMAC constant-time. | Audit tests `03b`, `04b`, `04c`. | Đã sửa |
| AUD-003 | P0 | Đặt lịch Owner Portal ghi field không tồn tại (`service`, `source`) vào Case, dùng status `Open`, thiếu `case_type` và nuốt lỗi tạo Appointment. | Ánh xạ catalog sang Select hợp lệ, validate ngày giờ tương lai, tạo Appointment/Case đúng schema và để transaction rollback khi lỗi. | Runtime payload contract `test_04`. | Đã sửa |
| AUD-004 | P0 | Webhook Membership báo nạp tiền thành công nhưng không cộng số dư; Service Visit chỉ lưu thanh toán trong notes, chống trùng chỉ dựa RAM/cache. | Khóa dòng ví, cập nhật balance trước/sau, thêm mã giao dịch unique và trạng thái/giá trị/thời điểm thanh toán trên Service Visit. | Audit tests `03c`–`03e`. | Đã sửa |
| AUD-005 | P1 | Check-in Appointment tạo Service Visit thiếu `original_price` bắt buộc rồi `except: pass`, khiến lịch đã check-in nhưng không có phiếu dịch vụ. | Lấy giá catalog, tạo đủ payload và không che giấu lỗi insert. | Audit tests `10b`, `10c`. | Đã sửa |
| AUD-006 | P1 | Analytics/automation truy vấn field không tồn tại: `PetCare Lead.source`, Care Recommendation legacy fields và `Pet.owner`. | Đối chiếu lại toàn bộ literal query với 15 DocType schema và dùng field thật. | Runtime contract `test_03`. | Đã sửa |
| AUD-007 | P1 | Có thể chỉ định thẻ hội viên Active của khách khác khi tạo Service Visit, đặc biệt thẻ family không gắn Pet. | Khóa dòng Membership và xác thực customer/pet/ngày hiệu lực trước khi trừ quyền lợi. | Membership test `test_03b_cross_customer_membership_is_rejected`. | Đã sửa |
| AUD-008 | P1 | Installer tạo Veterinarian/Groomer nhưng metadata dùng Technician; Front Desk được tạo nhưng thiếu quyền DocType nên không vận hành được trên Desk. | Chuẩn hóa role Technician, thêm Front Desk permissions và đồng bộ metadata với ma trận RBAC. | Runtime contract `test_07`, `test_08`. | Đã sửa |
| AUD-009 | P1 | Renewal dùng field không tồn tại `validity_days` và đặt status `Renewed` ngoài Select schema. | Dùng `duration_months`, `add_months` và bổ sung trạng thái lịch sử `Renewed`. | Payload/schema contract và Membership suite. | Đã sửa |
| AUD-010 | P2 | Public WordPress endpoint trả thẳng exception nội bộ, có thể lộ thông tin DB. | Log lỗi phía server và chỉ trả thông báo chung cho client. | WordPress suite + source review. | Đã sửa |
| AUD-011 | P2 | Catalog/payment thiếu một số validation số âm, category/species và amount bằng 0. | Thêm whitelist/biên dữ liệu và từ chối webhook amount không dương. | Audit `03c` và Service Operations suite. | Đã sửa |
| AUD-012 | P1 | Test cũ dùng dữ liệu mock sai schema nên vẫn xanh dù runtime query/payload sai. | Thêm Suite 13 kiểm tra compile, JSON, query fields, get_doc payload, guest allowlist, secrets và RBAC consistency. | 8/8 Runtime Readiness Contract pass. | Đã sửa |
| AUD-013 | P1 | Mật khẩu Administrator demo cố định được ghi trong script và nhiều tài liệu, dễ bị tái sử dụng ngoài local. | Xóa credential mặc định; deploy bắt buộc `PETCARE_ADMIN_PASSWORD` tối thiểu 12 ký tự và đặt lại mật khẩu trên site. | PowerShell parse + repository secret regression check. | Đã sửa |
| AUD-014 | P1 | Script deploy copy controller/DocType mới nhưng không chạy migrate và không copy hooks/setup, có thể để code mới chạy trên schema/quyền cũ. | Đồng bộ hooks/setup, bắt buộc `bench migrate`, dừng ngay nếu migrate hoặc runtime test lỗi. | PowerShell parse; live execution còn chờ Docker/Bench. | Đã sửa mã nguồn, chờ chạy live |

## Lệnh xác minh đã chạy

```powershell
python apps/petcare_crm/petcare_crm/tests/run_all_tests.py
```

Kết quả: `123 passed`, `0 failed`, `0 errors`, `0 skipped`, `0 blocked`.

## Giới hạn xác minh

Các test host và static contract chứng minh logic/sự nhất quán mã nguồn, nhưng không thay thế kiểm thử Frappe runtime. Trước khi merge cần chạy migrate, test app, đăng nhập từng role và thử các luồng ghi dữ liệu trên site thật theo checklist đi kèm.
