from openai import OpenAI

client = OpenAI()

def answer_from_knowledge(question, knowledge_text):
    prompt = f"""
You are a customer support AI.

KNOWLEDGE BASE:
{knowledge_text}

QUESTION:
{question}

RULES:
- Answer ONLY using the knowledge base
- If the answer is not in the knowledge, say:
  "I'm sorry, I don't have that information."
- Respond in clear professional English
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return response.output_text


if __name__ == "__main__":
    with open("knowledge.txt", "r", encoding="utf-8") as f:
        knowledge = f.read()

    while True:
        q = input("Ask a question (or type exit): ")
        if q.lower() == "exit":
            break

        answer = answer_from_knowledge(q, knowledge)
        print("\nAI:", answer, "\n")
