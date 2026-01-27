import json
from openai import OpenAI

client = OpenAI()

def generate_personas(count=5):
    prompt = f"""
You are a synthetic persona generator.

Create {count} realistic synthetic personas.

RULES:
- No real people
- Business-safe
- Diverse roles and industries
- Output ONLY valid JSON
- Each persona must include:
  - name
  - role
  - industry
  - pain_points (array)
  - goals (array)
  - communication_style
  - typical_requests (array)
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": "Output JSON only. No explanation."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    text = response.output_text.strip()
    start = text.find("[")
    end = text.rfind("]") + 1

    return json.loads(text[start:end])


if __name__ == "__main__":
    personas = generate_personas(5)

    with open("synthetic_personas.json", "w", encoding="utf-8") as f:
        json.dump(personas, f, indent=2)

    print("Synthetic personas generated and saved.")
