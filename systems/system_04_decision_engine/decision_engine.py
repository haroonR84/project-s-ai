from openai import OpenAI
from datetime import datetime

client = OpenAI()

def decide_action(issue_text, persona):
    prompt = f"""
You are a customer service decision engine.

INPUTS:
Issue:
{issue_text}

Persona:
{persona}

DECIDE AND OUTPUT ONLY JSON WITH:
- action (answer/escalate)
- priority (low/medium/high)
- response_tone (calm/neutral/empathetic)
- suggested_reply (1–2 sentences)
- confidence_score (0.0–1.0)

Rules:
- Output ONLY valid JSON object
- No explanations
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {"role": "system", "content": "Output ONLY valid JSON. No text."},
            {"role": "user", "content": prompt}
        ]
    )

    text = response.output[0].content[0].text.strip()
    start = text.find("{")
    end = text.rfind("}") + 1
    return text[start:end]


if __name__ == "__main__":
    issue_text = "My order was delayed and no one is responding."
    persona = {
        "customer_type": "returning",
        "tone": "angry",
        "preferred_channel": "whatsapp",
        "escalation_likelihood": "high"
    }

    decision_json = decide_action(issue_text, persona)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"decision_{timestamp}.json"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(decision_json)

    print("Decision generated")
    print(f"Saved to file: {filename}")
