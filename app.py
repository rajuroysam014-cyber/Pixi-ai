import os
import time
import streamlit as st
from google import genai
from google.genai import types

# Page settings
st.set_page_config(
    page_title="Pixi AI",
    page_icon="✦",
    layout="centered"
)

# System instructions
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

# Custom CSS
st.markdown("""
<style>
    .stApp {
        max-width: 900px;
        margin: auto;
    }
    [data-testid="stChatMessage"] {
        border-radius: 14px;
    }
    .hero {
        padding: 18px 4px 8px 4px;
    }
    .hero h1 {
        margin-bottom: 0;
    }
    .muted {
        color: #888;
        font-size: .92rem;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("✦ Pixi AI")
    st.caption("Your personal text assistant")
    st.caption("Model: Gemini Flash")
    st.divider()

    st.markdown("**Settings**")

    if st.button("＋ New chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.caption("Chat history stays in this browser session only.")
    st.caption("Powered by Google Gemini.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Header
st.markdown(
    '<div class="hero"><h1>✦ Pixi AI</h1>'
    '<div class="muted">বাংলা ও English — ask anything.</div></div>',
    unsafe_allow_html=True
)

# Read API key
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

# Initialize Gemini client
client = genai.Client(api_key=api_key)

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
prompt = st.chat_input("এখানে লিখুন... / Type your message...")

if prompt:

    # Display user message
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

    # Assistant response
    with st.chat_message("assistant"):

        with st.spinner("Pixi ভাবছে..."):

            models = [
                "gemini-3.8-flash",
                "gemini-3.5-flash-lite"
            ]

            answer = None
            last_error = None

            for model in models:

                # Retry up to 2 times per model
                for attempt in range(2):

                    try:
                        response = client.models.generate_content(
                            model=model,
                            contents=contents,
                            config=types.GenerateContentConfig(
                                system_instruction=SYSTEM_PROMPT,
                                max_output_tokens=2500
                            )
                        )

                        if response.text:
                            answer = response.text
                            break

                        last_error = Exception(
                            "Gemini কোনো text response দেয়নি।"
                        )
                        break

                    except Exception as e:

                        last_error = e
                        error_text = str(e).upper()

                        # Retry or switch model for temporary errors
                        if (
                            "503" in error_text
                            or "UNAVAILABLE" in error_text
                            or "404" in error_text
                            or "NOT_FOUND" in error_text
                        ):

                            if attempt == 0:
                                time.sleep(3)
                                continue

                            break

                        else:
                            st.error(
                                "Gemini API-তে সমস্যা হয়েছে।"
                            )
                            st.caption(str(e))
                            break

                if answer:
                    break

            # Show final answer
            if answer:

                st.markdown(answer)

                st.session_state.messages.append({
                    "role": "user",
                    "content": prompt
                })

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            else:

                st.error(
                    "দুঃখিত! Pixi এখন উত্তর দিতে পারছে না।"
                )

                if last_error:
                    st.caption(str(last_error))
