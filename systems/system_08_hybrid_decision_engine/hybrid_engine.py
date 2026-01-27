import json
from openai import OpenAI

client = OpenAI()

BUSINESS_RULES = [
    {
        "condition": "refund" in "refund",
        "action": "Escalate to billing team",
        "urgency": "high",
        "rule_name": "Refund Requests"
    },
    {
        "condition": "password" in "password",
        "action": "Send password reset instructions",
        "urgency": "low",
        "rule_name": "Password Reset"
    }
]

def apply_rules(case_text):
    text = case_text.lower()
    for rule in BUSINESS_RULES:
        if rule["rule_name"].lower().split()[0] in text:
            return {
                "source": "rule",
                "intent": rule["rule_name"],
                "urgency": rule["urgency"],
                "recommended_action": rule["action"],
                "confidence": 1.0,
                "explanation": f"Matched business rule: {rule['rule_name']}"
            }
    return None

def ai_decide(case_text):
    prompt = f"""
You are an AI decision engine.

Analyze the case and return a decision.

CASE:
{case_text}

Return JSON with:
- intent
- urgency (low, medium, high)
- confidence (0–1)
- recommended_action
- explanation
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {"role": "system", "content": "Return JSON only."},
            {"role": "user", "content": prompt}
        ]
    )

    text = response.output_text.strip()
    start = text.find("{")
    end = text.rfind("}") + 1
    result = json.loads(text[start:end])
    result["source"] = "ai"
    return result

if __name__ == "__main__":
    case = "Customer is asking for a refund due to delayed delivery."

    rule_result = apply_rules(case)

    if rule_result:
        decision = rule_result
    else:
        decision = ai_decide(case)

    with open("hybrid_decision.json", "w", encoding="utf-8") as f:
        json.dump(decision, f, indent=2)

    print("Hybrid decision generated and saved.")
