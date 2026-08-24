# My Expense's Tracker

## Project Name

**My Expense's Tracker**

## Project Description

My Expense's Tracker is a responsive personal finance web application for recording income and expenses, organizing transactions by category, monitoring monthly budgets, and understanding spending patterns.

The application is designed for **Shashi Kanth** and displays all amounts in **Indian Rupees (INR / ₹)**. It uses a local SQLite database, so transactions and budgets remain available between application runs.

## Features

- Overview dashboard with balance, income, expense, and recent activity summaries.
- Add, edit, and delete income or expense transactions.
- Transaction fields for title, amount, date, category, payment method, and notes.
- Search transactions and filter them by income or expense type.
- Create, update, and remove monthly category budgets.
- Budget progress bars and overspending indicators.
- Reports with category-based expense breakdowns.
- Client-side and server-side form validation.
- Clear success and error messages after actions.
- Responsive layout with mobile navigation.
- Starter transactions and budgets created automatically on first run.

## Technology Used

- **Python 3** - Application programming language.
- **Flask** - Web framework and routing.
- **SQLite** - Local database for transactions and budgets.
- **HTML5** - Page structure and accessible forms.
- **CSS3** - Responsive layout and visual styling.
- **JavaScript** - Mobile navigation, dismissible messages, and client-side validation.

## How to Install

1. Clone the repository and open the project directory:

	```powershell
	git clone https://github.com/msktest07/My_Expense-s_Tracker.git
	cd My_Expense_Tracker
	```

2. Create and activate a Python virtual environment:

	```powershell
	python -m venv .venv
	.\.venv\Scripts\Activate.ps1
	```

	On macOS or Linux, activate it with:

	```bash
	source .venv/bin/activate
	```

3. Install the required package:

	```powershell
	pip install -r requirements.txt
	```

## How to Run Locally

From the project directory, with the virtual environment activated, run:

```powershell
python app.py
```

Then open the local application in a browser:

**http://127.0.0.1:5000**

The `expenses.db` file is created automatically when the application starts. It is intentionally excluded from Git by `.gitignore` because it is local runtime data.

## GitHub Repository

https://github.com/msktest07/My_Expense-s_Tracker

## Live Application URL

The deployed production application is available at:

https://my-expense-s-tracker.vercel.app

For local development, use http://127.0.0.1:5000 after following the run instructions above.

## Project Structure

```text
My_Expense_Tracker/
├── app.py                 # Flask routes, validation, and database logic
├── requirements.txt       # Python dependencies
├── PLAN.md                # Development plan
├── README.md              # Project documentation
├── .gitignore             # Ignored local files
├── templates/             # HTML pages
└── static/                # CSS and JavaScript assets
```
