# Copyright (c) 2025, Saranya and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.core.doctype.communication.email import make

def on_submit(doc, method):
    if doc.docstatus == 1:
        if doc.workflow_state == "Pending":
            doc.status = "Pending"
        
    frappe.msgprint(f"Expense {doc.name} has been submitted.")

def on_approval(doc, method):
    if doc.status == "Approved":
        frappe.msgprint(f"Expense {doc.name} has been approved.") 

class Expenses(Document):
    
    def before_save(self):
        '''if self.workflow_state == "Approved":
            self.status = "Approved"
        elif self.workflow_state == "Rejected":
            self.status = "Rejected"'''
            
        category_budget_limit = frappe.db.get_value("Categories", self.category, "budget_limit")

        if self.amount > category_budget_limit:
            if self.docstatus == 0:  
                self.workflow_state = "Pending"
                self.status = "Pending"
                # self.send_high_value_notification()
        
        if self.status == "Pending" and self.expense_date < frappe.utils.nowdate():
            self.send_high_value_notification()

    def send_high_value_notification(self):
        approver_email = self.approved_by  

        if approver_email:
            message = f"""
            <p>Dear Approver,</p>
            <p>This is a reminder that the following document is overdue for approval:</p>
            <ul>
                <li>Expense Name: {self.name}</li>
                <li>Category: {self.category}</li>
                <li>Expense Date: {self.expense_date}</li>
                <li>Amount: {self.amount}</li>
            </ul>
            <p>Please log in to the system to review and approve the expense.</p>
            """

            make(
                recipients=[approver_email],
                subject="High-Value Expense Approval Needed",
                content=message,
                communication_medium="Email",
                send_email=True  
            )
            
    def on_update_after_submit(self):
        if self.docstatus == 1:  
            if self.workflow_state == "Approved":
                self.status = "Approved"
            elif self.workflow_state == "Rejected":
                self.status = "Rejected"
            

        
    