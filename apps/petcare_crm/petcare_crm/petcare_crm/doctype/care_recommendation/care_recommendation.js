// Copyright (c) 2026, PetCare Team and contributors
// For license information, please see license.txt

frappe.ui.form.on("Care Recommendation", {
    refresh(frm) {
        if (["NEW", "ASSIGNED", "CONTACTED"].includes(frm.doc.status)) {
            if (frm.doc.status !== "CONTACTED") {
                frm.add_custom_button(__("Đã Liên Hệ"), function () {
                    frm.set_value("status", "CONTACTED");
                    frm.save();
                }, __("Trạng Thái"));
            }
            frm.add_custom_button(__("Đã Đặt Lịch / Chuyển Đổi"), function () {
                frm.set_value("status", "CONVERTED");
                frm.save();
            }, __("Trạng Thái"));
            frm.add_custom_button(__("Bỏ Qua Đề Xuất"), function () {
                frm.set_value("status", "DISMISSED");
                frm.save();
            }, __("Trạng Thái"));
        }
    },
});

frappe.listview_settings["Care Recommendation"] = {
    filters: [["status", "=", "NEW"]],

    get_indicator: function (doc) {
        const colors = {
            DUE_SOON: "blue",
            AT_RISK: "red",
            RENEWAL: "orange",
        };
        const labels = {
            DUE_SOON: "Sắp Đến Hạn",
            AT_RISK: "Nguy Cơ Rời Bỏ",
            RENEWAL: "Cần Gia Hạn",
        };
        const color = colors[doc.recommendation_type] || "grey";
        const label = labels[doc.recommendation_type] || doc.recommendation_type;
        return [__(label), color, "recommendation_type,=," + doc.recommendation_type];
    },

    onload: function (listview) {
        listview.page.add_inner_button(__("Sắp Đến Hạn"), function () {
            listview.filter_area.add([
                ["Care Recommendation", "recommendation_type", "=", "DUE_SOON"],
            ]);
        });
        listview.page.add_inner_button(__("Nguy Cơ Rời Bỏ"), function () {
            listview.filter_area.add([
                ["Care Recommendation", "recommendation_type", "=", "AT_RISK"],
            ]);
        });
        listview.page.add_inner_button(__("Cần Gia Hạn"), function () {
            listview.filter_area.add([
                ["Care Recommendation", "recommendation_type", "=", "RENEWAL"],
            ]);
        });
    },
};
