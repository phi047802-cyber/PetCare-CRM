// Copyright (c) 2026, PetCare Team and contributors
// For license information, please see license.txt

frappe.ui.form.on("Pet", {
    refresh(frm) {
        if (!frm.is_new()) {
            // Nút Tạo Phiếu Dịch Vụ
            frm.add_custom_button(__("➕ Tạo Phiếu Dịch Vụ"), function() {
                frappe.new_doc("Service Visit", {
                    customer: frm.doc.customer || "",
                    pet: frm.doc.name
                });
            }, __("Hành Động"));

            // Nút Xem Chu Kỳ Chăm Sóc (Care Pattern Analytics)
            frm.add_custom_button(__("📊 Xem Chu Kỳ Chăm Sóc"), function() {
                frappe.prompt([
                    {
                        fieldname: "service_type",
                        fieldtype: "Select",
                        label: __("Loại Dịch Vụ"),
                        options: "Grooming\nSpa\nNail Care\nVaccination",
                        default: "Grooming",
                        reqd: 1
                    }
                ], function(values) {
                    frappe.call({
                        method: "petcare_crm.api.analyze_pet_care_pattern",
                        args: {
                            pet_name: frm.doc.name,
                            service_type: values.service_type
                        },
                        callback: function(r) {
                            if (!r.exc && r.message) {
                                let m = r.message;
                                let msg = `
                                    <div style="font-size: 13px; line-height: 1.6;">
                                        <b>Thú cưng:</b> ${m.pet}<br>
                                        <b>Dịch vụ:</b> ${m.service_type}<br>
                                        <b>Số lượt sử dụng:</b> ${m.number_of_visits} lượt<br>
                                        <b>Ngày sử dụng gần nhất:</b> ${m.last_visit_date || "Chưa có"}<br>
                                        <hr style="margin: 8px 0;">
                                        <b>Chu kỳ điển hình (EWMA):</b> <span style="color: #0d9488; font-weight: bold;">${m.typical_interval ? m.typical_interval + " ngày" : "Chưa đủ dữ liệu"}</span><br>
                                        <b>Độ tin cậy:</b> <span class="badge ${m.confidence === 'HIGH' ? 'badge-success' : (m.confidence === 'MEDIUM' ? 'badge-primary' : 'badge-warning')}">${m.confidence}</span><br>
                                        <b>Ngoại lai IQR đã lọc:</b> ${m.outliers_detected && m.outliers_detected.length ? m.outliers_detected.join(", ") + " ngày" : "Không có"}<br>
                                        <div style="margin-top: 8px; padding: 8px; background: #f8fafc; border-radius: 6px; font-style: italic; color: #64748b;">
                                            ${m.reason}
                                        </div>
                                    </div>
                                `;
                                frappe.msgprint({
                                    title: __("Phân Tích Chu Kỳ Chăm Sóc"),
                                    indicator: m.insufficient_data ? "orange" : "teal",
                                    message: msg
                                });
                            }
                        }
                    });
                }, __("Chọn Dịch Vụ Phân Tích"), __("Phân Tích"));
            }, __("Hành Động"));
        }
    }
});
