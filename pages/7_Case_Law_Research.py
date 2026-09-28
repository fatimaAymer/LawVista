import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("🔎 Case Law Finder")

st.write(
    "Find relevant Pakistani case law, precedents and judicial decisions "
    "for a legal issue."
)

st.divider()

legal_issue = st.text_area(
    "⚖️ Describe Your Legal Issue",
    placeholder=(
        "Example: My tenant has not paid rent for six months. "
        "Find relevant Pakistani case law..."
    ),
    height=140
)

col1, col2 = st.columns(2)

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
    legal_area = st.selectbox(
        "Area of Law",
        [
            "All Areas",
            "Constitutional Law",
            "Civil Law",
            "Criminal Law",
            "Family Law",
            "Property Law",
            "Corporate Law",
            "Tax Law",
            "Labour Law",
            "Banking Law",
            "Contract Law",
            "Rent Law",
            "Other"
        ]
    )

keywords = st.text_input(
    "🔑 Keywords (Optional)",
    placeholder="Example: tenant, rent, eviction, default"
)

st.divider()

if st.button("🔎 Find Relevant Cases", type="primary"):

    if not legal_issue.strip():
        st.warning("Please describe your legal issue first.")

    else:
        st.success("Legal issue received successfully.")
        prompt = f"""Find relevant Pakistani case law for the following legal issue.

Legal Issue: {legal_issue}
Court: {court}
Area of Law: {legal_area}
Keywords: {keywords}

Provide potentially relevant cases with case name, court, year, citation if reliably known, legal principle, and relevance to the issue.

Do not invent or guess case citations. Clearly state when a citation or case detail requires verification."""
        try:
            response = client.responses.create(
                model="gpt-5-nano",
                input=prompt
            )
        except Exception as e:
            st.error("AI case-law search is temporarily unavailable. Please check your API credits and try again later.")
            st.stop()
            st.subheader("⚖️ AI Case Law Results")
        st.markdown(response.output_text)

        st.subheader("⚖️ Case Law Results")

        st.write("**Legal Issue:**", legal_issue)
        st.write("**Court:**", court)
        st.write("**Area of Law:**", legal_area)

        if keywords:
            st.write("**Keywords:**", keywords)

        st.info(
            "The intelligent case-law search engine will be connected "
            "to Pakistani legal sources in the next development stage."
        )

st.divider()

st.caption(
    "LawVista case-law results are provided for legal research assistance. "
    "Case citations and judgments should be verified from authoritative sources."
)