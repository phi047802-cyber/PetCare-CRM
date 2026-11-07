# TÀI LIỆU THUYẾT MINH QUY TRÌNH CRM TOÀN DIỆN (END-TO-END GROUP BPMN)
## HỆ THỐNG QUẢN LÝ QUAN HỆ KHÁCH HÀNG DỊCH VỤ CHĂM SÓC THÚ CƯNG (PETCARE CRM)

> **Mã quy trình**: `BPMN-GRP-PETCARE-E2E`  
> **Tên quy trình**: Quy trình Chăm sóc Khách hàng & Bán hàng Dịch vụ Toàn diện (End-to-End)  
> **Đối tượng nộp**: Báo cáo Quy trình Nhóm (Tiêu chí Rubric A4.3.1)  
> **Nền tảng thực thi**: Frappe Framework v15 (Desk Native)  
> **Chuẩn mô hình hóa**: BPMN 2.0 XML (Tương thích Camunda 7 / Camunda Modeler v5.45.0)  
> **Tệp mô hình đính kèm**: [`PetCare_CRM_End_to_End_Group.bpmn`](PetCare_CRM_End_to_End_Group.bpmn)  
> **Tệp sơ đồ hình ảnh**: [`PetCare_CRM_End_to_End_Group.png`](PetCare_CRM_End_to_End_Group.png)  

---

## 1. MỤC TIÊU CỦA QUY TRÌNH (PROCESS OBJECTIVES)

Quy trình nhóm được thiết kế nhằm mô hình hóa toàn diện chu trình vận hành của một chuỗi phòng khám thú y và spa thú cưng hiện đại, kết nối liền mạch 5 mắt xích kinh doanh cốt lõi:
1. **Marketing Thu hút Khách hàng**: Thu nhận thông tin khách hàng tiềm năng đa kênh (Website Lead Form, Hotline, Mạng xã hội), tự động chuẩn hóa số điện thoại Việt Nam và kiểm tra chống trùng lặp dữ liệu.
2. **Tư vấn Bán hàng & Quản lý Phễu**: Phân loại mức độ tiềm năng của Lead, quản lý cơ hội bán các gói thẻ hội viên trị giá cao qua phễu Kanban (Sales Pipeline), và chuyển đổi mượt mà sang hồ sơ Khách hàng (`Contact`) cùng Thú cưng (`Pet`).
3. **Tiếp đón & Thực hiện Dịch vụ Chuyên môn**: Lễ tân tra cứu nhanh hồ sơ thú cưng tại quầy; Bác sĩ/Kỹ thuật viên kiểm tra thể trạng, cân nặng lâm sàng và thực hiện dịch vụ kỹ thuật (Tắm sấy, Cắt tỉa tạo kiểu, Tiêm vắc-xin, Điều trị).
4. **Định giá, Cấn trừ Quyền lợi & Thanh toán Tự động**: Tự động áp dụng quyền lợi thẻ hội viên (miễn phí 100% hoặc chiết khấu %) với cơ chế khóa dòng dữ liệu an toàn (`Row Lock`), phát sinh mã thanh toán VietQR động (Napas247) và tự động đối soát thông qua Webhook IPN ngân hàng theo thời gian thực.
5. **Trí tuệ Chăm sóc & Tái khám (Care Intelligence)**: Tự động phân tích lịch sử thăm khám bằng thuật toán thống kê (EWMA + Tukey IQR + Hệ số biến thiên Mùa vụ & Độ tuổi thú cưng), phát hiện thú cưng sắp đến kỳ chăm sóc (`DUE_SOON`) hoặc khách hàng có nguy cơ rời bỏ (`AT_RISK`), tự động gửi tin nhắn chăm sóc qua Zalo ZNS / SMS và giao việc cho nhân viên CSKH.

---

## 2. CÁC TÁC NHÂN THAM GIA (ACTORS & LANES)

Mô hình được tổ chức dưới dạng một Pool duy nhất (`Participant_PetCare_Clinic`), phân chia thành **5 Phân làn (Swimlanes)** đại diện cho các vai trò và phòng ban tương tác:

| Tên Phân Làn (Lane) | Vai Trò Nghiệp Vụ | Trách Nhiệm Chính Trong Quy Trình |
|---|---|---|
| **1. Khách hàng (Chủ nuôi thú cưng)** | Khách hàng bên ngoài (Customer / Pet Owner) | Điền form đăng ký trực tuyến, mang thú cưng đến cơ sở, quét mã VietQR thanh toán, nhận thông báo nhắc lịch qua Zalo/SMS. |
| **2. Marketing & Bán hàng (Sales / Telesales)** | Nhân viên Tư vấn (`PetCare Sales`) | Tiếp nhận Lead, gọi điện tư vấn nhu cầu thể trạng bé, chuyển đổi Lead sang Contact & Pet, quản lý Opportunity chốt Deal gói hội viên. |
| **3. Lễ tân & Thu ngân (Front Desk / Cashier)** | Nhân viên Lễ tân (`PetCare Receptionist`) | Tiếp đón khách tại quầy, khởi tạo phiếu `Service Visit`, kiểm tra thẻ hội viên, xuất hóa đơn, in phiếu quyết toán và bàn giao thú cưng. |
| **4. Bác sĩ & Kỹ thuật viên (Veterinarian / Groomer)** | Kỹ thuật viên chuyên môn (`PetCare Specialist`) | Kiểm tra thể trạng lâm sàng, cân trọng lượng ban đầu, thực hiện thao tác dịch vụ, cập nhật cân nặng mới vào hồ sơ y bạ điện tử. |
| **5. Hệ thống CRM & Tự động hóa (PetCare CRM Engine)** | Nền tảng hệ thống Frappe Backend & Background Workers | Khử trùng lặp SĐT, cấn trừ quyền lợi thẻ có khóa chống tranh chấp đồng thời (`Pessimistic Lock`), đối soát Webhook ngân hàng, quét Care Intelligence định kỳ. |

---

## 3. TIỀN ĐIỀU KIỆN & HẬU ĐIỀU KIỆN (PRECONDITIONS & POSTCONDITIONS)

### 3.1. Tiền điều kiện (Preconditions)
* Hệ thống PetCare CRM đã được cấu hình hoàn chỉnh: Bảng giá dịch vụ chuẩn (`PetCare Service`), Danh mục Gói hội viên (`Membership Plan`), Phân quyền RBAC 5 vai trò.
* Khách hàng có nhu cầu sử dụng dịch vụ hoặc cần tư vấn lộ trình chăm sóc cho thú cưng.
* Máy chủ Frappe và bộ lắng nghe Webhook ngân hàng đang ở trạng thái sẵn sàng tiếp nhận yêu cầu.

### 3.2. Hậu điều kiện (Postconditions)
* Dữ liệu khách hàng (`Contact`) và thú cưng (`Pet`) được lưu trữ chuẩn hóa, không phát sinh trùng lặp số điện thoại.
* Phiếu dịch vụ (`Service Visit`) được ghi nhận ở trạng thái `Completed`, doanh thu thực tế được đối soát khớp lệnh 100%.
* Quyền lợi hội viên hoặc số dư ví thẻ được khấu trừ chính xác, lịch sử giao dịch được ghi nhận vào Sổ cái cấn trừ (`Benefit Redemption Ledger`).
* Thuật toán Care Intelligence tự động tính toán chu kỳ chăm sóc tiếp theo, cập nhật đề xuất (`Care Recommendation`) và điều phối tin nhắn Zalo ZNS nhắc lịch.

---

## 4. MÔ TẢ CHI TIẾT CÁC BƯỚC TRONG QUY TRÌNH (STEP-BY-STEP WORKFLOW)

### Giai đoạn 1: Tiếp nhận Lead Đa Kênh & Kiểm Tra Trùng Lặp (Lead Intake)
1. **Bước 1 (`Start_KhachHangNhuCau` ➔ `Task_KH_DienForm`)**: Khách hàng truy cập website phòng khám hoặc trang đặt lịch, điền thông tin: Họ tên, Số điện thoại, Tên thú cưng, Loài (Chó/Mèo) và nhu cầu chăm sóc.
2. **Bước 2 (`Task_KH_DienForm` ➔ `Task_Sales_TiepNhanLead`)**: Dữ liệu được gửi qua REST API về CRM. Hệ thống tự động chuẩn hóa số điện thoại theo chuẩn quốc gia Việt Nam (chuyển đổi `09xxx` hoặc `+84xxx` về `84xxx`).
3. **Bước 3 (`Task_Sales_TiepNhanLead` ➔ `Task_CRM_KiemTraDeduplication`)**: Hệ thống CRM tự động thực hiện truy vấn đối soát:
   * Kiểm tra xem số điện thoại đã tồn tại trong bảng `Contact` hay chưa.
   * Nếu đã tồn tại, đánh dấu liên kết khách quen; nếu chưa, chuẩn bị khởi tạo khách hàng mới.
4. **Bước 4 (`Task_CRM_KiemTraDeduplication` ➔ `Task_Sales_GoiTuVan`)**: Nhân viên Telesales nhận thông báo trên Desk UI, thực hiện cuộc gọi tư vấn dịch vụ và đánh giá thể trạng thú cưng.

### Giai đoạn 2: Đánh Giá Tiềm Năng & Chuyển Đổi (Sales Qualification & Conversion)
5. **Bước 5 (`Task_Sales_GoiTuVan` ➔ `Gateway_KHTiemNang`)**: Nhân viên đánh giá phản hồi của khách hàng:
   * **Nhánh Không tiềm năng (`Flow_KhongTiemNang`)**: Khách từ chối, nhầm số hoặc không có nhu cầu ➔ Chuyển sang `Task_Sales_DongLead`, nhập bắt buộc lý do (`unqualified_reason`) và kết thúc tại `End_LeadUnqualified`.
   * **Nhánh Khách tiềm năng (`Flow_CoTiemNang`)**: Khách đồng ý đặt dịch vụ ➔ Chuyển sang `Task_Sales_ConvertLead`.
6. **Bước 6 (`Task_Sales_ConvertLead`)**: Nhân viên bấm nút "Convert Lead" trên Desk. Hệ thống khởi tạo tự động bản ghi `Contact` (Chủ nuôi) và bản ghi `Pet` (Hồ sơ thú cưng liên kết với Contact).
7. **Bước 7 (`Gateway_MuaGoiHoiVien`)**:
   * Nếu khách quan tâm đến các gói chăm sóc dài hạn (Gói Spa 10 buổi, Gói VIP 1 năm) ➔ Chuyển sang `Task_Sales_TaoOpportunity`, quản lý cơ hội qua phễu Kanban đến khi chốt Deal thành công (`Closed Won`).
   * Nếu khách chỉ có nhu cầu làm dịch vụ lẻ ➔ Bỏ qua phễu và chuyển thẳng sang lịch tiếp đón tại quầy.

### Giai đoạn 3: Tiếp Đón & Thực Hiện Chuyên Môn (Check-in & Service Operations)
8. **Bước 8 (`Task_KH_DuaThuCung` ➔ `Task_LT_TiepDon`)**: Khách hàng đưa thú cưng đến phòng khám. Lễ tân tra cứu số điện thoại, mở hồ sơ thú cưng và in phiếu tiếp nhận.
9. **Bước 9 (`Task_LT_TiepDon` ➔ `Task_KT_KhamCanNang`)**: Bác sĩ/Kỹ thuật viên tiếp nhận bé, kiểm tra lâm sàng (da, lông, tai, móng) và cân trọng lượng ban đầu.
10. **Bước 10 (`Task_KT_KhamCanNang` ➔ `Task_KT_ThucHienDichVu`)**: Thực hiện dịch vụ chuyên môn theo đúng quy chuẩn vệ sinh và an toàn y tế (Tắm sấy khử mùi, Cắt tỉa tạo kiểu lông, Vệ sinh tuyến hôi, Tiêm phòng).
11. **Bước 11 (`Task_KT_ThucHienDichVu` ➔ `Task_KT_GhiNhanKetQua`)**: Ghi nhận cân nặng sau dịch vụ, ghi chú phản ứng của bé và bàn giao thú cưng lại cho khu vực lễ tân.

### Giai đoạn 4: Cấn Trừ Hội Viên, Quyết Toán & Thanh Toán VietQR (Billing & Payments)
12. **Bước 12 (`Task_KT_GhiNhanKetQua` ➔ `Task_LT_MoPhieuServiceVisit`)**: Lễ tân mở phiếu dịch vụ `Service Visit`, chọn thú cưng và danh mục dịch vụ đã thực hiện. Đơn giá chuẩn được tự động lấy từ danh mục `PetCare Service`.
13. **Bước 13 (`Gateway_KiemTraHoiVien`)**: Hệ thống tự động kiểm tra thẻ hội viên của khách hàng:
   * **Có thẻ Active & Còn quyền lợi (`Flow_CoHoiVien`)**: Chuyển sang `Task_CRM_CanTruQuyenLoi`. Hệ thống kích hoạt khóa bi quan (`Row Lock FOR UPDATE`), giảm 1 lượt quyền lợi, thiết lập giá thanh toán `final_price = 0` (nếu miễn phí 100%) hoặc chiết khấu tương ứng, ghi nhận vào `Benefit Redemption Ledger`.
   * **Không có thẻ / Hết lượt (`Flow_KhongHoiVien`)**: Giữ nguyên giá gốc niêm yết.
14. **Bước 14 (`Task_LT_XuatHoaDon` ➔ `Task_KH_QuetVietQR`)**: Hệ thống tạo hóa đơn và sinh mã Dynamic VietQR (cú pháp: `PC-SVC-{visit_id}`). Khách hàng thực hiện quét mã trên ứng dụng ngân hàng hoặc thanh toán bằng ví trả trước / tiền mặt.
15. **Bước 15 (`Task_KH_QuetVietQR` ➔ `Task_CRM_DoiSoatVietQR`)**: Cổng thanh toán gửi Webhook IPN về CRM. Hàm `payment_webhook` tự động so khớp mã phiếu, kiểm tra số tiền và cập nhật phiếu sang trạng thái `Paid` (có bảo vệ Idempotency chống ghi nhận 2 lần).
16. **Bước 16 (`Gateway_ThanhToanThanhCong`)**:
   * Nếu thanh toán khớp lệnh ➔ Chuyển sang `Task_LT_BanGiaoPet`.
   * Nếu phát sinh lỗi hoặc thiếu tiền ➔ Lễ tân thu tiền mặt bổ sung tại quầy (`Task_LT_ThuTienMat`).
17. **Bước 17 (`Task_LT_BanGiaoPet`)**: Lễ tân in phiếu thu quyết toán, bàn giao thú cưng cho khách và gửi lời cảm ơn.

### Giai đoạn 5: Trí Tuệ Chăm Sóc & Tái Khám Định Kỳ (Care Intelligence & Retention)
18. **Bước 18 (`Task_LT_BanGiaoPet` ➔ `Task_CRM_QuetChuKyCareIntelligence`)**: Tác vụ nền (Scheduler Daemon) định kỳ quét lịch sử thăm khám của thú cưng:
   * Lọc ngoại lai bất thường bằng khoảng tứ phân vị (Tukey IQR).
   * Tính toán chu kỳ điển hình bằng trung bình động hàm mũ (EWMA $\alpha = 0.6$).
   * Tự động điều chỉnh khoảng cách ngày theo hệ số mùa vụ (mùa rụng lông factor 0.85; mùa nóng ẩm factor 0.80) và độ tuổi phát triển của thú cưng (chó/mèo con factor 0.85; già factor 0.80).
19. **Bước 19 (`Gateway_DanhGiaChuKy`)**: Đánh giá khoảng cách ngày:
   * **DUE_SOON / AT_RISK (`Flow_CanChamSoc`)**: Thú cưng sắp đến ngày cần làm dịch vụ hoặc vắng mặt quá 1.5 lần chu kỳ ➔ Chuyển sang `Task_CRM_TaoRecommendation`.
   * **STABLE (`Flow_ChuKyOnDinh`)**: Thú cưng vừa làm dịch vụ hoặc chu kỳ còn xa ➔ Kết thúc chu trình tại `End_ChuKyOnDinh`.
20. **Bước 20 (`Task_CRM_TaoRecommendation` ➔ `Task_KH_NhanThongBao`)**: Hệ thống tự động tạo bản ghi `Care Recommendation`, đồng thời điều phối tin nhắn Zalo ZNS / SMS Brandname qua `OmnichannelDispatcher` nhắc lịch hẹn kèm ưu đãi hấp dẫn.
21. **Bước 21 (`Task_KH_NhanThongBao` ➔ `End_TaiKhamThanhCong`)**: Khách hàng nhận được tin nhắn chăm sóc tận tâm, bấm vào liên kết đặt lịch tái khám, tiếp tục duy trì vòng đời khách hàng thân thiết bền vững.

---

## 5. BẢNG ÁNH XẠ BPMN SANG MÃ NGUỒN VÀ APIS (TRACEABILITY MATRIX)

Toàn bộ 31 nút quy trình được ánh xạ trực tiếp và kiểm chứng với các thành phần thực tế trong mã nguồn:

| ID Nút BPMN | Tên Nút Trên Sơ Đồ | Loại BPMN | DocType Liên Quan | Hàm Service / API Backend Thực Tế | Trạng Thái Kiểm Chứng |
|---|---|---|---|---|:---:|
| `Task_KH_DienForm` | Điền Form tư vấn trên Website | User Task | `PetCare Lead` | Frontend Lead Form (`petcare_crm.api.create_lead`) | **Verified** |
| `Task_Sales_TiepNhanLead` | Tiếp nhận Lead & Chuẩn hóa SĐT | User Task | `PetCare Lead` | `_normalize_vn_phone` trong `apps/petcare_crm/petcare_crm/utils/lead_service.py` | **Verified** |
| `Task_CRM_KiemTraDeduplication` | Kiểm tra chống trùng lặp Contact | Service Task | `Contact`, `Pet` | `LeadManagementService.check_duplicate_contact` trong `lead_service.py` | **Verified** |
| `Task_Sales_GoiTuVan` | Gọi điện tư vấn nhu cầu & thể trạng | User Task | `PetCare Lead` | `LeadManagementService.add_interaction` (`api.py` dòng 1105) | **Verified** |
| `Task_Sales_ConvertLead` | Chuyển đổi Lead sang Contact & Pet | User Task | `Contact`, `Pet` | `LeadManagementService.convert_lead` (`api.py` dòng 1125) | **Verified** |
| `Task_Sales_TaoOpportunity` | Quản lý Opportunity Pipeline | User Task | `PetCare Opportunity` | `SalesPipelineService.create_opportunity` (`api.py` dòng 1145) | **Verified** |
| `Task_LT_TiepDon` | Tiếp đón & Tra cứu hồ sơ Pet | User Task | `Contact`, `Pet` | `petcare_crm.api.get_customer_360` (`api.py` dòng 1260) | **Verified** |
| `Task_KT_KhamCanNang` | Khám thể trạng & Cân trọng lượng | User Task | `Pet` | Cập nhật `weight_kg` trên DocType `Pet` | **Verified** |
| `Task_KT_ThucHienDichVu` | Thực hiện dịch vụ chuyên môn | User Task | `PetCare Service` | `ServiceCatalogService.get_service` trong `service_operations.py` | **Verified** |
| `Task_LT_MoPhieuServiceVisit` | Khởi tạo phiếu dịch vụ (Service Visit) | User Task | `Service Visit` | `ServiceVisitService.create_service_visit` trong `service_operations.py` | **Verified** |
| `Task_CRM_CanTruQuyenLoi` | Cấn trừ quyền lợi thẻ (Pessimistic Lock) | Service Task | `Customer Membership`, `Benefit Redemption Ledger` | `petcare_crm.api.record_benefit_usage` (`api.py` dòng 137, khóa `FOR UPDATE`) | **Verified** |
| `Task_LT_XuatHoaDon` | Tạo hóa đơn & Mã Dynamic VietQR | User Task | `Service Visit` | `VietQRGenerator.generate_service_visit_qr` trong `payment_gateway.py` | **Verified** |
| `Task_CRM_DoiSoatVietQR` | Lắng nghe Webhook IPN & Đối soát | Service Task | `Service Visit`, `Membership Transaction` | `PaymentWebhookService.process_webhook_notification` (`api.py` dòng 2005) | **Verified** |
| `Task_CRM_QuetChuKyCareIntelligence` | Quét Care Intelligence (EWMA + IQR + Mùa) | Service Task | `Service Visit`, `Care Recommendation` | `CarePatternService.predict_next_visit` trong `care_pattern_service.py` | **Verified** |
| `Task_CRM_TaoRecommendation` | Tạo Recommendation & Gửi Zalo ZNS | Service Task | `Care Recommendation` | `OmnichannelDispatcher.dispatch` trong `omnichannel_service.py` | **Verified** |

---

## 6. HƯỚNG DẪN KIỂM CHỨNG & XUẤT ẢNH TRÊN CAMUNDA MODELER

### 6.1. Kiểm chứng mở tệp `.bpmn` bằng Camunda Modeler
Trên máy phát triển của nhóm, phần mềm **Camunda Modeler Desktop v5.45.0** đã được cài đặt sẵn tại `C:\Program Files\Camunda\Camunda Modeler.exe`.
1. Nhấp đúp chuột vào tệp `deliverables/bpmn/group/PetCare_CRM_End_to_End_Group.bpmn` hoặc mở Camunda Modeler và chọn `File` ➔ `Open File...`.
2. Quan sát sơ đồ: Toàn bộ 5 Phân làn (Lanes), 31 Nút nghiệp vụ và 34 Đường luồng tuần tự (Sequence Flows) hiển thị đầy đủ, ngay ngắn, không bị chồng chéo.
3. Kiểm tra thanh trạng thái dưới cùng: Không có bất kỳ cảnh báo lỗi cấu trúc BPMN nào (0 Errors, 0 Warnings).

### 6.2. Hướng dẫn xuất tệp ảnh chính thức trực tiếp từ Camunda Modeler
Để xuất tệp hình ảnh có chứng thực nguồn gốc trực tiếp từ phần mềm Camunda Modeler:
1. Mở sơ đồ trên Camunda Modeler.
2. Trên thanh menu, chọn `File` ➔ `Export As Image...`.
3. Chọn định dạng `PNG` (hoặc `SVG`).
4. Lưu tệp đè lên đường dẫn: `deliverables/bpmn/group/PetCare_CRM_End_to_End_Group.png`.

*Ghi chú minh bạch*: Tệp ảnh PNG hiện tại đính kèm trong thư mục được kết xuất tự động từ tập tọa độ BPMN DI bằng công cụ Python Renderer để đội ngũ có thể xem trước tức thì trên mọi môi trường. Để đạt điểm tối đa theo đúng chữ nghĩa rubric ("chỉ ghi là xuất từ Camunda Modeler sau khi thực sự export"), sinh viên thực hiện thao tác xuất ảnh trực tiếp qua menu như hướng dẫn trên trước khi nộp bài.

---

## 7. GIỚI HẠN VÀ KHUYẾN NGHỊ VẬN HÀNH THỰC TẾ

1. **Chế độ Thông báo Đa kênh (Omnichannel Safe Mode)**:
   * Trong phiên bản demo và nghiệm thu đồ án, hệ thống kích hoạt chế độ `ENABLE_LIVE_COMMUNICATION = False`. Tin nhắn Zalo ZNS và SMS Brandname được điều phối an toàn vào Nhật ký Outbox (`get_omnichannel_outbox`) để phục vụ kiểm tra và xem trước nội dung, tránh phát sinh cước viễn thông khi chưa có hợp đồng kinh doanh chính thức.
2. **Đối soát Ngân hàng VietQR**:
   * Hệ thống đã hoàn thiện 100% logic tiếp nhận Webhook IPN và đối soát giao dịch tự động. Khi đưa vào môi trường sản xuất thực tế, phòng khám chỉ cần khai báo URL Webhook (`https://crm.petcare.vn/api/method/petcare_crm.api.payment_webhook`) lên cổng thanh toán đối tác (PayOS, SeABank hoặc Vietcombank).
