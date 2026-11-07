// Copyright (c) 2026, PetCare CRM Team and contributors
// For license information, please see license.txt

frappe.ui.form.on("Service Visit", {
    refresh(frm) {
        // Lọc Thú Cưng theo Khách Hàng
        if (frm.doc.customer) {
            frm.set_query("pet", function() {
                return {
                    filters: {
                        customer: frm.doc.customer
                    }
                };
            });

            // Lọc Thẻ Hội Viên theo Khách Hàng
            frm.set_query("membership", function() {
                return {
                    filters: {
                        customer: frm.doc.customer,
                        status: "Active"
                    }
                };
            });
        }

        // Nút mở Case khiếu nại nếu khách hàng có phản hồi sau dịch vụ
        if (!frm.is_new() && frm.doc.status === "Completed") {
            frm.add_custom_button(__("⚠️ Ghi Nhận Khiếu Nại / Case"), function() {
                frappe.new_doc("PetCare Case", {
                    customer: frm.doc.customer,
                    pet: frm.doc.pet || "",
                    service_visit: frm.doc.name,
                    subject: __("Phản ánh sau dịch vụ {0} ngày {1}", [frm.doc.service || "", frm.doc.visit_date || ""])
                });
            }, __("Hành Động"));
        }
    },

    customer(frm) {
        // Reset pet nếu không còn thuộc customer này
        if (frm.doc.pet) {
            frappe.db.get_value("Pet", frm.doc.pet, "customer", function(r) {
                if (r && r.customer !== frm.doc.customer) {
                    frm.set_value("pet", "");
                }
            });
        }
        if (frm.doc.membership) {
            frappe.db.get_value("Customer Membership", frm.doc.membership, "customer", function(r) {
                if (r && r.customer !== frm.doc.customer) {
                    frm.set_value("membership", "");
                }
            });
        }
    },

    service(frm) {
        // Tự động điền đơn giá tiêu chuẩn từ danh mục
        if (frm.doc.service) {
            frappe.db.get_value("PetCare Service", frm.doc.service, ["standard_price", "service_name"], function(r) {
                if (r) {
                    if (!frm.doc.original_price || frm.doc.original_price === 0) {
                        frm.set_value("original_price", r.standard_price || 0);
                    }
                    if (!frm.doc.service_type) {
                        frm.set_value("service_type", r.service_name || "");
                    }
                }
            });
        }
    }
});

frappe.listview_settings["Service Visit"] = {
    filters: [],

    get_indicator: function(doc) {
        if (doc.status === "Completed") {
            return [__("Completed"), "green", "status,=,Completed"];
        } else if (doc.status === "Draft") {
            return [__("Draft"), "blue", "status,=,Draft"];
        } else if (doc.status === "Cancelled") {
            return [__("Cancelled"), "grey", "status,=,Cancelled"];
        }
        return [doc.status, "orange", "status,=," + doc.status];
    }
};
