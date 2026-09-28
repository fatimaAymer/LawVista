import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("✍️ AI Legal Drafting")

st.write(
    "Prepare structured legal document drafts for Pakistani legal matters."
)

st.divider()

# Document type
document_type = st.selectbox(
    "📄 Document Type",
    [
        "Legal Notice",
        "Application",
        "Agreement",
        "Affidavit",
        "Petition",
        "Reply",
        "Power of Attorney",
        "Undertaking",
        "Other"
    ]
)

# Parties
col1, col2 = st.columns(2)

with col1:
    first_party = st.text_input(
        "First Party / Applicant"
    )

with col2:
    second_party = st.text_input(
        "Second Party / Respondent"
    )

# Jurisdiction
jurisdiction = st.selectbox(
    "⚖️ Jurisdiction",
    [
        "Pakistan",
        "Islamabad Capital Territory",
        "Punjab",
        "Sindh",
        "Khyber Pakhtunkhwa",
        "Balochistan",
        "Azad Jammu & Kashmir",
        "Gilgit-Baltistan"
    ]
)

# Facts
facts = st.text_area(
    "📝 Facts / Background",
    placeholder="Enter the facts and background of the legal matter...",
    height=150
)

# Requirements
requirements = st.text_area(
    "📌 Drafting Requirements",
    placeholder="Explain what you want the legal document to contain...",
    height=120
)

# Language
language = st.selectbox(
    "🌐 Draft Language",
    [
        "English",
        "Urdu"
    ]
)

st.divider()

if st.button("✍️ Generate Draft", type="primary"):

    if not facts.strip():
        st.warning("Please enter the facts/background of the matter.")

    else:
        st.success("Draft information received successfully.")
        prompt = f"""Draft a professional {document_type} under the laws of {jurisdiction}.
First Party / Applicant: {first_party}
Second Party / Respondent: {second_party}
Facts / Background: {facts}
Drafting Requirements: {requirements}
Language: {language}

Prepare a structured legal draft. Do not invent case citations, statutory provisions, dates, or facts. Where information is missing, clearly mark it for completion or verification."""
try:
    response = client.responses.create(
        model="gpt-5-nano",
        input=prompt
    )
except Exception as e:
    st.error("AI drafting is temporarily unavailable. Please check your API credits and try again later.")
    st.stop()
    st.subheader("📄 Generated Legal Draft")
st.markdown(response.output_text)
st.subheader("📄 Draft Preview")

st.write("**Document Type:**", document_type)
st.write("**First Party / Applicant:**", first_party)
st.write("**Second Party / Respondent:**", second_party)
st.write("**Jurisdiction:**", jurisdiction)
st.write("**Language:**", language)

st.info(
            "AI drafting functionality will be connected in the next development stage."
        )

st.divider()

st.caption(
    "LawVista provides AI-assisted legal drafting support. "
    "Generated documents should be reviewed by a qualified legal professional."
)