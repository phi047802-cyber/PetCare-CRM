// Copyright (c) 2026, PetCare CRM Team and contributors
// For license information, please see license.txt

frappe.ui.form.on('PetCare Opportunity', {
    refresh: function(frm) {
        // Lọc danh sách thú cưng theo khách hàng đã chọn
        if (frm.doc.customer) {
            frm.set_query('pet', function() {
                return {
                    filters: {
                        customer: frm.doc.customer
                    }
                };
            });
        }

        // Tác vụ khi cơ hội chốt thành công (Closed Won)
        if (!frm.is_new() && frm.doc.stage === 'Closed Won') {
            frm.add_custom_button(__('Tạo Thẻ Hội Viên'), function() {
                frappe.new_doc('Customer Membership', {
                    customer: frm.doc.customer,
                    pet: frm.doc.pet || ''
                });
            }, __('Hành Động'));

            frm.add_custom_button(__('Mở Phiếu Dịch Vụ'), function() {
                frappe.new_doc('Service Visit', {
                    customer: frm.doc.customer,
                    pet: frm.doc.pet || ''
                });
            }, __('Hành Động'));
        }
    },

    customer: function(frm) {
        // Khi đổi khách hàng, reset trường pet nếu không còn khớp
        if (frm.doc.pet) {
            frappe.db.get_value('Pet', frm.doc.pet, 'customer', function(r) {
                if (r && r.customer !== frm.doc.customer) {
                    frm.set_value('pet', '');
                }
            });
        }
    },

    stage: function(frm) {
        if (frm.doc.stage === 'Closed Won') {
            frm.set_value('probability', 100);
        } else if (frm.doc.stage === 'Closed Lost') {
            frm.set_value('probability', 0);
        } else if (frm.doc.stage === 'Prospecting') {
            frm.set_value('probability', 20);
        } else if (frm.doc.stage === 'Qualification') {
            frm.set_value('probability', 40);
        } else if (frm.doc.stage === 'Proposal') {
            frm.set_value('probability', 60);
        } else if (frm.doc.stage === 'Negotiation') {
            frm.set_value('probability', 80);
        }
    }
});
