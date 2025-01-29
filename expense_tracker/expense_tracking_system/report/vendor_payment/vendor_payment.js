// Copyright (c) 2025, Saranya and contributors
// For license information, please see license.txt

frappe.query_reports["Vendor Payment"] = {
    "filters": [
        {
            "fieldname": "year",
            "label": __("Year"),
            "fieldtype": "Select",
            "options": [" ", "2023", "2024", "2025"],  
            "default": new Date().getFullYear(),  
        },
        {
            "fieldname": "month",
            "label": __("Month"),
            "fieldtype": "Select",
			//"options": "\n".join([calendar.month_abbr[i] for i in range(1, 13)]),  
            "options": [" ", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],  
            "default": new Date().getMonth() + 1,  
        },
		{
            "fieldname": "vendor",
            "label": __("Vendor"),
            "fieldtype": "Link",
			"options": "Vendors",
        },
    ],
};

