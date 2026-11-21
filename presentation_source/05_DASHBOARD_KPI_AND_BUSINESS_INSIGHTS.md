# PETCARE CRM — BÁO CÁO CHỈ SỐ KPI & PHÂN TÍCH QUẢN TRỊ (DASHBOARD, KPIS & BUSINESS INSIGHTS)

> **Mã hồ sơ**: `INSIGHTS-KPI-2026`  
> **Dự án**: PetCare CRM (Hệ thống CRM Dịch vụ Chăm sóc Thú cưng)  
> **Phân hệ thực thi**: [`petcare_crm/utils/analytics_service.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/utils/analytics_service.py) & Script Report [`petcare_kpi_overview`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/petcare_crm/report/petcare_kpi_overview/)  
> **Tài chính tham chiếu**: [`CLV_ABC_Model.xlsx`](file:///c:/Users/pc/Documents/Doan_CRM/deliverables/finance/CLV_ABC_Model.xlsx)  
> **Ngày lập hồ sơ**: 07/11/2026  

---

## 1. NGUYÊN TẮC QUẢN TRỊ DỮ LIỆU & TRUNG THỰC HỌC THUẬT

> [!IMPORTANT]
> **PHÂN ĐỊNH RẠCH RÒI GIỮA NGUỒN DỮ LIỆU THỰC THI VÀ MÔ HÌNH MÔ PHỎNG**  
> 1. **Dữ liệu Hệ thống (System Demo Data)**: Các chỉ số KPI số 1 đến số 8 được tính toán trực tiếp từ các bản ghi mẫu thuần Việt trong CSDL Frappe (`Contact`, `Pet`, `Service Visit`, `Customer Membership`, `Care Recommendation`).
> 2. **Kịch bản Mô phỏng Tài chính (Financial Simulation Scenarios)**: Các thông số như *Tỷ lệ Churn giảm từ 35% về 12%, Tần suất ghé tăng từ 6 lên 11 lần/năm, và Tăng trưởng CLV +38%* thuộc về mô hình tài chính chuyên đề A4.5 (`CLV_ABC_Model.xlsx`), được thiết kế để chứng minh phương pháp luận tài chính của sinh viên, không phải số liệu sổ sách kế toán của một doanh nghiệp có thật.

---

## 2. MA TRẬN 8 CHỈ SỐ KPI QUẢN TRỊ CHUẨN (CORE 8 KPIS)

| STT | Tên Chỉ Số (KPI) | Phân Hệ Nghiệp Vụ | Công Thức Tính Toán Thực Tế (Source Code) | Bộ Lọc Khả Dụng | Ý Nghĩa Kinh Doanh & Quyết Định Quản Trị Hỗ Trợ | Nguồn Dữ Liệu |
|:---:|---|---|---|---|---|:---:|
| **KPI-1** | **Tỷ Lệ Chuyển Đổi Lead** *(Lead Conversion Rate)* | CRM Core | $$\text{CR}_{\text{Lead}} = \frac{\text{Converted Leads}}{\text{Total Leads}} \times 100\%$$ | Khoảng ngày (`from_date`, `to_date`), Nguồn Lead (`lead_source`) | **Đo lường hiệu quả kênh tiếp thị**: Nhận diện kênh mang lại khách hàng chất lượng cao (Facebook Ads, Hotline, Walk-in); quyết định cắt giảm ngân sách các kênh kém chuyển đổi. | Demo Data (`PetCare Lead`) |
| **KPI-2** | **Doanh Thu Cơ Hội Dự Kiến Có Trọng Số** *(Weighted Pipeline Value)* | Bán Hàng & Deals | $$\text{Weighted Value} = \sum (\text{Expected Amount} \times \frac{\text{Probability}}{100})$$ | Giai đoạn (`stage`), Nhân viên Sales, Chi nhánh | **Dự báo dòng tiền tương lai**: Giúp ban lãnh đạo dự phóng doanh thu bán các gói thẻ hội viên VIP trong tháng tới để lên kế hoạch nhập khẩu vật tư và vắc-xin. | Demo Data (`PetCare Opportunity`) |
| **KPI-3** | **Số Thẻ Hội Viên Active & Tổng Số Dư Ví** *(Active Cards & Balance)* | Membership & Loyalty | $$\text{Active Count} = \text{Count}(\text{status} = \text{'Active'})$$<br>$$\text{Total Balance} = \sum \text{balance}$$ | Loại gói (`membership_plan`), Chi nhánh phát hành | **Kiểm soát nguồn vốn lưu động trả trước**: Khách hàng nạp tiền trước mang lại dòng tiền mặt nhàn rỗi (Float) giúp cơ sở nâng cấp trang thiết bị mà không cần vay vốn. | Demo Data (`Customer Membership`) |
| **KPI-4** | **Hội Viên Sắp Hết Hạn Trong 7 Ngày & 30 Ngày** *(Expiring Memberships)* | Membership & Loyalty | $$\text{Days Left} = \text{end\_date} - \text{today}$$<br>Lọc: $0 \le \text{Days Left} \le 7$ và $\le 30$ | Loại gói, Khách hàng, Thú cưng | **Chống mất hội viên trung thành**: Tự động kích hoạt nhiệm vụ cho nhân viên liên hệ tư vấn gia hạn kèm chính sách Rollover bảo lưu quyền lợi tồn. | Demo Data (`Customer Membership`) |
| **KPI-5** | **Doanh Thu Dịch Vụ Thực Nhận & Tổng Ưu Đãi** *(Net Revenue & Discounts)* | Vận Hành Dịch Vụ | $$\text{Net Rev} = \sum \text{final\_price}$$<br>$$\text{Discounts} = \sum \text{discount\_amount}$$<br>$$\text{Gross Rev} = \sum \text{original\_price}$$ | Khoảng ngày, Chi nhánh (`branch`), Loại dịch vụ | **Đo lường mức độ thâm hụt biên lợi nhuận do khuyến mãi**: Đánh giá xem việc giảm giá cho hội viên có thúc đẩy tăng lượt khách hay đang làm xói mòn lợi nhuận gộp. | Demo Data (`Service Visit`) |
| **KPI-6** | **Thú Cưng Sắp Đến Chu Kỳ Chăm Sóc** *(Due Soon Volume)* | Care Retention | $$\text{Predicted Date} - \text{today} \le 3 \text{ ngày}$$ | Loại dịch vụ (Tắm, Spa, Khám, Tiêm), Chi nhánh | **Tối ưu hóa công suất bàn Spa**: Giúp lễ tân chủ động lấp đầy các khung giờ vắng khách trong tuần bằng cách gọi điện nhắc lịch trước cho chủ nuôi. | Demo Data (`Care Recommendation`) |
| **KPI-7** | **Khách Hàng Có Nguy Cơ Rời Bỏ** *(At-Risk Customers)* | Care Retention | $$D_{\text{last visit}} \ge 1.5 \times C_{\text{ewma}}$$ | Mức độ ưu tiên (`Urgent`/`High`), Chi nhánh | **Kích hoạt chiến dịch Win-Back**: Phát hiện sớm thú cưng đã quá $1.5\times$ chu kỳ bình thường chưa quay lại để gửi voucher giảm giá hoặc gọi thăm hỏi sức khỏe bé. | Demo Data (`Care Recommendation`) |
| **KPI-8** | **Tỷ Lệ Giữ Chân Khách Hàng Thực Tế** *(Customer Retention Rate)* | Care Retention | $$\text{Retention Rate} = \frac{\text{Khách ghé } \ge 2 \text{ lần}}{\text{Tổng khách đã ghé}} \times 100\%$$ | Khoảng thời gian khảo sát, Chi nhánh | **Thước đo sức khỏe bền vững của phòng khám**: Tỷ lệ khách quay lại càng cao thì chi phí tiếp thị (CAC) càng giảm và giá trị vòng đời (CLV) càng tăng. | Demo Data (`Service Visit`) |

---

## 3. PHÂN TÍCH ĐỐI SÁNH HIỆU QUẢ ĐA CHI NHÁNH (MULTI-BRANCH BENCHMARKING)

Hệ thống cung cấp module phân tích phân mảnh số liệu giữa 4 chi nhánh trong chuỗi (được hiện thực tại hàm `get_branch_comparison_metrics` trong [`analytics_service.py`](file:///c:/Users/pc/Documents/Doan_CRM/apps/petcare_crm/petcare_crm/utils/analytics_service.py)):

```
┌─────────────────┬────────────────────┬────────────────────┬────────────────────┬────────────────────┐
│ Chỉ Số So Sánh  │ CN-TRUNGTAM (Q.1)  │ CN-QUAN1 (Bến Nghé)│ CN-THUDUC (Thảo Đ.)│ CN-BINHTHANH (XVNT)│
├─────────────────┼────────────────────┼────────────────────┼────────────────────┼────────────────────┤
│ Số lượt phục vụ │ 6 lượt (50.0%)     │ 3 lượt (25.0%)     │ 2 lượt (16.7%)     │ 1 lượt (8.3%)      │
│ Doanh số niêm yết│ 2.450.000 VNĐ      │ 1.150.000 VNĐ      │ 900.000 VNĐ        │ 450.000 VNĐ        │
│ Doanh thu thực thu│ 1.750.000 VNĐ     │ 800.000 VNĐ        │ 900.000 VNĐ        │ 450.000 VNĐ        │
│ Ưu đãi cấn trừ  │ 700.000 VNĐ (28.6%)│ 350.000 VNĐ (30.4%)│ 0 VNĐ (0.0%)       │ 0 VNĐ (0.0%)       │
│ Thẻ hội viên    │ 2 Thẻ Active       │ 1 Thẻ Expiring     │ 1 Thẻ Mới          │ 0 Thẻ              │
└─────────────────┴────────────────────┴────────────────────┴────────────────────┴────────────────────┘
```

### Hàm ý quản trị từ số liệu đa chi nhánh:
1. **Cơ sở Trung Tâm và Quận 1 có tỷ lệ hội viên rất cao (28% – 30% doanh số được cấn trừ)**: Chứng minh khách hàng trung tâm có xu hướng gắn bó lâu dài và ưa chuộng các gói trả trước.
2. **Cơ sở Thủ Đức và Bình Thạnh chủ yếu là khách vãng lai thanh toán 100% tiền mặt/VietQR**: Cần tăng cường sự hiện diện của nhân viên tư vấn (`PetCare Sales`) tại đây để chuyển đổi khách vãng lai thành hội viên có thẻ.

---

## 4. TỔNG HỢP MÔ HÌNH GIÁ THÀNH HOẠT ĐỘNG (ABC) & GIÁ TRỊ VÒNG ĐỜI (CLV)

Chuyên đề A4.5 kết nối trực tiếp dữ liệu schema CRM với mô hình tài chính quản trị chuyên sâu trong tệp [`deliverables/finance/CLV_ABC_Model.xlsx`](file:///c:/Users/pc/Documents/Doan_CRM/deliverables/finance/CLV_ABC_Model.xlsx).

### 4.1. Bóc tách 4 Trung tâm Chi phí Hoạt động (Activity-Based Costing - ABC)

Thay vì phân bổ cào bằng, chi phí vận hành phòng khám được tập hợp vào 4 Cost Pools:

```
[ TỔNG CHI PHÍ HOẠT ĐỘNG PHÒNG KHÁM PETCARE ]
│
├── 1. Pool Nhân Công Chuyên Môn (Direct Labor): Bác sĩ, Kỹ thuật viên Spa
│    └── Tác nhân tạo chi phí (Driver): Số giờ thao tác trực tiếp (Direct Labor Hours - DLH)
│
├── 2. Pool Vật Tư Tiêu Hao (Medical & Grooming Supplies): Thuốc, dầu tắm, vắc-xin, gạc
│    └── Tác nhân tạo chi phí (Driver): Suất tiêu hao vật tư chuẩn trên từng ca dịch vụ
│
├── 3. Pool Khấu Hao Trang Thiết Bị (Equipment Depreciation): Máy siêu âm, bồn tắm sục, lồng sấy
│    └── Tác nhân tạo chi phí (Driver): Số giờ vận hành máy móc kỹ thuật (Machine Hours - MH)
│
└── 4. Pool Chi Phí Quản Lý Chung (Facility & Administrative Overhead): Thuê mặt bằng, điện nước, phần mềm
     └── Tác nhân tạo chi phí (Driver): Diện tích phân bổ và số lượt tiếp đón tại quầy
```

#### Kết quả phân bổ giá thành và Tỷ suất Lợi nhuận biên ($CM\%$):
* **Dịch vụ Tiêm phòng vắc-xin (`SVC-VACCINE-5IN1`)**: Giá niêm yết 350.000 VNĐ. Giá thành ABC: 175.000 VNĐ. $\rightarrow$ **$CM\% = 50.0\%$** (Biên lợi nhuận cao, thời gian thực hiện nhanh).
* **Dịch vụ Grooming cắt tỉa tạo kiểu (`SVC-GROOM-BASIC`)**: Giá niêm yết 350.000 VNĐ. Giá thành ABC: 245.000 VNĐ (thâm dụng nhân công tay nghề cao). $\rightarrow$ **$CM\% = 30.0\%$**.
* **Dịch vụ Spa thảo dược cao cấp (`SVC-SPA-DELUXE`)**: Giá niêm yết 450.000 VNĐ. Giá thành ABC: 270.000 VNĐ. $\rightarrow$ **$CM\% = 40.0\%$**.

### 4.2. Mô hình Định giá trị Vòng đời Khách hàng (CLV) theo cấp độ Hộ gia đình

Công thức tính toán CLV áp dụng phương pháp **Chiết khấu dòng tiền đóng góp biên (Discounted Cash Flow)**:

$$\text{CLV} = \sum_{t=1}^{T} \frac{\left( \sum_{i=1}^{N_{\text{pets}}} \text{AOV}_i \times f_i \times \text{CM}\% - \text{Retention Cost} \right) \times (1 - \text{Churn Rate})^{t-1}}{(1 + r)^t} - \text{CAC}$$

Trong đó:
* $N_{\text{pets}}$: Số lượng thú cưng của hộ gia đình ($1:N$).
* $\text{AOV}_i$: Giá trị chi tiêu trung bình trên mỗi lượt dịch vụ (khoảng 350.000 – 450.000 VNĐ).
* $f_i$: Tần suất ghé thăm trong năm (thay đổi theo đòn bẩy Care Intelligence).
* $\text{CM}\%$: Tỷ suất lợi nhuận đóng góp biên sau khi trừ chi phí ABC ($35\% – 40\%$).
* $r$: Tỷ lệ chiết khấu dòng tiền (WACC giả định $10\%$/năm).
* $\text{CAC}$: Chi phí tiếp thị thu hút khách hàng ban đầu (khoảng 250.000 VNĐ).

#### So sánh 3 kịch bản kinh doanh mô phỏng (Simulation Benchmarks):
1. **Kịch bản Cơ sở (Chưa có CRM)**: Khách hàng thường xuyên bị quên lịch; tần suất $f = 6$ lần/năm; tỷ lệ rời bỏ $\text{Churn} = 35\%$/năm. $\rightarrow$ **$\text{CLV} \approx 4.820.000 \text{ VNĐ}$**.
2. **Kịch bản Có PetCare CRM (Chăm sóc chu kỳ sinh học & Nhắc Zalo ZNS)**: Tần suất tăng lên $f = 9$ lần/năm; tỷ lệ rời bỏ giảm xuống $\text{Churn} = 18\%$/năm. $\rightarrow$ **$\text{CLV} \approx 7.650.000 \text{ VNĐ}$** (*Tăng trưởng $+58.7\%$*).
3. **Kịch bản Nâng cao (Khách hàng sở hữu Thẻ VIP Đa Thú Cưng)**: Tần suất đạt $f = 12$ lần/năm; tỷ lệ rời bỏ giảm còn $\text{Churn} = 12\%$/năm. $\rightarrow$ **$\text{CLV} \approx 11.200.000 \text{ VNĐ}$** (*Tăng trưởng $+132\%$*).

---

## 5. HÀNH ĐỘNG QUẢN TRỊ GỢI Ý DÀNH CHO BAN GIÁM ĐỐC (ACTIONABLE RECOMMENDATIONS)

1. **Ưu tiên bán Gói Hội Viên Trả Trước cho các hộ nuôi từ 2 thú cưng trở lên**: Khách hàng nuôi nhiều bé có chi phí chăm sóc định kỳ rất cao; gói hội viên giúp họ tiết kiệm chi phí dịch vụ lẻ, đồng thời giữ chân họ gắn kết trọn đời với phòng khám.
2. **Chuyển dịch ngân sách từ Quảng cáo Facebook sang Chăm sóc Tái khám Zalo ZNS**: Chi phí giữ chân khách hàng cũ (Retention Cost $\approx 5.000$ VNĐ/tin ZNS) chỉ bằng **$1/50$** chi phí tìm khách hàng mới qua quảng cáo (CAC $\approx 250.000$ VNĐ).
3. **Thiết lập cơ chế phân quyền duyệt giá chặt chẽ**: Doanh thu cấn trừ quyền lợi hội viên chiếm tới 30% doanh số tại các cơ sở trung tâm, do đó mọi hành vi điều chỉnh giá hoặc cấp thẻ miễn phí bắt buộc phải thông qua tài khoản của `PetCare Manager`.
