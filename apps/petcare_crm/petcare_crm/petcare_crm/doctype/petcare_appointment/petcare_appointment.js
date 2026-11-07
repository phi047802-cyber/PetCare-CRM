// Copyright (c) 2026, PetCare CRM Team and contributors
// For license information, please see license.txt

frappe.ui.form.on("PetCare Appointment", {
    refresh(frm) {
        // Lọc Thú Cưng theo Khách Hàng đã chọn
        if (frm.doc.customer) {
            frm.set_query("pet", function() {
                return {
                    filters: {
                        customer: frm.doc.customer
                    }
                };
            });
        }

        if (!frm.is_new()) {
            // Nút Check-in Tiếp đón Lễ Tân
            if (frm.doc.status === "Scheduled" || frm.doc.status === "Confirmed") {
                frm.add_custom_button(__("✅ Check-in Tiếp Đón"), function() {
                    frappe.confirm(
                        __("Tiến hành check-in lịch hẹn #{0} cho thú cưng {1} và tự động khởi tạo phiếu dịch vụ?", [frm.doc.name, frm.doc.pet]),
                        function() {
                            frappe.call({
                                method: "petcare_crm.api.check_in_appointment",
                                args: {
                                    appointment_id: frm.doc.name
                                },
                                callback: function(r) {
                                    if (!r.exc) {
                                        frappe.show_alert({
                                            message: __("Check-in thành công. Đã tạo phiếu dịch vụ: {0}", [r.message && r.message.visit_id ? r.message.visit_id : ""]),
                                            indicator: "green"
                                        });
                                        frm.reload_doc();
                                    }
                                }
                            });
                        }
                    );
                }, __("Hành Động"));
            }

            // Nút Hủy Lịch Hẹn
            if (frm.doc.status !== "Completed" && frm.doc.status !== "Cancelled") {
                frm.add_custom_button(__("❌ Hủy Lịch"), function() {
                    frappe.prompt(
                        [
                            {
                                label: __("Lý do hủy lịch"),
                                fieldname: "reason",
                                fieldtype: "Small Text",
                                reqd: 1
                            }
                        ],
                        function(values) {
                            frappe.call({
                                method: "petcare_crm.api.cancel_appointment",
                                args: {
                                    appointment_id: frm.doc.name,
                                    reason: values.reason
                                },
                                callback: function(r) {
                                    if (!r.exc) {
                                        frappe.show_alert({
                                            message: __("Đã hủy lịch hẹn thành công."),
                                            indicator: "orange"
                                        });
                                        frm.reload_doc();
                                    }
                                }
                            });
                        },
                        __("Xác Nhận Hủy Lịch Hẹn")
                    );
                }, __("Hành Động"));
            }

            // Liên kết trực tiếp tới Service Visit nếu đã check-in
            if (frm.doc.linked_service_visit) {
                frm.add_custom_button(__("📋 Xem Phiếu Dịch Vụ ({0})", [frm.doc.linked_service_visit]), function() {
                    frappe.set_route("Form", "Service Visit", frm.doc.linked_service_visit);
                });
            }
        }
    },

    customer(frm) {
        if (frm.doc.customer) {
            frm.set_query("pet", function() {
                return {
                    filters: {
                        customer: frm.doc.customer
                    }
                };
            });
            // Reset pet neu pet hien tai khong thuoc ve customer
            if (frm.doc.pet) {
                frappe.db.get_value("Pet", frm.doc.pet, "customer", function(r) {
                    if (r && r.customer !== frm.doc.customer) {
                        frm.set_value("pet", "");
                    }
                });
            }
        }
    }
});
