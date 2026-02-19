import streamlit as st
import sounddevice as sd
import scipy.io.wavfile as wav
import tempfile
from openai import OpenAI

client = OpenAI()

st.set_page_config(page_title="Voice Customer Service Agent")
st.title("🎧 Voice Customer Service Agent")

SAMPLE_RATE = 44100
DURATION = 5  # seconds

st.write("Click record, speak your issue, and wait for AI voice reply.")

if st.button("🎙️ Record"):
    st.write("Recording...")
    audio = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1)
    sd.wait()

    temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    wav.write(temp_audio.name, SAMPLE_RATE, audio)

    st.write("Processing...")

    # Speech to Text
    with open(temp_audio.name, "rb") as f:
        transcript = client.audio.transcriptions.create(
            model="gpt-4o-transcribe",
            file=f
        )

    user_text = transcript.text
    st.write(f"🗣️ You said: {user_text}")

    # AI response
    response = client.responses.create(
    model="gpt-4.1-mini",
    input=[
        {
            "role": "system",
            "content": "You are a customer service AI. ALWAYS respond in clear, professional English only."
        },
        {
            "role": "user",
            "content": f"Customer said: {user_text}. Respond politely and helpfully."
        }
    ]
)

    reply_text = response.output_text
    st.write(f"🤖 AI says: {reply_text}")

    # Text to Speech
    speech = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=reply_text
    )

    audio_bytes = speech.read()
    st.audio(audio_bytes, format="audio/wav")
