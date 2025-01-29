import frappe
from frappe import _
import calendar

message = "Vendor"

month_map = {
    "Jan": 1,
    "Feb": 2,
    "Mar": 3,
    "Apr": 4,
    "May": 5,
    "Jun": 6,
    "Jul": 7,
    "Aug": 8,
    "Sep": 9,
    "Oct": 10,
    "Nov": 11,
    "Dec": 12
}

def execute(filters: dict | None = None):
    columns = get_columns(filters)
    data = get_data(filters)
    chart = get_chart(data)
    summary = get_summary(data)

    return columns, data, message, chart, summary

def get_columns(filters: dict) -> list[dict]:
    return [
        {
            "label": _("Vendor"),
            "fieldname": "vendor",
            "fieldtype": "Link",
            "options": "Vendors",  
        },
        {
            "label": _("Month"),
            "fieldname": "month",
            "fieldtype": "Data",
        },
        {
            "label": _("Total Payment"),
            "fieldname": "total_payment",
            "fieldtype": "Float",
        },
    ]

def get_data(filters: dict) -> list[dict]:
    query = """
        SELECT 
            vendor, 
            YEAR(expense_date) AS year,
            MONTH(expense_date) AS month,
            SUM(amount) AS total_payment
        FROM 
            `tabExpenses` 
        WHERE 1=1  
    """

    if filters:
        if "vendor" in filters and filters["vendor"]:
            query += f" AND vendor = '{filters['vendor']}'"
        
        if "month" in filters and filters["month"]:
            month_number = month_map.get(filters["month"])
            if month_number:
                query += f" AND MONTH(expense_date) = {month_number}"
        
        if "year" in filters and filters["year"]:
            query += f" AND YEAR(expense_date) = {filters['year']}"
    
    query += " GROUP BY vendor, year, month"
    
    data = frappe.db.sql(query, filters, as_dict=True)
    
    for row in data:
        row['month'] = calendar.month_abbr[row['month']]  
    
    return data

def get_chart(data) -> dict:
    chart_data = {
        "type": "pie",
        "data": {
            "labels": [row["vendor"] for row in data],
            "datasets": [{
                "name": _("Total Payment"),
                "values": [row["total_payment"] for row in data]
            }]
        },
        "title": _("Total Payments by Vendor"), 
        "colors": ["#FF5733", "#33FF57", "#3357FF", "#F3FF33"],
    }
    return chart_data

def get_summary(data) -> list[dict]:
    total_expense = sum([row["total_payment"] for row in data])
    vendors_count = len(set([row["vendor"] for row in data]))
    vendors_list = ", ".join(set([row["vendor"] for row in data]))
    
    summary = [
        {
            "label": _("Total Expense"),
            "value": total_expense,
            "datatype": "Currency",
            "color": "green", 
        },
        {
            "label": _("Number of Vendors"),
            "value": vendors_count,
            "datatype": "Int",
            "color": "blue",  
        },
        {
            "label": _("Vendors"),
            "value": vendors_list,
            "datatype": "Data",
            "color": "red",  
        },
    ]
    return summary
