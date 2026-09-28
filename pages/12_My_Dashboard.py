import streamlit as st

from auth import require_login, current_user_id
from database import get_connection


require_login()

st.set_page_config(
    page_title="User Dashboard | LawVista",
    page_icon="👤",
    layout="wide"
)

user_id = current_user_id()

# -------------------------
# LOAD USER
# -------------------------

conn = get_connection()
cursor = conn.cursor()

cursor.execute(
    """
    SELECT id, full_name, email, role, phone, city, created_at
    FROM users
    WHERE id = ?
    """,
    (user_id,)
)

user = cursor.fetchone()

if user is None:
    conn.close()
    st.error("User account could not be found.")
    st.stop()


# -------------------------
# DASHBOARD COUNTS
# -------------------------

cursor.execute(
    "SELECT COUNT(*) FROM cases WHERE user_id = ?",
    (user_id,)
)
case_count = cursor.fetchone()[0]

cursor.execute(
    "SELECT COUNT(*) FROM hearings WHERE user_id = ?",
    (user_id,)
)
hearing_count = cursor.fetchone()[0]

cursor.execute(
    "SELECT COUNT(*) FROM document_analysis WHERE user_id = ?",
    (user_id,)
)
document_count = cursor.fetchone()[0]

cursor.execute(
    "SELECT COUNT(*) FROM legal_drafts WHERE user_id = ?",
    (user_id,)
)
draft_count = cursor.fetchone()[0]

cursor.execute(
    "SELECT COUNT(*) FROM ai_chats WHERE user_id = ?",
    (user_id,)
)
chat_count = cursor.fetchone()[0]


# -------------------------
# PAGE HEADER
# -------------------------

st.title("👤 LawVista User Dashboard")

st.success(
    f"Welcome, {user['full_name']}!"
)

st.caption(
    "Your personal LawVista legal workspace."
)


# -------------------------
# PROFILE
# -------------------------

st.subheader("🪪 My Profile")

col1, col2, col3 = st.columns(3)

with col1:
    st.write("**Name:**", user["full_name"])
    st.write("**Email:**", user["email"])

with col2:
    st.write("**Role:**", user["role"].title())
    st.write("**Phone:**", user["phone"] or "Not provided")

with col3:
    st.write("**City:**", user["city"] or "Not provided")
    st.write("**Member Since:**", user["created_at"])


# -------------------------
# STATISTICS
# -------------------------

st.divider()
st.subheader("📊 My LawVista Activity")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("📁 Cases", case_count)

with col2:
    st.metric("📅 Hearings", hearing_count)

with col3:
    st.metric("📄 Documents", document_count)

with col4:
    st.metric("✍️ Drafts", draft_count)

with col5:
    st.metric("🤖 AI Chats", chat_count)


# -------------------------
# UPCOMING HEARINGS
# -------------------------

st.divider()
st.subheader("📅 Upcoming Hearings")

cursor.execute(
    """
    SELECT case_title, case_number, court,
           hearing_type, hearing_date, hearing_time
    FROM hearings
WHERE user_id = ?
ORDER BY hearing_date ASC, hearing_time ASC
LIMIT 5
""",
(user_id,)

)

hearings = cursor.fetchall()

if hearings:

    for hearing in hearings:

        with st.expander(
            f"⚖️ {hearing['case_title']} — "
            f"{hearing['hearing_date']}"
        ):
            st.write(
                "**Case Number:**",
                hearing["case_number"] or "Not provided"
            )

            st.write(
                "**Court:**",
                hearing["court"] or "Not provided"
            )

            st.write(
                "**Hearing Type:**",
                hearing["hearing_type"] or "Not provided"
            )

            st.write(
                "**Time:**",
                hearing["hearing_time"] or "Not provided"
            )

else:
    st.info("No hearings have been scheduled yet.")


# -------------------------
# RECENT AI ACTIVITY
# -------------------------

st.divider()
st.subheader("🤖 Recent AI Legal Assistant Activity")

cursor.execute(
    """
    SELECT question, answer, created_at
    FROM ai_chats
    WHERE user_id = ?
    ORDER BY id DESC
    LIMIT 3
    """,
    (user_id,)
)

chats = cursor.fetchall()

if chats:

    for chat in chats:
        with st.expander(chat["question"]):
            st.write(chat["answer"] or "No answer stored.")
            st.caption(chat["created_at"])

else:
    st.info("No AI Legal Assistant history yet.")


conn.close()


# -------------------------
# QUICK ACCESS
# -------------------------

st.divider()
st.subheader("⚡ Quick Access")

st.write(
    """
    Use the sidebar to access:

    • 🤖 AI Legal Assistant  
    • 📚 Laws Library  
    • ⚖️ Judgments  
    • 👨‍⚖️ Find Lawyer  
    • 📄 Document Analyzer  
    • ✍️ Legal Drafting  
    • 🔎 Case Law Finder  
    • 📁 Case Management  
    • 📅 Court Schedule  
    • 🎓 Law Student Mode
    """
)

st.caption(
    "LawVista — AI-Powered Legal Assistant for Pakistan"
)