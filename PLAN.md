# My Expense Tracker Development Plan

## 1. Application Name

**My Expense Tracker**

A responsive web application for recording, organizing, and understanding personal income and expenses.

## 2. Problem Statement

People often lose visibility into their spending because transactions are scattered across bank statements, notes, and spreadsheets. This makes it difficult to know where money is going, stay within a budget, and make informed financial decisions.

My Expense Tracker will provide one simple place to record transactions, categorize spending, set budgets, and view useful summaries. The first release will prioritize fast data entry, clear financial totals, and reliable data storage.

## 3. Target Users

- Individuals who want to track day-to-day personal spending.
- Students and young professionals managing a limited monthly budget.
- Families or households that want a shared high-level view of expenses.
- Users replacing a basic spreadsheet or paper-based tracking process.

The MVP will focus on a single user account. Shared household access can be considered for a later release.

## 4. Main Features

### MVP features

- User registration, login, logout, and protected account access.
- Add, edit, and delete income and expense transactions.
- Transaction fields for amount, type, category, date, payment method, note, and optional receipt image.
- Predefined categories with the ability to create and rename custom categories.
- Dashboard showing current balance, total income, total expenses, and recent transactions.
- Search, filtering, and sorting by date, type, category, and amount.
- Monthly budgets by category.
- Budget progress and overspending indicators.
- Reports with monthly totals and category breakdowns.
- Responsive layout for desktop, tablet, and mobile screens.
- Form validation, clear error messages, loading states, and empty states.
- Export transactions to CSV.

### Post-MVP candidates

- Recurring transactions and reminders.
- Import transactions from CSV or bank exports.
- Shared household accounts and role-based access.
- Multiple currencies and exchange-rate support.
- Automated spending insights and notifications.
- Native mobile application.

## 5. Pages and Screens Required

1. **Landing page** - Brief product introduction and entry points to sign in or register.
2. **Register page** - Create an account with validation.
3. **Login page** - Authenticate an existing user.
4. **Dashboard** - Financial summary, budget status, chart, and recent transactions.
5. **Transactions page** - Paginated transaction list with search, filters, sorting, and export.
6. **Add transaction page or modal** - Create income or expense records.
7. **Edit transaction page or modal** - Update an existing record.
8. **Budgets page** - Create and manage monthly category budgets.
9. **Reports page** - Date-range and category-based charts and summaries.
10. **Categories page** - Manage custom categories.
11. **Settings page** - Profile, currency, month-start preference, and account controls.
12. **Not-found and error screens** - Handle invalid routes and recoverable failures.

## 6. Technology Stack

### Frontend

- React with TypeScript.
- Vite for local development and production builds.
- React Router for page navigation.
- TanStack Query for server-state fetching, caching, and mutations.
- React Hook Form with Zod for form handling and validation.
- Tailwind CSS for responsive styling.
- Recharts for dashboard and report visualizations.
- Lucide React for interface icons.

### Backend

- Node.js with TypeScript.
- Express for the REST API.
- Zod for request and response validation.
- Prisma as the database ORM.
- JWT stored in secure, HTTP-only cookies for authentication.

### Database and storage

- PostgreSQL for users, transactions, budgets, categories, and settings.
- Object storage such as Cloudflare R2 or Amazon S3 for optional receipt images.

### Quality and tooling

- ESLint and Prettier for code quality and formatting.
- Vitest and React Testing Library for unit and component tests.
- Supertest for API tests.
- Playwright for end-to-end testing.
- Git and GitHub for version control and collaboration.

## 7. Project Folder Structure

```text
My_Expense_Tracker/
├── PLAN.md
├── README.md
├── package.json
├── .env.example
├── .gitignore
├── apps/
│   ├── web/
│   │   ├── src/
│   │   │   ├── app/              # App shell, routes, providers
│   │   │   ├── components/       # Shared UI components
│   │   │   ├── features/         # Dashboard, transactions, budgets, reports
│   │   │   ├── pages/             # Route-level screens
│   │   │   ├── hooks/             # Reusable React hooks
│   │   │   ├── lib/               # API client and utility functions
│   │   │   ├── types/             # Frontend types
│   │   │   ├── styles/            # Global styles and theme
│   │   │   └── main.tsx
│   │   ├── public/
│   │   └── index.html
│   └── api/
│       ├── src/
│       │   ├── config/             # Environment and application config
│       │   ├── middleware/         # Authentication, validation, errors
│       │   ├── modules/            # Auth, transactions, budgets, reports
│       │   ├── routes/             # API route registration
│       │   ├── services/           # Business logic and integrations
│       │   ├── lib/                # Prisma and shared utilities
│       │   └── server.ts
│       └── tests/
├── packages/
│   └── shared/                     # Shared schemas, types, and constants
├── prisma/
│   ├── schema.prisma
│   ├── migrations/
│   └── seed.ts
├── tests/
│   └── e2e/
└── docs/
    └── api.md
```

## 8. Data That Needs to Be Stored

### User

- `id`
- `name`
- `email`
- `passwordHash`
- `currency`
- `createdAt`
- `updatedAt`

### Category

- `id`
- `userId` for custom categories
- `name`
- `type` such as income, expense, or both
- `color`
- `isDefault`
- `createdAt`

### Transaction

- `id`
- `userId`
- `categoryId`
- `type` such as income or expense
- `amount` stored as a precise decimal
- `transactionDate`
- `paymentMethod`
- `note`
- `receiptUrl` as an optional value
- `createdAt`
- `updatedAt`

### Budget

- `id`
- `userId`
- `categoryId`
- `month`
- `year`
- `limitAmount`
- `createdAt`
- `updatedAt`

### Optional operational data

- Refresh-token or session records with expiry and revocation status.
- Audit records for sensitive account changes.
- Notification preferences and recurring transaction definitions in later releases.

Passwords must never be stored directly. Receipt uploads should be access-controlled, and all user-owned records must be filtered by the authenticated user ID.

## 9. Development Steps

### Phase 1: Discovery and setup

1. Confirm MVP scope, core user flows, and currency assumptions.
2. Initialize the monorepo, TypeScript, linting, formatting, and environment configuration.
3. Create the PostgreSQL database and initial Prisma schema.
4. Define shared validation schemas, API conventions, and error responses.

### Phase 2: Application foundation

1. Build the frontend app shell, routing, responsive navigation, and shared UI components.
2. Build the Express server, health endpoint, error middleware, and request validation.
3. Add database migrations and seed default categories.
4. Add authentication with registration, login, logout, protected routes, and password hashing.

### Phase 3: Core expense tracking

1. Implement transaction create, read, update, and delete API endpoints.
2. Build the add and edit transaction forms.
3. Build the transaction list with pagination, search, filters, sorting, and empty states.
4. Add CSV export and verify authorization for every transaction operation.

### Phase 4: Financial overview

1. Implement dashboard summary queries for balance, income, expenses, and recent activity.
2. Add monthly category budgets and progress calculations.
3. Build reports for trends and category breakdowns.
4. Add category management and user settings.

### Phase 5: Quality, security, and accessibility

1. Add unit tests for calculations, validation, and shared utilities.
2. Add API integration tests for authentication and CRUD authorization.
3. Add component tests for forms, filters, loading states, and error states.
4. Add Playwright tests for registration, transaction entry, budgets, and reports.
5. Review accessibility, keyboard navigation, responsive layouts, input validation, rate limiting, secure headers, and sensitive-data handling.
6. Test database backups, migration rollback procedures, and CSV export behavior.

### Phase 6: Release

1. Configure production environment variables and separate staging and production databases.
2. Build the frontend and API in a repeatable CI pipeline.
3. Deploy to staging and run smoke and end-to-end tests.
4. Deploy production with database migrations and monitoring enabled.
5. Collect feedback, fix release issues, and prioritize post-MVP features.

## 10. Deployment Approach

- Store the repository in GitHub and use GitHub Actions for install, lint, typecheck, test, and build checks on every pull request.
- Deploy the React frontend to Vercel or Netlify.
- Deploy the Node.js API to Render, Railway, or Fly.io.
- Use managed PostgreSQL from the selected hosting provider or Neon/Supabase.
- Store receipt images in private object storage with short-lived signed URLs.
- Keep secrets and database URLs in the hosting platform's encrypted environment variables.
- Run Prisma migrations as part of the controlled deployment process.
- Use HTTPS, secure HTTP-only cookies, CORS restrictions, rate limiting, and security headers in production.
- Add uptime checks, structured server logs, error tracking, and database backups before the public release.
- Use separate staging and production environments, with staging validated before production promotion.

### Definition of done for the MVP

A user can create an account, add and manage income and expenses, categorize transactions, set a monthly budget, view accurate dashboard and report totals, export their data, and use the app successfully on both desktop and mobile. Automated tests cover the main flows, and the production deployment has authentication, backups, monitoring, and secure configuration in place.
