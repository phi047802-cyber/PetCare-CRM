"""
T36: Automated unit tests for Module 1 — Membership & Benefit Management.
Run: bench --site petcare.localhost run-tests --app petcare_crm --module petcare_crm.tests.test_membership
"""
import frappe
import unittest
from datetime import date, timedelta


class TestMembershipModule(unittest.TestCase):

    def setUp(self):
        """Tạo test data sạch trước mỗi test."""
        frappe.set_user("Administrator")
        self._cleanup()
        self._create_test_data()

    def tearDown(self):
        """Xóa test data sau mỗi test."""
        frappe.db.rollback()

    def _cleanup(self):
        if hasattr(self, "customer_name") and self.customer_name:
            test_ms = frappe.db.get_list("Customer Membership", filters={"customer": self.customer_name}, pluck="name")
            if test_ms:
                frappe.db.delete("Membership Benefit", {"parent": ["in", test_ms]})
            frappe.db.delete("Customer Membership", {"customer": self.customer_name})
            frappe.db.delete("Contact", {"name": self.customer_name})
        frappe.db.delete("Plan Benefit", {"parent": "Test Plan Unit"})
        frappe.db.delete("Membership Benefit", {"parent": "Test Plan Unit"})
        frappe.db.delete("Customer Membership", {"membership_plan": "Test Plan Unit"})
        frappe.db.delete("Membership Plan", {"plan_name": "Test Plan Unit"})
        frappe.db.commit()

    def _create_test_data(self):
        today = date.today()

        # Tạo Contact sạch
        contact = frappe.get_doc({
            "doctype": "Contact",
            "first_name": "TestUnitCustomer",
            "is_primary_contact": 1,
        }).insert(ignore_permissions=True)
        self.customer_name = contact.name

        # Tạo Membership Plan
        plan = frappe.get_doc({
            "doctype": "Membership Plan",
            "plan_name": "Test Plan Unit",
            "price": 200000,
            "duration_months": 1,
            "benefits": [
                {
                    "benefit_type": "Grooming",
                    "total_quantity": 1,
                    "discount_type": "FREE",
                    "discount_value": 100.0,
                }
            ]
        }).insert(ignore_permissions=True)

        # Tạo Customer Membership
        self.ms = frappe.get_doc({
            "doctype": "Customer Membership",
            "customer": self.customer_name,
            "membership_plan": "Test Plan Unit",
            "start_date": str(today - timedelta(days=5)),
            "end_date": str(today + timedelta(days=25)),
            "status": "Active",
            "benefits": [
                {
                    "benefit_type": "Grooming",
                    "total_quantity": 1,
                    "used_quantity": 0,
                    "remaining_quantity": 1,
                    "discount_type": "FREE",
                    "discount_value": 100.0,
                }
            ]
        }).insert(ignore_permissions=True)
        frappe.db.commit()

    # ─────────────────────────────────────────────────────────────────────
    # TEST: get_active_membership
    # ─────────────────────────────────────────────────────────────────────

    def test_get_active_membership_returns_active(self):
        """get_active_membership trả về membership đang active."""
        result = frappe.call(
            "petcare_crm.api.get_active_membership",
            customer=self.customer_name
        )
        self.assertIsNotNone(result)
        self.assertEqual(result["status"], "Active")
        self.assertEqual(result["customer"], self.customer_name)

    def test_get_active_membership_returns_none_for_unknown(self):
        """get_active_membership trả về None nếu không có membership."""
        result = frappe.call(
            "petcare_crm.api.get_active_membership",
            customer="NONEXISTENT-CUSTOMER-999"
        )
        self.assertIsNone(result)

    # ─────────────────────────────────────────────────────────────────────
    # TEST: get_remaining_benefit
    # ─────────────────────────────────────────────────────────────────────

    def test_get_remaining_benefit_returns_correct_quantity(self):
        """get_remaining_benefit trả về đúng số lượt còn lại."""
        result = frappe.call(
            "petcare_crm.api.get_remaining_benefit",
            membership_name=self.ms.name,
            service_type="Grooming"
        )
        self.assertIsNotNone(result)
        self.assertEqual(result["remaining_quantity"], 1)
        self.assertEqual(result["benefit_type"], "Grooming")

    def test_get_remaining_benefit_returns_none_for_unknown_type(self):
        """Trả về None nếu service_type không có trong membership."""
        result = frappe.call(
            "petcare_crm.api.get_remaining_benefit",
            membership_name=self.ms.name,
            service_type="Vaccination"
        )
        self.assertIsNone(result)

    # ─────────────────────────────────────────────────────────────────────
    # TEST: record_benefit_usage — FLOW 1
    # ─────────────────────────────────────────────────────────────────────

    def test_record_benefit_reduces_remaining_by_one(self):
        """record_benefit_usage trừ đúng 1 lượt, remaining = 0."""
        result = frappe.call(
            "petcare_crm.api.record_benefit_usage",
            membership_name=self.ms.name,
            service_type="Grooming"
        )
        self.assertTrue(result["success"])
        self.assertEqual(result["remaining_quantity"], 0)
        self.assertEqual(result["used_quantity"], 1)

    def test_record_benefit_blocks_when_exhausted(self):
        """FLOW 1: record_benefit_usage ném lỗi khi remaining = 0."""
        # Trừ lần 1 (remaining về 0)
        frappe.call(
            "petcare_crm.api.record_benefit_usage",
            membership_name=self.ms.name,
            service_type="Grooming"
        )
        # Trừ lần 2 → phải throw ValidationError
        with self.assertRaises(frappe.exceptions.ValidationError):
            frappe.call(
                "petcare_crm.api.record_benefit_usage",
                membership_name=self.ms.name,
                service_type="Grooming"
            )

    def test_remaining_never_goes_negative(self):
        """Invariant: remaining_quantity không bao giờ < 0."""
        # Trừ hết lượt
        frappe.call(
            "petcare_crm.api.record_benefit_usage",
            membership_name=self.ms.name,
            service_type="Grooming"
        )
        # Kiểm tra database
        ms_doc = frappe.get_doc("Customer Membership", self.ms.name)
        for b in ms_doc.benefits:
            self.assertGreaterEqual(
                b.remaining_quantity, 0,
                f"remaining_quantity của {b.benefit_type} không được âm!"
            )

    def test_record_benefit_fails_for_expired_membership(self):
        """record_benefit_usage từ chối nếu membership đã expired."""
        # Chuyển status thành Expired
        ms_doc = frappe.get_doc("Customer Membership", self.ms.name)
        ms_doc.status = "Expired"
        ms_doc.save(ignore_permissions=True)
        frappe.db.commit()

        with self.assertRaises(frappe.exceptions.ValidationError):
            frappe.call(
                "petcare_crm.api.record_benefit_usage",
                membership_name=self.ms.name,
                service_type="Grooming"
            )

    def test_record_benefit_fails_for_invalid_count(self):
        """record_benefit_usage từ chối count <= 0."""
        with self.assertRaises(frappe.exceptions.ValidationError):
            frappe.call(
                "petcare_crm.api.record_benefit_usage",
                membership_name=self.ms.name,
                service_type="Grooming",
                count=0
            )
        with self.assertRaises(frappe.exceptions.ValidationError):
            frappe.call(
                "petcare_crm.api.record_benefit_usage",
                membership_name=self.ms.name,
                service_type="Grooming",
                count=-1
            )

    def test_record_benefit_fails_for_unknown_benefit_type(self):
        """record_benefit_usage từ chối nếu service_type không có trong gói."""
        with self.assertRaises(frappe.exceptions.ValidationError):
            frappe.call(
                "petcare_crm.api.record_benefit_usage",
                membership_name=self.ms.name,
                service_type="NonexistentService"
            )

    def test_record_benefit_multiple_count(self):
        """M1: Trừ nhiều lượt (count > 1) hoạt động chính xác."""
        today = date.today()
        multi_ms = frappe.get_doc({
            "doctype": "Customer Membership",
            "customer": self.customer_name,
            "membership_plan": "Test Plan Unit",
            "start_date": str(today - timedelta(days=2)),
            "end_date": str(today + timedelta(days=28)),
            "status": "Active",
            "benefits": [
                {
                    "benefit_type": "Grooming",
                    "total_quantity": 5,
                    "used_quantity": 0,
                    "remaining_quantity": 5,
                    "discount_type": "FREE",
                    "discount_value": 100.0,
                }
            ]
        }).insert(ignore_permissions=True)
        frappe.db.commit()

        # Trừ 2 lượt
        res = frappe.call(
            "petcare_crm.api.record_benefit_usage",
            membership_name=multi_ms.name,
            service_type="Grooming",
            count=2
        )
        self.assertTrue(res["success"])
        self.assertEqual(res["remaining_quantity"], 3)
        self.assertEqual(res["used_quantity"], 2)

        # Trừ thêm 3 lượt (vừa hết 5)
        res2 = frappe.call(
            "petcare_crm.api.record_benefit_usage",
            membership_name=multi_ms.name,
            service_type="Grooming",
            count=3
        )
        self.assertEqual(res2["remaining_quantity"], 0)
        self.assertEqual(res2["used_quantity"], 5)

        # Trừ thêm 1 lượt nữa -> Phải bị chặn
        with self.assertRaises(frappe.exceptions.ValidationError):
            frappe.call(
                "petcare_crm.api.record_benefit_usage",
                membership_name=multi_ms.name,
                service_type="Grooming",
                count=1
            )

    def test_multiple_benefit_types_isolation(self):
        """M1: Membership có nhiều benefit types (Grooming + Spa) trừ độc lập nhau."""
        today = date.today()
        dual_ms = frappe.get_doc({
            "doctype": "Customer Membership",
            "customer": self.customer_name,
            "membership_plan": "Test Plan Unit",
            "start_date": str(today - timedelta(days=2)),
            "end_date": str(today + timedelta(days=28)),
            "status": "Active",
            "benefits": [
                {
                    "benefit_type": "Grooming",
                    "total_quantity": 3,
                    "used_quantity": 0,
                    "remaining_quantity": 3,
                    "discount_type": "FREE",
                    "discount_value": 100.0,
                },
                {
                    "benefit_type": "Spa",
                    "total_quantity": 2,
                    "used_quantity": 0,
                    "remaining_quantity": 2,
                    "discount_type": "FREE",
                    "discount_value": 100.0,
                }
            ]
        }).insert(ignore_permissions=True)
        frappe.db.commit()

        # Trừ Grooming
        frappe.call(
            "petcare_crm.api.record_benefit_usage",
            membership_name=dual_ms.name,
            service_type="Grooming",
            count=1
        )

        # Kiểm tra Spa vẫn giữ nguyên 2 lượt
        spa_ben = frappe.call(
            "petcare_crm.api.get_remaining_benefit",
            membership_name=dual_ms.name,
            service_type="Spa"
        )
        self.assertEqual(spa_ben["remaining_quantity"], 2)

    def test_check_membership_renewal_detection(self):
        """T21 & M1: Gói hết hạn trong 5 ngày được phát hiện cần gia hạn."""
        today = date.today()
        expiring_ms = frappe.get_doc({
            "doctype": "Customer Membership",
            "customer": self.customer_name,
            "membership_plan": "Test Plan Unit",
            "start_date": str(today - timedelta(days=25)),
            "end_date": str(today + timedelta(days=4)),
            "status": "Active",
            "benefits": [
                {
                    "benefit_type": "Grooming",
                    "total_quantity": 1,
                    "used_quantity": 0,
                    "remaining_quantity": 1,
                    "discount_type": "FREE",
                    "discount_value": 100.0,
                }
            ]
        }).insert(ignore_permissions=True)
        frappe.db.commit()

        renewal_info = frappe.call(
            "petcare_crm.api.check_membership_renewal",
            customer=self.customer_name
        )
        self.assertGreaterEqual(renewal_info["count"], 1)
        found = any(r["membership_name"] == expiring_ms.name for r in renewal_info["renewals_needed"])
        self.assertTrue(found)

    def test_renew_membership_with_rollover_and_wallet_deduction(self):
        """Gia hạn gói với hình thức trừ Ví và cộng dồn số lượt còn lại (Rollover)."""
        from petcare_crm.api import renew_membership
        # Cập nhật số dư ví trước
        self.ms.balance = 500000
        self.ms.save(ignore_permissions=True)
        frappe.db.commit()

        old_end = frappe.utils.getdate(self.ms.end_date)
        res = renew_membership(
            membership_name=self.ms.name,
            payment_source="Wallet",
            allow_rollover=1
        )
        self.assertTrue(res["success"])
        self.assertEqual(res["balance"], 300000)

        # Kiểm tra document trong database
        updated_ms = frappe.get_doc("Customer Membership", self.ms.name)
        self.assertEqual(float(updated_ms.balance), 300000.0)
        self.assertEqual(updated_ms.status, "Active")
        
        # Quyền lợi 1 cũ + 1 mới = 2
        grooming_b = next(b for b in updated_ms.benefits if b.benefit_type == "Grooming")
        self.assertEqual(grooming_b.total_quantity, 2)
        self.assertEqual(grooming_b.remaining_quantity, 2)

        # Ngày hết hạn nối tiếp
        new_expected_end = frappe.utils.add_months(str(old_end), 1)
        self.assertEqual(str(updated_ms.end_date), str(new_expected_end))

    def test_renew_membership_fails_insufficient_wallet_balance(self):
        """Báo lỗi nếu chọn trừ Ví nhưng số dư tài khoản không đủ."""
        from petcare_crm.api import renew_membership
        self.ms.balance = 50000  # < 200,000 giá gói
        self.ms.save(ignore_permissions=True)
        frappe.db.commit()

        with self.assertRaises(frappe.ValidationError):
            renew_membership(
                membership_name=self.ms.name,
                payment_source="Wallet"
            )

    def test_renew_membership_cash_payment_preserves_balance(self):
        """Thanh toán tiền mặt không trừ vào số dư ví của khách."""
        from petcare_crm.api import renew_membership
        self.ms.balance = 150000
        self.ms.save(ignore_permissions=True)
        frappe.db.commit()

        res = renew_membership(
            membership_name=self.ms.name,
            payment_source="Cash",
            allow_rollover=1
        )
        self.assertTrue(res["success"])
        updated_ms = frappe.get_doc("Customer Membership", self.ms.name)
        self.assertEqual(float(updated_ms.balance), 150000.0)

    def test_renew_membership_blocked_when_plenty_of_turns_and_not_expiring(self):
        """Khóa gia hạn nếu khách còn >= 5 lượt và thẻ còn hạn dài (> 7 ngày) để tránh lãng phí."""
        from petcare_crm.api import renew_membership
        today = date.today()
        self.ms.balance = 500000
        self.ms.end_date = str(today + timedelta(days=20)) # Còn 20 ngày
        self.ms.benefits[0].total_quantity = 8
        self.ms.benefits[0].remaining_quantity = 6 # >= 5 lượt
        self.ms.save(ignore_permissions=True)
        frappe.db.commit()

        # Thử gia hạn bình thường -> Phải bị chặn và báo lỗi thân thiện
        with self.assertRaises(frappe.ValidationError):
            renew_membership(
                membership_name=self.ms.name,
                payment_source="Wallet"
            )

        # Nếu thẻ sắp hết hạn (còn 3 ngày) -> Được phép gia hạn nối tiếp để bảo lưu
        self.ms.end_date = str(today + timedelta(days=3))
        self.ms.save(ignore_permissions=True)
        frappe.db.commit()

        res = renew_membership(
            membership_name=self.ms.name,
            payment_source="Wallet",
            allow_rollover=1
        )
        self.assertTrue(res["success"])

    def test_renew_membership_fails_for_non_member_or_expired(self):
        """Không cho phép gia hạn nếu thẻ đã hết hạn hoặc khách chưa phải hội viên."""
        from petcare_crm.api import renew_membership
        # Đánh dấu thẻ là Expired
        self.ms.status = "Expired"
        self.ms.save(ignore_permissions=True)
        frappe.db.commit()

        with self.assertRaises(frappe.ValidationError):
            renew_membership(
                membership_name=self.ms.name,
                payment_source="Wallet"
            )

    def test_register_membership_upgrades_standard_wallet(self):
        """Khách vãng lai đã nạp ví tiêu chuẩn có thể đăng ký nâng cấp lên gói hội viên bình thường."""
        from petcare_crm.api import register_membership
        today = date.today()
        frappe.db.delete("Pet", {"pet_name": ["like", "TestPetUpgrade%"]})
        frappe.db.commit()
        pet_unique_name = f"TestPetUpgrade_{frappe.generate_hash(length=6)}"
        pet = frappe.get_doc({
            "doctype": "Pet",
            "pet_name": pet_unique_name,
            "customer": self.customer_name,
            "species": "Dog",
        }).insert(ignore_permissions=True)

        wallet_plan = "Tài Khoản Ví Tiêu Chuẩn (Standard Wallet)"
        if not frappe.db.exists("Membership Plan", wallet_plan):
            frappe.get_doc({
                "doctype": "Membership Plan",
                "plan_name": wallet_plan,
                "price": 0,
                "duration_months": 12,
                "benefits": []
            }).insert(ignore_permissions=True)

        wallet_ms = frappe.get_doc({
            "doctype": "Customer Membership",
            "customer": self.customer_name,
            "pet": pet.name,
            "membership_plan": wallet_plan,
            "start_date": str(today),
            "end_date": str(today + timedelta(days=365)),
            "status": "Active",
            "balance": 350000,
        }).insert(ignore_permissions=True)
        frappe.db.commit()

        res = register_membership(
            customer=self.customer_name,
            pet=pet.name,
            plan_name="Test Plan Unit"
        )
        self.assertTrue(res["success"])
        updated_ms = frappe.get_doc("Customer Membership", wallet_ms.name)
        self.assertEqual(updated_ms.membership_plan, "Test Plan Unit")
        self.assertEqual(float(updated_ms.balance), 350000.0)
        self.assertEqual(len(updated_ms.benefits), 1)

    def test_sync_transaction_to_crm_deal(self):
        """Kiểm tra crm_sync tự động tạo CRM Deal và CRM Lead tương ứng."""
        from petcare_crm.utils.crm_sync import sync_transaction_to_crm_deal
        deal_name = sync_transaction_to_crm_deal(
            customer=self.customer_name,
            deal_value=500000,
            title="Đăng Ký Gói Kiểm Thử",
            notes="Giao dịch test sync",
        )
        self.assertIsNotNone(deal_name)
        deal = frappe.get_doc("CRM Deal", deal_name)
        self.assertEqual(deal.status, "Won")
        self.assertEqual(float(deal.deal_value), 500000.0)
        self.assertEqual(deal.currency, "VND")
        # Cleanup
        frappe.delete_doc("CRM Deal", deal_name, ignore_permissions=True, force=True)

    def test_sync_transaction_ignores_zero_or_negative_amounts(self):
        """Giao dịch bằng 0 hoặc âm không tạo CRM Deal để tránh sai lệch doanh thu."""
        from petcare_crm.utils.crm_sync import sync_transaction_to_crm_deal
        deal_0 = sync_transaction_to_crm_deal(self.customer_name, 0, "Test Zero")
        deal_neg = sync_transaction_to_crm_deal(self.customer_name, -100000, "Test Negative")
        self.assertIsNone(deal_0)
        self.assertIsNone(deal_neg)

