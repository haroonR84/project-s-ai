from openai import OpenAI
import json

client = OpenAI()

def omni_brain(message, channel, persona=None):
    persona = persona or {}

    prompt = f"""
You are a unified customer service AI brain.

CHANNEL: {channel}

USER MESSAGE:
{message}

PERSONA:
{json.dumps(persona)}

RULES:
- ALWAYS respond in clear professional English
- Be polite, helpful, and concise
- Adapt tone to the channel
- If the issue is serious, suggest escalation
- Output ONLY valid JSON with these fields:
  - reply
  - action (answer/escalate)
  - priority (low/medium/high)
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": "Output ONLY valid JSON. No explanation. English only."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    text = response.output[0].content[0].text.strip()

    start = text.find("{")
    end = text.rfind("}") + 1

    return json.loads(text[start:end])


if __name__ == "__main__":
    test_message = "My refund is taking too long"
    test_channel = "whatsapp"
    test_persona = {
        "customer_type": "returning",
        "tone": "angry"
    }

    result = omni_brain(test_message, test_channel, test_persona)
    print(result)
