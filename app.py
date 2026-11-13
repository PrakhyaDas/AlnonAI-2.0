from __future__ import annotations
import re
import streamlit as st

from alnonai.content import (
    APP_NAME, DISCLAIMER, SAFETY_NOTICE, PRIVACY_NOTICE, TRANSLATIONS,
    TOPIC_TRANSLATIONS, BUILTIN_RESOURCES, RESOURCE_CATEGORIES,
)
from alnonai.core import build_grounded_answer, classify_intent, safety_check, urgent_response, hash_pin, verify_pin
from alnonai.db import (
    init_db, list_resources, add_resource, delete_resource,
    list_contacts, add_contact, delete_contact, get_setting, set_setting,
)

st.set_page_config(page_title="Calculator", page_icon="🧮", layout="wide", initial_sidebar_state="expanded")
init_db()

st.markdown("""
<style>
:root { color-scheme: light; }
.block-container {max-width: 1160px; padding-top: 1.25rem; padding-bottom: 3rem;}
.hero {background:linear-gradient(115deg,#143b4a,#24736f);padding:1.6rem 1.8rem;border-radius:20px;color:#fff;margin-bottom:1rem;}
.hero p {color:#e1f2ed;margin-bottom:0;}
.muted {color:#526b72;font-size:.92rem;}
div[data-testid="stMetric"] {background:#eff7f5;padding:12px;border-radius:14px;}
div.stButton > button {border-radius:12px; min-height:2.6rem;}
[data-testid="stSidebar"] {background:#f5faf8;}
:focus-visible {outline:3px solid #155e75 !important; outline-offset:2px !important;}
</style>
""", unsafe_allow_html=True)

# ----- PIN gate: app-level access barrier, not encryption or multi-user authentication -----
if "unlocked" not in st.session_state:
    st.session_state.unlocked = False
if "chat" not in st.session_state:
    st.session_state.chat = []
if "safety_plan" not in st.session_state:
    st.session_state.safety_plan = []

pin_salt = get_setting("pin_salt")
pin_hash = get_setting("pin_hash")
if not pin_salt or not pin_hash:
    st.markdown('<div class="hero"><h1>Calculator</h1><p>A discreet entry screen for AlnonAI.</p></div>', unsafe_allow_html=True)
    st.info("Create a PIN to open this app. Choose a PIN you do not use for banking or other accounts.")
    p1 = st.text_input("Create a 6–12 digit PIN", type="password", max_chars=12)
    p2 = st.text_input("Confirm PIN", type="password", max_chars=12)
    if st.button("Set PIN and open", type="primary"):
        if not re.fullmatch(r"\d{6,12}", p1 or ""):
            st.error("Use 6 to 12 digits.")
        elif p1 != p2:
            st.error("The PINs do not match.")
        else:
            salt, digest = hash_pin(p1)
            set_setting("pin_salt", salt); set_setting("pin_hash", digest)
            st.session_state.unlocked = True
            st.rerun()
    st.caption("Privacy note: this PIN gate does not encrypt the SQLite database or protect it from someone with server/file access.")
    st.stop()

if not st.session_state.unlocked:
    st.markdown('<div class="hero"><h1>Calculator</h1><p>Enter your access PIN to continue.</p></div>', unsafe_allow_html=True)
    entered = st.text_input("PIN", type="password", max_chars=12)
    if st.button("Open", type="primary"):
        if verify_pin(entered, pin_salt, pin_hash):
            st.session_state.unlocked = True
            st.rerun()
        else:
            st.error("PIN not recognised.")
    st.caption("If you forget the PIN, the local administrator can reset the local app database. This build has no remote account recovery.")
    st.stop()

# ----- Navigation / language -----
with st.sidebar:
    st.markdown("## 🩵 AlnonAI 2.0")
    st.caption("Support • health information • practical next steps")
    language = st.selectbox("Language / भाषा / భాష", list(TRANSLATIONS.keys()), index=0)
    tr = TRANSLATIONS[language]
    text_scale = st.select_slider("Text size", options=["Standard", "Large", "Extra large"], value="Standard")
    high_contrast = st.checkbox("High contrast", value=False)
    pages = [
        ("home", tr["home"]), ("assistant", tr["assistant"]), ("health", tr["health"]),
        ("support", tr["support"]), ("safety", tr["safety"]), ("family", tr["family"]),
        ("practical", tr["practical"]), ("privacy", tr["privacy"]),
    ]
    selected_label = st.radio("Navigate", [label for _, label in pages], label_visibility="collapsed")
    page = next(key for key, label in pages if label == selected_label)
    st.divider()
    if st.button("Lock AlnonAI", use_container_width=True):
        st.session_state.unlocked = False
        st.session_state.chat = []
        st.rerun()
    st.link_button("Emergency · Call 112", "tel:112", use_container_width=True)
    st.caption("Local prototype · not an emergency service")

_font_sizes = {"Standard": "1rem", "Large": "1.12rem", "Extra large": "1.25rem"}
_extra_css = f"body, p, li, label, input, textarea {{font-size: {_font_sizes[text_scale]} !important;}}"
if high_contrast:
    _extra_css += "body, [data-testid='stAppViewContainer'] {background:#fff !important;color:#000 !important;} p, label, span, h1, h2, h3 {color:#000 !important;} .hero h1, .hero p {color:#fff !important;} [data-testid='stSidebar'] {background:#f0f0f0 !important;} button {border:2px solid #000 !important;}"
st.markdown(f"<style>{_extra_css}</style>", unsafe_allow_html=True)

st.markdown('<div class="hero"><h1>AlnonAI</h1><p>From finding support to accessing healthcare.</p><p style="font-size:.88rem;margin-top:.55rem">A privacy-conscious support navigator for people and families affected by alcohol-related harm.</p></div>', unsafe_allow_html=True)

# ----- Pages -----
if page == "home":
    st.subheader(tr["welcome"])
    st.write("You can explore health information, find support, prepare for a professional conversation and create a simple safety plan. You decide what to share.")
    a,b,c = st.columns(3)
    a.metric("Knowledge base", "Source-linked", "Local retrieval")
    b.metric("Languages", "3", "English · हिन्दी · తెలుగు")
    c.metric("Your data", "Minimal", "Chat is session-only")
    st.markdown("### Start here")
    tiles = [
        ("💬 Ask AlnonAI", "Ask a question and see the sources used."),
        ("🏥 Health information", "Read plain-language information and prepare appointment questions."),
        ("📍 Find support", "Search official helplines and add locally verified organisations."),
        ("🛡️ Safety & contacts", "Create a personal plan and manage trusted contacts."),
        ("🤝 Family wellbeing", "Find supportive steps for family members and young people."),
        ("🎓 Practical support", "Explore legal aid, education, employment and financial support."),
    ]
    cols = st.columns(2)
    for i,(title,desc) in enumerate(tiles):
        with cols[i%2]:
            with st.container(border=True):
                st.markdown(f"**{title}**")
                st.write(desc)
    st.warning(SAFETY_NOTICE)
    st.caption(DISCLAIMER)

elif page == "assistant":
    st.subheader(tr["assistant"])
    st.write("Ask about health information, family wellbeing, treatment pathways or finding support. Answers are retrieved from a small local knowledge base and include source links.")
    st.info(tr["no_ai"])
    st.caption("Technical note: this is local lexical RAG (retrieval + source-grounded response assembly), not a generative LLM. It will say when it cannot find a source rather than invent an answer.")
    if st.button("Clear conversation"):
        st.session_state.chat = []
        st.rerun()
    for role, message in st.session_state.chat:
        with st.chat_message(role):
            st.markdown(message)
    prompt = st.chat_input(tr["ask"])
    if prompt:
        st.session_state.chat.append(("user", prompt))
        with st.chat_message("user"):
            st.markdown(prompt)
        if safety_check(prompt):
            response = urgent_response(language)
        else:
            response, _ = build_grounded_answer(prompt, language=language)
        st.session_state.chat.append(("assistant", response))
        with st.chat_message("assistant"):
            st.markdown(response)

elif page == "health":
    st.subheader(tr["health"])
    st.write("General information to support a conversation with a qualified professional. It cannot assess an individual's health.")
    topics = ["Alcohol and health", "Treatment and support", "Family wellbeing", "Mental wellbeing", "Health literacy"]
    topic = st.selectbox("Choose a topic", topics)
    st.markdown("### In plain language")
    st.write(TOPIC_TRANSLATIONS[language][topic])
    st.markdown("### Prepare for an appointment")
    st.write("You can ask a healthcare professional:")
    for q in ["What does this information mean for my situation?", "What are my options and what are the benefits and risks?", "What signs mean I should seek urgent help?", "What support is available for family members?", "How is my information kept confidential?"]:
        st.markdown(f"- {q}")
    notes = st.text_area("Your questions for the appointment (kept only in this browser session)", placeholder="Write only what you are comfortable keeping on this device.")
    if st.button("Prepare appointment note"):
        if notes.strip():
            st.success("Appointment note prepared. Copy it if useful; it is not saved to the database.")
            st.code(notes)
        else:
            st.info("Add at least one question first.")
    st.markdown("### Source-based questions")
    health_q = st.text_input("Ask about a health topic")
    if st.button("Retrieve health information"):
        if health_q.strip():
            answer, hits = build_grounded_answer(health_q, language=language)
            st.markdown(answer)
        else:
            st.warning("Enter a question first.")
    st.caption(DISCLAIMER)

elif page == "support":
    st.subheader(tr["support"])
    st.write("Official helplines are included below. Community organisations, NGOs and rehabilitation centres should be added only after someone verifies the provider and current contact details.")
    all_resources = BUILTIN_RESOURCES + list_resources()
    categories = ["All"] + sorted({r["category"] for r in all_resources})
    c1,c2 = st.columns([1,2])
    with c1: category = st.selectbox("Category", categories)
    with c2: query = st.text_input(tr["search"] + " name, service, city or description")
    filtered = all_resources
    if category != "All": filtered = [r for r in filtered if r["category"] == category]
    if query:
        q = query.casefold()
        filtered = [r for r in filtered if q in " ".join(str(v or "") for v in r.values()).casefold()]
    if not filtered: st.info("No matching listing. Try a broader search or ask an authorised local organisation to verify a listing before adding it.")
    for r in filtered:
        with st.container(border=True):
            st.markdown(f"**{r['name']}** · {r['category']}")
            st.write(r.get("description", ""))
            place = " · ".join(x for x in [r.get("city", ""), r.get("state", ""), r.get("country", "")] if x)
            if place: st.caption(place)
            phone = str(r.get("phone", "")).strip()
            if phone:
                st.write(f"Contact: **{phone}**")
                digits = re.sub(r"[^0-9+]", "", phone)
                if digits and len(digits) >= 3:
                    st.link_button("Call / open phone dialler", f"tel:{digits}")
            website = r.get("website", "")
            if website: st.markdown(f"[Open official website]({website})")
            source = r.get("source_url", "")
            if source: st.caption(f"Source / verification: {source}")
            if r.get("verified", 1): st.success("Official source listing")
            else: st.warning("User-added listing · verify before relying on it")
            if r.get("id"):
                if st.button("Delete this local listing", key=f"resdel_{r['id']}"):
                    delete_resource(r["id"]); st.rerun()
    with st.expander("Add a local organisation or service"):
        st.caption("Add only a real provider whose identity, service, contact details and source you have checked. New entries are marked unverified until reviewed by your project team.")
        with st.form("resource_form"):
            n = st.text_input("Organisation / service name")
            cat = st.selectbox("Type of support", RESOURCE_CATEGORIES)
            desc = st.text_area("What does it offer?")
            city = st.text_input("City / district")
            state = st.text_input("State")
            country = st.text_input("Country", value="India")
            phone = st.text_input("Public contact number (optional)")
            website = st.text_input("Official website (optional)")
            source = st.text_input("Verification source URL (required)")
            if st.form_submit_button("Save listing"):
                try:
                    add_resource(n,cat,desc,city,state,country,phone,website,source,verified=0)
                    st.success("Saved locally as an unverified listing.")
                    st.rerun()
                except ValueError as e:
                    st.error(str(e))

elif page == "safety":
    st.subheader(tr["safety"])
    st.error(SAFETY_NOTICE)
    st.markdown("### One-tap emergency options")
    e1,e2,e3 = st.columns(3)
    e1.link_button("Call emergency 112", "tel:112", type="primary", use_container_width=True)
    e2.link_button("Call Tele-MANAS 14416", "tel:14416", use_container_width=True)
    e3.link_button("Call Child Helpline 1098", "tel:1098", use_container_width=True)
    st.caption("Phone links depend on your device and browser. If they do not open, dial the number directly from a phone.")
    st.markdown("### Personal safety plan")
    st.write("Only write a plan if it is safe to do so. This checklist stays in the current session and is cleared when you lock or close the app.")
    plan_items = ["I know a safer place I can go to.", "I know a trusted person I can contact.", "I can reach a phone or emergency service.", "I have a plan for getting help without confronting anyone."]
    for item in plan_items:
        if st.checkbox(item, key="plan_" + str(plan_items.index(item))):
            if item not in st.session_state.safety_plan: st.session_state.safety_plan.append(item)
        elif item in st.session_state.safety_plan:
            st.session_state.safety_plan.remove(item)
    st.markdown("### Trusted contacts")
    contacts = list_contacts()
    if contacts:
        for c in contacts:
            x,y = st.columns([4,1])
            x.write(f"**{c['name']}** · {c['relationship'] or 'Relationship not specified'} · {c['phone']}")
            if y.button(tr["delete"], key=f"contactdel_{c['id']}"):
                delete_contact(c["id"]); st.rerun()
    else:
        st.info("No trusted contacts saved yet.")
    with st.form("contact_form"):
        n = st.text_input(tr["name"])
        rel = st.text_input("Relationship (optional)")
        ph = st.text_input(tr["phone"])
        if st.form_submit_button("Add trusted contact"):
            try:
                add_contact(n,rel,ph); st.success("Contact saved on this host."); st.rerun()
            except ValueError as e: st.error(str(e))
    st.markdown("### Consent-based location message")
    st.write("AlnonAI does not access GPS. If you choose, type an approximate location and manually share a message with someone you trust.")
    approximate_location = st.text_input(tr["location"])
    chosen = st.selectbox("Choose a trusted contact", ["No contact selected"] + [f"{c['name']} · {c['phone']}" for c in contacts])
    consent = st.checkbox(tr["consent"])
    if st.button("Prepare location message"):
        if not consent:
            st.warning("Consent is required before a location is included.")
        elif not approximate_location.strip():
            st.warning("Enter an approximate location, or leave location out and contact the person directly.")
        else:
            recipient = chosen if chosen != "No contact selected" else "a trusted person"
            st.success("Message prepared only. Nothing has been sent.")
            st.code(f"I would like support. My approximate location is: {approximate_location.strip()}. Please contact me if it is safe to do so. Intended recipient: {recipient}.")
    st.caption("Do not share location if doing so could increase risk. You remain in control of whether, when and with whom to share it.")

elif page == "family":
    st.subheader(tr["family"])
    st.write("Alcohol-related harm can affect everyone in a household. Support is available for family members too; you do not have to manage another person's health or behaviour on your own.")
    family_topics = [
        ("You are not responsible for another person's choices", "You can care about someone and still recognise that you cannot control their decisions. Focus on what helps keep you safe and supported."),
        ("Talk to a safe person", "A trusted adult, school counsellor, qualified mental-health professional or social worker may help you think through options. Choose someone who will take your concerns seriously."),
        ("Boundaries and safety", "It may help to decide what situations you will leave, who you can call and where you can go. Do not confront someone if that could put you in danger."),
        ("Support for mental wellbeing", "If stress or worry is affecting daily life, consider professional support. In India, Tele-MANAS can be reached at 14416. In an immediate emergency, call 112."),
    ]
    for title, body in family_topics:
        with st.expander(title, expanded=True): st.write(body)
    st.link_button("Tele-MANAS information", "https://dghs.mohfw.gov.in/national-mental-health-programme.php")
    st.link_button("Child Helpline information", "https://www.india.gov.in/category/benefits-social-development/subcategory/women-children/details/information-on-childline-service-by-ministry-of-women-and-child-development")
    st.caption("This section is educational and is not counselling or a substitute for local safeguarding support.")

elif page == "practical":
    st.subheader(tr["practical"])
    sections = [
        ("Education", "Explore scholarships, fee support, school or college continuation and education NGOs. Check current eligibility and deadlines on official websites.", "https://scholarships.gov.in/All-Scholarships"),
        ("Employment", "Look for recognised skill training, career guidance, apprenticeships and public employment services. Verify the provider before sharing documents or paying fees.", "https://www.ncs.gov.in/"),
        ("Legal information", "For legal advice, contact a qualified lawyer or legal services authority. NALSA's national legal-aid helpline is 15100. Eligibility and local referral depend on the case.", "https://nalsa.gov.in/promoting-inclusive-legal-system/"),
        ("Financial assistance and government schemes", "Use the Government of India myScheme portal to discover Central and State/UT schemes. Check eligibility, benefits, documents and application steps on the official scheme page. Never pay an intermediary who guarantees a benefit.", "https://www.myscheme.gov.in/"),
        ("NGO and rehabilitation support", "Ask about professional qualifications, service scope, costs, safeguarding, confidentiality, accessibility and follow-up. Do not rely on guaranteed-cure claims.", "https://www.who.int/news-room/fact-sheets/detail/alcohol"),
    ]
    for title, body, url in sections:
        with st.expander(title):
            st.write(body)
            st.markdown(f"[Official information / starting point]({url})")

elif page == "privacy":
    st.subheader(tr["privacy"])
    st.markdown("### Privacy design")
    st.markdown(PRIVACY_NOTICE)
    st.markdown("### PIN and discreet entry")
    st.write("The app opens behind a PIN screen styled as a calculator. The PIN is stored as a salted PBKDF2 verifier, not as plain text. This is an app-level access barrier only; it does not encrypt the SQLite database, secure the host, or provide separate accounts for multiple users.")
    if st.button("Change PIN"):
        st.session_state.show_pin_change = True
    if st.session_state.get("show_pin_change"):
        old = st.text_input("Current PIN", type="password", key="oldpin")
        new1 = st.text_input("New 6–12 digit PIN", type="password", key="newpin1")
        new2 = st.text_input("Confirm new PIN", type="password", key="newpin2")
        if st.button("Update PIN"):
            if not verify_pin(old, get_setting("pin_salt"), get_setting("pin_hash")):
                st.error("Current PIN is incorrect.")
            elif not re.fullmatch(r"\d{6,12}", new1 or "") or new1 != new2:
                st.error("Use matching 6–12 digit PINs.")
            else:
                salt, digest = hash_pin(new1); set_setting("pin_salt", salt); set_setting("pin_hash", digest)
                st.session_state.show_pin_change = False; st.success("PIN updated."); st.rerun()
    st.markdown("### Clinical and technical boundaries")
    st.markdown(DISCLAIMER)
    st.write("No clinician has validated this prototype. The urgent-language detector is a conservative phrase matcher and may miss emergencies or flag non-emergencies. The knowledge base is small and not a complete medical reference. Listings can become outdated.")
    st.markdown("### Sources currently used")
    source_links = [
        ("WHO — Alcohol fact sheet", "https://www.who.int/news-room/fact-sheets/detail/alcohol"),
        ("Ministry of Home Affairs — ERSS 112", "https://www.mha.gov.in/emergency-response-support-system-erss"),
        ("MoHFW / DGHS — Tele-MANAS", "https://dghs.mohfw.gov.in/national-mental-health-programme.php"),
        ("NALSA — Legal aid", "https://nalsa.gov.in/promoting-inclusive-legal-system/"),
        ("National Scholarship Portal", "https://scholarships.gov.in/All-Scholarships"),
    ]
    for label,url in source_links: st.markdown(f"- [{label}]({url})")
    st.caption("Last source review recorded in the bundled knowledge base: 12 November 2026. Verify each source again before public release.")

st.divider()
st.caption("AlnonAI 2.0 · Student prototype · Not a medical device, clinical service or emergency-response service.")
