import json
from openai import OpenAI

client = OpenAI()

def load_personas():
    with open("../system_03_persona_generator/synthetic_personas.json", "r", encoding="utf-8") as f:
        return json.load(f)

def generate_conversations(personas, count=5):
    prompt = f"""
You are a synthetic conversation generator.

Using the following personas:
{json.dumps(personas, indent=2)}

Create {count} realistic customer service conversations.

RULES:
- Use different personas
- Mix channels: chat, whatsapp, voice
- Each conversation must include:
  - persona_name
  - channel
  - intent
  - turns (array of {{role, message}})
  - outcome (resolved or escalated)
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
    conversations = generate_conversations(personas, count=5)

    with open("synthetic_conversations.json", "w", encoding="utf-8") as f:
        json.dump(conversations, f, indent=2)

    print("Synthetic conversations generated and saved.")
