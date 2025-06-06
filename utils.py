import pandas as pd
import os
from datetime import datetime

# Directory where CSV files live
DATA_DIR = "data"
SLEEP_FILE = os.path.join(DATA_DIR, "sleep.csv")
EXP_FILE = os.path.join(DATA_DIR, "expenses.csv")
TODO_FILE = os.path.join(DATA_DIR, "todo.csv")

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# If CSVs don't exist yet, create empty ones
for path in (SLEEP_FILE, EXP_FILE, TODO_FILE):
    if not os.path.isfile(path):
        pd.DataFrame().to_csv(path, index=False)

def load_data():
    """
    Reads all three CSV files and returns:
      sleep_df (with columns: date, start, end, duration),
      exp_df   (with columns: date, amount, category, status),
      todo_df  (with columns: date, task, status).
    """
    # 1) Sleep DataFrame
    # If file is empty, create an empty DataFrame with the expected columns
    if os.path.getsize(SLEEP_FILE) == 0:
        sleep_df = pd.DataFrame(columns=["date", "start", "end", "duration"])
    else:
        sleep_df = pd.read_csv(SLEEP_FILE, parse_dates=["date", "start", "end"])
        # Ensure "duration" exists (in hours)
        if "duration" not in sleep_df.columns:
            # Calculate it if start/end exist
            if "start" in sleep_df.columns and "end" in sleep_df.columns:
                sleep_df["duration"] = (
                    pd.to_datetime(sleep_df["end"]) - pd.to_datetime(sleep_df["start"])
                ).dt.total_seconds() / 3600.0
            else:
                sleep_df["duration"] = 0.0

    # 2) Expense DataFrame
    if os.path.getsize(EXP_FILE) == 0:
        exp_df = pd.DataFrame(columns=["date", "amount", "category", "status"])
    else:
        exp_df = pd.read_csv(EXP_FILE, parse_dates=["date"])
        # If any missing columns, fill them
        for col in ("amount", "category", "status"):
            if col not in exp_df.columns:
                exp_df[col] = ""

    # 3) To-Do DataFrame
    if os.path.getsize(TODO_FILE) == 0:
        todo_df = pd.DataFrame(columns=["date", "task", "status"])
    else:
        todo_df = pd.read_csv(TODO_FILE, parse_dates=["date"])
        # If any missing columns, fill them
        for col in ("task", "status"):
            if col not in todo_df.columns:
                todo_df[col] = ""

    return sleep_df, exp_df, todo_df

def save_sleep(start_dt, end_dt):
    """
    Appends a new sleep log. 
    - start_dt, end_dt are Python datetime objects.
    - Calculates duration in hours, then writes to sleep.csv.
    """
    duration_hrs = round((end_dt - start_dt).total_seconds() / 3600.0, 2)
    log_date = start_dt.date()
    new_row = {
        "date": pd.Timestamp(log_date),
        "start": pd.Timestamp(start_dt),
        "end": pd.Timestamp(end_dt),
        "duration": duration_hrs
    }
    sleep_df, exp_df, todo_df = load_data()
    sleep_df = pd.concat([sleep_df, pd.DataFrame([new_row])], ignore_index=True)
    sleep_df.to_csv(SLEEP_FILE, index=False)

def save_expense(exp_date, amount, category, status):
    """
    Appends a new expense. 
    - exp_date is a Python date object or string parseable by pandas.Timestamp.
    """
    new_row = {
        "date": pd.Timestamp(exp_date),
        "amount": float(amount),
        "category": category,
        "status": status
    }
    sleep_df, exp_df, todo_df = load_data()
    exp_df = pd.concat([exp_df, pd.DataFrame([new_row])], ignore_index=True)
    exp_df.to_csv(EXP_FILE, index=False)

def save_task(task_date, task_text, status):
    """
    Appends a new to-do task. 
    - task_date is a Python date object or string parseable by pandas.Timestamp.
    """
    new_row = {
        "date": pd.Timestamp(task_date),
        "task": task_text,
        "status": status
    }
    sleep_df, exp_df, todo_df = load_data()
    todo_df = pd.concat([todo_df, pd.DataFrame([new_row])], ignore_index=True)
    todo_df.to_csv(TODO_FILE, index=False)
