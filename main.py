import streamlit as st
import requests
import os
from dotenv import load_dotenv

# 🔐 Load API key from .env file
load_dotenv()
api_key = st.secrets["OPENROUTER_API_KEY"]

MODEL_NAME = "mistralai/mistral-7b-instruct"

# 🔧 Streamlit page config
st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="centered")
st.markdown("<h2 style='text-align:center;'>🤖 Smart Chatbot </h2><hr>", unsafe_allow_html=True)

# 🎨 Chat bubble styling
st.markdown("""
    <style>
        .message { 
            background-color:#f2f4f8; 
            padding:10px 15px; 
            border-radius:10px; 
            margin-bottom:10px;
            font-family: 'Segoe UI', sans-serif;
            color: #2c3e50;
            line-height: 1.6;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }

        .user { border-left: 5px solid #1f77b4; }
        .assistant { border-left: 5px solid #2ca02c; }

        .stButton button { 
            border-radius: 5px; 
            width: 100%; 
            font-family: 'Segoe UI', sans-serif;
        }
    </style>
""", unsafe_allow_html=True)


# 📦 Session state init
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "You are a helpful assistant."}]

# 🗨️ Chat history display
st.markdown("### 🗨️ Conversation")
for msg in st.session_state.messages[1:]:
    who = "user" if msg["role"] == "user" else "assistant"
    name = "🧑 You" if msg["role"] == "user" else "🤖 Assistant"
    st.markdown(f"<div class='message {who}'><strong>{name}:</strong><br>{msg['content']}</div>", unsafe_allow_html=True)

# ✍️ Input with dynamic key for auto-clear
input_key = f"user_input_{len(st.session_state.messages)}"
user_input = st.text_input("💬 Your message:", key=input_key)
send = st.button("🚀 Send", use_container_width=True)

# 🚀 Handle send
if send and user_input.strip():
    st.session_state.messages.append({"role": "user", "content": user_input})

    payload = {
        "model": MODEL_NAME,
        "messages": st.session_state.messages,
        "max_tokens": 400
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    try:
        res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        if res.status_code == 200:
            reply = res.json()["choices"][0]["message"]["content"]
        elif res.status_code == 402:
            reply = "⚠️ You're out of credits. Visit [OpenRouter Settings](https://openrouter.ai/settings/credits) to upgrade."
        else:
            reply = f"⚠️ Error {res.status_code}: {res.text}"
    except Exception as e:
        reply = f"⚠️ Exception: {e}"

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()  # 🔁 Clear input + refresh

# 🧹 Clear chat button at bottom
if st.button("🧹 Clear Chat", use_container_width=True):
    st.session_state.messages = [{"role": "system", "content": "You are a helpful assistant."}]
    st.rerun()

st.markdown("""
    <hr style="margin-top:2em; margin-bottom:0.5em;">
    <p style='text-align:center; font-size:12px; color:#999'>
        © 2025 <strong>Mishal</strong> — All rights reserved.
    </p>
""", unsafe_allow_html=True)
