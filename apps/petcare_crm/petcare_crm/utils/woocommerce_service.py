# Copyright (c) 2026, PetCare CRM Team and contributors
# For license information, please see license.txt

"""WooCommerce order webhook security and CRM synchronization services."""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import re
from decimal import Decimal, InvalidOperation
from typing import Any, Dict, Iterable, Optional, Tuple

import frappe
from frappe.utils import now_datetime

from petcare_crm.utils.exceptions import ValidationError


SUPPORTED_TOPICS = {
    "order.created",
    "order.updated",
    "order.deleted",
    "order.restored",
}


class WooCommerceWebhookSecurity:
    """Implements the signature format used by native WooCommerce webhooks."""

    @staticmethod
    def compute_signature(raw_body: Any, secret: str) -> str:
        if not secret:
            raise ValidationError("WooCommerce webhook secret chưa được cấu hình.")

        if isinstance(raw_body, str):
            raw_body = raw_body.encode("utf-8")
        if not isinstance(raw_body, (bytes, bytearray)):
            raise ValidationError("Webhook body phải là bytes hoặc chuỗi UTF-8.")

        digest = hmac.new(
            str(secret).encode("utf-8"), bytes(raw_body), hashlib.sha256
        ).digest()
        return base64.b64encode(digest).decode("ascii")

    @classmethod
    def verify_signature(cls, raw_body: Any, signature: str, secret: str) -> bool:
        if not signature:
            return False
        expected = cls.compute_signature(raw_body, secret)
        return hmac.compare_digest(expected, str(signature).strip())


class WooCommerceOrderSyncService:
    """Maps WooCommerce orders to Contact, Pet and PetCare Opportunity."""

    @staticmethod
    def _normalize_phone(phone: Any) -> str:
        cleaned = re.sub(r"[\s\-.()]", "", str(phone or "").strip())
        if cleaned.startswith("+84"):
            cleaned = "0" + cleaned[3:]
        elif cleaned.startswith("84") and len(cleaned) in (11, 12):
            cleaned = "0" + cleaned[2:]
        if not re.fullmatch(r"0\d{8,10}", cleaned):
            raise ValidationError(
                "Đơn WooCommerce thiếu số điện thoại Việt Nam hợp lệ trong billing.phone."
            )
        return cleaned

    @staticmethod
    def _parse_total(value: Any) -> float:
        try:
            amount = Decimal(str(value or "0"))
        except (InvalidOperation, ValueError):
            raise ValidationError("Tổng tiền đơn WooCommerce không hợp lệ.")
        if amount < 0:
            raise ValidationError("Tổng tiền đơn WooCommerce không được âm.")
        return float(amount)

    @staticmethod
    def _metadata_map(metadata: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        for item in metadata or []:
            if isinstance(item, dict) and item.get("key"):
                result[str(item["key"])] = item.get("value")
        return result

    @classmethod
    def normalize_order(cls, payload: Dict[str, Any]) -> Dict[str, Any]:
        if not isinstance(payload, dict):
            raise ValidationError("Payload WooCommerce phải là một JSON object.")

        order_id = str(payload.get("id") or "").strip()
        if not order_id or not order_id.isdigit():
            raise ValidationError("Payload WooCommerce thiếu order id hợp lệ.")

        billing = payload.get("billing") or {}
        if not isinstance(billing, dict):
            billing = {}

        first_name = str(billing.get("first_name") or "").strip()
        last_name = str(billing.get("last_name") or "").strip()
        customer_name = " ".join(x for x in (first_name, last_name) if x).strip()
        if not customer_name:
            raise ValidationError("Đơn WooCommerce thiếu tên khách hàng trong billing.")

        phone = cls._normalize_phone(billing.get("phone"))
        email = str(billing.get("email") or "").strip().lower() or None
        order_status = str(payload.get("status") or "pending").strip().lower()
        currency = str(payload.get("currency") or "VND").strip().upper()[:3]
        metadata = cls._metadata_map(payload.get("meta_data") or [])

        line_items = []
        for item in payload.get("line_items") or []:
            if not isinstance(item, dict):
                continue
            line_items.append(
                {
                    "product_id": str(item.get("product_id") or ""),
                    "variation_id": str(item.get("variation_id") or ""),
                    "sku": str(item.get("sku") or "").strip(),
                    "name": str(item.get("name") or "Sản phẩm/Dịch vụ").strip(),
                    "quantity": int(item.get("quantity") or 0),
                    "total": cls._parse_total(item.get("total")),
                }
            )

        return {
            "order_id": order_id,
            "order_number": str(payload.get("number") or order_id).strip(),
            "order_status": order_status,
            "currency": currency,
            "order_total": cls._parse_total(payload.get("total")),
            "customer_name": customer_name,
            "first_name": first_name or customer_name,
            "last_name": last_name,
            "phone": phone,
            "email": email,
            "line_items": line_items,
            "pet_name": str(
                metadata.get("_petcare_pet_name")
                or metadata.get("pet_name")
                or ""
            ).strip()
            or None,
            "pet_species": str(
                metadata.get("_petcare_pet_species")
                or metadata.get("pet_species")
                or "Other"
            ).strip(),
            "pet_breed": str(
                metadata.get("_petcare_pet_breed")
                or metadata.get("pet_breed")
                or ""
            ).strip()
            or None,
            "customer_note": str(payload.get("customer_note") or "").strip() or None,
        }

    @staticmethod
    def make_external_order_key(site_url: str, order_id: str) -> str:
        normalized_site = str(site_url or "unknown-site").strip().rstrip("/").lower()
        return hashlib.sha256(
            f"{normalized_site}:{order_id}".encode("utf-8")
        ).hexdigest()

    @staticmethod
    def map_pipeline_stage(order_status: str) -> Tuple[str, float, Optional[str]]:
        status = str(order_status or "pending").lower()
        if status in {"processing", "completed"}:
            return "Closed Won", 100.0, None
        if status in {"cancelled", "failed", "refunded", "trash"}:
            return "Closed Lost", 0.0, "Other"
        if status == "on-hold":
            return "Negotiation", 70.0, None
        return "Proposal", 50.0, None

    @staticmethod
    def _get_conf(key: str, default: Any = None) -> Any:
        conf = getattr(frappe, "conf", None)
        if conf is None:
            return default
        if hasattr(conf, "get"):
            return conf.get(key, default)
        return getattr(conf, key, default)

    @classmethod
    def _find_or_create_contact(cls, order: Dict[str, Any]) -> Tuple[str, bool]:
        contact_name = None
        for filters in (
            {"mobile_no": order["phone"]},
            {"phone": order["phone"]},
            {"email_id": order["email"]} if order.get("email") else None,
        ):
            if filters:
                contact_name = frappe.db.get_value("Contact", filters, "name")
                if contact_name:
                    return contact_name, False

        contact = frappe.get_doc(
            {
                "doctype": "Contact",
                "first_name": order["first_name"],
                "last_name": order["last_name"],
                "phone": order["phone"],
                "mobile_no": order["phone"],
                "email_id": order.get("email"),
                "is_primary_contact": 1,
            }
        )
        contact.insert(ignore_permissions=True)
        return contact.name, True

    @staticmethod
    def _normalize_species(species: str) -> str:
        value = str(species or "Other").strip().lower()
        mapping = {
            "dog": "Dog",
            "chó": "Dog",
            "cat": "Cat",
            "mèo": "Cat",
            "rabbit": "Rabbit",
            "thỏ": "Rabbit",
        }
        return mapping.get(value, "Other")

    @classmethod
    def _find_or_create_pet(
        cls, order: Dict[str, Any], contact_name: str
    ) -> Optional[str]:
        pet_name = order.get("pet_name")
        if not pet_name:
            return None
        existing = frappe.db.get_value(
            "Pet", {"customer": contact_name, "pet_name": pet_name}, "name"
        )
        if existing:
            return existing

        pet = frappe.get_doc(
            {
                "doctype": "Pet",
                "pet_name": pet_name,
                "customer": contact_name,
                "species": cls._normalize_species(order.get("pet_species")),
                "breed": order.get("pet_breed"),
                "notes": f"Tạo tự động từ đơn WooCommerce #{order['order_number']}",
            }
        )
        pet.insert(ignore_permissions=True)
        return pet.name

    @classmethod
    def _create_opportunity(
        cls, order: Dict[str, Any], contact_name: str, pet_name: Optional[str]
    ) -> str:
        stage, probability, lost_reason = cls.map_pipeline_stage(order["order_status"])
        item_names = ", ".join(item["name"] for item in order["line_items"][:3])
        title_suffix = f" - {item_names}" if item_names else ""
        opportunity = frappe.get_doc(
            {
                "doctype": "PetCare Opportunity",
                "opportunity_title": (
                    f"WooCommerce #{order['order_number']}{title_suffix}"
                )[:140],
                "customer": contact_name,
                "pet": pet_name,
                "stage": stage,
                "expected_amount": order["order_total"],
                "probability": probability,
                "sales_person": cls._get_conf(
                    "woocommerce_sales_owner", "Administrator"
                ),
                "lost_reason": lost_reason,
                "lost_notes": (
                    f"Đơn WooCommerce chuyển sang trạng thái {order['order_status']}"
                    if lost_reason
                    else None
                ),
            }
        )
        opportunity.insert(ignore_permissions=True)
        return opportunity.name

    @classmethod
    def _update_opportunity(cls, opportunity_name: str, order: Dict[str, Any]) -> None:
        opportunity = frappe.get_doc("PetCare Opportunity", opportunity_name)
        stage, probability, lost_reason = cls.map_pipeline_stage(order["order_status"])
        opportunity.stage = stage
        opportunity.probability = probability
        opportunity.expected_amount = order["order_total"]
        opportunity.lost_reason = lost_reason
        opportunity.lost_notes = (
            f"Đơn WooCommerce chuyển sang trạng thái {order['order_status']}"
            if lost_reason
            else None
        )
        opportunity.save(ignore_permissions=True)

    @classmethod
    def process_order(
        cls,
        payload: Dict[str, Any],
        topic: str,
        delivery_id: Optional[str],
        site_url: str,
    ) -> Dict[str, Any]:
        if topic not in SUPPORTED_TOPICS:
            raise ValidationError(f"WooCommerce topic '{topic}' không được hỗ trợ.")

        order = cls.normalize_order(payload)
        external_key = cls.make_external_order_key(site_url, order["order_id"])
        existing_name = frappe.db.get_value(
            "WooCommerce Order Sync",
            {"external_order_key": external_key},
            "name",
        )

        if existing_name:
            sync_doc = frappe.get_doc("WooCommerce Order Sync", existing_name)
            if delivery_id and sync_doc.last_delivery_id == delivery_id:
                return {
                    "status": "success",
                    "duplicate": True,
                    "sync_id": sync_doc.name,
                    "order_id": order["order_id"],
                    "opportunity_id": sync_doc.linked_opportunity,
                    "message": "Webhook delivery đã được xử lý trước đó.",
                }

            if sync_doc.linked_opportunity:
                cls._update_opportunity(sync_doc.linked_opportunity, order)
            sync_doc.order_status = order["order_status"]
            sync_doc.order_total = order["order_total"]
            sync_doc.currency = order["currency"]
            sync_doc.topic = topic
            sync_doc.last_delivery_id = delivery_id
            sync_doc.raw_payload = json.dumps(payload, ensure_ascii=False)
            sync_doc.sync_status = "Updated"
            sync_doc.processed_at = now_datetime()
            sync_doc.save(ignore_permissions=True)
            return {
                "status": "success",
                "duplicate": False,
                "updated": True,
                "sync_id": sync_doc.name,
                "order_id": order["order_id"],
                "opportunity_id": sync_doc.linked_opportunity,
                "message": "Đã cập nhật đơn WooCommerce trong CRM.",
            }

        contact_name, contact_created = cls._find_or_create_contact(order)
        pet_name = cls._find_or_create_pet(order, contact_name)
        opportunity_name = cls._create_opportunity(order, contact_name, pet_name)

        sync_doc = frappe.get_doc(
            {
                "doctype": "WooCommerce Order Sync",
                "external_order_key": external_key,
                "site_url": str(site_url or "unknown-site")[:255],
                "woocommerce_order_id": order["order_id"],
                "order_number": order["order_number"],
                "order_status": order["order_status"],
                "topic": topic,
                "last_delivery_id": delivery_id,
                "currency": order["currency"],
                "order_total": order["order_total"],
                "customer_name": order["customer_name"],
                "customer_phone": order["phone"],
                "customer_email": order.get("email"),
                "linked_customer": contact_name,
                "linked_pet": pet_name,
                "linked_opportunity": opportunity_name,
                "raw_payload": json.dumps(payload, ensure_ascii=False),
                "sync_status": "Created",
                "received_at": now_datetime(),
                "processed_at": now_datetime(),
            }
        )
        sync_doc.insert(ignore_permissions=True)

        return {
            "status": "success",
            "duplicate": False,
            "updated": False,
            "sync_id": sync_doc.name,
            "order_id": order["order_id"],
            "contact_id": contact_name,
            "contact_created": contact_created,
            "pet_id": pet_name,
            "opportunity_id": opportunity_name,
            "message": "Đã đồng bộ đơn WooCommerce vào PetCare CRM.",
        }

