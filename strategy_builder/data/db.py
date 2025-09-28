# -*- coding: utf-8 -*-
import os, sqlite3, datetime, json

DB_PATH = os.path.join(os.getcwd(), "strategies.db")

def get_conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    conn = get_conn()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS strategies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS strategy_components (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            strategy_id INTEGER NOT NULL,
            vision TEXT,
            message TEXT,
            goals TEXT,
            strategic_values TEXT,
            updated_at TEXT NOT NULL,
            FOREIGN KEY(strategy_id) REFERENCES strategies(id)
        )
    """)
    conn.commit()
    return conn

def create_strategy(name: str) -> int:
    conn = get_conn()
    c = conn.cursor()
    now = datetime.datetime.now().isoformat(timespec="seconds")
    c.execute("INSERT INTO strategies (name, created_at) VALUES (?, ?)", (name, now))
    conn.commit()
    return c.lastrowid

def upsert_components(strategy_id: int, vision: str, message: str, goals: list, values: list):
    conn = get_conn()
    c = conn.cursor()
    now = datetime.datetime.now().isoformat(timespec="seconds")
    goals_json = json.dumps(goals, ensure_ascii=False)
    values_json = json.dumps(values, ensure_ascii=False)
    row = c.execute("SELECT id FROM strategy_components WHERE strategy_id=?", (strategy_id,)).fetchone()
    if row:
        c.execute("""UPDATE strategy_components
                     SET vision=?, message=?, goals=?, strategic_values=?, updated_at=?
                     WHERE strategy_id=?""", (vision, message, goals_json, values_json, now, strategy_id))
    else:
        c.execute("""INSERT INTO strategy_components (strategy_id, vision, message, goals, strategic_values, updated_at)
                     VALUES (?,?,?,?,?,?)""", (strategy_id, vision, message, goals_json, values_json, now))
    conn.commit()

def get_strategy(strategy_id: int):
    conn = get_conn()
    c = conn.cursor()
    s = c.execute("SELECT id,name,created_at FROM strategies WHERE id=?", (strategy_id,)).fetchone()
    if not s: return None
    comp = c.execute("SELECT vision,message,goals,strategic_values,updated_at FROM strategy_components WHERE strategy_id=?", (strategy_id,)).fetchone()
    data = {"id": s[0], "name": s[1], "created_at": s[2]}
    if comp:
        data.update({
            "vision": comp[0] or "",
            "message": comp[1] or "",
            "goals": json.loads(comp[2]) if comp[2] else [],
            "values": json.loads(comp[3]) if comp[3] else [],
            "updated_at": comp[4]
        })
    else:
        data.update({"vision":"", "message":"", "goals":[], "values":[], "updated_at":None})
    return data

def list_strategies():
    conn = get_conn()
    c = conn.cursor()
    rows = c.execute("SELECT id,name,created_at FROM strategies").fetchall()
    return [{"id":r[0], "name":r[1], "created_at":r[2]} for r in rows]

def delete_strategy(strategy_id: int):
    conn = get_conn()
    c = conn.cursor()
    c.execute("DELETE FROM strategy_components WHERE strategy_id=?", (strategy_id,))
    c.execute("DELETE FROM strategies WHERE id=?", (strategy_id,))
    conn.commit()

def clone_strategy(strategy_id: int):
    s = get_strategy(strategy_id)
    if not s: return None
    new_id = create_strategy(f"{s['name']} - نسخة")
    upsert_components(new_id, s["vision"], s["message"], s["goals"], s["values"])
    return new_id


def update_strategy_name(strategy_id: int, name: str):
    conn = get_conn()
    c = conn.cursor()
    c.execute("UPDATE strategies SET name=? WHERE id=?", (name, strategy_id))
    conn.commit()
