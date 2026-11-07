# BIÊN BẢN NGHIỆM THU MILESTONE: MVP FREEZE (v0.7-mvp-freeze)
**Dự án**: PetCare CRM — Custom Frappe CRM App  
**Ngày nghiệm thu**: 2026-10-06  
**Chủ trì**: Phi (Lead Dev) | Phối hợp: Nhi (Module 1), Thấm (Module 2), Bình (QA/Điều phối)

---

## 1. MỤC TIÊU ĐÃ HOÀN THÀNH (WBS T22 – T26, T30)
1. **Tích hợp Module 1 (Membership) & Module 2 (Care Engine)**:
   - Module 2 đã gọi trực tiếp API & adapter của Module 1 thay cho dữ liệu giả định.
   - Hoàn thiện bridge layer `frappe_adapters.py` chuyển đổi Frappe DocType sang dataclass models.
2. **Xây dựng Recommendation Engine (`frappe_recommendation_engine.py`)**:
   - Tự động phát hiện pet sắp tới chu kỳ (`DUE_SOON`) hoặc vắng quá lâu (`AT_RISK`).
   - Tích hợp thông tin quyền lợi hội viên còn lại vào nội dung recommendation để cá nhân hóa thông điệp CSKH.
   - Cơ chế Deduplication Window (14 ngày) ngăn ngừa trùng lặp khuyến nghị.
3. **Public Whitelisted REST API**:
   - `petcare_crm.api.get_active_membership`
   - `petcare_crm.api.get_remaining_benefit`
   - `petcare_crm.api.record_benefit_usage` (atomic check, chống âm lượt)
   - `petcare_crm.api.get_care_status`
   - `petcare_crm.api.predict_next_service`
   - `petcare_crm.api.check_membership_renewal`
   - `petcare_crm.api.run_care_scan` (trigger quét toàn hệ thống)

---

## 2. KẾT QUẢ KIỂM THỬ 3 DEMO FLOWS (100% PASS)

| Flow | Kịch bản kiểm thử | Kỳ vọng | Kết quả | Trạng thái |
|---|---|---|---|:---:|
| **Flow 1** | Trừ lượt gói Membership & Chống âm lượt | Trừ lượt 1 thành công (remaining=0). Trừ lần 2 throw exception `Không đủ lượt`, remaining giữ nguyên 0. | Thao tác atomic chính xác, không thể xảy ra số dư âm | **PASS** |
| **Flow 2** | Chu kỳ chăm sóc Due Soon & Cá nhân hóa | Phát hiện `days_until_due <= 5` -> Sinh `Care Recommendation` DUE_SOON, Priority Medium, đính kèm membership + số lượt ưu đãi còn lại | Bản ghi `REC-xxxx` sinh tự động với đầy đủ nội dung cá nhân hóa | **PASS** |
| **Flow 3a**| Phát hiện rủi ro rời bỏ At Risk | Phát hiện `absence_ratio >= 1.5` -> Sinh `Care Recommendation` AT_RISK, Priority High | Sinh bản ghi AT_RISK High priority kèm thông điệp win-back | **PASS** |
| **Flow 3b**| Xử lý thiếu dữ liệu Insufficient Data | Pet có < 3 lượt khám -> `insufficient_data: True` | Bỏ qua không sinh recommendation rác | **PASS** |
| **Dedup**  | Cơ chế chống trùng lặp khuyến nghị | Chạy quét lại trong vòng 14 ngày | Không sinh bản ghi trùng lặp (`created = 0`) | **PASS** |

---

## 3. THÔNG TIN PHÁT HÀNH
- **Branch**: `develop`
- **Git Tag**: `v0.7-mvp-freeze`
- **Môi trường**: Docker Compose (Frappe v15 + MariaDB 10.6 + Redis + FrappeCRM)
- **Database Status**: Đã migrate 7 DocTypes và đồng bộ schema.

---
*Biên bản được xác nhận bởi Ban dự án PetCare CRM.*
