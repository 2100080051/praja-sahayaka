# Deployment Guide for Praja Sahayaka (Voice Agent)

Your application is now ready for deployment on **Streamlit Cloud**.

## 1. Prerequisites
- A GitHub account.
- A Streamlit Cloud account (sign up at share.streamlit.io).
- Your `GROQ_API_KEY`.

## 2. Repository Setup
1. Push this entire project folder to a new **GitHub Repository**.
2. Ensure the following files are in the root:
   - `app.py`
   - `requirements.txt`
   - `packages.txt`
   - `services/` folder
   - `sr_handler.py`

## 3. Deployment Steps
1. Log in to [Streamlit Cloud](https://share.streamlit.io/).
2. Click **"New app"**.
3. Select your GitHub repository, branch (usually `main`), and set "Main file path" to `app.py`.
4. **BEFORE** clicking Deploy, click **"Advanced settings"**.

## 4. Configure Secrets
1. In the Advanced Settings dialog, go to the **"Secrets"** section.
2. Add your Groq API key:
   ```toml
   GROQ_API_KEY = "your_actual_api_key_here"
   ```
3. Click "Save".

## 5. Deploy
1. Click **"Deploy!"**.
2. Streamlit Cloud will:
   - Install Python dependencies from `requirements.txt`.
   - Install system dependencies (ffmpeg) from `packages.txt`.
   - Start the app using `streamlit run app.py`.

## Notes on Persistence
- The conversation history is currently saved to a local JSON file (`data/conversation_history.json`).
- **Important**: On Streamlit Cloud, this file will be reset whenever the app restarts or goes to sleep. For permanent storage, consider connecting a database (like Google Sheets, Supabase, or Firestore).

## Notes on Audio
- The app uses `streamlit-mic-recorder` which works well on mobile and desktop browsers over HTTPS (which Streamlit Cloud provides automatically).
