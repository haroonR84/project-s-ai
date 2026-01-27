from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="gpt-4.1-mini",
    input="Say: OpenAI API connected successfully."
)

print(response.output_text)
