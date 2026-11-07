# QA Acceptance Report — Day 12
**Date**: 2026-10-06  
**Environment**: Docker Compose (Frappe v15 + MariaDB 10.6 + Redis + FrappeCRM)  
**Tester**: Phi (Lead Dev), Nhi (Module 1), Thấm (Module 2), Bình (QA Lead)

---

## 1. Flow 1 — Membership & Anti-negative Balance
- [x] `record_benefit_usage` lần 1 → success, remaining = 0, used = 1
- [x] `record_benefit_usage` lần 2 → ValidationError ("Không đủ lượt 'Grooming'. Còn lại: 0 lượt, Yêu cầu: 1 lượt"), remaining giữ nguyên 0
- [x] Message lỗi rõ ràng, user-friendly
- [x] Invariant: remaining_quantity không bao giờ âm trong MariaDB

## 2. Flow 2 — Due Soon Pattern
- [x] `get_care_status` Mochi / Grooming → `status: "DUE_SOON"`
- [x] `days_until_due <= 5` (dự đoán đúng chu kỳ 28-30 ngày)
- [x] `Care Recommendation` tự động tạo sau `run_care_scan()` hoặc `daily_petcare_scan()`
- [x] Linked Membership và thông điệp quyền lợi ưu đãi còn lại được đính kèm vào nội dung đề xuất
- [x] Priority: Medium

## 3. Flow 3 — At Risk & INSUFFICIENT_DATA
- [x] `get_care_status` Luna / Grooming → `status: "AT_RISK"`, `absence_ratio >= 1.5` (~2.08)
- [x] `Care Recommendation` tạo cho Luna với `Priority: High` và gợi ý chiến dịch win-back
- [x] `get_care_status` Lucky / Grooming → `insufficient_data: true` (chỉ có 2 visits, MIN_VISITS=3)
- [x] `Care Recommendation` cho Lucky KHÔNG được tạo (bỏ qua bản ghi rác)

## 4. Overall Quality Summary
- **P1 (Blocker) Issues**: 0
- **P2 (Major) Issues**: 0
- **P3/P4 Minor Issues**: 0
- **Unit Tests**: 15/15 tests passing (100% pass rate)
- **Sign-off**: ACCEPTED for Release v1.0-demo
