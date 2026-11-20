import os
import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Pixi AI", page_icon="✦", layout="centered")

SYSTEM_PROMPT = """
You are Pixi AI, a capable, thoughtful personal AI assistant.
You can communicate fluently in Bangla and English. Reply in the language the user uses;
if they mix Bangla and English, naturally mirror that style.
Be intelligent, analytical, accurate, practical, and clear. Think carefully before answering.
Do not fabricate facts, sources, quotations, or capabilities. State uncertainty honestly.
Ask a concise clarification only when essential. Avoid unnecessary praise and filler.
Use headings, bullets, examples, and step-by-step explanations when useful.
For current facts, say when information may be outdated unless live browsing is available.
You are text-only. Never claim to have voice features or access to the user's device/files
unless explicitly provided in the conversation.
"""

st.markdown("""
<style>
    .stApp {max-width: 900px; margin: auto;}
    [data-testid="stChatMessage"] {border-radius: 14px;}
    .hero {padding: 18px 4px 8px 4px;}
    .hero h1 {margin-bottom: 0;}
    .muted {color: #888; font-size: .92rem;}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("✦ Pixi AI")
    st.caption("Your personal text assistant")
    model = "gpt-5.5"
    st.caption("Model: GPT-5.5")
    st.divider()
    st.markdown("**Settings**")
    if st.button("＋ New chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.previous_response_id = None
        st.rerun()
    st.caption("Chat history stays in this browser session only.")
    st.caption("API key is read from Streamlit Secrets or environment variables.")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "previous_response_id" not in st.session_state:
    st.session_state.previous_response_id = None

st.markdown('<div class="hero"><h1>✦ Pixi AI</h1><div class="muted">বাংলা ও English — ask anything.</div></div>',
            unsafe_allow_html=True)

try:
    api_key = st.secrets.get("OPENAI_API_KEY", None)
except Exception:
    api_key = None
api_key = api_key or os.getenv("OPENAI_API_KEY")

if not api_key:
    st.warning("শুরু করতে OpenAI API key যোগ করতে হবে। নিচের README.md ফাইলে সেটআপের নিয়ম দেওয়া আছে।")
    st.stop()

client = OpenAI(api_key=api_key)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("এখানে লিখুন... / Type your message...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Pixi ভাবছে..."):
            try:
                kwargs = {
                    "model": model,
                    "instructions": SYSTEM_PROMPT,
                    "input": prompt,
                    "max_output_tokens": 2500,
                }
                if st.session_state.previous_response_id:
                    kwargs["previous_response_id"] = st.session_state.previous_response_id

                response = client.responses.create(**kwargs)
                answer = response.output_text or "দুঃখিত, এবার কোনো উত্তর পাওয়া যায়নি।"
                st.session_state.previous_response_id = response.id
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error("সমস্যা হয়েছে। API key, model access এবং internet connection পরীক্ষা করুন।")
                st.caption(str(e))
                st.session_state.messages.pop()