import streamlit as st
from openai import OpenAI

client = OpenAI()

st.set_page_config(page_title="AI Customer Service Chatbot")

st.title("AI Customer Service Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

user_input = st.chat_input("Type your message...")

if user_input:
    st.chat_message("user").write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    prompt = f"""
You are a customer service chatbot.

User message:
{user_input}

Respond politely, clearly, and helpfully.
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    bot_reply = response.output_text

    st.chat_message("assistant").write(bot_reply)
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
