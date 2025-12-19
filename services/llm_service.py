import os
import json
import requests
from dotenv import load_dotenv

import streamlit as st

load_dotenv()

# Try getting from secrets first (Streamlit Cloud), then env (Local)
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except (FileNotFoundError, KeyError, AttributeError):
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def query_llm(messages, model="llama-3.3-70b-versatile"):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": model,
        "messages": messages,
        "temperature": 0.3
    }
    
    response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        print(f"Groq API Error: {response.status_code} - {response.text}")
        return None

def planner_agent(user_input: str):
    system_prompt = """
    You are the Planner Agent for 'Praja Sahayaka'.
    Your goal is to precisely understand the user's intent.
    
    Actions:
    1. explain_scheme: Params: {"scheme_name": "..."}
    2. check_eligibility: Params: {"scheme_name": "...", "user_data": {...}}
    3. generate_checklist: Params: {"scheme_name": "..."}
    4. general_chat: Params: {}
    5. ask_missing_info: Params: {"missing_fields": [...]}
    
    Output ONLY valid JSON.
    """
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"User Input: {user_input}"}
    ]
    
    response = query_llm(messages)
    try:
        clean = response.replace("```json", "").replace("```", "").strip()
        return json.loads(clean)
    except:
        return {"action": "general_chat"}

def translator_to_telugu(text: str):
    return query_llm([{"role": "user", "content": f"Translate to Telugu: {text}"}])
