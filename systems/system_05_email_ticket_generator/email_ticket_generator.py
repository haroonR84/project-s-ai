import json
from openai import OpenAI

client = OpenAI()

def load_personas():
    with open("../system_03_persona_generator/synthetic_personas.json", "r", encoding="utf-8") as f:
        return json.load(f)

def generate_items(personas, count=6):
    prompt = f"""
You are a synthetic email and support ticket generator.

Using the following personas:
{json.dumps(personas, indent=2)}

Create {count} realistic business communications.

RULES:
- Mix email and support ticket formats
- Use different personas
- Each item must include:
  - persona_name
  - channel (email or ticket)
  - subject
  - body
  - intent
  - urgency (low, medium, high)
  - expected_action (reply, resolve, escalate)
- No real people or companies
- Output ONLY valid JSON array
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {"role": "system", "content": "Output JSON only. No explanation."},
            {"role": "user", "content": prompt}
        ]
    )

    text = response.output_text.strip()
    start = text.find("[")
    end = text.rfind("]") + 1
    return json.loads(text[start:end])


if __name__ == "__main__":
    personas = load_personas()
    items = generate_items(personas, count=6)

    with open("synthetic_emails_tickets.json", "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2)

    print("Synthetic emails and support tickets generated and saved.")
