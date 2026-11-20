# Pixi AI — Personal Text Assistant

A simple bilingual (Bangla + English) text-to-text AI chat app built with Streamlit and the OpenAI Responses API.

## What it includes
- Bangla and English conversations
- Context carried across turns in the current chat
- New chat button
- Selectable model
- API key kept outside the source code

## Requirements
- Python 3.10+
- An OpenAI API key with API billing/credits enabled
- Internet connection

## Run on Windows / macOS / Linux

1. Install Python 3.10 or newer.
2. Extract this ZIP and open a terminal in the `pixi_ai` folder.
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set your API key.

   **Windows PowerShell**
   ```powershell
   $env:OPENAI_API_KEY="your_api_key_here"
   ```

   **macOS / Linux**
   ```bash
   export OPENAI_API_KEY="your_api_key_here"
   ```

5. Start Pixi AI:

   ```bash
   streamlit run app.py
   ```

6. The app opens in your browser, usually at `http://localhost:8501`.

## API key safety
- Never share your API key or upload it publicly.
- Do not paste the key into `app.py`.
- API usage may cost money. Set a usage limit/budget in your API account.
- Chat messages are sent to the API provider to generate responses.

## Notes
- This starter version keeps chat history in Streamlit's current session only.
- Starting a new chat clears the current conversation context.
- The app does not have voice, web browsing, file upload, or permanent memory yet.
- If a model is unavailable to your API account, choose another model available to your account in the sidebar.