import os
import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(
page_title="Pixi AI",
page_icon="✦",
layout="centered"
)

SYSTEM_PROMPT = """
You are Pixi AI, a capable, thoughtful personal AI assistant.
You can communicate fluently in Bangla and English.
Reply in the language the user uses.
If they mix Bangla and English, naturally mirror that style.
Be intelligent, analytical, accurate, practical, and clear.
Think carefully before answering.
Do not fabricate facts, sources, quotations, or capabilities.
State uncertainty honestly.
Ask a concise clarification only when essential.
Avoid unnecessary praise and filler.
Use headings, bullets, examples, and step-by-step explanations when useful.
For current facts, say when information may be outdated unless live browsing is available.
You are text-only. Never claim to have voice features or access to the user's device/files.
"""

st.markdown("""

""", unsafe_allow_html=True)

Sidebar
with st.sidebar:
st.title("✦ Pixi AI")
st.caption("Your personal text assistant")
st.caption("Model: Gemini 3.8 Flash")
st.divider()


st.markdown("**Settings**")

if st.button("＋ New chat", use_container_width=True):
    st.session_state.messages = []
    st.rerun()

st.caption("Chat history stays in this browser session only.")
st.caption("Powered by Google Gemini.")

Initialize chat history
if "messages" not in st.session_state:
st.session_state.messages = []

Header
st.markdown(
'✦ Pixi AI'
'বাংলা ও English — ask anything.',
unsafe_allow_html=True
)

Read Gemini API key
try:
api_key = st.secrets.get("GEMINI_API_KEY", None)
except Exception:
api_key = None

api_key = api_key or os.getenv("GEMINI_API_KEY")

if not api_key:
st.warning(
"শুরু করতে Gemini API Key যোগ করতে হবে। "
"Streamlit Secrets-এ GEMINI_API_KEY সেট করুন।"
)
st.stop()

Initialize Gemini
client = genai.Client(api_key=api_key)

Display previous messages
for msg in st.session_state.messages:
with st.chat_message(msg["role"]):
st.markdown(msg["content"])

Chat input
prompt = st.chat_input("এখানে লিখুন... / Type your message...")

if prompt:
with st.chat_message("user"):
st.markdown(prompt)


# Prepare conversation history
contents = []

for msg in st.session_state.messages:
    role = "user" if msg["role"] == "user" else "model"
    contents.append({
        "role": role,
        "parts": [{"text": msg["content"]}]
    })

contents.append({
    "role": "user",
    "parts": [{"text": prompt}]
})

with st.chat_message("assistant"):
    with st.spinner("Pixi ভাবছে..."):
        try:
            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    max_output_tokens=2500
                )
            )

            answer = response.text or "দুঃখিত, এবার কোনো উত্তর পাওয়া যায়নি।"

            st.markdown(answer)

            st.session_state.messages.append({
                "role": "user",
                "content": prompt
            })

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })

        except Exception as e:
            st.error("সমস্যা হয়েছে। Gemini API Key ও Model Access পরীক্ষা করুন।")
            st.caption(str(e))
