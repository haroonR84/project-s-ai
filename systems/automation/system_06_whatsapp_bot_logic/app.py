import streamlit as st
from openai import OpenAI

client = OpenAI()

st.set_page_config(page_title="WhatsApp AI Support Bot (Simulated)")
st.title("📱 WhatsApp AI Support Bot (Simulation)")

if "stage" not in st.session_state:
    st.session_state.stage = "start"

if "messages" not in st.session_state:
    st.session_state.messages = []

def bot_say(text):
    st.chat_message("assistant").write(text)
    st.session_state.messages.append({"role": "assistant", "content": text})

def user_say(text):
    st.chat_message("user").write(text)
    st.session_state.messages.append({"role": "user", "content": text})

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

user_input = st.chat_input("Message")

if st.session_state.stage == "start":
    bot_say(
        "Welcome to Support 👋\n\n"
        "Please choose an option:\n"
        "1️⃣ Order issue\n"
        "2️⃣ Refund request\n"
        "3️⃣ Speak to agent"
    )
    st.session_state.stage = "menu"

elif user_input:
    user_say(user_input)

    if st.session_state.stage == "menu":
        if user_input.strip() == "1":
            prompt = "Customer has an order issue. Respond politely and ask for order ID."
            st.session_state.stage = "handling"
        elif user_input.strip() == "2":
            prompt = "Customer wants a refund. Respond politely and explain the process."
            st.session_state.stage = "handling"
        elif user_input.strip() == "3":
            bot_say("🔔 Connecting you to a human agent. Please wait.")
            st.session_state.stage = "end"
            st.stop()
        else:
            bot_say("Please reply with 1, 2, or 3.")
            st.stop()

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )

        bot_reply = response.output_text
        bot_say(bot_reply)

    elif st.session_state.stage == "handling":
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=f"Customer replied: {user_input}. Respond politely and help."
        )
        bot_say(response.output_text)
