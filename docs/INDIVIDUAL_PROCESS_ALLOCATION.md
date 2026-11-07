# BẢNG PHÂN CÔNG QUY TRÌNH NGHIỆP VỤ CÁ NHÂN (INDIVIDUAL PROCESS ALLOCATION)
## HỆ THỐNG PETCARE CRM - HỌC KỲ HIỆN HÀNH 2026

> **Dự án**: PetCare CRM (Hệ thống Quản lý Quan hệ Khách hàng Dịch vụ Thú cưng)  
> **Nền tảng**: Frappe Framework v15 (MariaDB 10.6, Python 3.10/3.14)  
> **Tiêu chuẩn mô hình hóa**: BPMN 2.0 (Camunda 7 Modeler XML + BPMNDiagram)  
> **Mã tài liệu**: `DOC-ALLOC-BPMN-INDIVIDUAL-2026`  
> **Trạng thái**: Đã phê duyệt cấu trúc bàn giao (Approved Baseline)

---

## 1. NGUYÊN TẮC PHÂN BỔ & ĐỐI CHIẾU TIÊU CHÍ (RUBRIC A4.3.2)

1. **Tính độc lập & Không trùng lặp**: Mỗi thành viên phụ trách một mảng quy trình độc lập, không chồng chéo về phạm vi API, DocType chịu trách nhiệm chính hoặc logic nghiệp vụ cốt lõi.
2. **Xác thực dựa trên mã nguồn thực tế**: Mọi ID quy trình (`FLOW-01`, `FLOW-02`, `FLOW-05`, `FLOW-07/08`), DocType (`PetCare Lead`, `PetCare Opportunity`, `Service Visit`, `Customer Membership`, `Care Recommendation`) và Endpoint `@frappe.whitelist()` đều có thật 100% trong `apps/petcare_crm/` và đã vượt qua bộ test 68/68 test cases.
3. **Độ sâu nghiệp vụ cá nhân (Sub-process Deep Dive)**: Quy trình cá nhân không phải là bản sao chép cắt nhỏ từ BPMN nhóm, mà mở rộng chi tiết các nhánh xử lý ngoại lệ, validation trường dữ liệu, kiểm tra tính toàn vẹn (ACID, Pessimistic Row Lock, idempotency) và tích hợp bên ngoài (VietQR, Zalo ZNS).
4. **Chuẩn định danh & Cấu trúc lưu trữ**: 
   - Thư mục: `deliverables/bpmn/individual/member_[1-4]/`
   - Tập tin sơ đồ BPMN: `deliverables/bpmn/individual/member_[X]/MSSV[X]_HoTen[X]_[TenQuyTrinh].bpmn`
   - Tập tin hình ảnh sơ đồ: `deliverables/bpmn/individual/member_[X]/MSSV[X]_HoTen[X]_[TenQuyTrinh].png`
   - Tập tin thuyết minh chi tiết: `deliverables/bpmn/individual/member_[X]/MSSV[X]_HoTen[X]_[TenQuyTrinh]_Explanation.docx` và `.md`

---

## 2. MA TRẬN PHÂN CÔNG TRÁCH NHIỆM 4 THÀNH VIÊN

> **Lưu ý bảo mật & khách quan**: Dự án sử dụng placeholder chuẩn `[MSSV] - [HỌ TÊN]` để sinh viên tự điền thông tin cá nhân trước khi nộp đồ án, tuyệt đối không tự bịa đặt thông tin sinh viên.

| STT | Thành viên (Placeholder) | Vai trò phân hệ | Mã quy trình | Tên quy trình nghiệp vụ chuyên sâu | DocType sở hữu chính | Whitelisted API độc quyền | Bộ Test kiểm chứng |
| :---: | :--- | :--- | :---: | :--- | :--- | :--- | :--- |
| **1** | `[MSSV1] - [HỌ TÊN 1]` | Phễu Tiếp nhận & Chuyển đổi Khách hàng | **FLOW-01** | Tiếp nhận Lead Đa kênh, Chuẩn hóa SĐT VN & Chuyển đổi Khách hàng - Thú cưng | `PetCare Lead`, `Contact`, `Pet` | `create_lead`<br>`update_lead_status`<br>`add_lead_interaction`<br>`convert_lead_to_customer`<br>`get_customer_360` | `test_lead_sales.py`<br>`test_e2e_lead_conversion.py` |
| **2** | `[MSSV2] - [HỌ TÊN 2]` | Quản lý Cơ hội Bán hàng & Phễu Doanh thu | **FLOW-02** | Quản lý Phễu Cơ hội Bán hàng (Opportunity Pipeline), Gating Giai đoạn & Chốt Won/Lost | `PetCare Opportunity`, `Contact`, `Pet`, `ToDo` | `create_opportunity`<br>`update_opportunity_stage`<br>`get_pipeline_summary`<br>`create_crm_todo`<br>`add_customer_interaction` | `test_lead_sales.py`<br>`test_sales_pipeline.py` |
| **3** | `[MSSV3] - [HỌ TÊN 3]` | Vận hành Dịch vụ, Thẻ & Quyết toán VietQR | **FLOW-05** | Mở Phiếu Dịch Vụ, Cấn trừ Quyền lợi Khóa Hàng (Pessimistic Lock) & Thanh toán VietQR IPN | `Service Visit`, `Customer Membership`, `PetCare Service`, `Benefit Redemption Ledger` | `record_pet_service_visit`<br>`record_benefit_usage`<br>`get_service_visit_payment_qr`<br>`payment_webhook`<br>`verify_customer_pet_access` | `test_membership.py`<br>`test_pricing_redemption.py`<br>`test_payment_qr.py` |
| **4** | `[MSSV4] - [HỌ TÊN 4]` | Động cơ Trí tuệ Giữ chân & Đa kênh Tự động | **FLOW-07/08** | Động cơ Phân tích Chu kỳ (EWMA + IQR), Quét At-Risk & Chăm sóc Tự động qua Zalo ZNS/SMS | `Care Recommendation`, `Service Visit`, `Pet`, `Contact` | `run_care_intelligence_scan`<br>`predict_next_service`<br>`get_care_status`<br>`update_recommendation_status`<br>`send_omnichannel_notification` | `test_care_engine.py`<br>`test_recommendation.py`<br>`test_omnichannel.py` |

---

## 3. CHI TIẾT PHẠM VI NGHIỆP VỤ VÀ RÀNH GIỚI TỪNG THÀNH VIÊN

### 3.1. THÀNH VIÊN 1: TIẾP NHẬN LEAD ĐA KÊNH & CHUYỂN ĐỔI (FLOW-01)
* **Người phụ trách**: `[MSSV1] - [HỌ TÊN 1]`
* **Tên tệp BPMN**: `deliverables/bpmn/individual/member_1/MSSV1_HoTen1_TiepNhanLead.bpmn`
* **Lanes tham gia**:
  1. `Khách Hàng Tiềm Năng` (External Participant)
  2. `Tư Vấn Viên / Telesales` (PetCare Sales Role)
  3. `Hệ Thống PetCare CRM` (Automated Engine / Service Layer)
* **Các điểm nghiệp vụ chuyên sâu riêng biệt**:
  - Tự động chuẩn hóa số điện thoại di động Việt Nam (`+84` -> `0`, kiểm tra đầu số nhà mạng 10 chữ số bằng regex `^(03|05|07|08|09)\d{8}$`).
  - Thuật toán kiểm tra trùng lặp (Deduplication Check): đối soát SĐT với bảng `Contact` và `PetCare Lead` hiện hữu để chặn spam hoặc nối lịch sử tương tác.
  - Phân luồng chuyển trạng thái nghiêm ngặt (`New` -> `Contacted` -> `Qualified` -> `Converted` hoặc `Unqualified` kèm bắt buộc lý do).
  - Giao dịch nguyên tử (Atomic Conversion Transaction): Tạo đồng thời `Contact` + `Pet` liên kết, đóng Lead thành `Converted`.

### 3.2. THÀNH VIÊN 2: QUẢN LÝ PHỄU CƠ HỘI BÁN HÀNG & CHỐT HỢP ĐỒNG (FLOW-02)
* **Người phụ trách**: `[MSSV2] - [HỌ TÊN 2]`
* **Tên tệp BPMN**: `deliverables/bpmn/individual/member_2/MSSV2_HoTen2_QuanLyOpportunity.bpmn`
* **Lanes tham gia**:
  1. `Khách Hàng` (Customer)
  2. `Nhân Viên Kinh Doanh` (PetCare Sales Role)
  3. `Hệ Thống PetCare CRM` (Pipeline Service / Frappe Desk Kanban)
* **Các điểm nghiệp vụ chuyên sâu riêng biệt**:
  - Mô hình hóa chu trình 5 giai đoạn: `Prospecting` (10%) -> `Qualification` (25%) -> `Proposal` (50%) -> `Negotiation` (75%) -> `Closed Won` (100%) / `Closed Lost` (0%).
  - Kiểm soát giá trị cơ hội: Bắt buộc `expected_amount > 0` và `expected_closing_date >= today()`.
  - Cổng kiểm soát (Stage Gating): Khi chuyển sang `Closed Lost`, bắt buộc nhập `lost_reason` và ghi nhận phân tích đối thủ cạnh tranh.
  - Tích hợp chốt deal (Won Hook): Kích hoạt tự động đề xuất đăng ký Thẻ Hội Viên hoặc đặt lịch dịch vụ trải nghiệm đầu tiên.

### 3.3. THÀNH VIÊN 3: VẬN HÀNH DỊCH VỤ, CẤN TRỪ ƯU ĐÃI & QUYẾT TOÁN VIETQR (FLOW-05)
* **Người phụ trách**: `[MSSV3] - [HỌ TÊN 3]`
* **Tên tệp BPMN**: `deliverables/bpmn/individual/member_3/MSSV3_HoTen3_DichVu_CanTru_VietQR.bpmn`
* **Lanes tham gia**:
  1. `Lễ Tân / Thu Ngân` (PetCare Receptionist Role)
  2. `Kỹ Thuật Viên Spa` (PetCare Specialist Role)
  3. `Hệ Thống PetCare CRM` (Pricing Engine & Benefit Service)
  4. `Cổng Thanh Toán VietQR / Ngân Hàng` (External Payment Gateway)
* **Các điểm nghiệp vụ chuyên sâu riêng biệt**:
  - Cơ chế Khóa hàng dòng dữ liệu chống xung đột ghi đồng thời (**Pessimistic Row Locking** - `FOR UPDATE`) khi cấn trừ số lượt ưu đãi trong `Customer Membership`.
  - Động cơ tính giá đa tầng (Multi-tier Pricing Engine): Ưu tiên lượt miễn phí (`FREE`) -> Chiết khấu phần trăm (`PERCENTAGE`) -> Thu đúng đơn giá gốc bảng dịch vụ.
  - Tạo động mã VietQR chuẩn EMVCo kèm mã hóa nội dung thanh toán `PETCARE_VISIT_{ID}`.
  - Xử lý Webhook IPN bất đồng bộ với xác thực chữ ký HMAC-SHA256 và khóa khử trùng (Idempotency Key) tránh ghi nhận doanh thu hai lần.

### 3.4. THÀNH VIÊN 4: ĐỘNG CƠ TRÍ TUỆ GIỮ CHÂN KHÁCH HÀNG & ZALO ZNS (FLOW-07/08)
* **Người phụ trách**: `[MSSV4] - [HỌ TÊN 4]`
* **Tên tệp BPMN**: `deliverables/bpmn/individual/member_4/MSSV4_HoTen4_CareIntelligence_ZaloZNS.bpmn`
* **Lanes tham gia**:
  1. `Frappe Scheduler Daemon` (Hệ thống chạy ngầm định kỳ)
  2. `Động Cơ CarePattern Engine` (Analytical Intelligence Core)
  3. `Chuyên Viên CSKH / Telesales` (PetCare Care Specialist Role)
  4. `Khách Hàng / Zalo ZNS Gateway` (Omnichannel Notification Channel)
* **Các điểm nghiệp vụ chuyên sâu riêng biệt**:
  - Giải thuật toán học nâng cao: Lọc dị thường thống kê bằng khoảng tứ phân vị (Tukey IQR Filter) + Tính trung bình dịch chuyển lũy thừa (EWMA $\alpha = 0.6$).
  - Phân loại trạng thái chu kỳ: `STABLE`, `DUE_SOON` ($\pm 3$ ngày), `AT_RISK` / `OVERDUE` ($\ge 1.5\times$ chu kỳ trung bình).
  - Cơ chế chặn trùng đề xuất (Anti-duplicate Gating): Không sinh `Care Recommendation` mới nếu đã có đề xuất mở trong vòng 7 ngày.
  - Tự động phát thông báo Zalo ZNS / SMS với cơ chế thử lại (Retry with Exponential Backoff) và bàn giao cho nhân viên thực hiện cuộc gọi tư vấn trực tiếp.

---

## 4. BẢNG KIỂM TRA TƯƠNG THÍCH CAMUNDA 7 & ĐẶC TẢ DI

Mỗi sơ đồ BPMN cá nhân được thiết kế tuân thủ nghiêm ngặt chuẩn **BPMN 2.0 XML** và tương thích hoàn toàn với **Camunda Modeler Desktop v5.45.0**:
- Định dạng XML chuẩn: Namespace `xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL"` và `xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI"`.
- Có đầy đủ tọa độ hiển thị (`dc:Bounds`) cho mọi node và tọa độ đường nối (`di:waypoint`) cho mọi sequence flow / message flow.
- Mở trực tiếp trên Camunda Modeler không bị lỗi thiếu sơ đồ (Missing Diagram) hay lỗi chồng lấn nhãn.

---

## 5. HƯỚNG DẪN XUẤT ẢNH PNG TỪ CAMUNDA MODELER DESKTOP

1. Khởi chạy Camunda Modeler tại đường dẫn: `C:\Program Files\Camunda\Camunda Modeler.exe`.
2. Mở tệp BPMN của từng thành viên: `File` -> `Open File...` -> Chọn tệp `.bpmn`.
3. Kiểm tra bố cục, căn chỉnh nhãn nếu cần.
4. Xuất ảnh chất lượng cao: Chọn `File` -> `Export As Image...` -> Chọn định dạng `PNG` -> Đặt tên trùng khớp `MSSV[X]_HoTen[X]_[TenQuyTrinh].png`.
5. Lưu tệp đè lên tệp ảnh đã được hệ thống kết xuất sơ bộ để đảm bảo chuẩn hiển thị chính thức của Camunda Modeler.
