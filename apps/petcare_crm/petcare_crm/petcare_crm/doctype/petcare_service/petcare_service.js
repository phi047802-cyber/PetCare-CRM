// Copyright (c) 2026, PetCare CRM Team and contributors
// For license information, please see license.txt

frappe.ui.form.on('PetCare Service', {
    refresh: function(frm) {
        if (!frm.is_new()) {
            frm.add_custom_button(__('Mở Phiếu Dịch Vụ Với Dịch Vụ Này'), function() {
                frappe.new_doc('Service Visit', {
                    service: frm.doc.name,
                    service_type: frm.doc.service_name,
                    original_price: frm.doc.standard_price
                });
            });
        }
    }
});
