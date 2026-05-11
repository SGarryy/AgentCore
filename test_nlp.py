from app.nlp.extractor import extract_intent
import json

result = extract_intent("Onboard new employee Sarah, she joins HR on Monday")
print(json.dumps(result, indent=2))