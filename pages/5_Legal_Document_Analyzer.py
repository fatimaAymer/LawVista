import streamlit as st
from openai import OpenAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
def extract_docx_text(uploaded_file):
    document = Document(uploaded_file)
    return "\n".join(
        paragraph.text
        for paragraph in document.paragraphs
        if paragraph.text.strip()
    )
from docx import Document

st.set_page_config(
    page_title="Document Analyzer | LawVista",
    page_icon="📄",
    layout="wide"
)

st.title("📄 AI Legal Document Analyzer")
st.write("Upload a legal document for analysis, summary and important-point extraction.")

uploaded_file = st.file_uploader(
    "Upload Legal Document",
    type=["pdf", "docx", "txt"]
)

analysis_type = st.multiselect(
    "Select Analysis",
    [
        "Document Summary",
        "Important Clauses",
        "Legal Issues",
        "Rights & Obligations",
        "Important Dates",
        "Parties Involved",
        "Possible Risks",
        "Relevant Laws",
        "Relevant Case Law",
        "Action Points"
    ],
    default=["Document Summary", "Important Clauses"]
)

language = st.selectbox(
    "Output Language",
    ["English", "Roman Urdu"]
)

if uploaded_file:
    st.success(f"Uploaded: {uploaded_file.name}")

    if st.button("🔍 Analyze Document"):
       document_text = extract_docx_text(uploaded_file)
    try:
       response = client.responses.create(
            model="gpt-5-nano",
            input=f"""Analyze this legal document:\n\n{document_text}"""
)
    except Exception as e:
            st.error("AI analysis is temporarily unavailable. Please check your API credits and try again later.")
            st.stop()
    st.info("Document received successfully. AI analysis will be connected in the next stage.")
    st.markdown(response.output_text)

    st.subheader("📝 Summary")
    st.write("AI-generated document summary will appear here.")

    st.subheader("⚖️ Legal Issues")
    st.write("Important legal issues will appear here.")

    st.subheader("📌 Important Clauses")
    st.write("Important clauses and obligations will appear here.")

    st.subheader("⚠️ Risks / Attention Points")
    st.write("Potential legal risks will appear here.")

    st.subheader("📚 Relevant Laws & Case Law")
    st.write("Relevant legal provisions and precedents will appear here.")

st.warning(
    "AI-generated analysis is informational and should be verified "
    "against the original document and authoritative legal sources."
)