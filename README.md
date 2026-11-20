✦ Pixi AI — Personal Text Assistant

A simple bilingual (Bangla + English) text-to-text AI chat app built with Streamlit and the Google Gemini API.

What it includes

- Bangla and English conversations
- Context carried across turns in the current chat
- New chat button
- Powered by Google Gemini
- Gemini API key kept outside the source code

Requirements

- Python 3.10+
- A Google Gemini API key
- Internet connection

Run on Windows / macOS / Linux

1. Install Python 3.10 or newer.

2. Download or extract this project and open a terminal in the "pixi_ai" folder.

3. Install dependencies:

pip install -r requirements.txt

4. Set your Gemini API key.

Windows PowerShell

$env:GEMINI_API_KEY="your_gemini_api_key_here"

macOS / Linux

export GEMINI_API_KEY="your_gemini_api_key_here"

5. Start Pixi AI:

streamlit run app.py

6. The app opens in your browser, usually at "http://localhost:8501".

API Key Safety

- Never share your Gemini API key.
- Do not upload your API key publicly.
- Do not paste the key into "app.py".
- API usage may cost money. Check your Google AI Studio usage limits.
- Chat messages are sent to Google Gemini to generate responses.

Notes

- Chat history stays in Streamlit's current session only.
- Starting a new chat clears the current conversation context.
- This version is text-only.
- The app does not have voice, web browsing, file upload, or permanent memory.
