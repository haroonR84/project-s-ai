from openai import OpenAI
import json

client = OpenAI()

def classify_question(message):
    prompt = f"""
Classify the following user message.

Message:
{message}

Answer ONLY one word:
- knowledge
- general
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return response.output_text.strip().lower()


def answer_from_knowledge(message, knowledge_text):
    prompt = f"""
You are a customer support AI.

KNOWLEDGE BASE:
{knowledge_text}

QUESTION:
{message}

RULES:
- Answer ONLY using the knowledge base
- If not found, say:
  "I'm sorry, I don't have that information."
- English only
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return response.output_text


def omni_brain(message, channel):
    prompt = f"""
You are a unified customer service AI brain.

CHANNEL: {channel}

USER MESSAGE:
{message}

RULES:
- Respond in clear professional English
- Be polite and helpful
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return response.output_text


def unified_brain(message, channel, knowledge_text):
    category = classify_question(message)

    if category == "knowledge":
        reply = answer_from_knowledge(message, knowledge_text)
        source = "knowledge_base"
    else:
        reply = omni_brain(message, channel)
        source = "general_ai"

    return {
        "reply": reply,
        "source": source
    }


if __name__ == "__main__":
    with open("../system_11_knowledge_base/knowledge.txt", "r", encoding="utf-8") as f:
        knowledge = f.read()

    while True:
        msg = input("User: ")
        if msg.lower() == "exit":
            break

        result = unified_brain(msg, "chat", knowledge)
        print("\nAI:", result["reply"])
        print("Source:", result["source"], "\n")
