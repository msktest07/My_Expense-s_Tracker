# My Expense's Tracker Development Plan

## 1. Application Name

**My Expense's Tracker**

A responsive personal finance web application for Shashi Kanth to record, organize, and understand income and expenses in Indian Rupees (INR).

## 2. Problem Statement

People often lose visibility into their spending because transactions are scattered across bank statements, notes, and spreadsheets. This makes it difficult to know where money is going, stay within a budget, and make informed financial decisions.

My Expense's Tracker provides one simple place to record transactions, categorize spending, set budgets, and view useful summaries. The first release prioritizes fast data entry, clear financial totals, validation, useful budget logic, and reliable local persistence.

## 3. Target Users

- Individuals who want to track day-to-day personal spending.
- Students and young professionals managing a monthly budget.
- Users replacing a basic spreadsheet or paper-based tracking process.

The current MVP uses a single configured profile, **Shashi Kanth**, and INR currency. Multi-user accounts and shared household access can be considered for a later release.

## 4. Main Features

### Current MVP features

- Add, edit, and delete income and expense transactions.
- Transaction fields for title, amount, type, category, date, payment method, and notes.
- Predefined categories and payment methods.
- Dashboard showing current balance, total income, total expenses, spending breakdown, budgets, and recent transactions.
- Search and filtering by transaction text and income/expense type.
- Monthly budgets by category.
- Budget progress and overspending indicators.
- Reports with total income, total expenses, net position, and category breakdowns.
- Responsive layout for desktop, tablet, and mobile screens.
- Client-side and server-side form validation.
- Success and error messages, empty states, and delete confirmation.
- SQLite persistence with starter data on first run.

### Post-MVP candidates

- User authentication and multiple profiles.
- Recurring transactions and reminders.
- Import transactions from CSV or bank exports.
- Shared household accounts and role-based access.
- Multiple currencies and exchange-rate support.
- Public receipt storage and uploads.
- Automated spending insights and notifications.

## 5. Pages and Screens Required

1. **Overview page** - Balance, income, expenses, spending breakdown, budget progress, and recent activity.
2. **Transactions page** - Searchable and filterable transaction table with edit and delete actions.
3. **Add transaction page** - Validated form for creating income or expense records.
4. **Edit transaction page** - Validated form for updating an existing record.
5. **Budgets page** - Create, update, review, and remove category budgets.
6. **Reports page** - Net position and category-based expense report.
7. **Responsive mobile navigation** - Collapsible navigation drawer for smaller screens.
8. **Future screens** - Authentication, profile settings, custom categories, CSV export, and error pages.

## 6. Technology Stack

### Application

- Python 3.
- Flask for routing, request handling, templates, and flash messages.
- SQLite with Python's built-in `sqlite3` module for persistence.
- Jinja templates for server-rendered HTML.
- HTML5, CSS3, and vanilla JavaScript for the interface and interactions.

### Deployment and tooling

- Git and GitHub for version control and source hosting.
- Vercel Python runtime with `api/index.py` as the serverless entrypoint.
- `vercel.json` for deployment routing.
- Python `venv` and `requirements.txt` for dependency management.
- `py_compile` and Flask test-client smoke checks for basic validation.

## 7. Project Folder Structure

```text
My_Expense_Tracker/
├── PLAN.md
├── README.md
├── app.py                 # Flask app, routes, validation, and database logic
├── requirements.txt       # Python dependencies
├── README.md              # Setup and usage documentation
├── PLAN.md                # This development plan
├── .gitignore             # Local environments and runtime files
├── vercel.json            # Vercel build and route configuration
├── api/
│   └── index.py           # Vercel serverless entrypoint
├── templates/             # Jinja HTML pages
│   ├── base.html
│   ├── dashboard.html
│   ├── transactions.html
│   ├── transaction_form.html
│   ├── budgets.html
│   └── reports.html
├── static/
│   ├── style.css          # Responsive visual design
│   └── app.js             # Navigation and client validation
└── expenses.db            # Local SQLite database, ignored by Git
```

## 8. Data That Needs to Be Stored

### Transaction

- `id`
- `title`
- `amount`
- `kind` such as income or expense
- `category`
- `transaction_date`
- `payment_method`
- `notes`
- `created_at`

### Budget

- `id`
- `id`
- `category`
- `amount`

### Application configuration

- Display title: `My Expense's Tracker`
- Username: `Shashi Kanth`
- Currency: INR (`₹`)
- Default categories and payment methods defined in `app.py`.

The local database is created and seeded automatically on first run. On Vercel, SQLite uses the platform's temporary directory; production persistence should move to a managed database before storing user-critical data.

## 9. Development Steps

### Phase 1: Foundation

1. Confirm the single-user INR scope and core transaction fields.
2. Create the Flask project, dependency file, templates, static assets, and SQLite schema.
3. Add automatic database initialization and seed starter transactions and budgets.

### Phase 2: Core workflows

1. Implement dashboard summary and spending calculations.
2. Implement transaction create, read, update, and delete routes.
3. Add server-side validation for amounts, dates, required fields, and transaction types.
4. Build transaction search and income/expense filters.

### Phase 3: Budget and reporting workflows

1. Implement monthly budget create/update logic with category uniqueness.
2. Calculate budget percentages and overspending states.
3. Build reports with category totals and percentage breakdowns.

### Phase 4: User experience and quality

1. Add responsive navigation and layouts for small screens.
2. Add client-side validation, success/error flash messages, empty states, and confirmations.
3. Run Python compilation, Flask test-client route checks, and manual browser checks.
4. Review accessibility, input handling, security configuration, and deployment limitations.

### Phase 5: Release and improvement

1. Commit the source and documentation to GitHub.
2. Configure Vercel's Python entrypoint and deployment routes.
3. Deploy to production and smoke-test every core page.
4. Replace temporary SQLite storage with managed persistence before multi-user production use.
5. Prioritize authentication, CSV export, custom categories, and recurring transactions.

## 10. Deployment Approach

- Push the project source from the local Git repository to GitHub: `msktest07/My_Expense-s_Tracker`.
- Connect the GitHub repository to Vercel and configure `api/index.py` as the Python serverless entrypoint through `vercel.json`.
- Deploy the Flask application to the Vercel production alias: `https://my-expense-s-tracker.vercel.app`.
- Keep dependencies in `requirements.txt` so Vercel can install Flask during the build.
- Keep `.env*`, `.vercel`, virtual environments, caches, and local SQLite data out of source control.
- Use HTTPS provided by Vercel and configure environment variables through the Vercel project settings.
- Note that Vercel's filesystem is ephemeral; use a managed database such as PostgreSQL or a hosted SQLite-compatible service before relying on persistent production writes.
- Add deployment smoke tests, error monitoring, backups, and a staging environment as the application grows.

### Definition of done for the MVP

A user can open the public application, add and manage income and expenses, categorize transactions, set a monthly budget, view accurate dashboard and report totals, and use the app successfully on desktop and mobile. The current single-user MVP is deployed to Vercel, documented in GitHub, and validated with route and form smoke tests. Managed persistence, authentication, and automated regression tests remain planned improvements.
