// Copyright (c) 2026, PetCare CRM Team and contributors
// For license information, please see license.txt

frappe.ui.form.on('PetCare Case', {
    refresh: function(frm) {
        if (frm.doc.customer) {
            frm.set_query('pet', function() {
                return {
                    filters: {
                        customer: frm.doc.customer
                    }
                };
            });
            frm.set_query('service_visit', function() {
                return {
                    filters: {
                        customer: frm.doc.customer
                    }
                };
            });
        }

        if (!frm.is_new() && frm.doc.status === 'In Progress') {
            frm.add_custom_button(__('Hoàn Tất Xử Lý (Resolve)'), function() {
                frappe.prompt([
                    {
                        fieldname: 'resolution',
                        fieldtype: 'Text',
                        label: __('Nội dung giải quyết / Phản hồi khách'),
                        reqd: 1
                    }
                ], function(values) {
                    frm.set_value('resolution', values.resolution);
                    frm.set_value('status', 'Resolved');
                    frm.save();
                }, __('Xác Nhận Giải Quyết Case'), __('Lưu & Giải Quyết'));
            }).addClass('btn-primary');
        }
    }
});
