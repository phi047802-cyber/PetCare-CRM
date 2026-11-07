import frappe

def get_context(context):
    context.no_cache = 1
    context.show_sidebar = False
    context.full_width = True
    context.title = "PetCare CRM — Cổng Dịch Vụ Khách Hàng & Quầy Lễ Tân"
    context.no_breadcrumbs = True
    context.no_header = True
    context.no_footer = True
