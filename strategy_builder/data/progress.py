# -*- coding: utf-8 -*-
import os, json
PROGRESS_FILE = os.path.join(os.getcwd(), "last_session.json")

def save_progress(strategy_id: int, step: int):
    try:
        with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
            json.dump({"strategy_id": strategy_id, "step": step}, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

def load_progress():
    try:
        with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None
