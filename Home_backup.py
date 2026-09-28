import streamlit as st

st.set_page_config(
    page_title="LawVista",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown("""
<style>

/* Main application background */
.stApp {
    background: linear-gradient(135deg, #f8fafc 0%, #eef3f8 100%);
}

/* Main content width */
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1250px;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #071a2f 0%, #0d2b45 100%);
}

[data-testid="stSidebar"] * {
    color: #f8fafc;
}

/* Headings */
h1, h2, h3 {
    color: #102a43;
    font-family: "Segoe UI", sans-serif;
}

/* Buttons */
.stButton > button {
    border-radius: 10px;
    border: 1px solid #c99a2e;
    font-weight: 600;
    padding: 0.55rem 1.2rem;
}

/* Input fields */
.stTextInput input,
.stTextArea textarea,
.stSelectbox div[data-baseweb="select"] {
    border-radius: 8px;
}



/* Dividers */
hr {
    border-color: #d8dee8;
}

</style>
""", unsafe_allow_html=True)
st.title("⚖️ LawVista")
st.subheader("AI-Powered Legal Assistant for Pakistan")

st.write("""
LawVista provides intelligent access to Pakistani laws,
judgments, legal assistance, lawyer contacts and legal education.
""")

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🤖 AI Legal Assistant")
    st.write("Ask questions about Pakistani law.")

    st.subheader("⚖️ Judgments")
    st.write("Search court judgments and judicial decisions.")

    st.subheader("👨‍⚖️ Find a Lawyer")
    st.write("Find lawyers and public professional contact sources.")

with col2:
    st.subheader("📚 Laws Library")
    st.write("Search Pakistani Acts, laws and legal provisions.")

    st.subheader("📄 Document Analyzer")
    st.write("Upload and analyze legal documents.")

    st.subheader("✍️ Legal Drafting")
    st.write("Prepare structured legal-document drafts.")

with col3:
    st.subheader("🔎 Case Law Finder")
    st.write("Find relevant precedents for a legal problem.")

    st.subheader("📁 Case Management")
    st.write("Manage cases, notes and case information.")

    st.subheader("📅 Court Schedule")
    st.write("Manage hearing dates and reminders.")

st.divider()

st.subheader("🎓 Law Student Mode")
st.write("Learn legal concepts, analyze cases and practice questions.")

st.info(
    "LawVista provides AI-assisted legal information. "
    "Important legal matters should be verified from authoritative sources "
    "and qualified legal professionals."
) 
