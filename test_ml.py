from app.ml.router import train_model, route_task

train_model()

tests = [
    "Onboard new employee Sarah to HR team",
    "Flag duplicate invoices from last month",
    "Triage bug on login page crashing",
    "Generate leads from retail sector",
    "Schedule vendor meeting for procurement",
]

print("\n=== Routing Test ===")
for text in tests:
    result = route_task(text)
    print(f"\nInput: {text}")
    print(f"Routed to: {result['routed_to']} (confidence: {result['confidence']})")