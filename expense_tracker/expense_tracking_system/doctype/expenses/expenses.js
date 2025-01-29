// Copyright (c) 2025, Saranya and contributors
// For license information, please see license.txt

frappe.ui.form.on('Expenses', {
    /*workflow_state: function(frm) {
        console.log('Workflow state changed:', frm.doc.workflow_state);
        if (frm.doc.workflow_state === "Approved") {
            frm.set_value('status', 'Approved');
        } else if (frm.doc.workflow_state === "Rejected") {
            frm.set_value('status', 'Rejected');
        }
    },*/
    
    category: function(frm) {
        if (frm.doc.category) {
            frm.fields_dict['vendor'].get_query = function() {
                return {
                    filters: {
                        'category': frm.doc.category  
                    }
                };
            };
        }
    },
    
    vendor: function(frm) {
        if (frm.doc.vendor) {
            frappe.db.get_doc('Vendors', frm.doc.vendor).then(vendor => {
                frm.set_value('contact', vendor.contact_person || ''); 
                frm.set_value('v_email', vendor.email || ''); 
                frm.set_value('contact_num', vendor.contact_number || ''); 
            }).catch(error => {
                frappe.msgprint(__('Could not fetch vendor details.'));
            });
        }
    },

    amount: function(frm) {
        validate_expense_amount(frm);
    }
});


function validate_expense_amount(frm) {
    if (frm.doc.category) {
        frappe.db.get_doc('Categories', frm.doc.category).then(category => {
            if (frm.doc.amount > category.budget_limit) {
                frappe.msgprint(__('Expense amount exceeds the budget limit of ' + category.budget_limit));
                //frm.set_value('amount', category.budget_limit); 
            }
        }).catch(error => {
            frappe.msgprint(__('Could not fetch category details.'));
        });
    }
}


