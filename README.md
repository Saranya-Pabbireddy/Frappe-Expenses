<<<<<<< HEAD
# Frappe-Expenses
Expense Tracking System Project 

Doctypes and Functionality
https://github.com/user-attachments/assets/29038969-4517-4abc-a844-386a35eab3ff

Script Reports and Dashboards
https://github.com/user-attachments/assets/33e8b3c5-3766-4b24-8514-025bfe7e00c4

Notifications and Print Formats
https://github.com/user-attachments/assets/8fcaa74d-5e74-4833-9058-4a8dc17e90e4

Emails Monthly & Pending Approvals
https://github.com/user-attachments/assets/35e275d6-c6c7-4718-8520-aa02b75977f5

Server Script Email & Hooks
https://github.com/user-attachments/assets/84d22302-e2f7-4e3c-82ec-3196fc4c688c

Notification Email
https://github.com/user-attachments/assets/2357bec2-bb47-4d58-b951-c61e99c3f8f5

Hooks Visual Studio Code
https://github.com/user-attachments/assets/ca19e91e-46db-47cf-a6b8-d871d19b135f

Scheduled Tasks
https://github.com/user-attachments/assets/5ef3e834-62f6-4b1a-90d9-28d957d6e6dd

=======
### Expense Tracking System

Expense Tracker

### Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch main
bench install-app expense_tracker
```

### Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/expense_tracker
pre-commit install
```

Pre-commit is configured to use the following tools for checking and formatting your code:

- ruff
- eslint
- prettier
- pyupgrade
### CI

This app can use GitHub Actions for CI. The following workflows are configured:

- CI: Installs this app and runs unit tests on every push to `develop` branch.
- Linters: Runs [Frappe Semgrep Rules](https://github.com/frappe/semgrep-rules) and [pip-audit](https://pypi.org/project/pip-audit/) on every pull request.


### License

mit
>>>>>>> f3f7b65 (feat: Initialize App)
