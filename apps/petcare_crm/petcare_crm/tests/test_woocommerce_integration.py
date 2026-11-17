# Copyright (c) 2026, PetCare CRM Team and contributors

"""Tests for the WooCommerce -> PetCare CRM order integration."""

import base64
import hashlib
import hmac
import os
import sys
import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, patch


sys.path.insert(0, os.path.abspath("apps/petcare_crm"))

if "frappe" not in sys.modules:
    mock_frappe = MagicMock()
    mock_frappe._ = lambda value: value
    mock_frappe.whitelist = lambda *args, **kwargs: (
        args[0] if args and callable(args[0]) else lambda fn: fn
    )
    mock_frappe_utils = MagicMock()
    mock_frappe_utils.now_datetime.return_value = "2026-11-07 12:00:00"
    mock_frappe.utils = mock_frappe_utils
    sys.modules["frappe"] = mock_frappe
    sys.modules["frappe.utils"] = mock_frappe_utils

import frappe

from petcare_crm.utils.exceptions import ValidationError
from petcare_crm.utils.woocommerce_service import (
    WooCommerceOrderSyncService,
    WooCommerceWebhookSecurity,
)


def sample_order(**overrides):
    data = {
        "id": 8451,
        "number": "PC-8451",
        "status": "processing",
        "currency": "VND",
        "total": "650000",
        "billing": {
            "first_name": "Nguyễn Văn",
            "last_name": "An",
            "phone": "091 234 5678",
            "email": "An.Nguyen@example.com",
        },
        "line_items": [
            {
                "product_id": 101,
                "variation_id": 0,
                "sku": "SPA-FULL",
                "name": "Gói Spa Toàn Diện",
                "quantity": 1,
                "total": "650000",
            }
        ],
        "meta_data": [
            {"key": "_petcare_pet_name", "value": "Milo"},
            {"key": "_petcare_pet_species", "value": "Chó"},
            {"key": "_petcare_pet_breed", "value": "Poodle"},
        ],
    }
    data.update(overrides)
    return data


class TestWooCommerceIntegration(unittest.TestCase):

    def test_01_signature_matches_native_woocommerce_format(self):
        body = b'{"id":8451,"status":"processing"}'
        secret = "shared-secret-2026"
        expected = base64.b64encode(
            hmac.new(secret.encode(), body, hashlib.sha256).digest()
        ).decode()
        actual = WooCommerceWebhookSecurity.compute_signature(body, secret)
        self.assertEqual(actual, expected)
        self.assertTrue(WooCommerceWebhookSecurity.verify_signature(body, actual, secret))

    def test_02_signature_rejects_tampered_payload(self):
        original = b'{"id":8451,"total":"650000"}'
        tampered = b'{"id":8451,"total":"6500000"}'
        signature = WooCommerceWebhookSecurity.compute_signature(original, "secret")
        self.assertFalse(
            WooCommerceWebhookSecurity.verify_signature(tampered, signature, "secret")
        )

    def test_03_order_normalization_maps_customer_pet_and_items(self):
        order = WooCommerceOrderSyncService.normalize_order(sample_order())
        self.assertEqual(order["order_id"], "8451")
        self.assertEqual(order["order_number"], "PC-8451")
        self.assertEqual(order["phone"], "0912345678")
        self.assertEqual(order["email"], "an.nguyen@example.com")
        self.assertEqual(order["pet_name"], "Milo")
        self.assertEqual(order["pet_species"], "Chó")
        self.assertEqual(order["line_items"][0]["sku"], "SPA-FULL")
        self.assertEqual(order["order_total"], 650000.0)

    def test_04_phone_normalization_accepts_country_code(self):
        payload = sample_order()
        payload["billing"]["phone"] = "+84 987-654-321"
        order = WooCommerceOrderSyncService.normalize_order(payload)
        self.assertEqual(order["phone"], "0987654321")

    def test_05_invalid_orders_are_rejected(self):
        cases = [
            {"id": None},
            {"billing": {"first_name": "", "last_name": "", "phone": "0912345678"}},
            {"billing": {"first_name": "An", "phone": "abc"}},
            {"total": "-1"},
        ]
        for overrides in cases:
            with self.subTest(overrides=overrides):
                with self.assertRaises(ValidationError):
                    WooCommerceOrderSyncService.normalize_order(sample_order(**overrides))

    def test_06_status_to_pipeline_mapping(self):
        self.assertEqual(
            WooCommerceOrderSyncService.map_pipeline_stage("processing"),
            ("Closed Won", 100.0, None),
        )
        self.assertEqual(
            WooCommerceOrderSyncService.map_pipeline_stage("cancelled"),
            ("Closed Lost", 0.0, "Other"),
        )

    def test_07_external_key_is_stable_and_site_scoped(self):
        key_1 = WooCommerceOrderSyncService.make_external_order_key(
            "https://shop.petcare.vn/", "8451"
        )
        key_2 = WooCommerceOrderSyncService.make_external_order_key(
            "https://SHOP.PETCARE.vn", "8451"
        )
        key_3 = WooCommerceOrderSyncService.make_external_order_key(
            "https://other.petcare.vn", "8451"
        )
        self.assertEqual(key_1, key_2)
        self.assertNotEqual(key_1, key_3)

    def test_08_new_order_creates_auditable_sync_record(self):
        created = {}

        def fake_get_doc(data):
            doc = SimpleNamespace(**data)
            doc.name = "WC-SYNC-0001"

            def insert(ignore_permissions=True):
                created.update(data)

            doc.insert = insert
            return doc

        with patch.object(frappe.db, "get_value", return_value=None), patch.object(
            frappe, "get_doc", side_effect=fake_get_doc
        ), patch.object(
            WooCommerceOrderSyncService,
            "_find_or_create_contact",
            return_value=("CONTACT-0001", True),
        ), patch.object(
            WooCommerceOrderSyncService, "_find_or_create_pet", return_value="PET-0001"
        ), patch.object(
            WooCommerceOrderSyncService, "_create_opportunity", return_value="OPP-0001"
        ):
            result = WooCommerceOrderSyncService.process_order(
                sample_order(), "order.created", "delivery-1", "https://shop.petcare.vn"
            )

        self.assertFalse(result["duplicate"])
        self.assertEqual(result["opportunity_id"], "OPP-0001")
        self.assertEqual(created["doctype"], "WooCommerce Order Sync")
        self.assertEqual(created["linked_customer"], "CONTACT-0001")
        self.assertEqual(created["linked_pet"], "PET-0001")

    def test_09_same_delivery_is_idempotent(self):
        sync_doc = SimpleNamespace(
            name="WC-SYNC-0001",
            last_delivery_id="delivery-1",
            linked_opportunity="OPP-0001",
        )
        with patch.object(frappe.db, "get_value", return_value="WC-SYNC-0001"), patch.object(
            frappe, "get_doc", return_value=sync_doc
        ), patch.object(WooCommerceOrderSyncService, "_update_opportunity") as update:
            result = WooCommerceOrderSyncService.process_order(
                sample_order(), "order.updated", "delivery-1", "https://shop.petcare.vn"
            )

        self.assertTrue(result["duplicate"])
        update.assert_not_called()

    def test_10_new_delivery_updates_existing_order_and_opportunity(self):
        saved = []
        sync_doc = SimpleNamespace(
            name="WC-SYNC-0001",
            last_delivery_id="delivery-1",
            linked_opportunity="OPP-0001",
        )
        sync_doc.save = lambda ignore_permissions=True: saved.append(True)

        with patch.object(frappe.db, "get_value", return_value="WC-SYNC-0001"), patch.object(
            frappe, "get_doc", return_value=sync_doc
        ), patch.object(WooCommerceOrderSyncService, "_update_opportunity") as update:
            result = WooCommerceOrderSyncService.process_order(
                sample_order(status="cancelled"),
                "order.updated",
                "delivery-2",
                "https://shop.petcare.vn",
            )

        self.assertTrue(result["updated"])
        self.assertEqual(sync_doc.order_status, "cancelled")
        self.assertTrue(saved)
        update.assert_called_once()

    def test_11_wordpress_plugin_contains_hooks_hmac_and_retry(self):
        plugin_file = os.path.join(
            "deliverables",
            "wordpress",
            "petcare-lead-capture",
            "includes",
            "class-petcare-woocommerce-sync.php",
        )
        with open(plugin_file, encoding="utf-8") as handle:
            source = handle.read()
        self.assertIn("woocommerce_checkout_order_processed", source)
        self.assertIn("woocommerce_order_status_changed", source)
        self.assertIn("hash_hmac('sha256'", source)
        self.assertIn("as_schedule_single_action", source)
        self.assertIn("X-WC-Webhook-Signature", source)


if __name__ == "__main__":
    unittest.main()

