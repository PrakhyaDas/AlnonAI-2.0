# Data governance and privacy notes

## Data minimisation

- Chat questions and assistant responses are held in Streamlit session state only and are not written to SQLite.
- The database stores trusted contacts, locally added resource entries and a salted PIN verifier.
- Safety checklist selections and appointment notes remain session-only.
- No GPS permission or browser geolocation API is used.
- Location sharing requires manual entry, a separate consent checkbox and user-initiated copying/sharing. No message is transmitted by the app.

## Storage and security limits

- SQLite is stored on the machine hosting the application.
- The PIN uses PBKDF2-HMAC-SHA256 with a random salt; the PIN itself is not stored.
- The PIN does not encrypt the database and does not provide multi-user identity or role separation.
- No encryption-at-rest, account recovery, audit log, rate limiting or independent penetration test is implemented.
- Public cloud storage may be ephemeral. Use fake data for public demonstrations.

## Health information governance

- Knowledge chunks include a title, topic, language, source URL and review date.
- The assistant returns retrieved text and citations rather than unsupported generative answers.
- Unknown questions receive a no-match response.
- Urgency phrase matching is separate from retrieval and is not a clinical triage model.
- Health content requires clinician review; Hindi and Telugu translations require fluent-speaker review.

## Resource directory governance

- Built-in entries point to official government/public-health sources.
- User-added providers are labelled unverified and require a source URL.
- Do not add an NGO, rehabilitation centre or clinic until its identity, qualifications, service scope, fees, safeguarding policy, location and current contact details are checked.
- Review entries periodically and remove expired or incorrect information.

## Consent and safeguarding

- Do not collect identity numbers, passwords, precise home addresses or unnecessary medical histories.
- Do not share location if doing so could increase risk.
- Do not promise confidentiality beyond the actual hosting and storage controls.
- For immediate danger in India, direct users to emergency services at 112; do not imply that AlnonAI dispatches help.
