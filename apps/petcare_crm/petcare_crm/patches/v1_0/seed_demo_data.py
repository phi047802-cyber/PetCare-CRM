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
9. Đề xuất chăm sóc (Care Recommendation) ở các trạng thái NEW, CONTACTED, CONVERTED.
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
        "city": "TP.HCM",
    },
    {
        "key": "Ngoc",
        "first_name": "Trần Thị Bích Ngọc",
        "email_id": "ngoc.tran@petcare-demo.vn",
        "phone": "0912345678",
        "address": "45 Xô Viết Nghệ Tĩnh, P.19, Bình Thạnh, TP.HCM",
        "city": "TP.HCM",
    },
    {
        "key": "Long",
        "first_name": "Lê Hoàng Long",
        "email_id": "long.le@petcare-demo.vn",
        "phone": "0983456789",
        "address": "78 Nguyễn Thị Thập, Tân Phú, Quận 7, TP.HCM",
        "city": "TP.HCM",
    },
    {
        "key": "Duc",
        "first_name": "Phạm Minh Đức",
        "email_id": "duc.pham@petcare-demo.vn",
        "phone": "0974567890",
        "address": "12 Tràng Thi, Hàng Trống, Hoàn Kiếm, Hà Nội",
        "city": "Hà Nội",
    },
    {
        "key": "Thao",
        "first_name": "Đỗ Thu Thảo",
        "email_id": "thao.do@petcare-demo.vn",
        "phone": "0965678901",
        "address": "88 Phố Huế, Hàng Bài, Hai Bà Trưng, Hà Nội",
        "city": "Hà Nội",
    },
    {
        "key": "Anh",
        "first_name": "Hoàng Mai Anh",
        "email_id": "anh.hoang@petcare-demo.vn",
        "phone": "0936789012",
        "address": "15 Bạch Đằng, Thạch Thang, Hải Châu, Đà Nẵng",
        "city": "Đà Nẵng",
    },
    {
        "key": "Kiet",
        "first_name": "Vũ Tuấn Kiệt",
        "email_id": "kiet.vu@petcare-demo.vn",
        "phone": "0947890123",
        "address": "25 Đại lộ Hòa Bình, Tân An, Ninh Kiều, Cần Thơ",
        "city": "Cần Thơ",
    },
    {
        "key": "Linh",
        "first_name": "Đặng Phương Linh",
        "email_id": "linh.dang@petcare-demo.vn",
        "phone": "0928901234",
        "address": "104 Lạch Tray, Ngô Quyền, Hải Phòng",
        "city": "Hải Phòng",
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
    {"service_code": "SRV-GROOM", "service_name": "Grooming Toàn Diện", "category": "Grooming & Spa", "standard_price": 350000.0, "default_cycle_days": 30, "target_species": "All"},
    {"service_code": "SRV-SPA", "service_name": "Spa & Tắm Thảo Dược", "category": "Grooming & Spa", "standard_price": 450000.0, "default_cycle_days": 21, "target_species": "All"},
    {"service_code": "SRV-VACCINE", "service_name": "Tiêm Phòng 7 Bệnh & Dại", "category": "Healthcare & Clinic", "standard_price": 280000.0, "default_cycle_days": 365, "target_species": "All"},
    {"service_code": "SRV-CHECKUP", "service_name": "Khám Sức Khỏe Tổng Quát", "category": "Healthcare & Clinic", "standard_price": 200000.0, "default_cycle_days": 180, "target_species": "All"},
]

DEMO_PLANS = [
    {
        "plan_name": "Gói Chăm Sóc Bạc (Silver)",
        "price": 550000.0,
        "duration_months": 3,
        "benefits": [
            {"benefit_type": "Grooming", "discount_type": "FREE", "total_quantity": 1, "discount_value": 0.0},
            {"benefit_type": "Spa", "discount_type": "PERCENTAGE", "total_quantity": 3, "discount_value": 10.0},
        ]
    },
    {
        "plan_name": "Gói Chăm Sóc Vàng (Gold)",
        "price": 890000.0,
        "duration_months": 6,
        "benefits": [
            {"benefit_type": "Grooming", "discount_type": "FREE", "total_quantity": 3, "discount_value": 0.0},
            {"benefit_type": "Spa", "discount_type": "PERCENTAGE", "total_quantity": 5, "discount_value": 20.0},
        ]
    },
    {
        "plan_name": "Gói Kim Cương VIP (Diamond VIP)",
        "price": 1490000.0,
        "duration_months": 12,
        "benefits": [
            {"benefit_type": "Grooming", "discount_type": "FREE", "total_quantity": 6, "discount_value": 0.0},
            {"benefit_type": "Spa", "discount_type": "FREE", "total_quantity": 2, "discount_value": 0.0},
            {"benefit_type": "Vaccination", "discount_type": "PERCENTAGE", "total_quantity": 10, "discount_value": 15.0},
        ]
    }
]

DEMO_LEADS = [
    {"lead_name": "Hoàng Gia Bảo", "phone": "0911223344", "email": "bao.hoang@demo.vn", "lead_source": "Facebook Ads", "status": "New", "priority": "High", "initial_pet_info": "Cún Husky 4 tháng cần tư vấn tiêm chủng"},
    {"lead_name": "Trần Mai Phương", "phone": "0933445566", "email": "phuong.tran@demo.vn", "lead_source": "Zalo", "status": "Contacted", "priority": "Medium", "initial_pet_info": "Mèo Anh lông dài cần cắt tỉa lông bết"},
    {"lead_name": "Nguyễn Văn An", "phone": "0901234567", "email": "an.nguyen@demo.vn", "lead_source": "Hotline", "status": "Converted", "priority": "High", "initial_pet_info": "Cún Corgi Bơ"},
    {"lead_name": "Lê Quốc Huy", "phone": "0977889900", "email": "huy.le@demo.vn", "lead_source": "Walk-in", "status": "Unqualified", "priority": "Low", "initial_pet_info": "Đã chuyển nhà, không còn nuôi cún"},
]

DEMO_OPPORTUNITIES = [
    {"opportunity_title": "DEMO - Nâng cấp gói VIP cho Nguyễn Văn An", "customer_key": "An", "pet_name": "Bơ", "expected_amount": 1490000.0, "stage": "Proposal", "probability": 60, "lost_reason": None, "lost_notes": None},
    {"opportunity_title": "DEMO - Gia hạn gói Vàng cho Trần Thị Bích Ngọc", "customer_key": "Ngoc", "pet_name": "Đậu Phộng", "expected_amount": 890000.0, "stage": "Closed Won", "probability": 100, "lost_reason": None, "lost_notes": None},
    {"opportunity_title": "DEMO - Win-back khách hàng Lê Hoàng Long", "customer_key": "Long", "pet_name": "Miu Miu", "expected_amount": 500000.0, "stage": "Closed Lost", "probability": 0, "lost_reason": "Competitor", "lost_notes": "Khách đang so sánh giá với đối thủ."},
    {"opportunity_title": "DEMO - Tái kích hoạt gói Phạm Minh Đức", "customer_key": "Duc", "pet_name": "Gấu Trúc", "expected_amount": 550000.0, "stage": "Prospecting", "probability": 20, "lost_reason": None, "lost_notes": None},
]

EXPECTED_DEMO_COUNTS = {
    "Contact": 8,
    "Address": 8,
    "Pet": 9,
    "PetCare Service": 4,
    "Membership Plan": 3,
    "Customer Membership": 4,
    "Service Visit": 12,
    "PetCare Appointment": 7,
    "PetCare Lead": 4,
    "PetCare Opportunity": 4,
    "Care Recommendation": 4,
    "PetCare Case": 2,
    "ToDo": 2,
}


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
    pet_map = _seed_pets(contact_map)

    # 5. Tạo các gói hội viên và thẻ hội viên
    membership_map = _seed_membership_plans_and_memberships(contact_map, pet_map)

    # 6. Tạo lịch sử dịch vụ (đáp ứng kịch bản Due Soon và At Risk)
    _seed_service_visits(contact_map, pet_map)

    # 6b. Tạo Lịch hẹn demo (PetCare Appointment)
    _seed_appointments(contact_map, pet_map)

    # 7. Tạo Leads và Sales Pipeline Opportunities
    _seed_leads_and_opportunities(contact_map, pet_map)

    # 8. Tạo Care Recommendations và ToDo tasks
    _seed_recommendations_and_tasks(contact_map, pet_map, membership_map)

    # 9. Tạo Service Recovery Cases
    _seed_cases(contact_map, pet_map)

    from petcare_crm.patches.v1_0.validate_demo_data import validate

    validation = validate(raise_on_error=True, print_report=False)
    frappe.db.commit()
    print("=" * 70)
    print("✅ ĐÃ KHỞI TẠO XONG TOÀN BỘ DỮ LIỆU DEMO THÀNH CÔNG!")
    _print_summary_report(validation)
    print("=" * 70)
    return validation


def _clean_existing_demo_records():
    """Xóa dữ liệu demo theo quan hệ phụ thuộc để script chạy lại không nhân đôi."""
    print("1. Đang làm sạch dữ liệu demo cũ...")
    contact_names = []
    for contact in DEMO_CONTACTS:
        for field in ("mobile_no", "phone", "email_id"):
            contact_names.extend(_get_names("Contact", {field: contact[field if field != "mobile_no" else "phone"]}))
    contact_names = sorted(set(contact_names))

    pet_names = _get_names(
        "Pet",
        {"customer": ["in", contact_names], "pet_name": ["in", [p["pet_name"] for p in DEMO_PETS]]},
    ) if contact_names else []

    recommendation_names = _get_names(
        "Care Recommendation", {"customer": ["in", contact_names]}
    ) if contact_names else []
    membership_names = _get_names(
        "Customer Membership", {"customer": ["in", contact_names]}
    ) if contact_names else []

    cleanup_plan = [
        ("ToDo", {"reference_type": "Care Recommendation", "reference_name": ["in", recommendation_names]} if recommendation_names else None),
        ("Benefit Redemption Ledger", {"membership": ["in", membership_names]} if membership_names else None),
        ("Membership Transaction", {"membership": ["in", membership_names]} if membership_names else None),
        ("WooCommerce Order Sync", {"contact": ["in", contact_names]} if contact_names else None),
        ("Care Recommendation", {"name": ["in", recommendation_names]} if recommendation_names else None),
        ("PetCare Case", {"customer": ["in", contact_names]} if contact_names else None),
        ("PetCare Appointment", {"customer": ["in", contact_names]} if contact_names else None),
        ("Service Visit", {"customer": ["in", contact_names]} if contact_names else None),
        ("PetCare Opportunity", {"customer": ["in", contact_names]} if contact_names else None),
        ("PetCare Opportunity", {"opportunity_title": ["like", "DEMO - %"]}),
        ("Customer Membership", {"name": ["in", membership_names]} if membership_names else None),
        ("PetCare Lead", {"phone": ["in", [lead["phone"] for lead in DEMO_LEADS]]}),
        ("Pet", {"name": ["in", pet_names]} if pet_names else None),
        ("Address", {"address_title": ["in", [f"DEMO - {contact['first_name']}" for contact in DEMO_CONTACTS]]}),
        ("Contact", {"name": ["in", contact_names]} if contact_names else None),
    ]

    for doctype, filters in cleanup_plan:
        if filters:
            _delete_documents(doctype, filters)

    print("   ✓ Dữ liệu cũ đã được dọn sạch.")


def _get_names(doctype: str, filters: Dict[str, Any]):
    """Lấy danh sách name nếu DocType tồn tại; dùng được cho cả Frappe v14/v15."""
    if not frappe.db.exists("DocType", doctype):
        return []
    rows = frappe.get_all(doctype, filters=filters, fields=["name"])
    return [row.name if hasattr(row, "name") else row["name"] for row in rows]


def _delete_documents(doctype: str, filters: Dict[str, Any]):
    """Xóa qua Document API để child rows và metadata liên quan không bị mồ côi."""
    for name in _get_names(doctype, filters):
        frappe.delete_doc(doctype, name, force=1, ignore_permissions=True)


def _seed_services():
    """Tạo bảng giá dịch vụ niêm yết chuẩn."""
    print("2. Đang tạo danh mục dịch vụ chuẩn (PetCare Service)...")
    for s in DEMO_SERVICES:
        if frappe.db.exists("PetCare Service", s["service_code"]):
            doc = frappe.get_doc("PetCare Service", s["service_code"])
            doc.update(s)
            doc.is_active = 1
            doc.save(ignore_permissions=True)
        else:
            doc = frappe.get_doc({
                "doctype": "PetCare Service",
                **s,
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
            "phone_nos": [{
                "phone": c["phone"],
                "is_primary_phone": 1,
                "is_primary_mobile_no": 1,
            }],
            "email_ids": [{"email_id": c["email_id"], "is_primary": 1}],
            "is_primary_contact": 1,
        })
        contact.insert(ignore_permissions=True)
        contact_map[c["key"]] = contact.name

        frappe.get_doc({
            "doctype": "Address",
            "address_title": f"DEMO - {c['first_name']}",
            "address_type": "Personal",
            "address_line1": c["address"],
            "city": c["city"],
            "country": "Vietnam",
            "is_primary_address": 1,
            "links": [{"link_doctype": "Contact", "link_name": contact.name}],
        }).insert(ignore_permissions=True)

    print(f"   ✓ Đã tạo {len(contact_map)} khách hàng CRM.")
    return contact_map


def _seed_pets(contact_map: Dict[str, str]) -> Dict[str, str]:
    """Tạo hồ sơ thú cưng (bao gồm Multi-Pet cho anh An)."""
    print("4. Đang tạo hồ sơ thú cưng (Pet)...")
    pet_map = {}
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
        pet_map[p["pet_name"]] = doc.name

    print(f"   ✓ Đã tạo {len(DEMO_PETS)} hồ sơ thú cưng (Anh An sở hữu 2 bé: Bơ & Đậu Đậu).")
    return pet_map


def _seed_membership_plans_and_memberships(contact_map: Dict[str, str], pet_map: Dict[str, str]) -> Dict[str, str]:
    """Tạo gói hội viên và cấp thẻ các trạng thái: Active, Expired, Expiring Soon, Exhausted."""
    print("5. Đang tạo gói và cấp thẻ hội viên...")
    today = date.today()

    # 1. Membership Plans
    for pl in DEMO_PLANS:
        if frappe.db.exists("Membership Plan", pl["plan_name"]):
            plan_doc = frappe.get_doc("Membership Plan", pl["plan_name"])
            plan_doc.price = pl["price"]
            plan_doc.duration_months = pl["duration_months"]
            plan_doc.description = "Gói demo chuẩn hóa cho đồ án PetCare CRM."
            plan_doc.set("benefits", [])
            for benefit in pl["benefits"]:
                plan_doc.append("benefits", benefit)
            plan_doc.save(ignore_permissions=True)
        else:
            plan_doc = frappe.get_doc({
                "doctype": "Membership Plan",
                "plan_name": pl["plan_name"],
                "price": pl["price"],
                "duration_months": pl["duration_months"],
                "description": "Gói demo chuẩn hóa cho đồ án PetCare CRM.",
                "benefits": pl["benefits"],
            })
            plan_doc.insert(ignore_permissions=True)

    # 2. Cấp thẻ:
    membership_map = {}
    # Thẻ 1: An (Bơ) - Gói Bạc, Active, Quyền lợi Grooming còn 1 lượt
    membership = frappe.get_doc({
        "doctype": "Customer Membership",
        "customer": contact_map["An"],
        "pet": pet_map["Bơ"],
        "membership_plan": "Gói Chăm Sóc Bạc (Silver)",
        "start_date": str(today - timedelta(days=60)),
        "end_date": str(today + timedelta(days=30)),
        "status": "Active",
        "benefits": [
            {"benefit_type": "Grooming", "discount_type": "FREE", "total_quantity": 1, "used_quantity": 0, "remaining_quantity": 1},
            {"benefit_type": "Spa", "discount_type": "PERCENTAGE", "discount_value": 10.0, "total_quantity": 3, "used_quantity": 1, "remaining_quantity": 2},
        ]
    })
    membership.insert(ignore_permissions=True)
    membership_map["An"] = membership.name

    # Thẻ 2: Ngoc (Đậu Phộng) - Gói Vàng, Expiring Soon (còn 4 ngày nữa hết hạn)
    membership = frappe.get_doc({
        "doctype": "Customer Membership",
        "customer": contact_map["Ngoc"],
        "pet": pet_map["Đậu Phộng"],
        "membership_plan": "Gói Chăm Sóc Vàng (Gold)",
        "start_date": str(today - timedelta(days=176)),
        "end_date": str(today + timedelta(days=4)),
        "status": "Active",
        "benefits": [
            {"benefit_type": "Grooming", "discount_type": "FREE", "total_quantity": 3, "used_quantity": 2, "remaining_quantity": 1},
        ]
    })
    membership.insert(ignore_permissions=True)
    membership_map["Ngoc"] = membership.name

    # Thẻ 3: Long (Miu Miu) - Gói Bạc, Active nhưng Quyền lợi Grooming ĐÃ DÙNG HẾT (Exhausted = 0)
    membership = frappe.get_doc({
        "doctype": "Customer Membership",
        "customer": contact_map["Long"],
        "pet": pet_map["Miu Miu"],
        "membership_plan": "Gói Chăm Sóc Bạc (Silver)",
        "start_date": str(today - timedelta(days=50)),
        "end_date": str(today + timedelta(days=40)),
        "status": "Active",
        "benefits": [
            {"benefit_type": "Grooming", "discount_type": "FREE", "total_quantity": 1, "used_quantity": 1, "remaining_quantity": 0},
        ]
    })
    membership.insert(ignore_permissions=True)
    membership_map["Long"] = membership.name

    # Thẻ 4: Duc (Gấu Trúc) - ĐÃ HẾT HẠN (Expired quá 20 ngày)
    membership = frappe.get_doc({
        "doctype": "Customer Membership",
        "customer": contact_map["Duc"],
        "pet": pet_map["Gấu Trúc"],
        "membership_plan": "Gói Chăm Sóc Bạc (Silver)",
        "start_date": str(today - timedelta(days=110)),
        "end_date": str(today - timedelta(days=20)),
        "status": "Expired",
        "benefits": []
    })
    membership.insert(ignore_permissions=True)
    membership_map["Duc"] = membership.name

    print("   ✓ Đã tạo 3 Plans và 4 Thẻ hội viên (Active, Expiring Soon, Benefit Exhausted, Expired).")
    return membership_map


def _seed_service_visits(contact_map: Dict[str, str], pet_map: Dict[str, str]):
    """Tạo lịch sử ghé thăm thiết lập các chu kỳ: Due Soon, At Risk, Normal, Insufficient."""
    print("6. Đang tạo lịch sử dịch vụ (Service Visits)...")
    today = date.today()

    # 1. Bé Bơ: Chu kỳ 30 ngày đều đặn, lần cuối cách đây 27 ngày -> DUE_SOON sau 3 ngày!
    for d in [today - timedelta(days=87), today - timedelta(days=57), today - timedelta(days=27)]:
        frappe.get_doc({
            "doctype": "Service Visit",
            "customer": contact_map["An"],
            "pet": pet_map["Bơ"],
            "service": "SRV-GROOM",
            "service_type": "Grooming Toàn Diện",
            "visit_date": str(d),
            "original_price": 350000.0,
            "discount_amount": 0.0,
            "final_price": 350000.0,
            "status": "Completed",
            "branch": "CN-TRUNGTAM",
            "notes": "Tắm sấy và cắt tỉa gọn gàng.",
        }).insert(ignore_permissions=True)

    # 2. Bé Miu Miu: Chu kỳ thông thường 25 ngày, đã vắng mặt 55 ngày -> AT_RISK (Ratio = 2.2x)!
    for d in [today - timedelta(days=105), today - timedelta(days=80), today - timedelta(days=55)]:
        frappe.get_doc({
            "doctype": "Service Visit",
            "customer": contact_map["Long"],
            "pet": pet_map["Miu Miu"],
            "service": "SRV-GROOM",
            "service_type": "Grooming Toàn Diện",
            "visit_date": str(d),
            "original_price": 350000.0,
            "discount_amount": 0.0,
            "final_price": 350000.0,
            "status": "Completed",
            "branch": "CN-TRUNGTAM",
            "notes": "Chải lông khử mùi chuyên sâu.",
        }).insert(ignore_permissions=True)

    # 3. Bé Đậu Phộng: Chu kỳ 21 ngày, lần cuối cách đây 19 ngày -> DUE_SOON sau 2 ngày!
    for d in [today - timedelta(days=61), today - timedelta(days=40), today - timedelta(days=19)]:
        frappe.get_doc({
            "doctype": "Service Visit",
            "customer": contact_map["Ngoc"],
            "pet": pet_map["Đậu Phộng"],
            "service": "SRV-GROOM",
            "service_type": "Grooming Toàn Diện",
            "visit_date": str(d),
            "original_price": 350000.0,
            "discount_amount": 350000.0 if d == (today - timedelta(days=19)) else 0.0,
            "final_price": 0.0 if d == (today - timedelta(days=19)) else 350000.0,
            "status": "Completed",
            "branch": "CN-QUAN1",
            "notes": "Cắt mặt Teddy Poodle xinh xắn.",
        }).insert(ignore_permissions=True)

    # 4. Bé Kem: Chu kỳ 14 ngày, mới đi 4 ngày trước -> NORMAL (Không cảnh báo)
    for d in [today - timedelta(days=32), today - timedelta(days=18), today - timedelta(days=4)]:
        frappe.get_doc({
            "doctype": "Service Visit",
            "customer": contact_map["Anh"],
            "pet": pet_map["Kem"],
            "service": "SRV-SPA",
            "service_type": "Spa & Tắm Thảo Dược",
            "visit_date": str(d),
            "original_price": 450000.0,
            "discount_amount": 0.0,
            "final_price": 450000.0,
            "status": "Completed",
            "branch": "CN-TRUNGTAM",
            "notes": "Tắm khoáng thảo dược mượt lông.",
        }).insert(ignore_permissions=True)

    print("   ✓ Đã tạo 12 lượt lịch sử Service Visits hình thành chu kỳ phân tích.")



def _seed_appointments(contact_map: Dict[str, str], pet_map: Dict[str, str]):
    """Tạo các lịch hẹn demo cho DocType PetCare Appointment."""
    print("6b. Đang tạo lịch hẹn (PetCare Appointment)...")
    today = date.today()
    demo_appts = [
        {"customer": contact_map["An"], "pet": pet_map["Bơ"], "service_type": "Spa", "service": "SRV-SPA", "date": str(today), "time": "09:00", "branch": "CN-TRUNGTAM", "status": "Scheduled", "notes": "Khách hẹn chăm sóc định kỳ cho bé Bơ"},
        {"customer": contact_map["Ngoc"], "pet": pet_map["Đậu Phộng"], "service_type": "Grooming", "service": "SRV-GROOM", "date": str(today), "time": "10:30", "branch": "CN-QUAN1", "status": "Scheduled", "notes": "Cắt tạo kiểu tròn Teddy"},
        {"customer": contact_map["Long"], "pet": pet_map["Miu Miu"], "service_type": "General Health Check", "service": "SRV-CHECKUP", "date": str(today), "time": "11:15", "branch": "CN-TRUNGTAM", "status": "Scheduled", "notes": "Kiểm tra tai mắt định kỳ"},
        {"customer": contact_map["Duc"], "pet": pet_map["Gấu Trúc"], "service_type": "Grooming", "service": "SRV-GROOM", "date": str(today), "time": "14:00", "branch": "CN-BINHTHANH", "status": "Scheduled", "notes": "Cắt tỉa lông chân và vệ sinh đệm chân"},
        {"customer": contact_map["Anh"], "pet": pet_map["Kem"], "service_type": "Spa", "service": "SRV-SPA", "date": str(today), "time": "15:30", "branch": "CN-TRUNGTAM", "status": "Confirmed", "notes": "Khách đặt qua Zalo CSKH sau khi nhận cảnh báo At Risk"},
        {"customer": contact_map["Thao"], "pet": pet_map["Sữa"], "service_type": "Spa", "service": "SRV-SPA", "date": str(today), "time": "16:45", "branch": "CN-QUAN1", "status": "Scheduled", "notes": "Gỡ rối lông xù và xông tinh dầu hoa cúc"},
        {"customer": contact_map["Kiet"], "pet": pet_map["Mít"], "service_type": "General Health Check", "service": "SRV-CHECKUP", "date": str(today), "time": "17:30", "branch": "CN-TRUNGTAM", "status": "Scheduled", "notes": "Khám nếp gấp da mặt và mắt đỏ"}
    ]
    for apt in demo_appts:
        if frappe and frappe.db.exists("DocType", "PetCare Appointment"):
            frappe.get_doc({
                "doctype": "PetCare Appointment",
                "customer": apt["customer"],
                "pet": apt["pet"],
                "service_type": apt["service_type"],
                "service": apt["service"],
                "appointment_date": apt["date"],
                "appointment_time": apt["time"],
                "branch": apt["branch"],
                "status": apt["status"],
                "notes": apt["notes"],
            }).insert(ignore_permissions=True)
    print(f"   ✓ Đã tạo {len(demo_appts)} lịch hẹn PetCare Appointment.")


def _seed_leads_and_opportunities(contact_map: Dict[str, str], pet_map: Dict[str, str]):
    """Tạo Leads và Opportunities ở nhiều giai đoạn bán hàng."""
    print("7. Đang tạo Leads và Sales Opportunities...")

    # 1. PetCare Leads
    for ld in DEMO_LEADS:
        frappe.get_doc({
            "doctype": "PetCare Lead",
            "lead_name": ld["lead_name"],
            "phone": ld["phone"],
            "email": ld["email"],
            "lead_source": ld["lead_source"],
            "status": ld["status"],
            "priority": ld["priority"],
            "initial_pet_info": ld["initial_pet_info"],
            "unqualified_reason": "Khách không có nhu cầu" if ld["status"] == "Unqualified" else None,
            "converted_contact": contact_map["An"] if ld["status"] == "Converted" else None,
            "converted_pet": pet_map["Bơ"] if ld["status"] == "Converted" else None,
        }).insert(ignore_permissions=True)

    # 2. PetCare Opportunities
    for op in DEMO_OPPORTUNITIES:
        frappe.get_doc({
            "doctype": "PetCare Opportunity",
            "opportunity_title": op["opportunity_title"],
            "customer": contact_map[op["customer_key"]],
            "pet": pet_map[op["pet_name"]],
            "expected_amount": op["expected_amount"],
            "stage": op["stage"],
            "probability": op["probability"],
            "lost_reason": op["lost_reason"],
            "lost_notes": op["lost_notes"],
        }).insert(ignore_permissions=True)

    print("   ✓ Đã tạo 4 Leads (New, Contacted, Converted, Unqualified) và 4 Opportunities đa giai đoạn.")


def _seed_recommendations_and_tasks(
    contact_map: Dict[str, str],
    pet_map: Dict[str, str],
    membership_map: Dict[str, str],
):
    """Tạo Care Recommendations ở nhiều trạng thái và các nhiệm vụ ToDo."""
    print("8. Đang tạo Care Recommendations và Tasks...")
    today = date.today()

    recs = [
        # Due Soon (New)
        {
            "customer_key": "An",
            "pet_name": "Bơ",
            "service_type": "Grooming",
            "rec_type": "DUE_SOON",
            "status": "NEW",
            "priority": "High",
            "recommendation_date": str(today),
            "task_date": str(today + timedelta(days=3)),
            "reason": "Bé Bơ sắp đến chu kỳ tắm sấy (còn 3 ngày). Khách hàng còn 1 lượt Grooming miễn phí trong Thẻ Bạc.",
            "action": "Gọi điện nhắc lịch tắm và đặt chỗ trước cho bé.",
            "membership_key": "An",
        },
        # At Risk (Contacted)
        {
            "customer_key": "Long",
            "pet_name": "Miu Miu",
            "service_type": "Grooming",
            "rec_type": "AT_RISK",
            "status": "CONTACTED",
            "priority": "High",
            "recommendation_date": str(today),
            "task_date": str(today),
            "reason": "Miu Miu đã vắng mặt 55 ngày (chu kỳ thông thường 25 ngày, tỷ lệ vắng 2.2x).",
            "action": "Tặng voucher giảm 20% dịch vụ Spa để khuyến khích quay lại.",
            "membership_key": "Long",
        },
        # Renewal Warning (New)
        {
            "customer_key": "Ngoc",
            "pet_name": "Đậu Phộng",
            "service_type": "Membership Renewal",
            "rec_type": "RENEWAL",
            "status": "NEW",
            "priority": "High",
            "recommendation_date": str(today),
            "task_date": str(today + timedelta(days=4)),
            "reason": "Gói Hội Viên Vàng của bé Đậu Phộng sẽ hết hạn sau 4 ngày.",
            "action": "Tư vấn gia hạn sớm để được rollover bảo lưu số lượt tồn.",
            "membership_key": "Ngoc",
        },
        # Converted (Lịch sử thành công)
        {
            "customer_key": "Anh",
            "pet_name": "Kem",
            "service_type": "Spa",
            "rec_type": "DUE_SOON",
            "status": "CONVERTED",
            "priority": "Medium",
            "recommendation_date": str(today - timedelta(days=5)),
            "task_date": str(today - timedelta(days=5)),
            "reason": "Đã liên hệ thành công và khách hàng đã hoàn thành buổi Spa ngày hôm qua.",
            "action": "Khách đã đến làm dịch vụ.",
            "membership_key": None,
        },
    ]

    for r in recs:
        doc = frappe.get_doc({
            "doctype": "Care Recommendation",
            "customer": contact_map[r["customer_key"]],
            "pet": pet_map[r["pet_name"]],
            "service_type": r["service_type"],
            "recommendation_type": r["rec_type"],
            "recommendation_date": r["recommendation_date"],
            "status": r["status"],
            "priority": r["priority"],
            "reason": r["reason"],
            "suggested_action": r["action"],
            "membership": membership_map.get(r["membership_key"]) if r["membership_key"] else None,
        })
        doc.insert(ignore_permissions=True)

        # Tạo ToDo cho các đề xuất New
        if r["status"] == "NEW":
            frappe.get_doc({
                "doctype": "ToDo",
                "reference_type": "Care Recommendation",
                "reference_name": doc.name,
                "description": f"CSKH: {r['reason']}",
                "allocated_to": "Administrator",
                "priority": r["priority"],
                "status": "Open",
                "date": r["task_date"],
            }).insert(ignore_permissions=True)

    print("   ✓ Đã tạo 4 Care Recommendations (Due Soon, At Risk, Renewal, Converted) và ToDos tương ứng.")


def _seed_cases(contact_map: Dict[str, str], pet_map: Dict[str, str]):
    """Tạo PetCare Case ghi nhận sự cố sau dịch vụ (Service Recovery)."""
    print("9. Đang tạo phản hồi & khiếu nại (PetCare Case)...")
    cases = [
        {
            "customer": contact_map["Long"],
            "pet": pet_map["Miu Miu"],
            "subject": "Mèo bị hoảng nhẹ khi sấy lồng",
            "desc": "Khách phản ánh mèo Miu Miu sợ tiếng quạt sấy lồng, yêu cầu lần sau chuyển sang sấy tay nhẹ nhàng.",
            "type": "Complaint",
            "priority": "High",
            "status": "New",
        },
        {
            "customer": contact_map["An"],
            "pet": pet_map["Bơ"],
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

    print("   ✓ Đã tạo 2 PetCare Cases (1 New cần xử lý, 1 Resolved).")


def _print_summary_report(validation: Dict[str, Any]):
    """In bảng tổng kết dữ liệu ra console."""
    print("📊 BẢNG TỔNG KẾT DỮ LIỆU SEED PETCARE CRM:")
    observed = validation["observed_counts"]
    print(f"  • Khách hàng (Contact)           : {observed['Contact']}")
    print(f"  • Địa chỉ liên kết (Address)     : {observed['Address']}")
    print(f"  • Hồ sơ Thú cưng (Pet)           : {observed['Pet']}")
    print(f"  • Khách hàng Multi-Pet           : Nguyễn Văn An (Bơ & Đậu Đậu)")
    print(f"  • Danh mục Dịch vụ (Service)     : {observed['PetCare Service']}")
    print(f"  • Gói Hội viên (Membership Plan) : {observed['Membership Plan']}")
    print(f"  • Thẻ Hội viên (Customer Member) : {observed['Customer Membership']}")
    print(f"  • Lượt Dịch vụ (Service Visit)   : {observed['Service Visit']}")
    print(f"  • Lịch hẹn (Appointment)         : {observed['PetCare Appointment']}")
    print(f"  • Tiềm năng (PetCare Lead)       : {observed['PetCare Lead']}")
    print(f"  • Cơ hội (PetCare Opportunity)   : {observed['PetCare Opportunity']}")
    print(f"  • Đề xuất CSKH (Care Rec)        : {observed['Care Recommendation']}")
    print(f"  • Khiếu nại/Hỗ trợ (Case)        : {observed['PetCare Case']}")
    print(f"  • Nhiệm vụ giao việc (ToDo)      : {observed['ToDo']}")
    print(f"  • Kết quả kiểm tra dataset       : {validation['status']}")
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
