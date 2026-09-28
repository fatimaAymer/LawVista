import streamlit as st

st.set_page_config(
    page_title="Judgments | LawVista",
    page_icon="⚖️",
    layout="wide"
)

st.title("⚖️ Judgments & Judicial Decisions")
st.write(
    "Search Pakistani court judgments, judicial decisions, "
    "case citations and precedents."
)

# Search
search = st.text_input(
    "🔎 Search Judgments",
    placeholder="Enter case name, citation, judge, keyword or legal issue..."
)

# Filters
col1, col2, col3 = st.columns(3)

with col1:
    court = st.selectbox(
        "Court",
        [
            "All Courts",
            "Supreme Court of Pakistan",
            "Federal Shariat Court",
            "Islamabad High Court",
            "Lahore High Court",
            "Sindh High Court",
            "Peshawar High Court",
            "Balochistan High Court",
            "Supreme Court of AJ&K",
            "High Court of AJ&K"
        ]
    )

with col2:
    year = st.selectbox(
        "Year",
        ["All Years"] + [str(y) for y in range(2026, 1999, -1)]
    )

with col3:
    category = st.selectbox(
        "Legal Area",
        [
            "All Areas",
            "Constitutional",
            "Criminal",
            "Civil",
            "Family",
            "Corporate",
            "Cyber Crime",
            "Tax",
            "Property",
            "Labour"
        ]
    )
judgments = []
judgments = [
    {
        "case_title": "Sample Constitutional Case",
        "citation": "FYP-DEMO-001",
        "court": "Supreme Court of Pakistan",
        "year": "2024",
        "category": "Constitutional",
        "summary": "Sample academic judgment record used to demonstrate LawVista's judgment search functionality."
    }
]

st.divider()

st.subheader("📑 Judgment Results")

if search:
    results = [
        judgment for judgment in judgments
        if search.lower() in judgment["case_title"].lower()
        or search.lower() in judgment["citation"].lower()
        or search.lower() in judgment["court"].lower()
        or search.lower() in judgment["category"].lower()
    ]

    if results:
        for judgment in results:
            st.subheader(judgment["case_title"])
            st.write(f"**Citation:** {judgment['citation']}")
            st.write(f"**Court:** {judgment['court']}")
            st.write(f"**Year:** {judgment['year']}")
            st.write(f"**Category:** {judgment['category']}")
            st.write(f"**Summary:** {judgment['summary']}")
    else:
        st.warning("No matching judgments found.")
else:
    st.info("Enter a case name, citation, court or legal category to search judgments.")

st.divider()

st.subheader("📋 Judgment Information")

col1, col2 = st.columns(2)

with col1:
    st.write("**Case Title:** —")
    st.write("**Court:** —")
    st.write("**Judge / Bench:** —")
    st.write("**Decision Date:** —")

with col2:
    st.write("**Citation:** —")
    st.write("**Case Number:** —")
    st.write("**Legal Issues:** —")
    st.write("**Status:** —")

st.subheader("📝 Judgment Summary")
st.write("Select a judgment to view its summary and important legal principles.")

st.subheader("⚖️ Judge / Bench Decision")
st.write("The relevant judge or bench decision will appear here.")

st.subheader("🔗 Official Source")
st.write(
    "A verified source link to the relevant court judgment "
    "will be displayed here."
)

st.warning(
    "Judgments and citations should be verified against the official "
    "court record before professional legal use."
)