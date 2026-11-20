"""
PetCare CRM v2.0 — Dual-Stack High Performance Preview & Unified API Server
Hỗ trợ đồng thời cả IPv4 (127.0.0.1) và IPv6 (::1/localhost),
đồng bộ dữ liệu thực giữa Portal (/) và Frappe Desk (/desk).
"""
import copy
import http.server
import json
import os
import socket
import sys
import threading
import urllib.parse
import webbrowser
from datetime import date, datetime, timedelta

# Configure UTF-8 for console output
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def _today_str() -> str:
    return date.today().isoformat()


def _future_str(days: int) -> str:
    return (date.today() + timedelta(days=days)).isoformat()


def _build_initial_store() -> dict:
    store_file = os.path.join(os.path.dirname(__file__), "default_store.json")
    if os.path.exists(store_file):
        try:
            with open(store_file, "r", encoding="utf-8") as sf:
                return json.load(sf)
        except Exception:
            pass
    return {
        "customers": [
            {
                "id": "CUST-0001",
                "name": "Nguyễn Văn An",
                "phone": "0901234567",
                "email": "an.nguyen@example.com",
                "tier": "Gói Vàng VIP (Gold Care)",
                "wallet": 850000,
                "lastVisit": "2026-10-28",
                "membershipId": "MEM-AN-GOLD-2026",
                "membershipExpiry": "2027-04-01",
            },
            {
                "id": "CUST-0002",
                "name": "Trần Minh Tuấn",
                "phone": "0912345678",
                "email": "tuan.tran@example.com",
                "tier": "Gói Bạc (Silver Care)",
                "wallet": 200000,
                "lastVisit": "2026-09-24",
                "membershipId": "MEM-TUAN-SILVER",
                "membershipExpiry": "2026-12-30",
            },
            {
                "id": "CUST-0003",
                "name": "Lê Thị Lan",
                "phone": "0987654321",
                "email": "lan.le@example.com",
                "tier": "Hội viên Sắp Hết Hạn",
                "wallet": 0,
                "lastVisit": "2026-10-15",
                "membershipId": "MEM-LAN-BASIC",
                "membershipExpiry": _future_str(4),
            },
        ],
        "pets": [
            {
                "id": "PET-BO",
                "ownerId": "CUST-0001",
                "name": "Bơ",
                "kind": "dog",
                "species": "Chó Corgi Wales",
                "weight": "11.5 kg",
                "ewmaCycleDays": 14,
                "daysSinceLast": 12,
                "benefits": [
                    {"serviceId": "SVC-GROOM", "label": "Tắm & Cắt tỉa lông (Grooming)", "used": 3, "total": 4},
                    {"serviceId": "SVC-SPA", "label": "Spa Thư giãn Thảo dược", "used": 4, "total": 6},
                ],
            },
            {
                "id": "PET-DAUDAU",
                "ownerId": "CUST-0001",
                "name": "Đậu Đậu",
                "kind": "dog",
                "species": "Chó Shiba Inu",
                "weight": "9.2 kg",
                "ewmaCycleDays": 21,
                "daysSinceLast": 18,
                "benefits": [
                    {"serviceId": "SVC-NAIL", "label": "Vệ sinh Tai & Cắt Móng", "used": 2, "total": 2},
                ],
            },
            {
                "id": "PET-MIUMIU",
                "ownerId": "CUST-0002",
                "name": "Miu Miu",
                "kind": "cat",
                "species": "Mèo Anh Lông Ngắn",
                "weight": "4.1 kg",
                "ewmaCycleDays": 15,
                "daysSinceLast": 55,
                "benefits": [
                    {"serviceId": "SVC-GROOM", "label": "Grooming Mèo Chuyên Sâu", "used": 1, "total": 3},
                ],
            },
            {
                "id": "PET-DAUPHONG",
                "ownerId": "CUST-0003",
                "name": "Đậu Phộng",
                "kind": "dog",
                "species": "Chó Poodle Tiny",
                "weight": "3.8 kg",
                "ewmaCycleDays": 14,
                "daysSinceLast": 11,
                "benefits": [
                    {"serviceId": "SVC-SPA", "label": "Tắm & Dưỡng Lông", "used": 2, "total": 2},
                ],
            },
        ],
        "plans": [
            {
                "name": "PLAN-BASIC",
                "plan_name": "Gói Cơ Bản (Basic Care)",
                "price": 1200000,
                "duration_months": 3,
                "description": "Phù hợp chăm sóc định kỳ 3 tháng cho 1 thú cưng.",
                "benefits": [
                    {"serviceId": "SVC-SPA", "label": "Tắm & Spa Thảo dược", "total": 3},
                    {"serviceId": "SVC-NAIL", "label": "Vệ sinh Tai & Cắt Móng", "total": 3},
                ],
            },
            {
                "name": "PLAN-SILVER",
                "plan_name": "Gói Bạc (Silver Care)",
                "price": 2400000,
                "duration_months": 6,
                "description": "Tiết kiệm 20% chi phí Grooming và Spa trong 6 tháng.",
                "benefits": [
                    {"serviceId": "SVC-GROOM", "label": "Tắm & Cắt tỉa lông (Grooming)", "total": 4},
                    {"serviceId": "SVC-SPA", "label": "Spa Thư giãn Thảo dược", "total": 4},
                ],
            },
            {
                "name": "PLAN-GOLD",
                "plan_name": "Gói Vàng VIP (Gold Care)",
                "price": 4500000,
                "duration_months": 12,
                "description": "Chăm sóc toàn diện 12 tháng, ưu tiên đặt lịch & bảo lưu lượt.",
                "benefits": [
                    {"serviceId": "SVC-GROOM", "label": "Tắm & Cắt tỉa lông (Grooming)", "total": 8},
                    {"serviceId": "SVC-SPA", "label": "Spa Thư giãn Thảo dược", "total": 8},
                    {"serviceId": "SVC-NAIL", "label": "Vệ sinh Tai & Cắt Móng", "total": 6},
                ],
            },
        ],
        "services": [
            {"id": "SVC-GROOM", "name": "Cắt tỉa & Tạo kiểu (Grooming)", "price": 350000, "duration": "90 phút", "cycle": "14 ngày", "icon": "scissors"},
            {"id": "SVC-SPA", "name": "Tắm & Spa Thảo dược", "price": 250000, "duration": "60 phút", "cycle": "7 ngày", "icon": "bath"},
            {"id": "SVC-NAIL", "name": "Vệ sinh Tai & Cắt Móng", "price": 100000, "duration": "30 phút", "cycle": "14 ngày", "icon": "sparkles"},
            {"id": "SVC-VAC", "name": "Tiêm chủng Vaccine Định kỳ", "price": 220000, "duration": "20 phút", "cycle": "365 ngày", "icon": "syringe"},
        ],
        "visits": [
            {"id": "VIS-2026-0105", "customerId": "CUST-0001", "petName": "Bơ", "serviceName": "Cắt tỉa & Tạo kiểu (Grooming)", "date": "2026-10-28", "orig": 350000, "discount": 350000, "final": 0, "note": "Khấu trừ Gói Vàng VIP"},
            {"id": "VIS-2026-0089", "customerId": "CUST-0001", "petName": "Đậu Đậu", "serviceName": "Vệ sinh Tai & Cắt Móng", "date": "2026-10-14", "orig": 100000, "discount": 100000, "final": 0, "note": "Khấu trừ Gói Vàng VIP"},
            {"id": "VIS-2026-0054", "customerId": "CUST-0001", "petName": "Bơ", "serviceName": "Tắm & Spa Thảo dược", "date": "2026-10-01", "orig": 250000, "discount": 250000, "final": 0, "note": "Khấu trừ Gói Vàng VIP"},
            {"id": "VIS-2026-0041", "customerId": "CUST-0002", "petName": "Miu Miu", "serviceName": "Grooming Mèo Chuyên Sâu", "date": "2026-09-24", "orig": 350000, "discount": 350000, "final": 0, "note": "Khấu trừ Gói Bạc"},
        ],
        "appointments": [
            {"id": "APT-001", "customerId": "CUST-0001", "customerName": "Nguyễn Văn An", "petId": "PET-BO", "petName": "Bơ", "serviceId": "SVC-GROOM", "serviceName": "Cắt tỉa & Tạo kiểu (Grooming)", "date": _today_str(), "time": "14:30", "staff": "KTV. Hoàng Nam (Grooming)", "status": "Scheduled"},
            {"id": "APT-002", "customerId": "CUST-0002", "customerName": "Trần Minh Tuấn", "petId": "PET-MIUMIU", "petName": "Miu Miu", "serviceId": "SVC-SPA", "serviceName": "Tắm & Spa Thảo dược", "date": _today_str(), "time": "16:00", "staff": "KTV. Minh Tú (Spa)", "status": "Scheduled"},
        ],
        "telemetry": [
            {"id": "REC-01", "customerId": "CUST-0002", "customerName": "Trần Minh Tuấn", "petName": "Miu Miu", "service": "Grooming", "ewmaDays": 15, "daysElapsed": 55, "ratio": 3.67, "type": "AT_RISK", "status": "NEW", "reason": "Vượt ngưỡng 3.67x chu kỳ EWMA (55 ngày chưa tái khám)."},
            {"id": "REC-02", "customerId": "CUST-0001", "customerName": "Nguyễn Văn An", "petName": "Bơ", "service": "Grooming", "ewmaDays": 14, "daysElapsed": 12, "ratio": 0.86, "type": "DUE_SOON", "status": "NEW", "reason": "Còn 1 lượt miễn phí Gói Vàng VIP, dự kiến đến hạn sau 2 ngày."},
            {"id": "REC-03", "customerId": "CUST-0003", "customerName": "Lê Thị Lan", "petName": "Đậu Phộng", "service": "Gia hạn thẻ", "ewmaDays": 14, "daysElapsed": 11, "ratio": 0.79, "type": "DUE_SOON", "status": "CONTACTED", "reason": "Thẻ hội viên hết hạn sau 4 ngày, cần nhắc gia hạn giữ ưu đãi."},
            {"id": "REC-04", "customerId": "CUST-0001", "customerName": "Nguyễn Văn An", "petName": "Đậu Đậu", "service": "Spa Thảo dược", "ewmaDays": 21, "daysElapsed": 18, "ratio": 0.86, "type": "DUE_SOON", "status": "NEW", "reason": "Sắp đến chu kỳ Spa định kỳ (còn 3 ngày)."},
            {"id": "REC-05", "customerId": "CUST-0001", "customerName": "Nguyễn Văn An", "petName": "Bơ", "service": "Tiêm chủng", "ewmaDays": 365, "daysElapsed": 120, "ratio": 0.33, "type": "NOMINAL", "status": "CONVERTED", "reason": "Chu kỳ ổn định — Đã đặt lịch kiểm tra định kỳ."},
        ],
        "leads": [
            {"id": "LEAD-001", "name": "Hoàng Gia Bảo", "phone": "0908112233", "source": "Website Form", "status": "Mới (New)"},
            {"id": "LEAD-002", "name": "Nguyễn Thu Hà", "phone": "0919445566", "source": "Facebook Ads", "status": "Đã liên hệ"},
            {"id": "LEAD-003", "name": "Võ Minh Triết", "phone": "0983221100", "source": "WooCommerce", "status": "Đã chuyển đổi"},
            {"id": "LEAD-004", "name": "Đặng Lan Anh", "phone": "0938776655", "source": "Giới thiệu", "status": "Đang tư vấn"},
        ],
        "opportunities": [
            {"title": "Gói Kim Cương Annual — Nguyễn Văn An", "value": 18500000, "stage": "Negotiation"},
            {"title": "Gói Chăm Sóc Toàn Diện — Công ty PetHouse", "value": 14200000, "stage": "Proposal"},
            {"title": "Gia hạn Gói Bạc 12 tháng — Trần Minh Tuấn", "value": 8900000, "stage": "Qualification"},
            {"title": "Nâng cấp Gói Vàng — Lê Thị Lan", "value": 5800000, "stage": "Prospecting"},
        ],
        "cases": [
            {"id": "CASE-101", "customer": "Trần Minh Tuấn", "subject": "Hỏi lịch tiêm phòng dại cho Miu Miu", "priority": "Trung bình", "status": "Đang xử lý"},
            {"id": "CASE-102", "customer": "Nguyễn Văn An", "subject": "Yêu cầu xuất hóa đơn VAT gói VIP", "priority": "Thấp", "status": "Đã giải quyết"},
        ],
        "outbox": [
            {
                "id": "MSG-1001",
                "channel": "Email",
                "recipient": "an.nguyen@example.com",
                "subject": "[PetCare] Xác nhận quyền lợi Gói Vàng VIP — Bé Bơ",
                "body": "Kính gửi Nguyễn Văn An, bé Bơ hiện còn 1 lượt Grooming miễn phí trong Gói Vàng VIP.",
                "sent_at": f"{_today_str()} 09:15:00",
                "status": "Delivered (Sandbox)",
            },
            {
                "id": "MSG-1002",
                "channel": "Zalo ZNS",
                "recipient": "0912345678",
                "subject": "Nhắc lịch chăm sóc định kỳ cho bé Miu Miu",
                "body": "Xin chào Trần Minh Tuấn, đã 55 ngày kể từ lần Grooming gần nhất của Miu Miu.",
                "sent_at": f"{_today_str()} 10:30:00",
                "status": "Delivered (Sandbox)",
            },
        ],
        "serviceRevenueMonth": 68400000,
    }


STORE_LOCK = threading.Lock()
PREVIEW_STORE = _build_initial_store()


class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "SAMEORIGIN")
        self.send_header("Connection", "close")
        super().end_headers()

    def _send_json(self, status_code: int, data: dict):
        payload = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_HEAD(self):
        clean_path = self.path.split("?")[0].rstrip("/")
        if clean_path == "/api/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            return
        if clean_path in ("", "/", "/frontend", "/frontend.html", "/index", "/index.html"):
            self.path = "/preview.html"
        elif clean_path in ("/app/petcare-crm", "/app", "/desk", "/desk_preview.html") or clean_path.startswith("/app/"):
            self.path = "/desk_preview.html"
        return super().do_HEAD()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        clean_path = parsed.path.rstrip("/")
        query = urllib.parse.parse_qs(parsed.query)

        if clean_path == "/api/health":
            self._send_json(200, {"status": "ok", "mode": "standalone-preview", "version": "2.0.0"})
            return

        if clean_path == "/api/method/petcare_crm.api.get_portal_overview":
            with STORE_LOCK:
                self._send_json(200, {"message": copy.deepcopy(PREVIEW_STORE)})
            return

        if clean_path == "/api/method/petcare_crm.api.get_available_plans":
            with STORE_LOCK:
                self._send_json(200, {"message": copy.deepcopy(PREVIEW_STORE["plans"])})
            return

        if clean_path == "/api/method/petcare_crm.api.get_appointments":
            with STORE_LOCK:
                self._send_json(200, {"message": {"appointments": copy.deepcopy(PREVIEW_STORE["appointments"])}})
            return

        if clean_path == "/api/method/petcare_crm.api.get_omnichannel_outbox":
            channel = (query.get("channel") or [None])[0]
            with STORE_LOCK:
                outbox = PREVIEW_STORE["outbox"]
                if channel:
                    outbox = [m for m in outbox if m["channel"].lower() == channel.lower()]
                self._send_json(200, {"message": {"success": True, "outbox": copy.deepcopy(outbox)}})
            return

        if clean_path in ("", "/", "/frontend", "/frontend.html", "/index", "/index.html"):
            self.path = "/preview.html"
        elif clean_path in ("/app/petcare-crm", "/app", "/desk", "/desk_preview.html") or clean_path.startswith("/app/"):
            self.path = "/desk_preview.html"
        return super().do_GET()

    def do_POST(self):
        clean_path = self.path.split("?")[0].rstrip("/")
        content_len = int(self.headers.get("Content-Length", 0) or 0)
        raw_body = self.rfile.read(content_len) if content_len > 0 else b"{}"
        try:
            body = json.loads(raw_body.decode("utf-8"))
        except Exception:
            self._send_json(400, {"error": "Invalid JSON body"})
            return

        if not clean_path.startswith("/api/method/petcare_crm.api."):
            self._send_json(404, {"error": f"Unknown endpoint: {clean_path}"})
            return

        method = clean_path.replace("/api/method/petcare_crm.api.", "")
        with STORE_LOCK:
            res = self._handle_api_method(method, body)
        self._send_json(200, {"message": res})

    def _handle_api_method(self, method: str, body: dict) -> dict:
        global PREVIEW_STORE

        if method == "reset_demo_dataset":
            PREVIEW_STORE = _build_initial_store()
            return {"success": True, "state": copy.deepcopy(PREVIEW_STORE)}

        if method == "suggest_best_benefit":
            price = max(0.0, float(body.get("original_price", 350000) or 0))
            service_type = str(body.get("service_type", "Grooming"))
            customer_key = str(body.get("customer", "CUST-0001"))
            pet_id = body.get("pet")
            svc_id = body.get("service_id")

            cust = next(
                (c for c in PREVIEW_STORE["customers"] if c["id"] == customer_key or c["name"] == customer_key),
                None,
            )
            discount = 0.0
            best_opt = None
            if cust:
                pets = [p for p in PREVIEW_STORE["pets"] if p["ownerId"] == cust["id"]]
                if pet_id:
                    pets = [p for p in pets if p["id"] == pet_id or p["name"] == pet_id]
                for p in pets:
                    for b in p["benefits"]:
                        if (svc_id and b["serviceId"] == svc_id) or (not svc_id and service_type.lower() in b["label"].lower()):
                            if b["used"] < b["total"]:
                                discount = price
                                best_opt = {
                                    "membership": cust["membershipId"],
                                    "plan": cust["tier"],
                                    "discount_type": "FREE",
                                    "discount_amount": discount,
                                    "final_price": max(0.0, price - discount),
                                    "remaining_quantity": b["total"] - b["used"],
                                }
                                break
                    if best_opt:
                        break
            return {
                "found": best_opt is not None,
                "customer": customer_key,
                "service_type": service_type,
                "original_price": price,
                "best_option": best_opt,
            }

        if method == "top_up_membership":
            cust_id = body.get("customer")
            amount = max(0.0, float(body.get("amount", 0) or 0))
            pay_method = str(body.get("payment_method", "Chuyển khoản VietQR"))
            cust = next((c for c in PREVIEW_STORE["customers"] if c["id"] == cust_id), None)
            if not cust or amount <= 0:
                return {"success": False, "message": "Khách hàng hoặc số tiền nạp không hợp lệ."}
            cust["wallet"] += amount
            tx_id = f"TOPUP-{1000 + len(PREVIEW_STORE['visits'])}"
            PREVIEW_STORE["visits"].insert(0, {
                "id": tx_id,
                "customerId": cust["id"],
                "petName": "Ví hội viên",
                "serviceName": f"Nạp tiền vào ví ({pay_method})",
                "date": _today_str(),
                "orig": amount,
                "discount": 0,
                "final": amount,
                "note": f"Cộng số dư ví · Số dư mới: {int(cust['wallet']):,} ₫".replace(",", "."),
            })
            return {"success": True, "wallet": cust["wallet"], "transaction_id": tx_id}

        if method in ("register_membership", "renew_membership"):
            cust_id = body.get("customer")
            pet_id = body.get("pet")
            plan_name = body.get("plan_name") or body.get("new_plan_name")
            allow_rollover = bool(int(body.get("allow_rollover", 1)))

            cust = next((c for c in PREVIEW_STORE["customers"] if c["id"] == cust_id), None)
            plan = next((pl for pl in PREVIEW_STORE["plans"] if pl["name"] == plan_name or pl["plan_name"] == plan_name), None)
            if not cust or not plan:
                return {"success": False, "message": "Không tìm thấy khách hàng hoặc gói hội viên."}

            cust["tier"] = plan["plan_name"]
            cust["membershipId"] = f"MEM-{cust['id'][-4:]}-{plan['name'].replace('PLAN-', '')}"
            cust["membershipExpiry"] = _future_str(plan["duration_months"] * 30)

            target_pets = [p for p in PREVIEW_STORE["pets"] if p["ownerId"] == cust["id"] and (not pet_id or p["id"] == pet_id)]
            for p in target_pets:
                old_remaining = {}
                if allow_rollover:
                    for old_b in p["benefits"]:
                        rem = max(0, old_b["total"] - old_b["used"])
                        if rem > 0:
                            old_remaining[old_b["serviceId"]] = rem
                p["benefits"] = [
                    {
                        "serviceId": pb["serviceId"],
                        "label": pb["label"],
                        "used": 0,
                        "total": pb["total"] + old_remaining.get(pb["serviceId"], 0),
                    }
                    for pb in plan["benefits"]
                ]
            PREVIEW_STORE["serviceRevenueMonth"] += plan["price"]
            return {"success": True, "membership_id": cust["membershipId"], "expiry": cust["membershipExpiry"]}

        if method == "quick_record_visit":
            cust_id = body.get("customer")
            pet_id = body.get("pet")
            service_id = body.get("service_id")
            visit_date = body.get("visit_date") or _today_str()
            cust = next((c for c in PREVIEW_STORE["customers"] if c["id"] == cust_id), None)
            pet = next((p for p in PREVIEW_STORE["pets"] if p["id"] == pet_id), None)
            svc = next((s for s in PREVIEW_STORE["services"] if s["id"] == service_id), None)
            if not cust or not pet or not svc:
                return {"success": False, "message": "Thiếu thông tin tiếp nhận."}

            benefit = next((b for b in pet["benefits"] if b["serviceId"] == svc["id"] and b["used"] < b["total"]), None)
            discount = svc["price"] if benefit else 0
            final_price = max(0, svc["price"] - discount)
            if benefit:
                benefit["used"] += 1
            pet["daysSinceLast"] = 0
            cust["lastVisit"] = visit_date
            PREVIEW_STORE["serviceRevenueMonth"] += final_price

            new_id = f"VIS-2026-0{106 + len(PREVIEW_STORE['visits'])}"
            PREVIEW_STORE["visits"].insert(0, {
                "id": new_id,
                "customerId": cust["id"],
                "petName": pet["name"],
                "serviceName": svc["name"],
                "date": visit_date,
                "orig": svc["price"],
                "discount": discount,
                "final": final_price,
                "note": f"Khấu trừ {cust['tier']}" if benefit else "Thanh toán trực tiếp tại quầy",
            })
            for t in PREVIEW_STORE["telemetry"]:
                if t["customerId"] == cust["id"] and t["petName"] == pet["name"] and t["status"] != "CONVERTED":
                    t["status"] = "CONVERTED"
            return {"success": True, "visit_id": new_id, "final_price": final_price}

        if method == "create_appointment":
            cust_id = body.get("customer")
            pet_id = body.get("pet")
            service_id = body.get("service_id")
            cust = next((c for c in PREVIEW_STORE["customers"] if c["id"] == cust_id), None)
            pet = next((p for p in PREVIEW_STORE["pets"] if p["id"] == pet_id), None)
            svc = next((s for s in PREVIEW_STORE["services"] if s["id"] == service_id), None)
            if not cust or not pet or not svc:
                return {"success": False, "message": "Dữ liệu đặt lịch không hợp lệ."}
            apt_id = f"APT-00{len(PREVIEW_STORE['appointments']) + 1}"
            PREVIEW_STORE["appointments"].insert(0, {
                "id": apt_id,
                "customerId": cust["id"],
                "customerName": cust["name"],
                "petId": pet["id"],
                "petName": pet["name"],
                "serviceId": svc["id"],
                "serviceName": svc["name"],
                "date": body.get("appointment_date") or _today_str(),
                "time": body.get("appointment_time") or "15:00",
                "staff": body.get("assigned_staff") or "BS. Trần Quốc Bảo",
                "status": "Scheduled",
            })
            return {"success": True, "appointment_id": apt_id}

        if method == "check_in_appointment":
            apt_id = body.get("appointment_name")
            apt = next((a for a in PREVIEW_STORE["appointments"] if a["id"] == apt_id), None)
            if apt:
                apt["status"] = "Checked In"
                return {"success": True, "appointment": apt}
            return {"success": False, "message": "Không tìm thấy lịch hẹn."}

        if method == "cancel_appointment":
            apt_id = body.get("appointment_name")
            apt = next((a for a in PREVIEW_STORE["appointments"] if a["id"] == apt_id), None)
            if apt:
                apt["status"] = "Cancelled"
                return {"success": True}
            return {"success": False}

        if method in ("send_omnichannel_notification", "send_test_email"):
            channel = "Email" if method == "send_test_email" else str(body.get("channel", "Email"))
            recipient = str(body.get("recipient") or body.get("recipient_email") or "customer@example.com")
            subject = str(body.get("subject") or body.get("template_id") or "[PetCare CRM] Thông báo chăm sóc thú cưng")
            content = str(body.get("body") or body.get("message") or "Hệ thống PetCare CRM xác nhận gửi thông báo thành công.")
            msg_id = f"MSG-{1001 + len(PREVIEW_STORE['outbox'])}"
            entry = {
                "id": msg_id,
                "channel": channel,
                "recipient": recipient,
                "subject": subject,
                "body": content,
                "sent_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "status": "Delivered (Sandbox)",
            }
            PREVIEW_STORE["outbox"].insert(0, entry)
            return {"success": True, "message_id": msg_id, "entry": entry}

        if method == "update_recommendation_status":
            rec_id = body.get("recommendation_name")
            new_status = body.get("status", "CONTACTED")
            rec = next((r for r in PREVIEW_STORE["telemetry"] if r["id"] == rec_id), None)
            if rec:
                rec["status"] = new_status
                return {"success": True, "recommendation": rec}
            return {"success": False}

        if method == "create_customer_and_pet":
            name = str(body.get("name", "")).strip()
            phone = str(body.get("phone", "")).strip()
            email = str(body.get("email", "")).strip() or "khachhang@petcare.vn"
            pet_name = str(body.get("pet_name", "")).strip()
            pet_breed = str(body.get("pet_breed", "")).strip() or "Chó Poodle"
            cust_id = f"CUST-000{len(PREVIEW_STORE['customers']) + 1}"
            PREVIEW_STORE["customers"].insert(0, {
                "id": cust_id,
                "name": name,
                "phone": phone,
                "email": email,
                "tier": "Hội viên Mới (Standard)",
                "wallet": 0,
                "lastVisit": _today_str(),
                "membershipId": "MEM-NEW",
                "membershipExpiry": _future_str(30),
            })
            if pet_name:
                PREVIEW_STORE["pets"].insert(0, {
                    "id": f"PET-{len(PREVIEW_STORE['pets']) + 10}",
                    "ownerId": cust_id,
                    "name": pet_name,
                    "kind": "cat" if "mèo" in pet_breed.lower() else "dog",
                    "species": pet_breed,
                    "weight": "4.5 kg",
                    "ewmaCycleDays": 14,
                    "daysSinceLast": 0,
                    "benefits": [{"serviceId": "SVC-SPA", "label": "Tắm & Spa Chào Mừng", "used": 0, "total": 1}],
                })
            PREVIEW_STORE["leads"].insert(0, {
                "id": f"LEAD-00{len(PREVIEW_STORE['leads']) + 1}",
                "name": name,
                "phone": phone,
                "source": "Direct Desk / Portal",
                "status": "Đã chuyển đổi",
            })
            return {"success": True, "customer_id": cust_id}

        if method == "create_opportunity":
            opp = {
                "title": str(body.get("title", "Cơ hội mới")),
                "value": float(body.get("value", 0) or 0),
                "stage": str(body.get("stage", "Prospecting")),
            }
            PREVIEW_STORE["opportunities"].insert(0, opp)
            return {"success": True, "opportunity": opp}

        return {"success": False, "error": f"Unhandled method: {method}"}

    def log_message(self, format, *args):
        sys.stdout.write(f"[PetCare Server] {format % args}\n")


class DualStackThreadingServer(http.server.ThreadingHTTPServer):
    address_family = socket.AF_INET6
    allow_reuse_address = True
    daemon_threads = True

    def server_bind(self):
        try:
            self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
        except (AttributeError, OSError):
            pass
        super().server_bind()


def run():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(base_dir)

    port = 8080
    httpd = None

    for p in [8080, 8000, 5000]:
        try:
            httpd = DualStackThreadingServer(("::", p), CustomHandler)
            port = p
            break
        except Exception:
            try:
                class IPv4Server(http.server.ThreadingHTTPServer):
                    allow_reuse_address = True
                    daemon_threads = True
                httpd = IPv4Server(("0.0.0.0", p), CustomHandler)
                port = p
                break
            except Exception:
                continue

    url_local = f"http://localhost:{port}"
    url_ip = f"http://127.0.0.1:{port}"

    print("=" * 70)
    print("  PETCARE CRM v2.0 — UNIFIED PREVIEW & API SERVER READY")
    print(f"  ● Portal & POS : {url_ip}")
    print(f"  ● Frappe Desk  : {url_ip}/desk")
    print(f"  ● Localhost    : {url_local}")
    print("=" * 70)
    try:
        webbrowser.open(url_ip)
    except Exception:
        pass

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nĐã đóng máy chủ preview.")
        httpd.server_close()


if __name__ == "__main__":
    run()
