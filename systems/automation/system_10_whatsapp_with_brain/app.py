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
- Be polite and concise
- Adapt tone to WhatsApp style
- If needed, suggest escalation
- Output ONLY valid JSON with:
  - reply
  - action (answer/escalate)
  - priority (low/medium/high)
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": "Output ONLY valid JSON. English only."
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


st.set_page_config(page_title="WhatsApp AI Support Bot")
st.title("📱 WhatsApp AI Support Bot (Omni-Brain)")

if "stage" not in st.session_state:
    st.session_state.stage = "menu"

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

def bot_say(text):
    st.chat_message("assistant").write(text)
    st.session_state.messages.append({"role": "assistant", "content": text})

def user_say(text):
    st.chat_message("user").write(text)
    st.session_state.messages.append({"role": "user", "content": text})

if st.session_state.stage == "menu":
    bot_say(
        "Welcome 👋 Please choose an option:\n"
        "1️⃣ Order issue\n"
        "2️⃣ Refund request\n"
        "3️⃣ Speak to agent"
    )
    st.session_state.stage = "waiting"

user_input = st.chat_input("Message")

if user_input:
    user_say(user_input)

    if user_input.strip() == "3":
        bot_say("🔔 Connecting you to a human agent.")
        st.stop()

    result = omni_brain(
        message=user_input,
        channel="whatsapp",
        persona={"customer_type": "general"}
    )

    bot_say(result["reply"])
