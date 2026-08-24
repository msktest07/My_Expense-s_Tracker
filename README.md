# My Expense's Tracker

A responsive personal finance dashboard built with Python, Flask, SQLite, HTML, CSS, and JavaScript.

## Run locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000 in your browser.

The app uses `expenses.db` for local persistence and creates starter transactions and budgets on first run. The displayed profile is **Shashi Kanth** and all amounts are in **INR (₹)**.
