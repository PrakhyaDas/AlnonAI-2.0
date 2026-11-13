# AlnonAI 2.0

**From finding support to accessing healthcare.**

AlnonAI is a privacy-conscious support navigator for people and families affected by alcohol-related harm. This repository contains a runnable Streamlit implementation designed to be easy to run locally and upload to GitHub. It preserves the original project's support-navigation purpose while adding a small, source-grounded healthcare information retrieval layer.

## Run it

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Open the local URL printed by Streamlit and create a 6–12 digit PIN on first launch. Full steps: [DEPLOYMENT.md](DEPLOYMENT.md).

## Features implemented

- **Discreet PIN entry:** calculator-styled lock screen; salted PBKDF2 PIN verifier; change PIN and lock app.
- **Support assistant:** local BM25-style lexical retrieval over a curated multilingual knowledge base; source links displayed with answers; unknown questions return a no-match response instead of invented advice.
- **Healthcare information:** plain-language health literacy, family wellbeing, appointment question preparation and health-topic retrieval.
- **Urgency recognition:** conservative English/Hindi/Telugu phrase flags that show an emergency referral message; this is not a clinical triage system.
- **Support directory:** official India emergency, mental-health, child-support, legal-aid and education portal entries; search/filter; add local NGO, rehabilitation and other provider entries with source URLs.
- **Emergency and trusted contacts:** call links for published helplines, add/delete trusted contacts and create a session-only safety checklist.
- **Consent-based location sharing:** no GPS access; user manually enters an approximate location, explicitly consents and receives a message preview to share themselves. Nothing is transmitted automatically.
- **Education, employment, legal and financial signposting.**
- **Languages and accessibility:** English, Hindi and Telugu UI labels and selected curated content; semantic headings, standard Streamlit controls, keyboard focus styling and high-contrast theme.
- **Privacy disclosures:** chat is session-only; local contacts/resources are stored in SQLite; limitations are shown in the app.

## Technical design

- Python + Streamlit UI
- SQLite persistence for trusted contacts, resources and settings
- PBKDF2-HMAC-SHA256 PIN verifier with per-PIN random salt
- Local BM25-style lexical retrieval with Unicode tokenisation
- JSON knowledge base with source URL, title, language, topic and review date
- Rule-based urgent phrase detector, separate from retrieval

## Tests

```bash
python -m compileall -q app.py alnonai
pytest -q
```

GitHub Actions runs compilation and tests on pushes and pull requests.

## Safety and privacy limits

This is a student prototype, not a medical device, diagnosis system, treatment service or emergency-response service. It has not been clinically validated, translation-reviewed, security-audited or penetration-tested. Urgency detection can miss emergencies. For immediate danger in India, call 112 or seek emergency care. The app never sends alerts or location automatically.

The PIN is an app-level gate, **not encryption**. SQLite data is not encrypted at rest. Streamlit cloud storage may be ephemeral; use fake data for public demos. A production release needs per-user authentication, managed encrypted storage, consent and retention controls, clinician review, translation review and security testing.

## Important product scope decision

The original AlnonAI GitHub project is an Expo/React Native app. This Streamlit implementation is a complete runnable alternative for a fast prototype and competition demonstration; it is not a merge into the original mobile codebase. The two codebases should not be represented as one integrated app until a deliberate migration is completed.

See [DEPLOYMENT.md](DEPLOYMENT.md), [SOURCE_REGISTER.md](SOURCE_REGISTER.md), [ARCHITECTURE.md](ARCHITECTURE.md), [DATA_GOVERNANCE.md](DATA_GOVERNANCE.md), [DEMO_SCRIPT.md](DEMO_SCRIPT.md), [IMPLEMENTATION_AUDIT.md](IMPLEMENTATION_AUDIT.md), [FEATURE_TRACEABILITY.md](FEATURE_TRACEABILITY.md) and [DEVELOPMENT_STATUS.md](DEVELOPMENT_STATUS.md).
