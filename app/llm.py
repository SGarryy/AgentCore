import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "mistral"


def generate_response(agent_result: dict, user_input: str) -> str:
    prompt = f"""You are AgentCore, an intelligent enterprise automation assistant.

A user submitted this request:
"{user_input}"

The following agent handled it:
Agent: {agent_result['agent']}
Status: {agent_result['status']}
Steps completed:
{chr(10).join(agent_result['steps'])}
Result: {agent_result['output']}

Write a short, friendly, professional 2-3 sentence summary of what was accomplished.
Do not repeat the steps. Just summarize the outcome naturally."""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )
        data = response.json()
        return data.get("response", agent_result["output"]).strip()
    except Exception as e:
        return agent_result["output"]