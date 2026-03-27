import os
import json
import requests

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def analyze_with_openai(text):
    url = "https://api.openai.com/v1/responses"

    prompt = f"""
You are a smart CRM AI assistant.

Understand the BUSINESS INTENT of the message.

Message:
{text}

Return ONLY JSON:

{{
  "intent": "High purchase intent | Interested lead | Not interested",
  "score": number,
  "priority": "high | medium | low",
  "status": "Hot | Warm | Cold",
  "next_action": "text",
  "next_action_type": "send_pricing | schedule_demo | send_followup | close_lead"
}}

Rules:
- Asking price/quote/cost → HIGH (85–95)
- Asking demo/details → MEDIUM (60–75)
- Rejecting → LOW (10–35)
- Think like sales expert, not keyword matcher
"""

    response = requests.post(
        url,
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "gpt-4.1-mini",
            "input": prompt
        },
        timeout=60
    )

    data = response.json()

    # extract output text
    output_text = ""
    for item in data.get("output", []):
        if item.get("type") == "message":
            for c in item.get("content", []):
                if c.get("type") == "output_text":
                    output_text += c.get("text", "")

    return json.loads(output_text)