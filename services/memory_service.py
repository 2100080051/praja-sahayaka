import json
import os
from datetime import datetime

HISTORY_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "conversation_history.json")

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def save_interaction(user_text: str, agent_response: str, plan: dict = None):
    history = load_history()
    
    entry = {
        "timestamp": datetime.now().isoformat(),
        "user_input": user_text,
        "agent_response": agent_response,
        "plan_details": plan
    }
    
    history.append(entry)
    
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
    
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def get_recent_context(limit=3):
    history = load_history()
    recent = history[-limit:]
    context_str = ""
    for item in recent:
        context_str += f"User: {item['user_input']}\nAgent: {item['agent_response']}\n"
    return context_str
