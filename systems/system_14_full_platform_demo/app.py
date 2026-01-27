import streamlit as st
import json
import csv
import os
import tempfile
from datetime import datetime
from openai import OpenAI

# ================= SETUP =================
client = OpenAI()
LOG_FILE = "conversation_logs.csv"

st.set_page_config(page_title="AI Customer Service Platform", layout="centered")
st.title("🧠 AI Customer Service Platform Demo")

# ================= LOGGING =================
def log_event(channel, message, action, priority, source):
    file_exists = os.path.isfile(LOG_FILE)
    with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(
                ["timestamp", "channel", "message", "action", "priority", "source"]
            )
        writer.writerow(
            [datetime.now().isoformat(), channel, message, action, priority, source]
        )

# ================= AI FUNCTIONS =================
def classify_question(message):
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=f"""
Classify the following message.
Reply with ONLY one word:
- knowledge
- general

Message:
{message}
"""
    )
    return response.output_text.strip().lower()

def answer_from_knowledge(message, knowledge_text):
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=f"""
You are a customer support AI.

KNOWLEDGE BASE:
{knowledge_text}

QUESTION:
{message}

RULES:
- Answer ONLY using the knowledge base
- If the answer is not present, say:
  "I'm sorry, I don't have that information."
- English only
"""
    )
    return response.output_text

def omni_brain(message, channel):
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=f"""
You are a professional customer service AI.

CHANNEL: {channel}
CUSTOMER MESSAGE:
{message}

RULES:
- English only
- Polite, clear, and helpful
"""
    )
    return response.output_text

# ================= LOAD KNOWLEDGE =================
with open("../system_11_knowledge_base/knowledge.txt", "r", encoding="utf-8") as f:
    knowledge = f.read()

# ================= UI STATE =================
channel = st.selectbox("Select Channel", ["chat", "whatsapp", "voice"])

if "messages" not in st.session_state:
    st.session_state.messages = []

# ================= RENDER CHAT HISTORY =================
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# ================= INPUT HANDLING =================
user_input = None

if channel == "voice":
    st.markdown("### 🎤 Voice Input")
    audio = st.audio_input("Record your voice")

    if audio is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(audio.read())
            audio_path = tmp.name

        transcript = client.audio.transcriptions.create(
            model="gpt-4o-transcribe",
            file=open(audio_path, "rb")
        )

        user_input = transcript.text
        st.markdown(f"**🗣️ You said:** {user_input}")

else:
    user_input = st.chat_input("Type customer message here...")

# ================= PROCESS MESSAGE =================
if user_input:
    st.chat_message("user").write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    category = classify_question(user_input)

    if category == "knowledge":
        reply = answer_from_knowledge(user_input, knowledge)
        source = "knowledge_base"
    else:
        reply = omni_brain(user_input, channel)
        source = "general_ai"

    action = "escalate" if "manager" in reply.lower() else "answer"
    priority = "high" if "delay" in user_input.lower() else "medium"

    log_event(channel, user_input, action, priority, source)

    st.chat_message("assistant").write(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})
