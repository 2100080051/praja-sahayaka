import json
import os

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "schemes.json")

def load_schemes():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)["schemes"]

def get_scheme_details(scheme_name_query: str):
    if not scheme_name_query:
        return None
    schemes = load_schemes()
    for scheme in schemes:
        if scheme_name_query.lower() in scheme["id"] or scheme_name_query in scheme["name_telugu"]:
            return scheme
    return None

def check_eligibility(scheme_id: str, user_data: dict):
    schemes = load_schemes()
    target_scheme = next((s for s in schemes if s["id"] == scheme_id), None)
    
    if not target_scheme:
        return {"eligible": False, "reason": "Scheme not found"}

    rules = target_scheme["eligibility_rules"]
    reasons = []
    
    if "occupation" in rules:
        if user_data.get("occupation") not in rules["occupation"]:
            reasons.append(f"Occupation must be one of {rules['occupation']}")
            
    if "income_limit" in rules:
        if user_data.get("income", float('inf')) > rules["income_limit"]:
            reasons.append(f"Income must be less than {rules['income_limit']}")

    if "age_min" in rules:
        if user_data.get("age", 0) < rules["age_min"]:
            reasons.append(f"Age must be at least {rules['age_min']}")

    if reasons:
        return {"eligible": False, "reasons": reasons}
    
    return {"eligible": True, "message": "You are eligible!"}

def get_application_checklist(scheme_id: str):
    schemes = load_schemes()
    target_scheme = next((s for s in schemes if s["id"] == scheme_id), None)
    
    if not target_scheme:
         return None
         
    return target_scheme.get("documents_required", ["Basic KYC documents (Aadhaar, Pan, Bank details)"])

def get_available_schemes():
    schemes = load_schemes()
    return [s["name_telugu"] for s in schemes]
