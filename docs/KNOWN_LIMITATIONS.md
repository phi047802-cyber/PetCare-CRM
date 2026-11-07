# CÁC GIỚI HẠN HIỆN TẠI & ĐỊNH HƯỚNG MỞ RỘNG (KNOWN LIMITATIONS & EXTENDED WORK)

> **Dự án**: PetCare CRM (Hệ Thống CRM Dịch Vụ Chăm Sóc Thú Cưng)  
> **Nền tảng**: Frappe Framework v15  
> **Phiên bản tài liệu**: 2.0 (Post-Prompt 10 Extension Release)  
> **Trạng thái kiểm thử**: 68/68 Tests PASS (100%) across 8 Test Suites  

---

## 1. Tuyên Bố Về Trạng Thái Hệ Thống (Maturity Declaration)

> [!IMPORTANT]
> PetCare CRM đã được nâng cấp toàn diện từ cấp độ Proof of Concept lên **Advanced Functional Prototype Ready-for-Integration** với đầy đủ các luồng nghiệp vụ cốt lõi, kiến trúc Clean Architecture, bộ 47 REST APIs đạt chuẩn, và toàn bộ bộ kiểm thử tự động **68/68 tests** đạt 100% tỷ lệ thành công.
> 
> Hệ thống đáp ứng trọn vẹn yêu cầu bảo vệ giao dịch (Atomic Transaction), chống trùng lặp (Idempotency), đối soát ngân hàng tự động (Dynamic VietQR IPN), điều phối thông báo đa kênh (Zalo ZNS & SMS Brandname), và bộ API chuyên biệt dành riêng cho Ứng dụng di động của Chủ nuôi (Pet Owner Mobile App).

---

## 2. Báo Cáo Xử Lý Các Giới Hạn Đã Triển Khai (Resolved Limitations)

Dưới đây là chi tiết các hạng mục giới hạn đã được phân tích, chọn lọc và **triển khai hoàn tất ngay trong mã nguồn**:

| Hạng mục ban đầu | Phân loại & Khả năng làm ngay | Trạng thái giải quyết | Module kỹ thuật triển khai |
|---|---|---|---|
| **2.1. Yếu tố Mùa vụ & Độ tuổi thú cưng** | Làm được ngay trong Rule-based Engine | **ĐÃ HOÀN THÀNH (RESOLVED)** | `SeasonalAdjustmentHelper`, `PetAgeAdjustmentHelper` trong `care_pattern_service.py` |
| **2.2. Dynamic VietQR & Webhook ngân hàng** | Làm được ngay theo chuẩn Napas247 & Webhook IPN | **ĐÃ HOÀN THÀNH (RESOLVED)** | `VietQRGenerator`, `PaymentWebhookService` trong `payment_gateway.py` |
| **2.3. Thông báo đa kênh (ZNS, SMS Brandname)** | Làm được ngay qua Gateway Pattern & Outbox Preview | **ĐÃ HOÀN THÀNH (RESOLVED)** | `OmnichannelDispatcher`, `ZaloZNSAdapter`, `SMSBrandnameAdapter` trong `omnichannel_service.py` |
| **2.4. Cổng dịch vụ Chủ nuôi (Owner App API)** | Làm được ngay qua REST API Suite trong Frappe | **ĐÃ HOÀN THÀNH (RESOLVED)** | Bộ 4 endpoints Cổng Chủ Nuôi (`owner_portal_*`) trong `api.py` |
| **2.5. Vận hành Đa Chi Nhánh (Multi-branch)** | Làm được ngay qua Data Scoping & KPI Comparison | **ĐÃ HOÀN THÀNH (RESOLVED)** | `CLINIC_BRANCHES` trong `config.py` và `get_branch_comparison_metrics` trong `analytics_service.py` |

---

### Chi Tiết Kỹ Thuật Đã Triển Khai:

### 2.1. Về Thuật Toán Phân Tích Chu Kỳ (Care Intelligence)
* **Yếu tố Mùa vụ (Seasonal Shedding Factor)**:
  * Đã bổ sung `SeasonalAdjustmentHelper` nhận diện mùa rụng lông mùa xuân (tháng 3-4, factor = `0.85`), mùa nóng ẩm mưa nhiều gây viêm da (tháng 5-8, factor = `0.80`), và mùa thay lông đón lạnh mùa thu (tháng 9-10, factor = `0.88`).
* **Yếu tố Độ tuổi Thú cưng (Developmental Age Factor)**:
  * Đã bổ sung `PetAgeAdjustmentHelper` phân hóa chó/mèo con (< 12 tháng tuổi, factor = `0.85` do lông mọc nhanh và cần tạo thói quen vệ sinh) và thú cưng già (> 7 tuổi, factor = `0.80` nhằm tăng cường tần suất kiểm tra khớp và da lông).
* **Minh bạch thuật toán (Explainability)**:
  * Chu kỳ dự đoán hiển thị rõ các hệ số điều chỉnh trong `reason` (ví dụ: *"Dự đoán ngày 2026-04-24 dựa trên chu kỳ điển hình 21.7 ngày (hệ số mùa vụ=0.85, hệ số độ tuổi=0.85)..."*).

### 2.2. Về Thanh Toán & Tích Hợp Cổng Tài Chính (Payment Gateways)
* **Dynamic VietQR Generator**:
  * Tạo URL mã QR động chuẩn Napas247 QuickLink cho từng phiếu `Service Visit` (`PC-SVC-{visit_id}`) và giao dịch nạp ví hội viên (`PC-MEM-{membership_id}-{txn_id}`).
  * Khách hàng quét mã bằng ứng dụng bất kỳ của 40+ ngân hàng Việt Nam (Vietcombank, MB, Techcombank, ACB...).
* **Payment Webhook & Tự Động Đối Soát (Auto-Reconciliation)**:
  * Tích hợp `PaymentWebhookService` và API `@frappe.whitelist(allow_guest=True) payment_webhook` tiếp nhận biến động số dư ngân hàng theo thời gian thực.
  * Tự động bóc tách cú pháp chuyển khoản bằng Regex, đối soát số tiền, và cập nhật trạng thái phiếu dịch vụ hoặc tự động nạp tiền ví thẻ hội viên.
  * Cơ chế chống gian lận & Idempotency: Giao dịch ngân hàng đã xử lý sẽ bị từ chối nếu có yêu cầu replay lặp lại.

### 2.3. Về Kênh Giao Tiếp Khách Hàng Đa Kênh (Omnichannel Communication)
* **Omnichannel Notification Gateway**:
  * Cung cấp kiến trúc điều phối thông báo hỗ trợ 3 kênh: `ZALO_ZNS` (Zalo Cloud API), `SMS_BRANDNAME` (Viettel/VNPT telco format), và `EMAIL`.
  * Cơ chế **Safe Mode Outbox Preview**: Toàn bộ tin nhắn trong môi trường thử nghiệm được ghi nhận vào nhật ký Outbox để nhân viên CSKH có thể xem trước chính xác nội dung hiển thị trên điện thoại khách hàng mà không tốn phí viễn thông thực tế.
  * Khi kích hoạt `ENABLE_LIVE_COMMUNICATION = True`, hệ thống kết nối trực tiếp đến hạ tầng viễn thông.

### 2.4. Về Giao Diện Khách Hàng (Customer-facing Portal / Mobile App)
* **Bộ REST APIs chuẩn cho Ứng dụng Di Động Chủ Nuôi (Pet Owner App)**:
  * `owner_portal_get_pets(customer_id)`: Trả về danh sách thú cưng, giống loài, cân nặng và ngày hẹn dịch vụ tiếp theo.
  * `owner_portal_get_health_timeline(customer_id, pet_id)`: Sổ y bạ / dòng thời gian lịch sử tiêm phòng, khám chữa bệnh và chăm sóc spa.
  * `owner_portal_get_membership_wallet(customer_id)`: Tra cứu số dư thẻ hội viên, quyền lợi miễn phí còn lại, thời hạn hiệu lực.
  * `owner_portal_book_appointment(customer_id, pet_id, service_id, preferred_datetime)`: Chủ nuôi tự bấm đặt lịch online qua ứng dụng điện thoại; hệ thống tự động sinh `PetCare Case` phân công tiếp nhận cho nhân viên lễ tân.

### 2.5. Về Quy Mô & Vận Hành Đa Chi Nhánh (Multi-branch Operations)
* **Multi-branch Data Scoping**:
  * Bổ sung mạng lưới chi nhánh chuẩn (`CN-TRUNGTAM`, `CN-QUAN1`, `CN-THUDUC`, `CN-BINHTHANH`).
  * Mở rộng `AnalyticsService.get_branch_comparison_metrics` phân tích phân đoạn doanh thu và lưu lượng khách khám theo từng cơ sở trực thuộc.

---

## 3. Các Giới Hạn Khách Quan Còn Lại (Remaining Infrastructure Prerequisites)

Các hạng mục dưới đây thuộc về yếu tố **pháp lý thương mại và hạ tầng doanh nghiệp bên ngoài**, cần được thiết lập khi đưa vào môi trường sản xuất thực tế:

1. **Hợp đồng Doanh nghiệp Viễn thông**:
   * Việc chuyển từ `Safe Mode` sang `Live Mode` cho Zalo ZNS và SMS Brandname đòi hỏi hợp đồng thương mại trực tiếp với VNG Cloud (Tick vàng Zalo OA) và các nhà mạng (Viettel, VNPT) cùng giấy phép định danh thương hiệu.
2. **Tài khoản Merchant Ngân hàng**:
   * Để cấp phát tài khoản ngân hàng ảo (Virtual Account) chuyên dụng cho từng khách hàng theo thời gian thực (thay vì số tài khoản chung của phòng khám), cần ký hợp đồng cổng thanh toán (PayOS, Cass, SeABank, VNPay).
3. **Mô hình Machine Learning quy mô lớn**:
   * Việc thay thế Rule-based EWMA/IQR bằng mô hình Học máy sâu (Deep Learning / Random Forest) cần tối thiểu 100,000 lượt dịch vụ được gán nhãn thực tế sau 6 - 12 tháng vận hành chuỗi phòng khám.

---

## 4. Bảng Tổng Hợp Kiểm Thử Sau Mở Rộng

```
================================================================================
PETCARE CRM — AUTOMATED TEST SUITE & END-TO-END VALIDATOR
================================================================================
Suite 1: CRM Core & Lead/Opportunity Lifecycle              : [PASS] (4/4 tests)
Suite 2: PetCare Service Operations & Visit Catalog          : [PASS] (4/4 tests)
Suite 3: Membership Lifecycle, Benefits & Redemption Engine  : [PASS] (8/8 tests)
Suite 4: Care Intelligence, Pattern Analytics & Deduplication: [PASS] (11/11 tests)
Suite 5: Workflow Automation & Scheduled Jobs                : [PASS] (9/9 tests)
Suite 6: Security, RBAC Matrix & Analytics KPIs              : [PASS] (11/11 tests)
Suite 7: End-to-End (E2E) Scenarios A-F                      : [PASS] (11/11 tests)
Suite 8: Advanced Extensions & Resolved Limitations          : [PASS] (10/10 tests)
--------------------------------------------------------------------------------
TỔNG SỐ KỊCH BẢN KIỂM THỬ: 68/68 TESTS PASS (100% SUCCESS RATE)
================================================================================
```
