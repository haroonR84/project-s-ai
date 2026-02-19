import json
from openai import OpenAI

client = OpenAI()

def decide(case_text):
    prompt = f"""
You are an AI decision engine for business operations.

Analyze the following case and return a decision.

CASE:
{case_text}

RULES:
- Output ONLY valid JSON
- Include the following fields:
  - intent
  - urgency (low, medium, high)
  - confidence (0–1)
  - recommended_action
  - explanation (short, business-focused)
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
    return json.loads(text[start:end])


if __name__ == "__main__":
    sample_case = """
Customer says their order is delayed by 10 days
and they are asking for a refund immediately.
"""

    decision = decide(sample_case)

    with open("decision_output.json", "w", encoding="utf-8") as f:
        json.dump(decision, f, indent=2)

    print("Decision generated and saved.")
