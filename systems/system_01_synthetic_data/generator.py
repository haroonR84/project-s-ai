from openai import OpenAI
import json
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
        input=prompt
    )

    return response.output_text


if __name__ == "__main__":
    data_type = "frequently asked questions"
    count = 10

    output = generate_synthetic_data(data_type, count)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{data_type.replace(' ', '_')}_{timestamp}.json"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(output)

    print(f"Generated {count} {data_type}")
    print(f"Saved to file: {filename}")
