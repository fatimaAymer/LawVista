import streamlit as st

st.set_page_config(
    page_title="Laws Library | LawVista",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Pakistan Laws Library")
st.write("Search and browse Pakistani Acts, laws, rules and legal provisions.")

search = st.text_input(
    "🔎 Search laws",
    placeholder="Example: Constitution, PPC, CrPC, Contract Act..."
)

category = st.selectbox(
    "Select Category",
    [
        "All Laws",
        "Constitutional Law",
        "Criminal Law",
        "Civil Law",
        "Family Law",
        "Corporate & Commercial Law",
        "Cyber Law",
        "Tax Law",
        "Labour Law",
        "Property Law"
    ]
)

st.subheader("⚖️ Important Pakistani Laws")

laws = [
    {
    "title": "Constitution of the Islamic Republic of Pakistan, 1973",
    "category": "Constitutional Law",
    "summary": "The supreme law of Pakistan defining the structure of the State, fundamental rights, institutions, Parliament, judiciary and constitutional governance.",
    "source": "Official Constitution of Pakistan",
    "year": "1973",
    },
    
    {
    "title": "Pakistan Penal Code, 1860",
    "category": "Criminal Law",
    "summary": "The principal criminal law defining offences and punishments in Pakistan.",
    "source": "Pakistan Penal Code, 1860",
    "year": "1860",
},
    {
    "title": "Code of Criminal Procedure, 1898",
    "category": "Criminal Law",
    "summary": "The principal procedural law governing criminal investigation, trial, bail, arrest and criminal court proceedings in Pakistan.",
    "source": "Code of Criminal Procedure, 1898",
    "year": "1898",
},
    {
    "title": "Code of Civil Procedure, 1908",
    "category": "Civil Law",
    "summary": "The principal procedural law governing civil suits, court proceedings, decrees, orders and execution of civil judgments in Pakistan.",
    "source": "Code of Civil Procedure, 1908",
    "year": "1908",
},

    {
    "title": "Qanun-e-Shahadat Order, 1984",
    "category": "Civil Law",
    "summary": "The principal law of evidence in Pakistan governing relevancy, admissibility and proof of facts in judicial proceedings.",
    "source": "Qanun-e-Shahadat Order, 1984",
    "year": "1984",
},
    {
    "title": "Contract Act, 1872",
    "category": "Corporate & Commercial Law",
    "summary": "The principal law governing contracts, agreements, obligations and enforceable promises in Pakistan.",
    "source": "Contract Act, 1872",
    "year": "1872",
},
    {
    "title": "Specific Relief Act, 1877",
    "category": "Civil Law",
    "summary": "Provides civil remedies including specific performance, recovery of possession, injunctions and other forms of specific relief.",
    "source": "Specific Relief Act, 1877",
    "year": "1877",
},
{
    "title": "Muslim Family Laws Ordinance, 1961",
    "category": "Family Law",
    "summary": "Regulates important aspects of Muslim family law in Pakistan, including marriage registration, polygamy, divorce and maintenance.",
    "source": "Muslim Family Laws Ordinance, 1961",
    "year": "1961",
},
{
    "title": "Companies Act, 2017",
    "category": "Corporate & Commercial Law",
    "summary": "Provides the legal framework for incorporation, management, regulation and governance of companies in Pakistan.",
    "source": "Companies Act, 2017",
    "year": "2017",
},
{
    "title": "Prevention of Electronic Crimes Act, 2016",
    "category": "Cyber Law",
    "summary": "Provides the legal framework for specified electronic offences, investigation procedures and related cybercrime matters in Pakistan.",
    "source": "Prevention of Electronic Crimes Act, 2016",
    "year": "2016",
},
]

for law in laws:
    if not search or search.lower() in (law["title"] if isinstance(law, dict) else law).lower():
        with st.expander(f"📖 {law['title'] if isinstance(law, dict) else law}"):
             st.write(law["summary"] if isinstance(law, dict) else "Law text, sections, explanations and source documents will be available here.")
    if st.button("Open Law", key=law):
               st.session_state["selected_law"] = law
               st.success(f"Opening: {law['title'] if isinstance(law, dict) else law}")
               st.subheader(law["title"] if isinstance(law, dict) else law)
    if isinstance(law, dict):
                st.write(f"**Year:** {law['year']}")
                st.write(f"**Summary:** {law['summary']}")

st.divider()

st.info(
    "LawVista will connect this library with authoritative Pakistani "
    "legal sources and searchable legal documents."
)