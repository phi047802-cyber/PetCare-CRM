// Copyright (c) 2026, PetCare CRM Team and contributors
// For license information, please see license.txt

frappe.ui.form.on('PetCare Lead', {
    refresh: function(frm) {
        // Nút chuyển đổi Lead sang Contact & Pet
        if (!frm.is_new() && frm.doc.status === 'Qualified' && !frm.doc.converted_contact) {
            frm.add_custom_button(__('Chuyển Đổi Lead'), function() {
                frappe.prompt([
                    {
                        fieldname: 'pet_name',
                        fieldtype: 'Data',
                        label: __('Tên Thú Cưng'),
                        reqd: 0,
                        default: frm.doc.initial_pet_info ? frm.doc.initial_pet_info.substring(0, 30) : ''
                    },
                    {
                        fieldname: 'species',
                        fieldtype: 'Select',
                        label: __('Loài'),
                        options: 'Dog\nCat\nRabbit\nOther',
                        default: 'Dog'
                    },
                    {
                        fieldname: 'breed',
                        fieldtype: 'Data',
                        label: __('Giống Loài')
                    },
                    {
                        fieldname: 'create_opportunity',
                        fieldtype: 'Check',
                        label: __('Tạo kèm Cơ hội bán hàng (Opportunity)'),
                        default: 0
                    },
                    {
                        depends_on: 'eval:doc.create_opportunity==1',
                        fieldname: 'expected_amount',
                        fieldtype: 'Currency',
                        label: __('Giá trị dự kiến (VNĐ)'),
                        default: 500000
                    }
                ], function(values) {
                    frappe.call({
                        method: 'petcare_crm.api.convert_lead_to_customer',
                        args: {
                            lead_id: frm.doc.name,
                            pet_name: values.pet_name,
                            species: values.species,
                            breed: values.breed,
                            create_opportunity: values.create_opportunity ? 1 : 0,
                            opportunity_amount: values.expected_amount || 0
                        },
                        freeze: true,
                        freeze_message: __('Đang chuyển đổi Lead...'),
                        callback: function(r) {
                            if (!r.exc && r.message && r.message.status === 'success') {
                                frappe.msgprint({
                                    title: __('Chuyển Đổi Thành Công'),
                                    indicator: 'green',
                                    message: __('Đã tạo Khách hàng: <b>{0}</b><br>Thú cưng: <b>{1}</b>', [
                                        r.message.contact_id,
                                        r.message.pet_id || __('(Chưa tạo)')
                                    ])
                                });
                                frm.reload_doc();
                            }
                        }
                    });
                }, __('Xác Nhận Chuyển Đổi Lead'), __('Chuyển Đổi'));
            }).addClass('btn-primary');
        }

        // Nút thêm hoạt động tương tác / cuộc gọi
        if (!frm.is_new()) {
            frm.add_custom_button(__('Ghi Nhận Cuộc Gọi / Trao Đổi'), function() {
                frappe.prompt([
                    {
                        fieldname: 'interaction_type',
                        fieldtype: 'Select',
                        label: __('Loại tương tác'),
                        options: 'Phone Call\nZalo Message\nIn-person Consultation\nEmail',
                        default: 'Phone Call',
                        reqd: 1
                    },
                    {
                        fieldname: 'notes',
                        fieldtype: 'Small Text',
                        label: __('Nội dung trao đổi'),
                        reqd: 1
                    },
                    {
                        fieldname: 'set_status_contacted',
                        fieldtype: 'Check',
                        label: __('Cập nhật trạng thái Lead sang "Contacted"'),
                        default: frm.doc.status === 'New' ? 1 : 0
                    }
                ], function(values) {
                    frappe.call({
                        method: 'petcare_crm.api.add_lead_interaction',
                        args: {
                            lead_id: frm.doc.name,
                            interaction_type: values.interaction_type,
                            notes: values.notes,
                            set_contacted: values.set_status_contacted ? 1 : 0
                        },
                        callback: function(r) {
                            if (!r.exc) {
                                frappe.show_alert({message: __('Đã lưu ghi chú tương tác'), indicator: 'green'});
                                frm.reload_doc();
                            }
                        }
                    });
                }, __('Ghi Nhận Hoạt Động Tương Tác'), __('Lưu'));
            });
        }
    }
});
