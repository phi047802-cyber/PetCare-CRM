// Copyright (c) 2026, PetCare CRM Team and contributors
// For license information, please see license.txt

frappe.ui.form.on('Benefit Redemption Ledger', {
    refresh: function(frm) {
        // Giao diện kiểm toán chỉ đọc đối với các bản ghi lịch sử
        if (frm.doc.status === 'Reverted') {
            frm.set_intro(__('Bản ghi cấn trừ này đã được hoàn tác vào {0}. Lý do: {1}', [
                frm.doc.reverted_time || '',
                frm.doc.reverted_reason || ''
            ]), 'red');
        }
    }
});
