import frappe
from frappe.utils import today, add_months, get_first_day, get_last_day
from frappe.core.doctype.communication.email import make

def check_pending_approvals():

    pending_expenses = frappe.get_all(
        'Expenses',
        filters={'status': 'Pending', 'approval_required': 1, 'approved_by': ['is', 'set']},
        fields=['name', 'description', 'category', 'expense_date', 'amount', 'approved_by']
    )
    
    if pending_expenses:
        for expense in pending_expenses:
            approver_email = expense.get('approved_by')
            
            if approver_email:
                message = f"""
                <p>Dear Approver,</p>
                <p>This is a reminder that the following document is overdue for approval:</p>
                <ul>
                    <li>Expense Name: {expense.get('description')}</li>
                    <li>Category: {expense.get('category')}</li>
                    <li>Expense Date: {expense.get('expense_date')}</li>
                    <li>Amount: {expense.get('amount')}</li>
                </ul>
                <p>Please log in to the system to review and approve the expense.</p>
                """
                
                make(
                    recipients=[approver_email],
                    subject="Pending Expense Approval Reminder",
                    content=message,
                    communication_medium="Email",
                    send_email=True  
                )
                print(f"Sent email to {approver_email} for expense {expense.get('description')}")
            else:
                print(f"No approver found for expense {expense.get('description')}")

def generate_monthly_report():

    first_day = get_first_day(add_months(today(), -1))
    last_day = get_last_day(add_months(today(), -1))

    monthly_expenses = frappe.get_all(
        'Expenses',
        filters={'expense_date': ['between', [first_day, last_day]], 'approved_by': ['is', 'set']},
        fields=['name', 'description', 'category', 'expense_date', 'amount', 'status', 'approved_by']
    )

    if monthly_expenses:

        expenses_by_approver = {}
        total_expenses = 0
        for expense in monthly_expenses:
            approver_email = expense.get('approved_by')
            if approver_email:
                expenses_by_approver.setdefault(approver_email, []).append(expense)
                total_expenses += expense.get('amount')

        for approver_email, expenses in expenses_by_approver.items():
            report_rows = [
                f"""
                <tr>
                    <td>{expense.get('name')}</td>
                    <td>{expense.get('description')}</td>
                    <td>{expense.get('category')}</td>
                    <td>{expense.get('expense_date')}</td>
                    <td>{expense.get('amount')}</td>
                    <td>{expense.get('status')}</td>
                </tr>
                """ for expense in expenses
            ]
            
            report_rows.append(f"""
            <tr>
                <td colspan="5" style="text-align:right;"><strong>Total Expense for the Month:</strong></td>
                <td><strong>{total_expenses}</strong></td>
            </tr>
            """)
            
            report_content = f"""
            <p>Dear {approver_email},</p>
            <p>Here is the expense report for the past month, containing expenses approved by you:</p>
            <table border="1" cellpadding="5" cellspacing="0">
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Description</th>
                        <th>Category</th>
                        <th>Expense Date</th>
                        <th>Amount</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    {''.join(report_rows)}
                </tbody>
            </table>
            <p>Regards,</p>
            <p>Expense Tracker</p>
            """

            make(
                recipients=[approver_email],
                subject="Monthly Expense Report",
                content=report_content,
                communication_medium="Email",
                send_email=True
            )
            print(f"Monthly report sent to {approver_email}")
    else:
        print("No expenses found for the past month.")