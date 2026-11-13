# AlnonAI 2.0 — Project description

## One-sentence summary

AlnonAI 2.0 is a multilingual, privacy-conscious support navigator that helps people and families affected by alcohol-related harm find clear health information, professional referrals and practical support.

## Problem

People affected by alcohol-related harm may struggle to distinguish reliable health information from unsupported claims, find appropriate services, or identify practical support for family wellbeing, legal needs, education and employment. Information is often scattered across separate websites and service directories.

## Proposed solution

AlnonAI combines a local source-grounded retrieval assistant with a searchable support directory, healthcare literacy content, family wellbeing guidance and a personal safety workflow. It is designed to help people prepare for professional conversations and find official starting points, not to diagnose or treat anyone.

## Main functions

1. **Support assistant:** retrieves relevant passages from a curated local knowledge base and displays source links. It does not invent an answer when retrieval finds no match.
2. **Health literacy:** presents selected information in plain language and helps users prepare questions for qualified professionals.
3. **Urgency signposting:** conservative phrase matching displays a clear emergency referral. It is not a medical triage system.
4. **Family wellbeing:** explains safe boundaries, trusted support and professional referrals.
5. **Service navigation:** official helplines, legal aid, scholarship and government-scheme portals, employment services and locally added NGO/rehabilitation listings.
6. **Safety workflow:** trusted contacts, a session-only safety checklist and manual location-message preparation after explicit consent.
7. **Discreet entry:** calculator-styled PIN screen with salted PBKDF2 verifier.
8. **Accessibility and language:** English, Hindi and Telugu interface options, selected translated content, adjustable text size and high-contrast mode.

## Technical implementation

- Python and Streamlit for the interface.
- SQLite for local trusted contacts, resource listings and settings.
- PBKDF2-HMAC-SHA256 for PIN verification.
- Unicode tokenisation and BM25-style lexical retrieval over JSON knowledge chunks.
- Source metadata stored with each chunk and displayed in answers.
- Separate rule-based urgent phrase detection.

## What is different

The project preserves AlnonAI's original support-navigation purpose instead of becoming a generic health chatbot. Healthcare information is integrated with practical support, family wellbeing and service access. The assistant is deliberately constrained to source-linked content and explicitly states when it cannot find a reliable match.

## Safety, privacy and limitations

This is an educational prototype, not a medical device, diagnostic system, treatment service or emergency response service. It has not been clinically validated, translation-reviewed or security-audited. The urgency detector may miss emergencies. The PIN is an app-level access gate, not encryption; the SQLite database is not encrypted at rest. No GPS, SMS, WhatsApp or automatic alert is sent. Public cloud demos should use fake data only.

## Evaluation plan

Evaluate retrieval relevance and citation correctness using a clinician-reviewed question set; measure urgent phrase detection false positives and false negatives; ask fluent Hindi and Telugu reviewers to assess translations; test keyboard navigation, contrast and text scaling; and conduct a privacy/security review before any real-world deployment.
