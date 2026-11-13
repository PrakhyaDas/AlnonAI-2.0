# AlnonAI 2.0 internal service design

This prototype is a single-process Streamlit application, not a deployed public API. The following module boundaries keep future migration to a mobile app or REST service straightforward.

| Module | Responsibility | Current implementation |
|---|---|---|
| `alnonai.core` | Safety phrase check, intent classification, retrieval, grounded response | Local Python functions |
| `alnonai.db` | Contacts, resources, app settings | SQLite with parameterised SQL |
| `alnonai.content` | Localised UI strings, referral entries and guidance | Python dictionaries |
| `data/knowledge_base.json` | Curated knowledge chunks and citations | JSON records |
| `app.py` | User interface and consent flow | Streamlit |

## Proposed future endpoints

- `POST /assistant/query`: accepts `{question, language, consent_to_external_processing}`; returns `{answer, sources, urgency_flag, disclaimer}`.
- `GET /resources`: filters by category, location and verification status.
- `POST /resources`: adds a resource with provenance; new records default to unverified.
- `GET /contacts` / `POST /contacts` / `DELETE /contacts/{id}`: user-scoped trusted contacts.
- `POST /safety/location-preview`: creates a message preview only; never sends or dispatches it.

A future API must require per-user authentication, authorisation, encrypted transport and storage, rate limits, audit controls, consent records, deletion/retention workflows and a security review. Never expose the local prototype's shared SQLite database as a multi-user production service.
