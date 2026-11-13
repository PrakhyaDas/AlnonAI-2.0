# AlnonAI 2.0 — Feature Traceability Matrix

**Status legend**

- **Implemented:** working code was found in the inspected source or starter package.
- **Partial:** some UI, schema or static guidance exists, but the complete user workflow does not.
- **Documented:** described in a project PDF/README/proposal but no working implementation was found.
- **Missing:** no implementation was found in the inspected files.
- **Target:** planned for AlnonAI 2.0; not a claim that it exists today.

| Feature | Original PDF / proposal | Original GitHub repo | AlnonAI 2.0 Streamlit build (12 Nov 2026) | Remaining gap |
|---|---|---|---|---|
| Discreet calculator entry | Described and shown in screenshots | Calculator UI exists; fixed code was hard-coded and publicly documented | Implemented: calculator-styled gate, user-chosen PIN, salted PBKDF2 verifier, lock/change PIN | PIN is only an app gate; DB is not encrypted and there is no multi-user auth |
| AI support assistant | Shown as a dashboard feature | Dashboard label only; no working chat route or model integration found | Implemented as local extractive RAG with Unicode tokenisation, BM25-style ranking, citations and no-match fallback | No generative LLM; knowledge base is small and requires clinician review |
| Emergency contacts | Panic alerts to designated contacts described | README describes contacts; only a config key found, no contact CRUD screen | Official emergency/mental-health/child helplines plus trusted-contact CRUD and phone links | No automatic alert, SMS or delivery confirmation |
| Trusted contacts | Safe communication network described | No working contact-management workflow found | Implemented: local SQLite add/list/delete | Local single-user DB only; not encrypted |
| Panic / safety workflow | Panic button described | Dashboard card only; tap handler is empty; README says backend needed for alerts | Implemented as emergency phone links, session-only safety checklist and trusted contacts | No remote alert or dispatch; user must call/share manually |
| NGO directory | Curated resources described | Resources card only; no working directory found | Implemented: searchable local directory, source URL required, user-added entries labelled unverified | No pre-populated local NGO dataset; manual verification needed |
| Rehabilitation centres | Mentioned in original resource concept and proposal | No working directory found | Implemented category and listing workflow; entries default unverified | No verified local centre listings supplied |
| Legal information / legal aid | Proposal identifies legal protections and legal-aid navigation | Missing | Official NALSA legal-aid helpline and source-linked signposting | No state/district-specific legal directory or legal advice |
| Government schemes | Proposal identifies government-program navigation | Missing | myScheme official portal included in support/practical navigation | No in-app eligibility engine; user must check official scheme criteria |
| Education support | Identified as a family impact/support need in the proposal | Missing | National Scholarship Portal link and signposting | No live scheme scraping or eligibility determination |
| Employment support | Identified as a practical support category in the requested scope | Missing | National Career Service link and signposting | No live vacancy integration or job matching |
| Financial assistance | PDF describes financial guidance; proposal includes financial navigation | Missing as a working screen | myScheme and official portal signposting | No personalised financial advice or scheme eligibility engine |
| Maps / nearby services | PDF says Maps integration was added | README describes lookup as backend-dependent; no map code found | Manual approximate location entry only | No maps or GPS integration |
| Consent-based location sharing | PDF describes location sharing | README lists backend requirements; no share flow found | Implemented as manual location message preview behind a separate consent checkbox | No automatic transmission, expiry or GPS; user manually shares preview |
| Audio recording | PDF describes recording with consent | No recorder flow found | Missing | Deferred pending legal/safeguarding review; never covert or automatic |
| Community chat | PDF describes peer support | Dashboard card only; README says coming soon | Missing | Deferred until moderation, reporting, blocking and safeguarding are designed |
| Health-literacy explanations | Not in original scope | Missing | Curated plain-language content in English, Hindi and Telugu; appointment preparation | Needs clinician and fluent-speaker review; no personalised medical interpretation |
| Family wellbeing resources | Family support is central to the proposal | Missing | Static multilingual family wellbeing guidance and Tele-MANAS referral | Not a counselling service; needs local support directory |
| Urgency recognition | Panic/safety concept exists | Panic card only; no classifier found | Conservative phrase matcher for English/Hindi/Telugu with emergency referral | Not clinical triage; clinician-authored evaluation set needed |
| Professional referrals | Proposal's core purpose is to connect users to real services | No working referral flow found | Official 112, Tele-MANAS, Child Helpline, NALSA, NSP and myScheme starting points | Local provider listings require verification and regular review |
| English / Hindi / Telugu | Proposal calls for Indian-language access | Missing | UI and selected content in all three languages; multilingual retrieval tests | Full translation coverage and independent review incomplete |
| Accessibility | Discreet/mobile-first intent is present | Basic mobile UI only; no audit found | Text scaling, high-contrast mode, semantic headings and keyboard focus styling | No formal screen-reader or WCAG audit |
| Privacy / data controls | Privacy is a core design principle | AsyncStorage helper; no full privacy model found | Session-only chat/notes, local SQLite contacts/resources, salted PIN, explicit location consent | No DB encryption, multi-user auth, audit logs or security audit |

## 12 November 2026 implementation update

The current Streamlit build now implements the functions listed in the third column. These are working local-prototype workflows, not proof of production readiness. The original Expo repository remains unchanged and separate. See `DEVELOPMENT_STATUS.md` and `DEPLOYMENT.md` for exact limits.

## Preservation rule

AlnonAI 2.0 remains a support-navigation platform for people and families affected by alcohol-related harm. Healthcare features extend that purpose; they do not replace the original support, safety and practical-assistance pathways with a generic medical chatbot.

## Source notes

- Original repository: https://github.com/PrakhyaDas/AlnonAI
- Calculator: https://github.com/PrakhyaDas/AlnonAI/blob/main/DisguiseCalc.tsx
- Dashboard: https://github.com/PrakhyaDas/AlnonAI/blob/main/HiddenDashboard.tsx
- Storage helper: https://github.com/PrakhyaDas/AlnonAI/blob/main/storage.ts
- Configuration: https://github.com/PrakhyaDas/AlnonAI/blob/main/config.ts
- Repository README: https://github.com/PrakhyaDas/AlnonAI#readme
- Original project PDF: `AlnonAi pdf.pdf`, pp. 1–3, supplied in the project materials.
- Research/technology proposal: `AlnonAI: Closing the Distance Between People and the Help That Already Exists`, supplied in the project materials.
