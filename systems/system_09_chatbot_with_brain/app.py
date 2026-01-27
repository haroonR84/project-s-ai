import streamlit as st
import json
from openai import OpenAI

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
                "content": "Output ONLY valid JSON. English only. No explanation."
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


st.set_page_config(page_title="AI Customer Support Chatbot")
st.title("💬 AI Customer Support Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

user_input = st.chat_input("Type your message")

if user_input:
    st.chat_message("user").write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    result = omni_brain(
        message=user_input,
        channel="chat",
        persona={"customer_type": "general"}
    )

    reply = result["reply"]

    st.chat_message("assistant").write(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})
