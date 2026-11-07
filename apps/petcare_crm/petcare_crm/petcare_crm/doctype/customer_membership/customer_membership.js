frappe.ui.form.on('Customer Membership', {
    refresh(frm) {
        // Nút Nạp Tiền — chỉ hiện khi membership Active
        if (frm.doc.status === 'Active') {
            frm.add_custom_button(__('💰 Nạp Tiền'), function() {
                let d = new frappe.ui.Dialog({
                    title: '💰 Nạp Tiền Hội Viên',
                    fields: [
                        {
                            fieldname: 'info_html', fieldtype: 'HTML',
                            options: `<div style="margin-bottom:10px; padding:10px; background:#f0fdfa; border-radius:8px;">
                                <b>Hội viên:</b> ${frm.doc.customer || ''}<br>
                                <b>Gói:</b> ${frm.doc.membership_plan || ''}<br>
                                <b>Số dư hiện tại:</b> ${format_currency(frm.doc.balance || 0)}
                            </div>`
                        },
                        { label: 'Số tiền nạp (VND)', fieldname: 'amount', fieldtype: 'Currency', reqd: 1 },
                        { label: 'Phương thức thanh toán', fieldname: 'payment_method', fieldtype: 'Select',
                          options: 'Cash\nBank Transfer\nMomo\nZaloPay\nCard', default: 'Cash', reqd: 1 },
                        { label: 'Mã tham chiếu', fieldname: 'reference_no', fieldtype: 'Data' },
                        { label: 'Ghi chú', fieldname: 'notes', fieldtype: 'Small Text' },
                    ],
                    primary_action_label: 'Xác nhận nạp tiền',
                    primary_action(values) {
                        frappe.call({
                            method: 'petcare_crm.api.top_up_membership',
                            args: {
                                membership_name: frm.doc.name,
                                amount: values.amount,
                                payment_method: values.payment_method,
                                reference_no: values.reference_no,
                                notes: values.notes,
                            },
                            callback(r) {
                                if (r.message && r.message.success) {
                                    frappe.msgprint({
                                        title: __('Thành công'),
                                        indicator: 'green',
                                        message: r.message.message
                                    });
                                    frm.reload_doc();
                                    d.hide();
                                }
                            }
                        });
                    }
                });
                d.show();
            }, __('Hành Động'));
        }

        // Nút Gia Hạn Hội Viên (Active hoặc Expired)
        if (!frm.is_new() && ['Active', 'Expired'].includes(frm.doc.status)) {
            frm.add_custom_button(__('🔄 Gia Hạn Hội Viên'), function() {
                frappe.prompt([
                    {
                        fieldname: 'payment_source',
                        fieldtype: 'Select',
                        label: __('Nguồn thanh toán'),
                        options: 'Wallet\nCash\nBank Transfer',
                        default: 'Wallet',
                        reqd: 1
                    },
                    {
                        fieldname: 'allow_rollover',
                        fieldtype: 'Check',
                        label: __('Kế thừa quyền lợi còn dư (Rollover)'),
                        default: 1
                    }
                ], function(values) {
                    frappe.call({
                        method: 'petcare_crm.api.renew_membership',
                        args: {
                            membership_name: frm.doc.name,
                            payment_source: values.payment_source,
                            allow_rollover: values.allow_rollover ? 1 : 0
                        },
                        freeze: true,
                        freeze_message: __('Đang xử lý gia hạn hội viên...'),
                        callback: function(r) {
                            if (!r.exc && r.message && r.message.status === 'success') {
                                frappe.msgprint({
                                    title: __('Gia Hạn Thành Công'),
                                    indicator: 'green',
                                    message: __('Đã kích hoạt thẻ mới: <b>{0}</b>', [r.message.new_membership_id])
                                });
                                frappe.set_route('Form', 'Customer Membership', r.message.new_membership_id);
                            }
                        }
                    });
                }, __('Xác Nhận Gia Hạn Thẻ'), __('Gia Hạn'));
            }, __('Hành Động'));
        }
    }
});

frappe.listview_settings['Customer Membership'] = {
    filters: [],

    get_indicator: function(doc) {
        if (doc.status === 'Active') {
            var today = frappe.datetime.get_today();
            var end_date = doc.end_date;
            var diff = frappe.datetime.get_diff(end_date, today);
            if (diff <= 7 && diff >= 0) {
                return [__('Expiring Soon'), 'orange', 'status,=,Active'];
            }
            return [__('Active'), 'green', 'status,=,Active'];
        }
        if (doc.status === 'Expired') {
            return [__('Expired'), 'red', 'status,=,Expired'];
        }
        return [__('Cancelled'), 'grey', 'status,=,Cancelled'];
    },

    onload: function(listview) {
        listview.page.add_inner_button(__('Đang Hiệu Lực'), function() {
            listview.filter_area.add([
                ['Customer Membership', 'status', '=', 'Active']
            ]);
        });
        listview.page.add_inner_button(__('Đã Hết Hạn'), function() {
            listview.filter_area.add([
                ['Customer Membership', 'status', '=', 'Expired']
            ]);
        });
    }
};
