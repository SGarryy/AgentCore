import spacy
import re
from datetime import datetime

nlp = spacy.load("en_core_web_sm")

INTENT_KEYWORDS = {
    "hr_agent": ["onboard", "hire", "employee", "recruit", "joining", "staff", "payroll"],
    "finance_agent": ["invoice", "reconcile", "payment", "billing", "expense", "budget", "duplicate"],
    "it_agent": ["bug", "triage", "ticket", "crash", "error", "issue", "support", "fix"],
    "sales_agent": ["lead", "prospect", "customer", "deal", "pitch", "retail", "convert"],
    "operations_agent": ["schedule", "procure", "supply", "logistics", "vendor", "order"],
}

PRIORITY_KEYWORDS = {
    "high": ["urgent", "asap", "critical", "immediately", "emergency", "now"],
    "medium": ["soon", "today", "monday", "this week"],
    "low": ["whenever", "low priority", "sometime", "no rush"],
}

def extract_intent(text: str) -> dict:
    doc = nlp(text.lower())
    entities = {"persons": [], "dates": [], "orgs": [], "misc": []}
    original_doc = nlp(text)
    for ent in original_doc.ents:
        if ent.label_ == "PERSON":
            entities["persons"].append(ent.text)
        elif ent.label_ in ["DATE", "TIME"]:
            entities["dates"].append(ent.text)
        elif ent.label_ == "ORG":
            entities["orgs"].append(ent.text)
        else:
            entities["misc"].append(ent.text)
    detected_intent = "unknown"
    matched_keywords = []
    max_matches = 0
    for agent, keywords in INTENT_KEYWORDS.items():
        matches = [kw for kw in keywords if kw in text.lower()]
        if len(matches) > max_matches:
            max_matches = len(matches)
            detected_intent = agent
            matched_keywords = matches
    detected_priority = "medium"
    for priority, keywords in PRIORITY_KEYWORDS.items():
        if any(kw in text.lower() for kw in keywords):
            detected_priority = priority
            break
    return {
        "raw_text": text,
        "intent": detected_intent,
        "entities": entities,
        "priority": detected_priority,
        "matched_keywords": matched_keywords,
        "timestamp": datetime.now().isoformat()
    }