from tools.definitions import get_scheme_details, check_eligibility, get_available_schemes, get_application_checklist
from services.llm_service import query_llm
from services.memory_service import get_recent_context
import json

def search_scheme_knowledge(scheme_name: str, search_results=None):
    context = ""
    if search_results:
        context = f"\nHere is some information found online:\n{json.dumps(search_results)}\n"
        
    system_prompt = f"""
    You are an expert on Indian Government Schemes (Telangana, Andhra Pradesh & Central).
    The user is asking about: {scheme_name}.
    {context}
    
    Provide a valid JSON summary of this scheme.
    Format:
    {{
        "name_telugu": "...", 
        "description_telugu": "...", 
        "benefits_telugu": "...", 
        "eligibility_rules": {{...}},
        "state": "Telangana/Andhra Pradesh/Central" 
    }}
    
    If it is a Central scheme, mark state as "Central". 
    If it is specific to a state, mark appropriately.
    If you don't know and no online info helps, return null.
    """
    response = query_llm([{"role": "system", "content": system_prompt}])
    try:
        clean = response.replace("```json", "").replace("```", "").strip()
        data = json.loads(clean)
        return data
    except:
        return None

def executor_agent(plan: dict):
    action = plan.get("action")
    params = plan.get("parameters", {})
    
    if action == "explain_scheme":
        scheme_name = params.get("scheme_name")
        scheme = get_scheme_details(scheme_name)
        
        if scheme:
            # Explicitly add segregation hint for the LLM
            state_map = {
                "telangana": "TELANGANA STATE GOVERNMENT",
                "andhra_pradesh": "ANDHRA PRADESH STATE GOVERNMENT",
                "central": "CENTRAL GOVERNMENT (INDIA)"
            }
            scheme["segregation_hint"] = state_map.get(scheme.get("state"), "GOVERNMENT")
            return {"status": "success", "data": scheme, "type": "scheme_details"}
        else:
            # Try online search
            from tools.definitions import search_online_schemes
            search_results = search_online_schemes(scheme_name)
            
            llm_scheme = search_scheme_knowledge(scheme_name, search_results)
            if llm_scheme:
                 return {"status": "success", "data": llm_scheme, "type": "scheme_details_web", "source": "llm_knowledge_web"}
            
            return {"status": "error", "message": "Scheme not found", "available": get_available_schemes()}

    elif action == "check_eligibility":
        scheme_name = params.get("scheme_name")
        user_data = params.get("user_data", {})
        
        if not scheme_name:
             return {"status": "needs_info", "missing": ["scheme_name"]}
             
        scheme = get_scheme_details(scheme_name)
        if not scheme:
            return {"status": "error", "message": "Scheme not found"}
            
        result = check_eligibility(scheme["id"], user_data)
        return {"status": "success", "data": result, "type": "eligibility_result", "scheme_name": scheme["name_telugu"]}

    elif action == "ask_missing_info":
        return {"status": "needs_info", "missing": params.get("missing_fields")}

    elif action == "generate_checklist":
        scheme_name = params.get("scheme_name")
        if not scheme_name:
             return {"status": "needs_info", "missing": ["scheme_name"]}
             
        scheme = get_scheme_details(scheme_name)
        if not scheme:
             return {"status": "error", "message": "Scheme not found"}
             
        docs = get_application_checklist(scheme["id"])
        return {"status": "success", "data": docs, "type": "checklist", "scheme_name": scheme["name_telugu"]}

    elif action == "general_chat":
        return {"status": "chat", "context": "general_interaction"}
        
    return {"status": "error", "message": "Unknown action"}

def responder_agent(user_input: str, execution_result: dict):
    history_context = get_recent_context()
    
    system_prompt = """
    You are 'Praja Sahayaka', a friendly and knowledgeable AI assistant for Indian Government Schemes.
    
    TONE:
    - Warm, professional, and empathetic (Human-like). 
    - NOT robotic. Use natural Telugu phrasing (e.g., "అవునండి", "ఖచ్చితంగా", "మీరు చెప్పింది నిజమే").
    - Be encouraging.
    
    INSTRUCTIONS:
    - Output MUST be in PURE TELUGU script.
    - Answer accurately based strictly on the provided 'System Execution Result'.
    - If the result contains a checklist, list the documents clearly with bullet points.
    - If eligibility is confirmed, congratulate them warmly.
    - If details are missing, ask for them politely, explaining WHY they are needed.
    - SEGREGATION: Clearly mention if the scheme belongs to TELANGANA, ANDHRA PRADESH, or CENTRAL GOVERNMENT at the beginning of the explanation.
    """
    
    context = f"History:\n{history_context}\n\nCurrent User Input: {user_input}\nSystem Execution Result: {execution_result}"
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": context}
    ]
    
    return query_llm(messages)
