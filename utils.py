
import pandas as pd
import os
from datetime import datetime

DATA_DIR = "data"
SLEEP_FILE = os.path.join(DATA_DIR, "sleep.csv")
EXP_FILE = os.path.join(DATA_DIR, "expenses.csv")
TODO_FILE = os.path.join(DATA_DIR, "todo.csv")

os.makedirs(DATA_DIR, exist_ok=True)
for f in [SLEEP_FILE, EXP_FILE, TODO_FILE]:
    if not os.path.exists(f):
        pd.DataFrame().to_csv(f, index=False)

def _read_csv(path, **kwargs):
    return pd.read_csv(path, **kwargs) if os.path.getsize(path) else pd.DataFrame()

def load_data():
    sleep_df = _read_csv(SLEEP_FILE, parse_dates=['date', 'start', 'end'])
    exp_df = _read_csv(EXP_FILE, parse_dates=['date'])
    todo_df = _read_csv(TODO_FILE, parse_dates=['date'])

    # Backwards compatibility: convert old 'done' bool to status
    if 'status' not in todo_df.columns and not todo_df.empty:
        todo_df['status'] = todo_df.get('done', False).map(lambda x: "Completed" if x else "Pending")
        todo_df.drop(columns=[c for c in ['done'] if c in todo_df.columns], inplace=True)

    # Ensure correct dtypes
    if not sleep_df.empty and 'duration' in sleep_df.columns:
        sleep_df['duration'] = sleep_df['duration'].astype(float)
    return sleep_df, exp_df, todo_df

def save_sleep(start_dt, end_dt):
    sleep_df, _, _ = load_data()
    new = {
        'date': pd.Timestamp(start_dt.date()),
        'start': start_dt,
        'end': end_dt,
        'duration': (end_dt - start_dt).seconds / 3600
    }
    sleep_df = pd.concat([sleep_df, pd.DataFrame([new])], ignore_index=True)
    sleep_df.to_csv(SLEEP_FILE, index=False)

def save_expense(exp_date, amount, category, status):
    _, exp_df, _ = load_data()
    new = {
        'date': pd.Timestamp(exp_date),
        'amount': float(amount),
        'category': category,
        'status': status
    }
    exp_df = pd.concat([exp_df, pd.DataFrame([new])], ignore_index=True)
    exp_df.to_csv(EXP_FILE, index=False)

def save_task(task_date, task_text, status):
    _, _, todo_df = load_data()
    new = {'date': pd.Timestamp(task_date), 'task': task_text, 'status': status}
    todo_df = pd.concat([todo_df, pd.DataFrame([new])], ignore_index=True)
    todo_df.to_csv(TODO_FILE, index=False)
