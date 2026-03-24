import sqlite3
from datetime import datetime

DB_NAME = "focus.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Tasks table
    c.execute('''CREATE TABLE IF NOT EXISTS tasks
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  task_name TEXT NOT NULL,
                  is_completed INTEGER DEFAULT 0,
                  created_at DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    # Study sessions table (for recent activity and hours)
    c.execute('''CREATE TABLE IF NOT EXISTS study_sessions
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  subject TEXT NOT NULL,
                  hours REAL,
                  created_at DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    # Settings table for user preferences like exam date
    c.execute('''CREATE TABLE IF NOT EXISTS settings
                 (key TEXT PRIMARY KEY,
                  value TEXT)''')
    conn.commit()
    conn.close()

# Initialize the database
init_db()

def add_task(task_name):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO tasks (task_name) VALUES (?)", (task_name,))
    conn.commit()
    conn.close()

def complete_task(task_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE tasks SET is_completed = 1 WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

def get_tasks():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, task_name, is_completed FROM tasks ORDER BY created_at DESC")
    tasks = [{"id": r[0], "task_name": r[1], "is_completed": bool(r[2])} for r in c.fetchall()]
    conn.close()
    return tasks

def add_session(subject, hours):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO study_sessions (subject, hours) VALUES (?, ?)", (subject, hours))
    conn.commit()
    conn.close()

def get_recent_activity(limit=3):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT subject, created_at FROM study_sessions ORDER BY created_at DESC LIMIT ?", (limit,))
    sessions = [{"subject": r[0], "created_at": r[1]} for r in c.fetchall()]
    conn.close()
    return sessions

def set_exam_date(date_str):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO settings (key, value) VALUES ('exam_date', ?)", (date_str,))
    conn.commit()
    conn.close()

def get_exam_date():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT value FROM settings WHERE key = 'exam_date'")
    row = c.fetchone()
    conn.close()
    return row[0] if row else None

def get_dashboard_data():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Hours today
    c.execute("SELECT SUM(hours) FROM study_sessions WHERE date(created_at) = date('now')")
    hours_today = c.fetchone()[0] or 0.0
    
    # Tasks completed (X/Y)
    c.execute("SELECT COUNT(*) FROM tasks WHERE date(created_at) = date('now')")
    total_tasks = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM tasks WHERE is_completed = 1 AND date(created_at) = date('now')")
    completed_tasks = c.fetchone()[0]
    tasks_completed_str = f"{completed_tasks}/{total_tasks}" if total_tasks > 0 else "0/0"
    
    # Focus score
    focus_score = int((completed_tasks / total_tasks * 100)) if total_tasks > 0 else 0
    
    # Days remaining
    exam_date_str = get_exam_date()
    days_remaining = 0
    if exam_date_str:
        try:
            exam_date = datetime.strptime(exam_date_str, "%Y-%m-%d")
            today = datetime.now()
            today_flat = datetime(today.year, today.month, today.day)
            diff = (exam_date - today_flat).days
            days_remaining = max(0, diff)
        except:
            pass
    
    # Recent activity
    c.execute("SELECT subject, created_at FROM study_sessions ORDER BY created_at DESC LIMIT 3")
    recent_data = []
    for r in c.fetchall():
        dt = datetime.strptime(r[1], "%Y-%m-%d %H:%M:%S")
        time_str = dt.strftime("%H:%M")
        recent_data.append({"subject": r[0], "created_at": time_str})
        
    conn.close()
    
    return {
        "hours_today": hours_today,
        "days_remaining": days_remaining,
        "tasks_completed": tasks_completed_str,
        "focus_score": focus_score,
        "recent_activity": recent_data
    }
