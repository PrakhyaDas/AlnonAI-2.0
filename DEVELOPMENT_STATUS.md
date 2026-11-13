# Development status — AlnonAI 2.0

Last updated: 12 November 2026

| Stage | Status | Evidence |
|---|---|---|
| 1. Inspect existing implementation | Complete | `IMPLEMENTATION_AUDIT.md`, `FEATURE_TRACEABILITY.md` |
| 2. Preserve/reconstruct original features | Implemented in Streamlit alternative | Resource categories, contacts, emergency links, safety plan, consent-gated manual location message, PIN gate, practical support sections |
| 3. Interface | Implemented | Streamlit responsive layout, navigation, three language options, keyboard focus styling |
| 4. Backend/database | Implemented for local single-user prototype | SQLite schema and migration, contacts/resources/settings |
| 5. AI assistant and RAG | Implemented as local extractive RAG | Unicode tokenisation, BM25-style retrieval, citations, no-match behaviour; no LLM |
| 6. Healthcare safety/referral layer | Implemented as conservative signposting | urgent phrase detector, 112 referral, Tele-MANAS and Child Helpline directory entries |
| 7. Multilingual/accessibility | Partial | English/Hindi/Telugu UI and selected curated content; requires fluent-speaker review and formal accessibility audit |
| 8. Testing/evaluation/deployment | Local automated tests and deployment instructions included | `tests/`, GitHub Actions, `DEPLOYMENT.md`; requires actual environment testing and external review |
| 9. Competition submission | Draft materials included | `PROJECT_DESCRIPTION.md`, `DEMO_SCRIPT.md`, source register; final one-page PDF/video require owner review and recording |

## Known gaps that must not be hidden

- Not merged into the original Expo app.
- No real external generative AI model; RAG is local lexical retrieval and extractive assembly.
- No verified local NGO or rehabilitation-centre dataset is bundled.
- No automatic GPS, SMS, WhatsApp, email or emergency dispatch.
- No multi-user accounts, encryption at rest or production security audit.
- No clinician validation or independent Hindi/Telugu translation review.
