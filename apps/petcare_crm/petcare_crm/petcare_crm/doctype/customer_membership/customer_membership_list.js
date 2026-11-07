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
