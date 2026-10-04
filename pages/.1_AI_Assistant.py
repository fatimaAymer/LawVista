import streamlit as st
from openai import OpenAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(
    page_title="AI Legal Assistant | LawVista",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Legal Assistant")
st.write("Ask questions about Pakistani law in English or Roman Urdu.")

language = st.selectbox(
    "Select Language",
    ["English", "Roman Urdu"]
)

question = st.text_area(
    "Enter your legal question",
    placeholder="Example: What is bail under Pakistani law?"
)

if st.button("⚖️ Ask LawVista"):
    if question.strip():
      st.info("LawVista is preparing your legal answer...")
      try:
    response = client.responses.create(
        model="gpt-5-nano",
        input=question
    )
    st.write(response.output_text)

except Exception:
    st.error(
        "Unable to connect to the AI service right now. "
        "Please check your internet connection and try again."
    )
    st.stop()
    
      st.write(response.output_text)
      st.write("**Your Question:**", question)
      st.write("**Language:**", language)
else:
        st.warning("Please enter a legal question.")

st.divider()

st.caption(
    "LawVista provides AI-assisted legal information. "
    "Important legal matters should be verified from authoritative sources "
    "or a qualified lawyer."
)