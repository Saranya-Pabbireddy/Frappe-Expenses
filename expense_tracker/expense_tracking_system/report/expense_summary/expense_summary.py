# Copyright (c) 2025, Saranya and contributors
# For license information, please see license.txt

import frappe
from frappe import _
import calendar


def execute(filters: dict | None = None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data


def get_columns() -> list[dict]:
    return [
        {
            "label": _("Year"),
            "fieldname": "year",
            "fieldtype": "Int",
        },
        {
            "label": _("Month"),
            "fieldname": "month",
            "fieldtype": "Data",
        },
		{
            "label": _("Category"),
            "fieldname": "category",
            "fieldtype": "Link",
            "options": "Categories", 
        },
        {
            "label": _("Total Expense"),
            "fieldname": "total_expense",
            "fieldtype": "Float",
        }
		
    ]


def get_data(filters: dict) -> list[dict]:
    query = """
        SELECT 
            YEAR(expense_date) AS year,
            MONTH(expense_date) AS month,
			category,
            SUM(amount) AS total_expense
        FROM `tabExpenses`
        GROUP BY category
        ORDER BY total_expense DESC  
        LIMIT 5;
    """
    raw_data = frappe.db.sql(query, filters, as_dict=True)

    data = []
    for row in raw_data:
        row['month'] = calendar.month_abbr[row['month']]
        data.append(row)

    return data
