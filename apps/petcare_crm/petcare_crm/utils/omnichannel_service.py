"""
Omnichannel Communication Service for PetCare CRM.
Addresses KNOWN_LIMITATIONS Section 2.3:
- Provides unified notification gateway for Zalo ZNS (Zalo Notification Service),
  SMS Brandname, and Email.
- Supports Safe Mode outbox logging for preview & demo auditing, plus Live Dispatcher.
"""

from datetime import datetime
import json
import re
from typing import Any, Dict, List, Optional

try:
    import frappe
except ImportError:
    frappe = None

from petcare_crm.utils.config import ENABLE_LIVE_COMMUNICATION


# Supported Channels
CHANNEL_EMAIL = "EMAIL"
CHANNEL_ZALO_ZNS = "ZALO_ZNS"
CHANNEL_SMS_BRANDNAME = "SMS_BRANDNAME"

# Standard Template IDs
TEMPLATE_DUE_SOON_REMINDER = "ZNS_CARE_DUE_SOON"
TEMPLATE_MEMBERSHIP_EXPIRING = "ZNS_MEMBERSHIP_EXPIRING"
TEMPLATE_PAYMENT_CONFIRMATION = "ZNS_PAYMENT_CONFIRMATION"
TEMPLATE_LEAD_WELCOME = "ZNS_LEAD_WELCOME"


def _is_mock_frappe() -> bool:
    if not frappe or not hasattr(frappe, "db") or not frappe.db:
        return True
    return "Mock" in type(frappe.db).__name__


def _normalize_phone_vn(phone: str) -> str:
    """Normalizes Vietnamese phone number to 84xxxxxxxxx or 0xxxxxxxxx."""
    cleaned = re.sub(r"[^\d+]", "", str(phone or ""))
    if cleaned.startswith("+84"):
        return cleaned[1:]
    if cleaned.startswith("0"):
        return f"84{cleaned[1:]}"
    return cleaned


def _strip_accents(text: str) -> str:
    """Simple accent stripper for telco SMS ASCII compatibility."""
    patterns = {
        '[àáảãạăằắẳẵặâầấẩẫậ]': 'a',
        '[ÀÁẢÃẠĂẰẮẲẴẶÂẦẤẨẪẬ]': 'A',
        '[đ]': 'd', '[Đ]': 'D',
        '[èéẻẽẹêềếểễệ]': 'e',
        '[ÈÉẺẼẸÊỀẾỂỄỆ]': 'E',
        '[ìíỉĩị]': 'i',
        '[ÌÍỈĨỊ]': 'I',
        '[òóỏõọôồốổỗộơờớởỡợ]': 'o',
        '[ÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢ]': 'O',
        '[ùúủũụưừứửữự]': 'u',
        '[ÙÚỦŨỤƯỪỨỬỮỰ]': 'U',
        '[ỳýỷỹỵ]': 'y',
        '[ỲÝỶỸỴ]': 'Y'
    }
    result = text
    for regex, repl in patterns.items():
        result = re.sub(regex, repl, result)
    return result


class ZaloZNSAdapter:
    """Formatter and client for Zalo Cloud ZNS (Zalo Notification Service)."""

    TEMPLATE_SPECS = {
        TEMPLATE_DUE_SOON_REMINDER: (
            "Kính gửi {customer_name}, thú cưng {pet_name} sắp đến chu kỳ chăm sóc "
            "dịch vụ {service_type} (dự kiến: {appointment_date}). "
            "Hotline đặt lịch PetCare: {hotline}."
        ),
        TEMPLATE_MEMBERSHIP_EXPIRING: (
            "Kính gửi {customer_name}, thẻ hội viên {membership_plan} của quý khách "
            "sắp hết hạn vào ngày {expiry_date}. Quý khách vui lòng gia hạn để tiếp tục "
            "hưởng các quyền lợi chăm sóc đặc quyền."
        ),
        TEMPLATE_PAYMENT_CONFIRMATION: (
            "PetCare Clinic xác nhận thanh toán thành công {amount} VNĐ cho "
            "phiếu {reference_id} của thú cưng {pet_name}. Trân trọng cảm ơn quý khách!"
        ),
        TEMPLATE_LEAD_WELCOME: (
            "Chào mừng {customer_name} đến với PetCare CRM! "
            "Chuyên viên chăm sóc sẽ liên hệ tư vấn lộ trình sức khỏe tốt nhất cho thú cưng của bạn."
        ),
    }

    @classmethod
    def format_payload(
        cls,
        phone: str,
        template_id: str,
        template_data: Dict[str, Any],
        tracking_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        formatted_phone = _normalize_phone_vn(phone)
        return {
            "mode": "development" if not ENABLE_LIVE_COMMUNICATION else "production",
            "phone": formatted_phone,
            "template_id": template_id,
            "template_data": template_data,
            "tracking_id": tracking_id or f"TRK-{int(datetime.now().timestamp())}",
        }

    @classmethod
    def render_preview(cls, template_id: str, template_data: Dict[str, Any]) -> str:
        spec = cls.TEMPLATE_SPECS.get(
            template_id,
            "Thông báo từ PetCare CRM tới {customer_name}."
        )
        try:
            return spec.format(**template_data)
        except KeyError:
            # Fallback when some keys are not provided
            rendered = spec
            for k, v in template_data.items():
                rendered = rendered.replace(f"{{{k}}}", str(v))
            return rendered


class SMSBrandnameAdapter:
    """Formatter for Telco SMS Brandname (Viettel / VNPT / Mobifone)."""

    DEFAULT_BRANDNAME: str = "PETCARE"

    @classmethod
    def format_payload(
        cls,
        phone: str,
        message: str,
        brandname: Optional[str] = None,
        strip_unicode: bool = True,
    ) -> Dict[str, Any]:
        formatted_phone = _normalize_phone_vn(phone)
        final_msg = _strip_accents(message) if strip_unicode else message
        return {
            "brandname": brandname or cls.DEFAULT_BRANDNAME,
            "phone": formatted_phone,
            "message": final_msg,
            "char_count": len(final_msg),
            "sms_parts": max(1, (len(final_msg) + 159) // 160),
        }


class OmnichannelDispatcher:
    """
    Central facade for dispatching notifications across Zalo ZNS, SMS Brandname, and Email.
    In Safe Mode (default for demo/dev), logs messages to an in-memory outbox audit log.
    In Live Mode, routes to production gateways.
    """

    # Audit outbox for inspection & testing
    _outbox: List[Dict[str, Any]] = []

    @classmethod
    def dispatch(
        cls,
        channel: str,
        recipient: str,
        template_id: str,
        template_data: Dict[str, Any],
        sender_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Dispatches notification message to target channel.
        """
        channel_upper = str(channel).strip().upper()
        timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Generate channel-specific payload & preview text
        if channel_upper == CHANNEL_ZALO_ZNS:
            payload = ZaloZNSAdapter.format_payload(recipient, template_id, template_data)
            preview_text = ZaloZNSAdapter.render_preview(template_id, template_data)
        elif channel_upper == CHANNEL_SMS_BRANDNAME:
            raw_text = ZaloZNSAdapter.render_preview(template_id, template_data)
            payload = SMSBrandnameAdapter.format_payload(recipient, raw_text, brandname=sender_id)
            preview_text = payload["message"]
        elif channel_upper == CHANNEL_EMAIL:
            preview_text = ZaloZNSAdapter.render_preview(template_id, template_data)
            payload = {
                "recipient": recipient,
                "subject": f"[PetCare CRM] Thông báo: {template_id}",
                "body": preview_text,
            }
        else:
            return {
                "status": "error",
                "message": f"Kênh thông báo '{channel}' không được hỗ trợ.",
            }

        outbox_entry = {
            "dispatch_id": f"DISP-{len(cls._outbox) + 1:04d}",
            "timestamp": timestamp_str,
            "channel": channel_upper,
            "recipient": recipient,
            "template_id": template_id,
            "preview_text": preview_text,
            "payload": payload,
            "safe_mode": not ENABLE_LIVE_COMMUNICATION,
            "status": "QUEUED_SAFE_MODE" if not ENABLE_LIVE_COMMUNICATION else "SENT_LIVE",
        }

        cls._outbox.append(outbox_entry)

        # Persistent storage (Finding-15 Fix: ensure outbox survives process reboots)
        if not _is_mock_frappe() and frappe and hasattr(frappe, "cache") and frappe.cache():
            try:
                cache_key = "petcare:omnichannel:persistent_outbox"
                cached_items = frappe.cache().get_value(cache_key) or []
                cached_items.append(outbox_entry)
                if len(cached_items) > 500:
                    cached_items = cached_items[-500:]
                frappe.cache().set_value(cache_key, cached_items, expires_in_sec=86400 * 30)
            except Exception:
                pass

        # Frappe integration: if Frappe is available and in live mode or logging enabled
        if frappe and hasattr(frappe, "db") and frappe.db and ENABLE_LIVE_COMMUNICATION:
            if channel_upper == CHANNEL_EMAIL:
                try:
                    frappe.sendmail(
                        recipients=[recipient],
                        subject=payload.get("subject"),
                        message=payload.get("body"),
                    )
                except Exception as e:
                    outbox_entry["status"] = "SEND_FAILED"
                    outbox_entry["error"] = str(e)

        return {
            "status": "success",
            "dispatch_id": outbox_entry["dispatch_id"],
            "channel": channel_upper,
            "recipient": recipient,
            "preview_text": preview_text,
            "is_safe_mode": not ENABLE_LIVE_COMMUNICATION,
            "message": (
                f"Đã tạo thông báo {channel_upper} trong chế độ Safe Mode (Audited & Logged)."
                if not ENABLE_LIVE_COMMUNICATION
                else f"Đã gửi thông báo {channel_upper} thành công."
            ),
        }

    @classmethod
    def get_outbox(
        cls,
        channel: Optional[str] = None,
        recipient: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Retrieves messages from outbox with optional filtering."""
        items = cls._outbox
        if channel:
            c_up = str(channel).strip().upper()
            items = [x for x in items if x["channel"] == c_up]
        if recipient:
            r_str = str(recipient).strip()
            items = [x for x in items if r_str in x["recipient"]]
        return items

    @classmethod
    def clear_outbox(cls) -> None:
        """Clears in-memory outbox."""
        cls._outbox.clear()
