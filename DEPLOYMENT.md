# Run and deploy AlnonAI 2.0

## Local run (recommended for the first demo)

1. Install Python 3.10 or newer.
2. Extract the ZIP and open a terminal in the `alnonai_2` folder.
3. Create and activate a virtual environment:

   **Windows PowerShell**
   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   **macOS / Linux**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

4. Install dependencies and run:
   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   streamlit run app.py
   ```
5. Open the local URL shown by Streamlit (normally `http://localhost:8501`). On first run, create a 6–12 digit PIN.

## Run tests

```bash
python -m compileall -q app.py alnonai
pytest -q
```

## Upload to GitHub

Create a new empty repository, then from this folder:

```bash
git init
git add .
git commit -m "Build AlnonAI 2.0 support and healthcare navigator"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git push -u origin main
```

Do not commit `alnonai.sqlite3`, `.env`, `.streamlit/secrets.toml`, personal contacts or private data. `.gitignore` excludes the local database and secrets.

## Streamlit Community Cloud (public demo only)

1. Push the code to GitHub.
2. In Streamlit Community Cloud, create an app from that repository.
3. Set the main file path to `app.py`.
4. Deploy. The service installs `requirements.txt` automatically.

**Important:** this build uses a local SQLite file. Cloud app filesystems can be ephemeral and a public deployment is not a safe place for private contact or safety data. Use fake demo data only. A real multi-user release needs a managed database, user-specific access controls, encryption, retention controls, secure secrets, threat modelling and an independent security review. Do not treat the PIN as production authentication.

## What works without API keys

- PIN setup, PIN verification and lock/unlock.
- Local source-linked retrieval assistant (no external AI API).
- English, Hindi and Telugu UI and curated health/family content.
- Searchable official helplines and support/resource directory.
- Add/delete trusted contacts and local resource entries.
- Personal safety checklist and consent-gated, manual location-message preview.
- Appointment question preparation and practical support signposting.

## Explicit limitations

- No automatic GPS, SMS, WhatsApp, email, push notification or emergency dispatch.
- No external LLM or cloud AI call; retrieval is local and extractive.
- No pre-populated local NGO or rehabilitation-centre directory because listings must be verified for the relevant location.
- No encryption at rest or multi-user authentication; the PIN only gates the app interface.
- No clinical validation, formal translation review, accessibility audit or penetration test has been completed.
