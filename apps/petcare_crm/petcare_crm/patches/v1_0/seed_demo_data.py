"""
Seed Demo Data Toàn Diện Thuần Việt cho PetCare CRM (Prompt 10 Final).
Đáp ứng đầy đủ 10 tiêu chí dữ liệu mẫu:
1. Lead mới, Lead đang tư vấn, Lead đã chuyển đổi, Lead không tiềm năng.
2. Khách hàng có 1 thú cưng và nhiều thú cưng (Multi-pet).
3. Cơ hội bán hàng (PetCare Opportunity) ở nhiều giai đoạn (Prospecting, Proposal, Won, Lost).
4. Danh mục dịch vụ chuẩn (PetCare Service) và lịch sử thăm khám (Service Visit).
5. Gói hội viên và thẻ hội viên Active, Expired, Expiring Soon.
6. Quyền lợi hội viên khả dụng (Available) và đã dùng hết (Exhausted).
7. Thú cưng sắp đến hạn (DUE_SOON).
8. Khách hàng có nguy cơ rời bỏ (AT_RISK).
9. Đề xuất chăm sóc (Care Recommendation) ở các trạng thái New, Contacted, Converted, Dismissed.
10. Nhiệm vụ công việc (ToDo) và phản hồi dịch vụ (PetCare Case).

Cách chạy:
  bench --site petcare.localhost execute petcare_crm.patches.v1_0.seed_demo_data.execute
"""

from datetime import date, timedelta
from typing import Dict, Any
import sys

# Configure stdout and stderr for UTF-8 on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

try:
    import frappe
except ImportError:
    frappe = None


# ─────────────────────────────────────────────────────────────────────
# DEMO IDENTIFIER SCOPES (Phạm vi dữ liệu mẫu an toàn)
# ─────────────────────────────────────────────────────────────────────

DEMO_CONTACTS = [
    {
        "key": "An",
        "first_name": "Nguyễn Văn An",
        "email_id": "an.nguyen@petcare-demo.vn",
        "phone": "0901234567",
        "address": "120 Nguyễn Huệ, Bến Nghé, Quận 1, TP.HCM",
    },
    {
        "key": "Ngoc",
        "first_name": "Trần Thị Bích Ngọc",
        "email_id": "ngoc.tran@petcare-demo.vn",
        "phone": "0912345678",
        "address": "45 Xô Viết Nghệ Tĩnh, P.19, Bình Thạnh, TP.HCM",
    },
    {
        "key": "Long",
        "first_name": "Lê Hoàng Long",
        "email_id": "long.le@petcare-demo.vn",
        "phone": "0983456789",
        "address": "78 Nguyễn Thị Thập, Tân Phú, Quận 7, TP.HCM",
    },
    {
        "key": "Duc",
        "first_name": "Phạm Minh Đức",
        "email_id": "duc.pham@petcare-demo.vn",
        "phone": "0974567890",
        "address": "12 Tràng Thi, Hàng Trống, Hoàn Kiếm, Hà Nội",
    },
    {
        "key": "Thao",
        "first_name": "Đỗ Thu Thảo",
        "email_id": "thao.do@petcare-demo.vn",
        "phone": "0965678901",
        "address": "88 Phố Huế, Hàng Bài, Hai Bà Trưng, Hà Nội",
    },
    {
        "key": "Anh",
        "first_name": "Hoàng Mai Anh",
        "email_id": "anh.hoang@petcare-demo.vn",
        "phone": "0936789012",
        "address": "15 Bạch Đằng, Thạch Thang, Hải Châu, Đà Nẵng",
    },
    {
        "key": "Kiet",
        "first_name": "Vũ Tuấn Kiệt",
        "email_id": "kiet.vu@petcare-demo.vn",
        "phone": "0947890123",
        "address": "25 Đại lộ Hòa Bình, Tân An, Ninh Kiều, Cần Thơ",
    },
    {
        "key": "Linh",
        "first_name": "Đặng Phương Linh",
        "email_id": "linh.dang@petcare-demo.vn",
        "phone": "0928901234",
        "address": "104 Lạch Tray, Ngô Quyền, Hải Phòng",
    },
]

DEMO_PETS = [
    # Customer An: Multi-pet (2 Pets: Bơ & Đậu Đậu)
    {"pet_name": "Bơ", "customer_key": "An", "species": "Dog", "breed": "Corgi", "birth_date": "2024-03-15", "weight_kg": 11.5, "notes": "Thích chải lông, ăn vặt ức gà sấy."},
    {"pet_name": "Đậu Đậu", "customer_key": "An", "species": "Dog", "breed": "Shiba Inu", "birth_date": "2024-07-20", "weight_kg": 9.2, "notes": "Cún thứ 2 của anh An, hiếu động và nghịch ngợm."},
    
    # Other customers with 1 pet each
    {"pet_name": "Đậu Phộng", "customer_key": "Ngoc", "species": "Dog", "breed": "Poodle", "birth_date": "2024-09-10", "weight_kg": 4.2, "notes": "Lông xoăn tít, cần tạo kiểu Teddy tròn định kỳ."},
    {"pet_name": "Miu Miu", "customer_key": "Long", "species": "Cat", "breed": "British Shorthair", "birth_date": "2023-06-20", "weight_kg": 4.8, "notes": "Hơi nhút nhát, thích cào cằm mát-xa tai."},
    {"pet_name": "Gấu Trúc", "customer_key": "Duc", "species": "Dog", "breed": "Pomeranian (Phốc Sóc)", "birth_date": "2024-05-01", "weight_kg": 3.0, "notes": "Lông dày 2 lớp, rất lanh lợi."},
    {"pet_name": "Sữa", "customer_key": "Thao", "species": "Cat", "breed": "Persian Cat (Mèo Ba Tư)", "birth_date": "2022-11-12", "weight_kg": 5.2, "notes": "Lông xù dài, cần dưỡng ẩm mượt chống rụng."},
    {"pet_name": "Kem", "customer_key": "Anh", "species": "Dog", "breed": "Golden Retriever", "birth_date": "2023-08-25", "weight_kg": 29.5, "notes": "Cực kỳ thân thiện, thích tắm khoáng thảo dược."},
    {"pet_name": "Mít", "customer_key": "Kiet", "species": "Dog", "breed": "Pug", "birth_date": "2024-01-18", "weight_kg": 8.0, "notes": "Cần vệ sinh nếp gấp mặt và lau tai kỹ."},
    {"pet_name": "Mun", "customer_key": "Linh", "species": "Cat", "breed": "Domestic Shorthair (Mèo Mướp)", "birth_date": "2025-01-05", "weight_kg": 3.5, "notes": "Mèo cưng mới nhận nuôi, chuẩn bị tiêm vaccine."},
]

DEMO_SERVICES = [
    {"service_code": "SRV-GROOM", "service_name": "Grooming Toàn Diện", "category": "Grooming", "standard_price": 350000.0, "default_cycle_days": 30, "target_species": "All"},
    {"service_code": "SRV-SPA", "service_name": "Spa & Tắm Thảo Dược", "category": "Spa", "standard_price": 450000.0, "default_cycle_days": 21, "target_species": "All"},
    {"service_code": "SRV-VACCINE", "service_name": "Tiêm Phòng 7 Bệnh & Dại", "category": "Medical", "standard_price": 280000.0, "default_cycle_days": 365, "target_species": "All"},
    {"service_code": "SRV-CHECKUP", "service_name": "Khám Sức Khỏe Tổng Quát", "category": "Medical", "standard_price": 200000.0, "default_cycle_days": 180, "target_species": "All"},
]

DEMO_PLANS = [
    {
        "plan_name": "Gói Chăm Sóc Bạc (Silver)",
        "price": 550000.0,
        "validity_days": 90,
        "benefits": [
            {"service_type": "Grooming", "discount_type": "FREE", "quantity": 1, "discount_value": 0.0},
            {"service_type": "Spa", "discount_type": "PERCENTAGE", "quantity": 3, "discount_value": 10.0},
        ]
    },
    {
        "plan_name": "Gói Chăm Sóc Vàng (Gold)",
        "price": 890000.0,
        "validity_days": 180,
        "benefits": [
            {"service_type": "Grooming", "discount_type": "FREE", "quantity": 3, "discount_value": 0.0},
            {"service_type": "Spa", "discount_type": "PERCENTAGE", "quantity": 5, "discount_value": 20.0},
        ]
    },
    {
        "plan_name": "Gói Kim Cương VIP (Diamond VIP)",
        "price": 1490000.0,
        "validity_days": 365,
        "benefits": [
            {"service_type": "Grooming", "discount_type": "FREE", "quantity": 6, "discount_value": 0.0},
            {"service_type": "Spa", "discount_type": "FREE", "quantity": 2, "discount_value": 0.0},
            {"service_type": "Medical", "discount_type": "PERCENTAGE", "quantity": 10, "discount_value": 15.0},
        ]
    }
]


def execute():
    """Điểm khởi chạy chính từ Frappe Bench."""
    if not frappe:
        print("Lỗi: Frappe framework không khả dụng trong môi trường hiện tại.")
        return

    frappe.set_user("Administrator")
    print("=" * 70)
    print("🚀 BẮT ĐẦU KHỞI TẠO BỘ DỮ LIỆU DEMO PETCARE CRM (PROMPT 10)")
    print("=" * 70)

    # 1. Dọn dẹp dữ liệu demo cũ
    _clean_existing_demo_records()

    # 2. Tạo danh mục dịch vụ chuẩn
    _seed_services()

    # 3. Tạo danh bạ khách hàng
    contact_map = _seed_contacts()

    # 4. Tạo hồ sơ thú cưng (bao gồm khách hàng có nhiều Pet)
    _seed_pets(contact_map)

    # 5. Tạo các gói hội viên và thẻ hội viên
    _seed_membership_plans_and_memberships(contact_map)

    # 6. Tạo lịch sử dịch vụ (đáp ứng kịch bản Due Soon và At Risk)
    _seed_service_visits(contact_map)

    # 6b. Tạo Lịch hẹn demo (PetCare Appointment)
    _seed_appointments(contact_map)

    # 7. Tạo Leads và Sales Pipeline Opportunities
    _seed_leads_and_opportunities(contact_map)

    # 8. Tạo Care Recommendations và ToDo tasks
    _seed_recommendations_and_tasks(contact_map)

    # 9. Tạo Service Recovery Cases
    _seed_cases(contact_map)

    frappe.db.commit()
    print("=" * 70)
    print("✅ ĐÃ KHỞI TẠO XONG TOÀN BỘ DỮ LIỆU DEMO THÀNH CÔNG!")
    _print_summary_report()
    print("=" * 70)


def _clean_existing_demo_records():
    """Xóa an toàn các bản ghi demo cũ dựa trên nhận diện định danh."""
    print("1. Đang làm sạch dữ liệu demo cũ...")
    demo_phones = [c["phone"] for c in DEMO_CONTACTS]
    demo_emails = [c["email_id"] for c in DEMO_CONTACTS]

    # Xóa Contacts demo
    for p in demo_phones:
        frappe.db.delete("Contact", {"phone": p})
        frappe.db.delete("Contact", {"mobile_no": p})

    # Xóa Leads demo
    for p in demo_phones:
        frappe.db.delete("PetCare Lead", {"phone": p})

    # Xóa Pets demo
    pet_names = [p["pet_name"] for p in DEMO_PETS]
    for pn in pet_names:
        frappe.db.delete("Pet", {"pet_name": pn})
        frappe.db.delete("Service Visit", {"pet": pn})
        frappe.db.delete("Care Recommendation", {"pet": pn})
        if frappe.db.exists("DocType", "PetCare Appointment"):
            frappe.db.delete("PetCare Appointment", {"pet": pn})

    # Xóa Membership Plans
    plan_names = [p["plan_name"] for p in DEMO_PLANS]
    for pl in plan_names:
        frappe.db.delete("Membership Plan", {"name": pl})
        frappe.db.delete("Customer Membership", {"membership_plan": pl})

    frappe.db.commit()
    print("   ✓ Dữ liệu cũ đã được dọn sạch.")


def _seed_services():
    """Tạo bảng giá dịch vụ niêm yết chuẩn."""
    print("2. Đang tạo danh mục dịch vụ chuẩn (PetCare Service)...")
    for s in DEMO_SERVICES:
        if not frappe.db.exists("PetCare Service", s["service_code"]):
            doc = frappe.get_doc({
                "doctype": "PetCare Service",
                "service_code": s["service_code"],
                "service_name": s["service_name"],
                "category": s["category"],
                "standard_price": s["standard_price"],
                "default_cycle_days": s["default_cycle_days"],
                "target_species": s["target_species"],
                "is_active": 1,
            })
            doc.insert(ignore_permissions=True)
    print(f"   ✓ Đã tạo/đồng bộ {len(DEMO_SERVICES)} dịch vụ.")


def _seed_contacts() -> Dict[str, str]:
    """Tạo danh bạ khách hàng chuẩn."""
    print("3. Đang tạo danh bạ khách hàng (Contact)...")
    contact_map = {}
    for c in DEMO_CONTACTS:
        parts = c["first_name"].split(" ", 1)
        first_name = parts[0]
        last_name = parts[1] if len(parts) > 1 else ""

        contact = frappe.get_doc({
            "doctype": "Contact",
            "first_name": first_name,
            "last_name": last_name,
            "phone": c["phone"],
            "mobile_no": c["phone"],
            "email_id": c["email_id"],
            "address": c["address"],
            "is_primary_contact": 1,
        })
        contact.insert(ignore_permissions=True)
        contact_map[c["key"]] = contact.name

    print(f"   ✓ Đã tạo {len(contact_map)} khách hàng CRM.")
    return contact_map


def _seed_pets(contact_map: Dict[str, str]):
    """Tạo hồ sơ thú cưng (bao gồm Multi-Pet cho anh An)."""
    print("4. Đang tạo hồ sơ thú cưng (Pet)...")
    for p in DEMO_PETS:
        cust_id = contact_map.get(p["customer_key"])
        if not cust_id:
            continue

        doc = frappe.get_doc({
            "doctype": "Pet",
            "pet_name": p["pet_name"],
            "customer": cust_id,
            "species": p["species"],
            "breed": p["breed"],
            "birth_date": p["birth_date"],
            "weight_kg": p["weight_kg"],
            "notes": p["notes"],
        })
        doc.insert(ignore_permissions=True)

    print(f"   ✓ Đã tạo {len(DEMO_PETS)} hồ sơ thú cưng (Anh An sở hữu 2 bé: Bơ & Đậu Đậu).")


def _seed_membership_plans_and_memberships(contact_map: Dict[str, str]):
    """Tạo gói hội viên và cấp thẻ các trạng thái: Active, Expired, Expiring Soon, Exhausted."""
    print("5. Đang tạo gói và cấp thẻ hội viên...")
    today = date.today()

    # 1. Membership Plans
    for pl in DEMO_PLANS:
        if not frappe.db.exists("Membership Plan", pl["plan_name"]):
            plan_doc = frappe.get_doc({
                "doctype": "Membership Plan",
                "plan_name": pl["plan_name"],
                "price": pl["price"],
                "validity_days": pl["validity_days"],
                "is_active": 1,
            })
            plan_doc.insert(ignore_permissions=True)

    # 2. Cấp thẻ:
    # Thẻ 1: An (Bơ) - Gói Bạc, Active, Quyền lợi Grooming còn 1 lượt
    frappe.get_doc({
        "doctype": "Customer Membership",
        "customer": contact_map["An"],
        "membership_plan": "Gói Chăm Sóc Bạc (Silver)",
        "start_date": str(today - timedelta(days=60)),
        "end_date": str(today + timedelta(days=30)),
        "status": "Active",
        "benefits": [
            {"benefit_type": "Grooming", "discount_type": "FREE", "total_quantity": 1, "used_quantity": 0, "remaining_quantity": 1},
            {"benefit_type": "Spa", "discount_type": "PERCENTAGE", "discount_value": 10.0, "total_quantity": 3, "used_quantity": 1, "remaining_quantity": 2},
        ]
    }).insert(ignore_permissions=True)

    # Thẻ 2: Ngoc (Đậu Phộng) - Gói Vàng, Expiring Soon (còn 4 ngày nữa hết hạn)
    frappe.get_doc({
        "doctype": "Customer Membership",
        "customer": contact_map["Ngoc"],
        "membership_plan": "Gói Chăm Sóc Vàng (Gold)",
        "start_date": str(today - timedelta(days=176)),
        "end_date": str(today + timedelta(days=4)),
        "status": "Active",
        "benefits": [
            {"benefit_type": "Grooming", "discount_type": "FREE", "total_quantity": 3, "used_quantity": 2, "remaining_quantity": 1},
        ]
    }).insert(ignore_permissions=True)

    # Thẻ 3: Long (Miu Miu) - Gói Bạc, Active nhưng Quyền lợi Grooming ĐÃ DÙNG HẾT (Exhausted = 0)
    frappe.get_doc({
        "doctype": "Customer Membership",
        "customer": contact_map["Long"],
        "membership_plan": "Gói Chăm Sóc Bạc (Silver)",
        "start_date": str(today - timedelta(days=50)),
        "end_date": str(today + timedelta(days=40)),
        "status": "Active",
        "benefits": [
            {"benefit_type": "Grooming", "discount_type": "FREE", "total_quantity": 1, "used_quantity": 1, "remaining_quantity": 0},
        ]
    }).insert(ignore_permissions=True)

    # Thẻ 4: Duc (Gấu Trúc) - ĐÃ HẾT HẠN (Expired quá 20 ngày)
    frappe.get_doc({
        "doctype": "Customer Membership",
        "customer": contact_map["Duc"],
        "membership_plan": "Gói Chăm Sóc Bạc (Silver)",
        "start_date": str(today - timedelta(days=110)),
        "end_date": str(today - timedelta(days=20)),
        "status": "Expired",
        "benefits": []
    }).insert(ignore_permissions=True)

    print("   ✓ Đã tạo 3 Plans và 4 Thẻ hội viên (Active, Expiring Soon, Benefit Exhausted, Expired).")


def _seed_service_visits(contact_map: Dict[str, str]):
    """Tạo lịch sử ghé thăm thiết lập các chu kỳ: Due Soon, At Risk, Normal, Insufficient."""
    print("6. Đang tạo lịch sử dịch vụ (Service Visits)...")
    today = date.today()

    # 1. Bé Bơ: Chu kỳ 30 ngày đều đặn, lần cuối cách đây 27 ngày -> DUE_SOON sau 3 ngày!
    for d in [today - timedelta(days=87), today - timedelta(days=57), today - timedelta(days=27)]:
        frappe.get_doc({
            "doctype": "Service Visit",
            "customer": contact_map["An"],
            "pet": "Bơ",
            "service_type": "Grooming Toàn Diện",
            "visit_date": str(d),
            "original_price": 350000.0,
            "discount_amount": 0.0,
            "final_price": 350000.0,
            "notes": "Tắm sấy và cắt tỉa gọn gàng.",
        }).insert(ignore_permissions=True)

    # 2. Bé Miu Miu: Chu kỳ thông thường 25 ngày, đã vắng mặt 55 ngày -> AT_RISK (Ratio = 2.2x)!
    for d in [today - timedelta(days=105), today - timedelta(days=80), today - timedelta(days=55)]:
        frappe.get_doc({
            "doctype": "Service Visit",
            "customer": contact_map["Long"],
            "pet": "Miu Miu",
            "service_type": "Grooming Toàn Diện",
            "visit_date": str(d),
            "original_price": 350000.0,
            "discount_amount": 0.0,
            "final_price": 350000.0,
            "notes": "Chải lông khử mùi chuyên sâu.",
        }).insert(ignore_permissions=True)

    # 3. Bé Đậu Phộng: Chu kỳ 21 ngày, lần cuối cách đây 19 ngày -> DUE_SOON sau 2 ngày!
    for d in [today - timedelta(days=61), today - timedelta(days=40), today - timedelta(days=19)]:
        frappe.get_doc({
            "doctype": "Service Visit",
            "customer": contact_map["Ngoc"],
            "pet": "Đậu Phộng",
            "service_type": "Grooming Toàn Diện",
            "visit_date": str(d),
            "original_price": 350000.0,
            "discount_amount": 350000.0 if d == (today - timedelta(days=19)) else 0.0,
            "final_price": 0.0 if d == (today - timedelta(days=19)) else 350000.0,
            "notes": "Cắt mặt Teddy Poodle xinh xắn.",
        }).insert(ignore_permissions=True)

    # 4. Bé Kem: Chu kỳ 14 ngày, mới đi 4 ngày trước -> NORMAL (Không cảnh báo)
    for d in [today - timedelta(days=32), today - timedelta(days=18), today - timedelta(days=4)]:
        frappe.get_doc({
            "doctype": "Service Visit",
            "customer": contact_map["Anh"],
            "pet": "Kem",
            "service_type": "Spa & Tắm Thảo Dược",
            "visit_date": str(d),
            "original_price": 450000.0,
            "discount_amount": 0.0,
            "final_price": 450000.0,
            "notes": "Tắm khoáng thảo dược mượt lông.",
        }).insert(ignore_permissions=True)

    print("   ✓ Đã tạo 12 lượt lịch sử Service Visits hình thành chu kỳ phân tích.")



def _seed_appointments(contact_map: Dict[str, str]):
    """Tạo các lịch hẹn demo cho DocType PetCare Appointment."""
    print("6b. Đang tạo lịch hẹn (PetCare Appointment)...")
    today = date.today()
    demo_appts = [
        {"customer": contact_map["An"], "pet": "Bơ", "service_type": "Spa & Tắm Thảo Dược", "date": str(today), "time": "09:00", "branch": "CN-TRUNGTAM", "status": "Scheduled", "notes": "Khách hẹn chăm sóc định kỳ cho bé Bơ"},
        {"customer": contact_map["Ngoc"], "pet": "Đậu Phộng", "service_type": "Grooming Toàn Diện", "date": str(today), "time": "10:30", "branch": "CN-QUAN1", "status": "Scheduled", "notes": "Cắt tạo kiểu tròn Teddy"},
        {"customer": contact_map["Long"], "pet": "Miu Miu", "service_type": "Khám Sức Khỏe Tổng Quát", "date": str(today), "time": "11:15", "branch": "CN-TRUNGTAM", "status": "Scheduled", "notes": "Kiểm tra tai mắt định kỳ"},
        {"customer": contact_map["Duc"], "pet": "Gấu Trúc", "service_type": "Grooming Toàn Diện", "date": str(today), "time": "14:00", "branch": "CN-BINHTHANH", "status": "Scheduled", "notes": "Cắt tỉa lông chân và vệ sinh đệm chân"},
        {"customer": contact_map["Anh"], "pet": "Kem", "service_type": "Spa & Tắm Thảo Dược", "date": str(today), "time": "15:30", "branch": "CN-TRUNGTAM", "status": "Confirmed", "notes": "Khách đặt qua Zalo CSKH sau khi nhận cảnh báo At Risk"},
        {"customer": contact_map["Thao"], "pet": "Sữa", "service_type": "Spa & Tắm Thảo Dược", "date": str(today), "time": "16:45", "branch": "CN-QUAN1", "status": "Scheduled", "notes": "Gỡ rối lông xù và xông tinh dầu hoa cúc"},
        {"customer": contact_map["Kiet"], "pet": "Mít", "service_type": "Khám Sức Khỏe Tổng Quát", "date": str(today), "time": "17:30", "branch": "CN-TRUNGTAM", "status": "Scheduled", "notes": "Khám nếp gấp da mặt và mắt đỏ"}
    ]
    for apt in demo_appts:
        if frappe and frappe.db.exists("DocType", "PetCare Appointment"):
            frappe.get_doc({
                "doctype": "PetCare Appointment",
                "customer": apt["customer"],
                "pet": apt["pet"],
                "service_type": apt["service_type"],
                "appointment_date": apt["date"],
                "appointment_time": apt["time"],
                "branch": apt["branch"],
                "status": apt["status"],
                "notes": apt["notes"],
            }).insert(ignore_permissions=True)
    print(f"   ✓ Đã tạo {len(demo_appts)} lịch hẹn PetCare Appointment.")


def _seed_leads_and_opportunities(contact_map: Dict[str, str]):
    """Tạo Leads và Opportunities ở nhiều giai đoạn bán hàng."""
    print("7. Đang tạo Leads và Sales Opportunities...")

    # 1. PetCare Leads
    leads = [
        {"name": "Hoàng Gia Bảo", "phone": "0911223344", "email": "bao.hoang@demo.vn", "source": "Facebook Ads", "status": "New", "priority": "High", "pet_info": "Cún Husky 4 tháng cần tư vấn tiêm chủng"},
        {"name": "Trần Mai Phương", "phone": "0933445566", "email": "phuong.tran@demo.vn", "source": "Zalo", "status": "Contacted", "priority": "Medium", "pet_info": "Mèo Anh lông dài cần cắt tỉa lông bết"},
        {"name": "Nguyễn Văn An", "phone": "0901234567", "email": "an.nguyen@demo.vn", "source": "Hotline", "status": "Converted", "priority": "High", "pet_info": "Cún Corgi Bơ"},
        {"name": "Lê Quốc Huy", "phone": "0977889900", "email": "huy.le@demo.vn", "source": "Walk-in", "status": "Unqualified", "priority": "Low", "pet_info": "Đã chuyển nhà, không còn nuôi cún"},
    ]

    for ld in leads:
        frappe.get_doc({
            "doctype": "PetCare Lead",
            "lead_name": ld["name"],
            "phone": ld["phone"],
            "email": ld["email"],
            "lead_source": ld["source"],
            "status": ld["status"],
            "priority": ld["priority"],
            "initial_pet_info": ld["pet_info"],
            "unqualified_reason": "Khách không có nhu cầu" if ld["status"] == "Unqualified" else None,
            "converted_contact": contact_map["An"] if ld["status"] == "Converted" else None,
            "converted_pet": "Bơ" if ld["status"] == "Converted" else None,
        }).insert(ignore_permissions=True)

    # 2. PetCare Opportunities
    opps = [
        {"customer": contact_map["An"], "amount": 1490000.0, "stage": "Proposal", "prob": 60, "notes": "Tư vấn nâng cấp Gói Kim Cương VIP"},
        {"customer": contact_map["Ngoc"], "amount": 890000.0, "stage": "Closed Won", "prob": 100, "notes": "Khách đã đăng ký Gói Vàng"},
        {"customer": contact_map["Long"], "amount": 500000.0, "stage": "Closed Lost", "prob": 0, "notes": "Khách so sánh giá đối thủ"},
        {"customer": contact_map["Duc"], "amount": 550000.0, "stage": "Prospecting", "prob": 20, "notes": "Đang tư vấn tái kích hoạt gói dịch vụ"},
    ]

    for op in opps:
        frappe.get_doc({
            "doctype": "PetCare Opportunity",
            "customer": op["customer"],
            "opportunity_amount": op["amount"],
            "sales_stage": op["stage"],
            "probability": op["prob"],
            "notes": op["notes"],
        }).insert(ignore_permissions=True)

    print("   ✓ Đã tạo 4 Leads (New, Contacted, Converted, Unqualified) và 4 Opportunities đa giai đoạn.")


def _seed_recommendations_and_tasks(contact_map: Dict[str, str]):
    """Tạo Care Recommendations ở nhiều trạng thái và các nhiệm vụ ToDo."""
    print("8. Đang tạo Care Recommendations và Tasks...")
    today = date.today()

    recs = [
        # Due Soon (New)
        {
            "customer": contact_map["An"],
            "pet": "Bơ",
            "service_type": "Grooming Toàn Diện",
            "rec_type": "DUE_SOON",
            "status": "New",
            "priority": "High",
            "due_date": str(today + timedelta(days=3)),
            "reason": "Bé Bơ sắp đến chu kỳ tắm sấy (còn 3 ngày). Khách hàng còn 1 lượt Grooming miễn phí trong Thẻ Bạc.",
            "action": "Gọi điện nhắc lịch tắm và đặt chỗ trước cho bé.",
        },
        # At Risk (Contacted)
        {
            "customer": contact_map["Long"],
            "pet": "Miu Miu",
            "service_type": "Grooming Toàn Diện",
            "rec_type": "AT_RISK",
            "status": "Contacted",
            "priority": "Urgent",
            "due_date": str(today),
            "reason": "Miu Miu đã vắng mặt 55 ngày (chu kỳ thông thường 25 ngày, tỷ lệ vắng 2.2x).",
            "action": "Tặng voucher giảm 20% dịch vụ Spa để khuyến khích quay lại.",
        },
        # Renewal Warning (New)
        {
            "customer": contact_map["Ngoc"],
            "pet": "Đậu Phộng",
            "service_type": "Gói Hội Viên",
            "rec_type": "RENEWAL",
            "status": "New",
            "priority": "High",
            "due_date": str(today + timedelta(days=4)),
            "reason": "Gói Hội Viên Vàng của bé Đậu Phộng sẽ hết hạn sau 4 ngày.",
            "action": "Tư vấn gia hạn sớm để được rollover bảo lưu số lượt tồn.",
        },
        # Converted (Lịch sử thành công)
        {
            "customer": contact_map["Anh"],
            "pet": "Kem",
            "service_type": "Spa & Tắm Thảo Dược",
            "rec_type": "DUE_SOON",
            "status": "Converted",
            "priority": "Medium",
            "due_date": str(today - timedelta(days=5)),
            "reason": "Đã liên hệ thành công và khách hàng đã hoàn thành buổi Spa ngày hôm qua.",
            "action": "Khách đã đến làm dịch vụ.",
        },
    ]

    for r in recs:
        doc = frappe.get_doc({
            "doctype": "Care Recommendation",
            "customer": r["customer"],
            "pet": r["pet"],
            "service_type": r["service_type"],
            "recommendation_type": r["rec_type"],
            "status": r["status"],
            "priority": r["priority"],
            "due_date": r["due_date"],
            "reason": r["reason"],
            "suggested_action": r["action"],
        })
        doc.insert(ignore_permissions=True)

        # Tạo ToDo cho các đề xuất New
        if r["status"] == "New":
            frappe.get_doc({
                "doctype": "ToDo",
                "reference_type": "Care Recommendation",
                "reference_name": doc.name,
                "description": f"CSKH: {r['reason']}",
                "allocated_to": "Administrator",
                "priority": r["priority"],
                "status": "Open",
                "date": r["due_date"],
            }).insert(ignore_permissions=True)

    print("   ✓ Đã tạo 4 Care Recommendations (Due Soon, At Risk, Renewal, Converted) và ToDos tương ứng.")


def _seed_cases(contact_map: Dict[str, str]):
    """Tạo PetCare Case ghi nhận sự cố sau dịch vụ (Service Recovery)."""
    print("9. Đang tạo phản hồi & khiếu nại (PetCare Case)...")
    cases = [
        {
            "customer": contact_map["Long"],
            "pet": "Miu Miu",
            "subject": "Mèo bị hoảng nhẹ khi sấy lồng",
            "desc": "Khách phản ánh mèo Miu Miu sợ tiếng quạt sấy lồng, yêu cầu lần sau chuyển sang sấy tay nhẹ nhàng.",
            "type": "Complaint",
            "priority": "High",
            "status": "Open",
        },
        {
            "customer": contact_map["An"],
            "pet": "Bơ",
            "subject": "Tư vấn dinh dưỡng lông mượt sau tắm",
            "desc": "Khách hỏi thêm về các loại hạt dinh dưỡng bổ sung Omega 3 cho lông cún óng ả.",
            "type": "Inquiry",
            "priority": "Low",
            "status": "Resolved",
            "resolution": "Đã tư vấn viên dầu cá cá hồi hồi phục nang lông.",
        }
    ]

    for cs in cases:
        frappe.get_doc({
            "doctype": "PetCare Case",
            "customer": cs["customer"],
            "pet": cs["pet"],
            "subject": cs["subject"],
            "description": cs["desc"],
            "case_type": cs["type"],
            "priority": cs["priority"],
            "status": cs["status"],
            "resolution": cs.get("resolution"),
        }).insert(ignore_permissions=True)

    print("   ✓ Đã tạo 2 PetCare Cases (1 Open cần xử lý, 1 Resolved).")


def _print_summary_report():
    """In bảng tổng kết dữ liệu ra console."""
    print("📊 BẢNG TỔNG KẾT DỮ LIỆU SEED PETCARE CRM:")
    print(f"  • Khách hàng (Contact)           : {frappe.db.count('Contact')}")
    print(f"  • Hồ sơ Thú cưng (Pet)           : {frappe.db.count('Pet')}")
    print(f"  • Khách hàng Multi-Pet           : Nguyễn Văn An (Bơ & Đậu Đậu)")
    print(f"  • Danh mục Dịch vụ (Service)     : {frappe.db.count('PetCare Service')}")
    print(f"  • Gói Hội viên (Membership Plan) : {frappe.db.count('Membership Plan')}")
    print(f"  • Thẻ Hội viên (Customer Member) : {frappe.db.count('Customer Membership')}")
    print(f"  • Lượt Dịch vụ (Service Visit)   : {frappe.db.count('Service Visit')}")
    print(f"  • Tiềm năng (PetCare Lead)       : {frappe.db.count('PetCare Lead')}")
    print(f"  • Cơ hội (PetCare Opportunity)   : {frappe.db.count('PetCare Opportunity')}")
    print(f"  • Đề xuất CSKH (Care Rec)        : {frappe.db.count('Care Recommendation')}")
    print(f"  • Khiếu nại/Hỗ trợ (Case)        : {frappe.db.count('PetCare Case')}")
    print(f"  • Nhiệm vụ giao việc (ToDo)      : {frappe.db.count('ToDo')}")
    print("-" * 70)
    print("🎬 KỊCH BẢN DEMO SẴN SÀNG:")
    print("  Story 1 (Lead -> Sales): Lead mới 'Hoàng Gia Bảo' và Opportunity 'Gói Kim Cương'.")
    print("  Story 2 (Service & Mem): Bơ (Corgi) sử dụng Thẻ Bạc còn 1 lượt Free Grooming.")
    print("  Story 3 (Care Retention): Miu Miu (At Risk 55d), Bơ (Due Soon 3d), Đậu Phộng (Renewal 4d).")


if __name__ == "__main__":
    if frappe:
        execute()
    else:
        print("[PetCare Seed Script] Script sẵn sàng chạy qua bench execute:")
        print("  bench --site petcare.localhost execute petcare_crm.patches.v1_0.seed_demo_data.execute")
