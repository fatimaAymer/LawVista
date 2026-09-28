import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("🎓 Law Student Mode")

st.write(
    "Learn Pakistani law, understand legal concepts, study cases "
    "and practice legal questions."
)

st.divider()

st.subheader("📚 Legal Learning Assistant")

topic = st.text_input(
    "🔍 What do you want to learn?",
    placeholder="Example: Explain Article 199 of the Constitution of Pakistan"
)

col1, col2 = st.columns(2)

with col1:
    subject = st.selectbox(
        "📖 Subject",
        [
            "Constitutional Law",
            "Criminal Law",
            "Civil Law",
            "Law of Contract",
            "Law of Evidence",
            "Family Law",
            "Property Law",
            "Company Law",
            "Administrative Law",
            "International Law",
            "Jurisprudence",
            "Other"
        ]
    )

with col2:
    level = st.selectbox(
        "🎯 Explanation Level",
        [
            "Very Simple",
            "Law Student",
            "Detailed",
            "Exam Preparation"
        ]
    )

learning_mode = st.selectbox(
    "🧠 Learning Mode",
    [
        "Explain a Legal Concept",
        "Case Study",
        "Question & Answer",
        "MCQ Practice",
        "Exam Preparation",
        "Legal Terminology"
    ]
)

st.divider()

if st.button("🎓 Start Learning", type="primary"):

    if not topic.strip():
        st.warning("Please enter a legal topic or question.")

    else:
        st.success("Learning request received.")
        prompt = f"""Act as an educational tutor for a Pakistani law student.

Topic / Question: {topic}
Subject: {subject}
Explanation Level: {level}
Learning Mode: {learning_mode}

Explain the topic accurately and clearly according to the selected learning mode and level. Use structured headings and practical examples where useful. Do not invent case citations, statutory provisions, or legal authorities. Clearly identify anything that should be verified from an authoritative legal source."""
        try:
            response = client.responses.create(
                model="gpt-5-nano",
                input=prompt
            )
        except Exception as e:
            st.error("AI Study Assistant is temporarily unavailable. Please check your API credits and try again later.")
            st.stop()
            st.subheader("📚 AI Study Assistant")
        st.markdown(response.output_text)

        st.subheader("📖 Study Assistant")

        st.write("**Topic:**", topic)
        st.write("**Subject:**", subject)
        st.write("**Level:**", level)
        st.write("**Learning Mode:**", learning_mode)

        st.info(
            "The AI legal tutor will generate explanations, "
            "case examples, questions and study material here "
            "after we connect the AI engine."
        )

st.divider()

st.subheader("⚡ Quick Study Areas")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🇵🇰 Constitution")
    st.write("Study constitutional articles, rights and institutions.")

with col2:
    st.markdown("### ⚖️ Case Law")
    st.write("Understand important judgments and legal principles.")

with col3:
    st.markdown("### 📝 Exam Practice")
    st.write("Practice questions, MCQs and legal problem solving.")

st.divider()

st.warning(
    "Law Student Mode is intended for education and research. "
    "Legal information should be verified from authoritative sources."
)