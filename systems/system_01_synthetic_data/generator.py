from openai import OpenAI
from datetime import datetime

client = OpenAI()

def generate_synthetic_data(data_type, count):
    prompt = f"""
You are a synthetic data generator.

Generate {count} realistic {data_type} records.

Rules:
- Do NOT use real company names
- Do NOT use real people
- Make data business-realistic
- Each record must be unique
- Output STRICT JSON array
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": "You ONLY output valid JSON. No text. No explanation."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    output = response.output[0].content[0].text.strip()

    start = output.find("[")
    end = output.rfind("]") + 1

    return output[start:end]


if __name__ == "__main__":
    data_type = "customer support tickets"
    count = 5

    json_output = generate_synthetic_data(data_type, count)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{data_type.replace(' ', '_')}_{timestamp}.json"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(json_output)

    print(f"Generated {count} {data_type}")
    print(f"Saved to file: {filename}")
