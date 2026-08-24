from datetime import date, datetime
from pathlib import Path
import os
import sqlite3
import tempfile

from flask import Flask, flash, g, redirect, render_template, request, url_for


BASE_DIR = Path(__file__).resolve().parent
DATABASE = Path(tempfile.gettempdir()) / "expenses.db" if "VERCEL" in os.environ else BASE_DIR / "expenses.db"

app = Flask(__name__)
app.config["SECRET_KEY"] = "change-this-secret-key"

CATEGORIES = [
    ("Food & Dining", "#f97316"),
    ("Transport", "#0ea5e9"),
    ("Bills & Utilities", "#8b5cf6"),
    ("Shopping", "#ec4899"),
    ("Health", "#14b8a6"),
    ("Entertainment", "#eab308"),
    ("Salary", "#22c55e"),
    ("Other", "#64748b"),
]


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(_error=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = sqlite3.connect(DATABASE)
    db.executescript(
        """
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            amount REAL NOT NULL CHECK(amount > 0),
            kind TEXT NOT NULL CHECK(kind IN ('income', 'expense')),
            category TEXT NOT NULL,
            transaction_date TEXT NOT NULL,
            payment_method TEXT NOT NULL,
            notes TEXT DEFAULT '',
            created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL UNIQUE,
            amount REAL NOT NULL CHECK(amount > 0)
        );
        """
    )
    if db.execute("SELECT COUNT(*) FROM transactions").fetchone()[0] == 0:
        today = date.today()
        sample_data = [
            ("Monthly salary", 85000, "income", "Salary", today.isoformat(), "Bank transfer", "August salary"),
            ("Apartment rent", 24000, "expense", "Bills & Utilities", today.replace(day=2).isoformat(), "UPI", "Monthly rent"),
            ("Grocery run", 2850, "expense", "Food & Dining", today.replace(day=8).isoformat(), "Card", "Weekly groceries"),
            ("Metro pass", 1200, "expense", "Transport", today.replace(day=12).isoformat(), "UPI", "Office commute"),
        ]
        db.executemany(
            "INSERT INTO transactions (title, amount, kind, category, transaction_date, payment_method, notes, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            [(*row, datetime.now().isoformat()) for row in sample_data],
        )
    if db.execute("SELECT COUNT(*) FROM budgets").fetchone()[0] == 0:
        db.executemany(
            "INSERT OR IGNORE INTO budgets (category, amount) VALUES (?, ?)",
            [("Food & Dining", 12000), ("Transport", 5000), ("Shopping", 8000)],
        )
    db.commit()
    db.close()


def get_summary():
    db = get_db()
    totals = db.execute(
        "SELECT COALESCE(SUM(CASE WHEN kind='income' THEN amount ELSE 0 END), 0) income, "
        "COALESCE(SUM(CASE WHEN kind='expense' THEN amount ELSE 0 END), 0) expenses FROM transactions"
    ).fetchone()
    category_rows = db.execute(
        "SELECT category, SUM(amount) total FROM transactions WHERE kind='expense' GROUP BY category ORDER BY total DESC"
    ).fetchall()
    return {
        "income": totals["income"],
        "expenses": totals["expenses"],
        "balance": totals["income"] - totals["expenses"],
        "category_rows": category_rows,
    }


def validate_transaction(form):
    errors = []
    title = form.get("title", "").strip()
    kind = form.get("kind", "expense")
    category = form.get("category", "").strip()
    payment_method = form.get("payment_method", "").strip()
    notes = form.get("notes", "").strip()
    raw_amount = form.get("amount", "").strip()
    transaction_date = form.get("transaction_date", "").strip()
    try:
        amount = float(raw_amount)
        if amount <= 0:
            raise ValueError
    except ValueError:
        amount = 0
        errors.append("Enter an amount greater than ₹0.")
    if not title or len(title) > 60:
        errors.append("Add a title between 1 and 60 characters.")
    if kind not in {"income", "expense"}:
        errors.append("Choose a valid transaction type.")
    if not category:
        errors.append("Choose a category.")
    if not payment_method:
        errors.append("Choose a payment method.")
    try:
        datetime.strptime(transaction_date, "%Y-%m-%d")
    except ValueError:
        errors.append("Choose a valid transaction date.")
    return errors, (title, amount, kind, category, transaction_date, payment_method, notes)


@app.context_processor
def inject_globals():
    return {"app_title": "My Expense's Tracker", "username": "Shashi Kanth", "today": date.today().isoformat()}


@app.route("/")
def dashboard():
    db = get_db()
    summary = get_summary()
    recent = db.execute("SELECT * FROM transactions ORDER BY transaction_date DESC, id DESC LIMIT 6").fetchall()
    budgets = db.execute("SELECT * FROM budgets ORDER BY category").fetchall()
    spent = {
        row["category"]: row["total"]
        for row in db.execute("SELECT category, SUM(amount) total FROM transactions WHERE kind='expense' GROUP BY category")
    }
    return render_template("dashboard.html", active="dashboard", summary=summary, recent=recent, budgets=budgets, spent=spent)


@app.route("/transactions")
def transactions():
    db = get_db()
    search = request.args.get("search", "").strip()
    kind = request.args.get("kind", "all")
    query = "SELECT * FROM transactions WHERE (title LIKE ? OR category LIKE ? OR notes LIKE ?)"
    params = [f"%{search}%"] * 3
    if kind in {"income", "expense"}:
        query += " AND kind = ?"
        params.append(kind)
    query += " ORDER BY transaction_date DESC, id DESC"
    rows = db.execute(query, params).fetchall()
    return render_template("transactions.html", active="transactions", transactions=rows, search=search, kind=kind)


@app.route("/transactions/add", methods=("GET", "POST"))
def add_transaction():
    if request.method == "POST":
        errors, values = validate_transaction(request.form)
        if errors:
            for error in errors:
                flash(error, "error")
            return render_template("transaction_form.html", active="transactions", categories=CATEGORIES, form=request.form, page_title="Add transaction")
        db = get_db()
        db.execute(
            "INSERT INTO transactions (title, amount, kind, category, transaction_date, payment_method, notes, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (*values, datetime.now().isoformat()),
        )
        db.commit()
        flash("Transaction added successfully.", "success")
        return redirect(url_for("transactions"))
    return render_template("transaction_form.html", active="transactions", categories=CATEGORIES, form={}, page_title="Add transaction")


@app.route("/transactions/<int:transaction_id>/edit", methods=("GET", "POST"))
def edit_transaction(transaction_id):
    db = get_db()
    transaction = db.execute("SELECT * FROM transactions WHERE id = ?", (transaction_id,)).fetchone()
    if transaction is None:
        flash("That transaction could not be found.", "error")
        return redirect(url_for("transactions"))
    if request.method == "POST":
        errors, values = validate_transaction(request.form)
        if errors:
            for error in errors:
                flash(error, "error")
            return render_template("transaction_form.html", active="transactions", categories=CATEGORIES, form=request.form, page_title="Edit transaction")
        db.execute(
            "UPDATE transactions SET title=?, amount=?, kind=?, category=?, transaction_date=?, payment_method=?, notes=? WHERE id=?",
            (*values, transaction_id),
        )
        db.commit()
        flash("Transaction updated successfully.", "success")
        return redirect(url_for("transactions"))
    return render_template("transaction_form.html", active="transactions", categories=CATEGORIES, form=transaction, page_title="Edit transaction")


@app.post("/transactions/<int:transaction_id>/delete")
def delete_transaction(transaction_id):
    db = get_db()
    result = db.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
    db.commit()
    flash("Transaction deleted." if result.rowcount else "Transaction was not found.", "success" if result.rowcount else "error")
    return redirect(request.referrer or url_for("transactions"))


@app.route("/budgets", methods=("GET", "POST"))
def budgets():
    db = get_db()
    if request.method == "POST":
        category = request.form.get("category", "").strip()
        try:
            amount = float(request.form.get("amount", "0"))
            if amount <= 0:
                raise ValueError
        except ValueError:
            flash("Budget amount must be greater than ₹0.", "error")
            return redirect(url_for("budgets"))
        if not category:
            flash("Choose a budget category.", "error")
            return redirect(url_for("budgets"))
        db.execute("INSERT INTO budgets (category, amount) VALUES (?, ?) ON CONFLICT(category) DO UPDATE SET amount=excluded.amount", (category, amount))
        db.commit()
        flash("Budget saved successfully.", "success")
        return redirect(url_for("budgets"))
    budget_rows = db.execute("SELECT * FROM budgets ORDER BY category").fetchall()
    spent = {row["category"]: row["total"] for row in db.execute("SELECT category, SUM(amount) total FROM transactions WHERE kind='expense' GROUP BY category")}
    return render_template("budgets.html", active="budgets", budgets=budget_rows, spent=spent, categories=CATEGORIES)


@app.post("/budgets/<int:budget_id>/delete")
def delete_budget(budget_id):
    db = get_db()
    db.execute("DELETE FROM budgets WHERE id = ?", (budget_id,))
    db.commit()
    flash("Budget removed.", "success")
    return redirect(url_for("budgets"))


@app.route("/reports")
def reports():
    summary = get_summary()
    total = summary["expenses"] or 1
    breakdown = [
        {"category": row["category"], "total": row["total"], "percent": round(row["total"] / total * 100)}
        for row in summary["category_rows"]
    ]
    return render_template("reports.html", active="reports", summary=summary, breakdown=breakdown)


with app.app_context():
    init_db()


if __name__ == "__main__":
    app.run(debug=True)
