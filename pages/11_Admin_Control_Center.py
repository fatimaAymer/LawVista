import streamlit as st
from auth import require_role
require_role(["admin"])

st.title("⚙️ LawVista Admin")

st.write(
    "Administration dashboard for managing LawVista content, "
    "users, legal resources and system information."
)

st.divider()

# Dashboard statistics
st.subheader("📊 System Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("👥 Users", "0")

with col2:
    st.metric("⚖️ Cases", "0")

with col3:
    st.metric("📚 Laws", "0")

with col4:
    st.metric("📄 Documents", "0")

st.divider()

# Legal database management
st.subheader("📚 Legal Database Management")

admin_action = st.selectbox(
    "Select Administrative Action",
    [
        "Add Law / Act",
        "Add Judgment",
        "Add Lawyer Record",
        "Manage Legal Documents",
        "Manage Users",
        "System Settings"
    ]
)

if admin_action == "Add Law / Act":

    st.text_input(
        "Law / Act Name",
        placeholder="Example: Constitution of Pakistan 1973"
    )

    st.text_input(
        "Year",
        placeholder="Example: 1973"
    )

    st.text_area(
        "Description",
        placeholder="Enter information about the law...",
        height=120
    )

    st.file_uploader(
        "Upload Law Document",
        type=["pdf", "docx", "txt"]
    )

elif admin_action == "Add Judgment":

    st.text_input(
        "Case Name",
        placeholder="Example: State vs Ahmed"
    )

    st.text_input(
        "Citation",
        placeholder="Example: PLD 2026 SC 100"
    )

    st.selectbox(
        "Court",
        [
            "Supreme Court of Pakistan",
            "Federal Shariat Court",
            "Islamabad High Court",
            "Lahore High Court",
            "Sindh High Court",
            "Peshawar High Court",
            "Balochistan High Court",
            "Supreme Court of AJ&K",
            "High Court of AJ&K",
            "Other"
        ]
    )

    st.file_uploader(
        "Upload Judgment",
        type=["pdf", "docx", "txt"]
    )

elif admin_action == "Add Lawyer Record":

    st.text_input("Lawyer Name")

    st.text_input("Bar Council / Association")

    st.text_input("City")

    st.text_input("Area of Practice")

elif admin_action == "Manage Users":

    st.info(
        "User accounts, roles and permissions will be managed here."
    )

elif admin_action == "Manage Legal Documents":

    st.info(
        "Uploaded laws, judgments and legal documents will be managed here."
    )

elif admin_action == "System Settings":

    st.info(
        "AI configuration, database settings and system controls "
        "will be managed here."
    )

st.divider()

if st.button("💾 Save Admin Record", type="primary"):
    st.success(
        "Admin interface is working. Database saving will be connected next."
    )

st.divider()

st.warning(
    "Admin access will be protected with authentication "
    "before LawVista is deployed publicly."
)

st.caption(
    "LawVista Administration Panel"
)