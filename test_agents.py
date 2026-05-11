from app.nlp.extractor import extract_intent
from app.ml.router import route_task
from app.agents.dispatcher import dispatch

tests = [
    "Onboard new employee Sarah to HR team on Monday",
    "Flag duplicate invoices from last month urgently",
    "Triage bug on login page crashing on mobile",
    "Generate leads from retail sector",
    "Schedule vendor meeting for procurement this week",
]

print("=== AgentCore Full Pipeline Test ===\n")
for text in tests:
    nlp_result = extract_intent(text)
    ml_result = route_task(text)
    agent_result = dispatch(ml_result["routed_to"], nlp_result)

    print(f"Input: {text}")
    print(f"Intent: {nlp_result['intent']} | Routed to: {ml_result['routed_to']} ({ml_result['confidence']})")
    print(f"Agent: {agent_result['agent']} | Status: {agent_result['status']}")
    print(f"Output: {agent_result['output']}")
    print("-" * 60)