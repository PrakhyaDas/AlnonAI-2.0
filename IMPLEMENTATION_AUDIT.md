# AlnonAI 2.0 — Stage 1 Implementation Audit

**Audit date:** 11 November 2026  
**Purpose:** Establish what already exists, what is only described, and what must be rebuilt before adding healthcare AI.

## 1. Sources inspected

1. **Original public repository:** [PrakhyaDas/AlnonAI](https://github.com/PrakhyaDas/AlnonAI), `main` branch. The repository page showed two commits and a root-level file listing at the time of review.
2. **Original implementation files:** [`DisguiseCalc.tsx`](https://github.com/PrakhyaDas/AlnonAI/blob/main/DisguiseCalc.tsx), [`HiddenDashboard.tsx`](https://github.com/PrakhyaDas/AlnonAI/blob/main/HiddenDashboard.tsx), [`storage.ts`](https://github.com/PrakhyaDas/AlnonAI/blob/main/storage.ts), [`config.ts`](https://github.com/PrakhyaDas/AlnonAI/blob/main/config.ts), [`index.tsx`](https://github.com/PrakhyaDas/AlnonAI/blob/main/index.tsx), [`_layout.tsx`](https://github.com/PrakhyaDas/AlnonAI/blob/main/_layout.tsx), [`package.json`](https://github.com/PrakhyaDas/AlnonAI/blob/main/package.json), [`.env`](https://github.com/PrakhyaDas/AlnonAI/blob/main/.env), [`.gitignore`](https://github.com/PrakhyaDas/AlnonAI/blob/main/.gitignore) and [repository README](https://github.com/PrakhyaDas/AlnonAI#readme).
3. **Original project PDF:** `AlnonAi pdf.pdf`, three pages, previously supplied in the project materials. It describes the calculator disguise, panic alerts, Maps-based nearby help, consent-based audio recording, community chat, resources and financial guidance.
4. **Research/technology proposal:** `AlnonAI: Closing the Distance Between People and the Help That Already Exists`, previously supplied in the project materials. It defines the core purpose as navigation to real, verified services rather than diagnosis or treatment.
5. **AlnonAI 2.0 starter package:** `alnonai_2_project.zip`, a separate Streamlit/Python prototype created on 10 November 2026 and inspected locally for this audit.

**Important distinction:** The GitHub repository is the original app baseline. The Streamlit starter package is a separate prototype. It has not been merged into the GitHub repository, and no GitHub files were changed during this audit.

## 2. Original repository: implementation map

### Technology and structure

- Frontend: React Native with Expo; Expo Router is configured.
- Package metadata identifies Expo SDK 54, React 19, React Native 0.81 and Expo Router 6.
- `@supabase/supabase-js` is a dependency and a Supabase URL plus public anon key are present in the tracked `.env` file.
- `storage.ts` is a small AsyncStorage wrapper exposing generic `save`, `load`, `remove` and `clear` functions.
- `config.ts` defines a fixed secret code and storage-key names for user data, emergency contacts and settings.

### Actual flow visible in the source

```text
index.tsx
  └── redirects to /screens/DisguiseCalc
        └── DisguiseCalc.tsx
              └── if display equals fixed code, pushes /screens/HiddenDashboard
                    ├── Panic & Safety       (route string exists; tap handler is empty)
                    ├── AI Support Chat       (route string exists; tap handler is empty)
                    ├── Resources             (route string exists; tap handler is empty)
                    └── Community             (route string exists; tap handler is empty)
```

The dashboard's `Lock & Exit` control routes back to the calculator. The inspected code does not clear app storage or invalidate an authenticated session when this happens.

### Findings in the original source

| Area | What the inspected source shows | Status |
|---|---|---|
| Calculator disguise | A calculator-style screen exists. | UI implemented |
| Secret unlock | The unlock value is hard-coded as `2580` in the screen and repeated in configuration. The repository README also documents the value. | Demonstration gate only; not secure PIN protection |
| Calculator arithmetic | The calculator evaluates the display string using JavaScript `eval`. | Replace with a constrained arithmetic parser before reuse |
| Hidden dashboard | Four cards are rendered for Panic & Safety, AI Support Chat, Resources and Community. | UI labels only |
| Dashboard navigation | Each card defines a route, but its `onPress` handler is `() => {}`. | Not wired |
| Lock & Exit | Returns to the calculator route. | Navigation only; no secure-session cleanup shown |
| Local storage | Generic AsyncStorage helpers exist. | Utility only; no typed feature-specific data model found |
| Emergency contacts | A storage key is named in configuration, and the README describes emergency contacts. | No contact-management screen or contact CRUD found in the inspected source |
| Panic alerts / SMS | README says backend deployment is required for SMS notifications. | Not implemented in inspected source |
| AI chat | README says a backend is required. No chat screen or model/API integration appears in the inspected source. | Not implemented in inspected source |
| Resources / nearby services | README describes location-based lookups as a backend requirement. No resource-directory screen or Maps integration appears in the inspected source. | Not implemented in inspected source |
| Community | README labels this as “coming soon”. | Planned placeholder |
| Audio recording | Mentioned in the original PDF and README backend requirements; no recording flow appears in the inspected source. | Not implemented in inspected source |
| Supabase | Client dependency and public project configuration exist. No schema, migration, access policy or working data flow was found in the inspected files. | Configuration present; backend behaviour unverified |

### Repository structure issue

The repository README describes an `app/screens/` structure, but the visible `main`-branch file listing places `index.tsx`, `_layout.tsx`, `DisguiseCalc.tsx` and `HiddenDashboard.tsx` at the repository root and does not show the documented `app/screens/` directory. At the same time, `index.tsx` and `_layout.tsx` refer to `/screens/...` routes. This mismatch needs to be resolved and verified with an actual Expo run before extending the app.

## 3. Original concept and documented feature set

The three-page project PDF records these original ideas:

- Calculator-style discreet entry and a secret code.
- Panic button that alerts designated contacts.
- Google Maps integration to locate nearby help centres and support groups.
- Location sharing for rapid response.
- Audio recording for documentation, explicitly described as consent-based.
- Community chat / peer support.
- Curated resources, articles, guides and service contact information.
- Financial guidance.

The research proposal adds a clearer product principle: AlnonAI should translate a person's plain-language description into relevant categories, retrieve named services from a closed, checked source list and explain the next step in plain language. It explicitly should not diagnose, treat or replace a doctor, lawyer or counsellor.

These are **documented concepts**, not proof that each feature was operational in the original repository.

## 4. AlnonAI 2.0 starter prototype map

The local `alnonai_2` package is a separate Python/Streamlit prototype.

| File / module | Current responsibility |
|---|---|
| `app.py` | Streamlit pages: Home, Ask AlnonAI, Healthcare navigator, Find support, Safety & trusted contacts, Education & livelihoods, About & privacy |
| `alnonai/core.py` | Keyword-based intent classification, keyword urgency flag and fixed response templates |
| `alnonai/content.py` | Static health-literacy guidance and safety/privacy notices |
| `alnonai/db.py` | SQLite tables and CRUD for resources, contacts, safety notes and settings |
| `data/resource_import_template.csv` | Starter CSV columns for resource imports |
| `tests/test_core.py` | Five small tests for the baseline rules and responses |

### Current prototype capability

- A basic support chat exists, but it is rule-based and not an LLM or RAG system.
- Healthcare navigator content is static, not retrieved from a source corpus.
- A generic resource directory exists, but it starts empty and requires verified entries to be added.
- Trusted contacts can be added and deleted in the local prototype database.
- Safety notes are stored locally.
- Education, employment, legal and financial categories have general signposting text.
- Chat is held in Streamlit session state and is not intentionally written to SQLite.
- The code was checked locally on 11 November 2026: `compileall` completed and `pytest` reported **5 passed**. This is a small software test result only, not clinical validation, security testing or usability testing.

### Missing from the starter prototype

- No real LLM, embedding model, vector index or RAG retrieval.
- No source citations attached to generated answers.
- No verified service dataset; the resource directory is empty by default.
- No SMS alert or emergency-contact notification workflow.
- No GPS lookup or consent-based location sharing.
- No calculator disguise or PIN gate.
- No audio recording or community-chat module.
- No English/Hindi/Telugu language selector or reviewed translations.
- No accessibility audit or assistive-technology testing.
- No production authentication, encryption-at-rest, role-based access, security audit or deployment configuration.

## 5. Feature traceability

See [`FEATURE_TRACEABILITY.md`](FEATURE_TRACEABILITY.md) for the feature-by-feature matrix across the original PDF, original repository, current starter prototype and target AlnonAI 2.0.

## 6. High-priority engineering and safeguarding issues

1. **Replace the fixed PIN.** A code embedded in client source and documented in the README is not a private credential. Use a user-chosen PIN flow with platform secure storage for a verifier, sensible attempt throttling and a clear recovery path. Do not store a raw PIN. A local gate is not a substitute for device security.
2. **Remove `eval`.** Use a small arithmetic parser with an explicit allow-list of digits and operators; do not evaluate arbitrary JavaScript strings.
3. **Fix routing before adding screens.** Align the Expo Router directory with the configured route tree and make each dashboard item navigate to a real screen.
4. **Treat panic alerts as a separate, consentful workflow.** Confirm the chosen recipients and message, make accidental activation difficult, show whether an alert was actually sent and provide a manual fallback. Never imply that the app is an emergency service.
5. **Keep location sharing one-time and explicit.** Ask immediately before each share, show the recipient and exact data being shared, provide an expiry and do not collect background location by default.
6. **Defer audio recording.** The original PDF describes consent-based recording, but this feature needs jurisdiction-specific legal and safeguarding review. It must never start automatically or covertly, and the interface must not encourage a person to record if doing so could increase danger.
7. **Defer public community chat.** It requires moderation, reporting/blocking, abuse escalation, age-appropriate safeguarding and privacy operations before it is safe to launch.
8. **Verify Supabase policies.** The public repository contains a Supabase anon client key in `.env`; an anon key is designed for client use, but the database must enforce Row Level Security and least-privilege policies. No policy configuration was present in the inspected repository files. Do not put a service-role key in the client or repository.
9. **Resolve licensing language.** The repository includes an MIT license while its README also says “Private - Not for distribution”. Confirm the intended reuse terms before publishing a competition submission.

## 7. Recommended baseline for the next stage

Use the original Expo app as the product baseline so the discreet calculator concept and mobile-first experience are not discarded. Treat the Streamlit package as a reference prototype for content and data behaviour, not as a second product to maintain indefinitely. Rebuild the missing screens under a valid Expo Router structure, then connect them to a secure backend. Keep the clinical knowledge service separate from the safety/referral rules so generative text can never override an urgent handoff.

**Stage 1 outcome:** Original assets and current code have been mapped. The next incomplete stage is **Stage 2 — preserve and reconstruct the original feature set**.
