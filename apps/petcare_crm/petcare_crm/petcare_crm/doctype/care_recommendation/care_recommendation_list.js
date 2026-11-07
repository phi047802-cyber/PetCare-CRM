frappe.listview_settings['Care Recommendation'] = {
    filters: [["status", "=", "NEW"]],

    get_indicator: function(doc) {
        const colors = {
            'DUE_SOON': 'blue',
            'AT_RISK': 'red',
            'RENEWAL': 'orange'
        };
        const labels = {
            'DUE_SOON': 'Sắp Đến Hạn',
            'AT_RISK': 'Nguy Cơ Rời Bỏ',
            'RENEWAL': 'Cần Gia Hạn'
        };
        const color = colors[doc.recommendation_type] || 'grey';
        const label = labels[doc.recommendation_type] || doc.recommendation_type;
        return [__(label), color, 'recommendation_type,=,' + doc.recommendation_type];
    },

    onload: function(listview) {
        listview.page.add_inner_button(__('Sắp Đến Hạn'), function() {
            listview.filter_area.add([
                ['Care Recommendation', 'recommendation_type', '=', 'DUE_SOON']
            ]);
        });
        listview.page.add_inner_button(__('Nguy Cơ Rời Bỏ'), function() {
            listview.filter_area.add([
                ['Care Recommendation', 'recommendation_type', '=', 'AT_RISK']
            ]);
        });
        listview.page.add_inner_button(__('Cần Gia Hạn'), function() {
            listview.filter_area.add([
                ['Care Recommendation', 'recommendation_type', '=', 'RENEWAL']
            ]);
        });
    }
};
