"""
Mock Test Suite for Suite 8: Advanced Extensions & Resolved Limitations.
Verifies all capabilities implemented to resolve KNOWN_LIMITATIONS.md:
1. Care Intelligence: Seasonal shedding adjustment factor (Spring/Summer/Autumn).
2. Care Intelligence: Pet developmental age factor (Puppy/Kitten vs Adult vs Senior).
3. Care Intelligence: End-to-end adjusted visit prediction with explainable reason.
4. Payment: Dynamic VietQR URL & payload generation for Service Visits & Membership Top-Up.
5. Payment: Bank transfer webhook auto-reconciliation for Service Visits.
6. Payment: Webhook idempotency protection against duplicate replay.
7. Payment: Webhook handling for unmatched transfer syntax.
8. Omnichannel: Safe Mode dispatching & preview for Zalo ZNS and SMS Brandname.
9. Multi-Branch: Comparative revenue and visit volume partitioning across clinic branches.
10. Owner Portal: Self-service appointment booking & pet health book API contracts.
"""

import unittest
import sys
import os
from datetime import date, timedelta
from unittest.mock import MagicMock

# Ensure apps/petcare_crm is on sys.path
sys.path.insert(0, os.path.abspath("apps/petcare_crm"))

# Mock frappe if not installed
if "frappe" not in sys.modules:
    mock_frappe = MagicMock()
    mock_frappe._ = lambda x: x
    mock_frappe.throw = lambda msg, *args, **kwargs: (_ for _ in ()).throw(Exception(msg))
    mock_frappe.logger = lambda name: MagicMock()
    sys.modules["frappe"] = mock_frappe
    sys.modules["frappe.model"] = MagicMock()
    sys.modules["frappe.model.document"] = MagicMock()

from petcare_crm.utils.models import ServiceVisit
from petcare_crm.utils.care_pattern_service import (
    SeasonalAdjustmentHelper,
    PetAgeAdjustmentHelper,
    VisitPredictionService,
    CarePatternService,
)
from petcare_crm.utils.payment_gateway import (
    VietQRGenerator,
    PaymentWebhookService,
    VietQRConfig,
)
from petcare_crm.utils.omnichannel_service import (
    OmnichannelDispatcher,
    CHANNEL_ZALO_ZNS,
    CHANNEL_SMS_BRANDNAME,
    CHANNEL_EMAIL,
    TEMPLATE_DUE_SOON_REMINDER,
    TEMPLATE_PAYMENT_CONFIRMATION,
)
from petcare_crm.utils.analytics_service import AnalyticsService


class TestExtendedCapabilities(unittest.TestCase):
    """Test suite covering the 10 extended capabilities resolving known limitations."""

    def setUp(self):
        # Clear state
        PaymentWebhookService._processed_transaction_ids.clear()
        OmnichannelDispatcher.clear_outbox()

    # ─────────────────────────────────────────────────────────────────
    # 1. CARE INTELLIGENCE: SEASONAL ADJUSTMENT
    # ─────────────────────────────────────────────────────────────────
    def test_01_seasonal_adjustment_factors(self):
        """Kiểm tra hệ số mùa vụ theo chu kỳ rụng lông và khí hậu ẩm ướt."""
        # Spring shedding season (March, April) -> factor 0.85
        factor_mar = SeasonalAdjustmentHelper.get_seasonal_factor(3, "Grooming")
        factor_apr = SeasonalAdjustmentHelper.get_seasonal_factor(4, "Spa & Cắt tỉa")
        self.assertEqual(factor_mar, 0.85)
        self.assertEqual(factor_apr, 0.85)

        # Summer monsoon / humidity season (June, July) -> factor 0.80
        factor_jun = SeasonalAdjustmentHelper.get_seasonal_factor(6, "Tắm trị liệu")
        self.assertEqual(factor_jun, 0.80)

        # Autumn pre-winter molting (September, October) -> factor 0.88
        factor_oct = SeasonalAdjustmentHelper.get_seasonal_factor(10, "Grooming")
        self.assertEqual(factor_oct, 0.88)

        # Non-grooming service (e.g., General Checkup, Vaccination) -> factor 1.0 (no seasonal haircut effect)
        factor_vax = SeasonalAdjustmentHelper.get_seasonal_factor(3, "Vaccination")
        self.assertEqual(factor_vax, 1.0)

    # ─────────────────────────────────────────────────────────────────
    # 2. CARE INTELLIGENCE: PET AGE ADJUSTMENT
    # ─────────────────────────────────────────────────────────────────
    def test_02_pet_age_adjustment_factors(self):
        """Kiểm tra hệ số chu kỳ theo giai đoạn phát triển của thú cưng."""
        # Puppy / Kitten under 12 months -> factor 0.85 (faster hair growth & socialization)
        puppy_factor = PetAgeAdjustmentHelper.get_age_factor(5, "Grooming")
        self.assertEqual(puppy_factor, 0.85)

        # Adult pet (24 months) -> factor 1.0 (standard adult maintenance)
        adult_factor = PetAgeAdjustmentHelper.get_age_factor(24, "Grooming")
        self.assertEqual(adult_factor, 1.0)

        # Senior pet over 84 months (7+ years) -> factor 0.80 (requires frequent gentle care)
        senior_factor = PetAgeAdjustmentHelper.get_age_factor(96, "Grooming")
        self.assertEqual(senior_factor, 0.80)

        # Age calculation from birth date
        ref_date = date(2026, 10, 1)
        birth_date = date(2026, 4, 1)  # 6 months old
        calc_months = PetAgeAdjustmentHelper.calculate_age_months(birth_date, ref_date)
        self.assertIn(calc_months, (5, 6))

    # ─────────────────────────────────────────────────────────────────
    # 3. CARE INTELLIGENCE: PREDICTION WITH SEASON & AGE ADJUSTMENT
    # ─────────────────────────────────────────────────────────────────
    def test_03_prediction_with_seasonal_and_age_adjustment(self):
        """Dự đoán chu kỳ có tính đến yếu tố mùa vụ và độ tuổi."""
        # Setup visits every 30 days
        base = date(2026, 1, 1)
        visits = [
            ServiceVisit(pet="Lucky", customer="CT-001", service_type="Grooming", visit_date=base),
            ServiceVisit(pet="Lucky", customer="CT-001", service_type="Grooming", visit_date=base + timedelta(days=30)),
            ServiceVisit(pet="Lucky", customer="CT-001", service_type="Grooming", visit_date=base + timedelta(days=60)),
            ServiceVisit(pet="Lucky", customer="CT-001", service_type="Grooming", visit_date=base + timedelta(days=90)), # ~April 1
        ]

        # 3a. Baseline without adjustment: typical interval = 30 days
        base_pred = VisitPredictionService.predict_next_visit(
            pet="Lucky", service_type="Grooming", visits=visits, current_date=base + timedelta(days=90)
        )
        self.assertAlmostEqual(base_pred.average_interval, 30.0, places=1)
        self.assertEqual(base_pred.predicted_next_visit, base + timedelta(days=120))
        self.assertEqual(base_pred.seasonal_factor, 1.0)

        # 3b. With Spring shedding seasonal adjustment (ref_date in April -> factor 0.85)
        # Expected interval: 30 * 0.85 = 25.5 -> 26 days
        season_pred = VisitPredictionService.predict_next_visit(
            pet="Lucky",
            service_type="Grooming",
            visits=visits,
            current_date=date(2026, 4, 2),
            enable_seasonal_adjustment=True,
        )
        self.assertEqual(season_pred.seasonal_factor, 0.85)
        self.assertAlmostEqual(season_pred.adjusted_interval, 25.5, places=1)
        self.assertEqual(season_pred.predicted_next_visit, base + timedelta(days=90 + 26))
        self.assertIn("hệ số mùa vụ=0.85", season_pred.reason)

        # 3c. Combined seasonal (0.85) + puppy (< 12 months, 0.85) -> combined 0.7225
        # 30 * 0.7225 = 21.68 -> 22 days forward
        combined_pred = VisitPredictionService.predict_next_visit(
            pet="Lucky",
            service_type="Grooming",
            visits=visits,
            current_date=date(2026, 4, 2),
            pet_age_months=6,
            enable_seasonal_adjustment=True,
            enable_age_adjustment=True,
        )
        self.assertEqual(combined_pred.seasonal_factor, 0.85)
        self.assertEqual(combined_pred.age_factor, 0.85)
        self.assertAlmostEqual(combined_pred.adjusted_interval, 21.68, places=1)
        self.assertEqual(combined_pred.predicted_next_visit, base + timedelta(days=90 + 22))

    # ─────────────────────────────────────────────────────────────────
    # 4. VIETQR GENERATION FOR SERVICE VISIT & MEMBERSHIP
    # ─────────────────────────────────────────────────────────────────
    def test_04_dynamic_vietqr_url_and_payload(self):
        """Tạo dynamic VietQR theo chuẩn Napas247 cho Service Visit và Thẻ hội viên."""
        # 4a. Service Visit QR
        visit_qr = VietQRGenerator.generate_service_visit_qr(
            visit_id="SV-2026-00042",
            amount=350000.0,
            customer_name="Nguyễn Văn A",
        )
        self.assertEqual(visit_qr["status"], "success")
        self.assertEqual(visit_qr["transfer_content"], "PC-SVC-SV-2026-00042")
        self.assertEqual(visit_qr["amount"], 350000.0)
        self.assertIn("img.vietqr.io/image/970436", visit_qr["qr_image_url"])
        self.assertIn("PC-SVC-SV-2026-00042", visit_qr["qr_image_url"])

        # 4b. Membership Wallet Top-Up QR
        mem_qr = VietQRGenerator.generate_membership_topup_qr(
            membership_id="MB-2026-00008",
            amount=1000000.0,
            transaction_id="TXN99",
        )
        self.assertEqual(mem_qr["status"], "success")
        self.assertEqual(mem_qr["transfer_content"], "PC-MEM-MB-2026-00008-TXN99")
        self.assertEqual(mem_qr["amount"], 1000000.0)
        self.assertIn("PC-MEM-MB-2026-00008-TXN99", mem_qr["qr_image_url"])

    # ─────────────────────────────────────────────────────────────────
    # 5. PAYMENT WEBHOOK AUTO-RECONCILIATION
    # ─────────────────────────────────────────────────────────────────
    def test_05_payment_webhook_service_visit_reconciliation(self):
        """Xử lý webhook tự động đối soát thanh toán Service Visit."""
        res = PaymentWebhookService.process_webhook_notification(
            gateway_transaction_id="VCB_TXN_998811",
            amount=350000.0,
            content="MB BANK CHUYEN TIEN PHIEU PC-SVC-SV-2026-00042 PETCARE",
            gateway="VIETCOMBANK",
        )
        self.assertEqual(res["status"], "success")
        self.assertEqual(res["payment_type"], "SERVICE_VISIT")
        self.assertEqual(res["visit_id"], "SV-2026-00042")
        self.assertEqual(res["amount_paid"], 350000.0)

    # ─────────────────────────────────────────────────────────────────
    # 6. PAYMENT WEBHOOK IDEMPOTENCY GUARD
    # ─────────────────────────────────────────────────────────────────
    def test_06_payment_webhook_idempotency_protection(self):
        """Kiểm tra cơ chế Idempotency: webhook retry không đối soát 2 lần."""
        tx_id = "VCB_IDEMPOTENT_777"
        first_call = PaymentWebhookService.process_webhook_notification(
            gateway_transaction_id=tx_id,
            amount=200000.0,
            content="PC-SVC-SV-2026-00099",
        )
        self.assertEqual(first_call["status"], "success")

        # Second call with identical gateway_transaction_id
        second_call = PaymentWebhookService.process_webhook_notification(
            gateway_transaction_id=tx_id,
            amount=200000.0,
            content="PC-SVC-SV-2026-00099",
        )
        self.assertEqual(second_call["status"], "idempotent_skip")
        self.assertIn("trước đó", second_call["message"])

    # ─────────────────────────────────────────────────────────────────
    # 7. PAYMENT WEBHOOK UNMATCHED TRANSFER SYNTAX
    # ─────────────────────────────────────────────────────────────────
    def test_07_payment_webhook_unmatched_syntax(self):
        """Xử lý nội dung chuyển khoản tự do không khớp mã định danh."""
        res = PaymentWebhookService.process_webhook_notification(
            gateway_transaction_id="VCB_RANDOM_123",
            amount=150000.0,
            content="TIEN AN TOI NGUYEN VAN A CHUYEN TIEN",
        )
        self.assertEqual(res["status"], "unmatched")
        self.assertIn("không khớp cú pháp", res["message"])

    # ─────────────────────────────────────────────────────────────────
    # 8. OMNICHANNEL DISPATCHER & SAFE MODE PREVIEW
    # ─────────────────────────────────────────────────────────────────
    def test_08_omnichannel_dispatcher_safe_mode(self):
        """Kiểm tra điều phối tin nhắn đa kênh (Zalo ZNS, SMS) trong Safe Mode."""
        # 8a. Dispatch Zalo ZNS
        zns_res = OmnichannelDispatcher.dispatch(
            channel=CHANNEL_ZALO_ZNS,
            recipient="0912345678",
            template_id=TEMPLATE_DUE_SOON_REMINDER,
            template_data={
                "customer_name": "Anh Hoàng",
                "pet_name": "Milu",
                "service_type": "Tắm sấy & Cắt tỉa",
                "appointment_date": "2026-11-05",
                "hotline": "028.3888.9999",
            },
        )
        self.assertEqual(zns_res["status"], "success")
        self.assertTrue(zns_res["is_safe_mode"])
        self.assertIn("Milu sắp đến chu kỳ chăm sóc", zns_res["preview_text"])

        # 8b. Dispatch SMS Brandname
        sms_res = OmnichannelDispatcher.dispatch(
            channel=CHANNEL_SMS_BRANDNAME,
            recipient="0988776655",
            template_id=TEMPLATE_PAYMENT_CONFIRMATION,
            template_data={
                "amount": "500,000",
                "reference_id": "SV-2026-00100",
                "pet_name": "Kiki",
            },
        )
        self.assertEqual(sms_res["status"], "success")

        # 8c. Inspect Outbox
        outbox = OmnichannelDispatcher.get_outbox()
        self.assertEqual(len(outbox), 2)
        self.assertEqual(outbox[0]["channel"], "ZALO_ZNS")
        self.assertEqual(outbox[1]["channel"], "SMS_BRANDNAME")

    # ─────────────────────────────────────────────────────────────────
    # 9. MULTI-BRANCH KPI COMPARISON
    # ─────────────────────────────────────────────────────────────────
    def test_09_multi_branch_kpi_comparison(self):
        """Phân tích so sánh doanh thu và lượt khám giữa các chi nhánh phòng khám."""
        visits_store = [
            {"branch": "CN-TRUNGTAM", "original_price": 500000, "discount_amount": 0, "final_price": 500000},
            {"branch": "CN-TRUNGTAM", "original_price": 300000, "discount_amount": 50000, "final_price": 250000},
            {"branch": "CN-QUAN1", "original_price": 400000, "discount_amount": 0, "final_price": 400000},
            {"branch": "CN-THUDUC", "original_price": 200000, "discount_amount": 20000, "final_price": 180000},
        ]
        comparison = AnalyticsService.get_branch_comparison_metrics(visits_store=visits_store)
        self.assertGreaterEqual(comparison["total_branches"], 4)

        branches_map = {b["branch_code"]: b for b in comparison["branches"]}
        # CN-TRUNGTAM: 2 visits, 750k net
        self.assertEqual(branches_map["CN-TRUNGTAM"]["visit_count"], 2)
        self.assertEqual(branches_map["CN-TRUNGTAM"]["net_revenue"], 750000.0)

        # CN-QUAN1: 1 visit, 400k net
        self.assertEqual(branches_map["CN-QUAN1"]["visit_count"], 1)
        self.assertEqual(branches_map["CN-QUAN1"]["net_revenue"], 400000.0)

    # ─────────────────────────────────────────────────────────────────
    # 10. PET OWNER SELF-SERVICE PORTAL DATA CONTRACTS
    # ─────────────────────────────────────────────────────────────────
    def test_10_owner_portal_contract_validation(self):
        """Kiểm tra tính toàn vẹn của Data Contract cho Cổng/App Chủ Nuôi."""
        # Test imports and signatures from api module
        from petcare_crm import api

        self.assertTrue(hasattr(api, "owner_portal_get_pets"))
        self.assertTrue(hasattr(api, "owner_portal_get_health_timeline"))
        self.assertTrue(hasattr(api, "owner_portal_get_membership_wallet"))
        self.assertTrue(hasattr(api, "owner_portal_book_appointment"))
        self.assertTrue(hasattr(api, "get_service_visit_payment_qr"))
        self.assertTrue(hasattr(api, "payment_webhook"))
        self.assertTrue(hasattr(api, "send_omnichannel_notification"))


if __name__ == "__main__":
    unittest.main()
