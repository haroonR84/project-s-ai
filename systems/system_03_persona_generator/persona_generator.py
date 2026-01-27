from openai import OpenAI
from datetime import datetime

client = OpenAI()

def generate_personas(count):
    prompt = f"""
Generate {count} synthetic customer personas.

Each persona must include:
- persona_id
- age_range
- location_type (urban/suburban/rural)
- customer_type (new/returning/premium)
- preferred_channel (chat/whatsapp/voice)
- tone (calm/neutral/angry)
- common_intents (array)
- escalation_likelihood (low/medium/high)

Rules:
- No real people
- No real companies
- Output ONLY a JSON array
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {"role": "system", "content": "Output ONLY valid JSON. No explanation."},
            {"role": "user", "content": prompt}
        ]
    )

    text = response.output[0].content[0].text.strip()
    start = text.find("[")
    end = text.rfind("]") + 1
    return text[start:end]


if __name__ == "__main__":
    count = 8
    personas_json = generate_personas(count)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"customer_personas_{timestamp}.json"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(personas_json)

    print(f"Generated {count} customer personas")
    print(f"Saved to file: {filename}")
