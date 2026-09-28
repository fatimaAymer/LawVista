import streamlit as st
from database import get_connection
from datetime import date
from auth import require_login, current_user_id
require_login()
user_id = current_user_id()

st.title("📁 Case Management")

st.write(
    "Create and manage legal cases, client information, notes and important dates."
)

st.divider()

st.subheader("➕ Add New Case")

case_title = st.text_input(
    "Case Title",
    placeholder="Example: Ali vs Ahmed"
)

col1, col2 = st.columns(2)

with col1:
    client_name = st.text_input(
        "👤 Client Name",
        placeholder="Enter client name"
    )

    case_number = st.text_input(
        "🔢 Case Number",
        placeholder="Example: Civil Suit 123/2026"
    )

with col2:
    court = st.selectbox(
        "⚖️ Court",
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
            "District Court",
            "Sessions Court",
            "Civil Court",
            "Other"
        ]
    )

    case_status = st.selectbox(
        "📌 Case Status",
        [
            "Active",
            "Pending",
            "Next Hearing",
            "Reserved",
            "Decided",
            "Closed"
        ]
    )

case_type = st.selectbox(
    "📚 Case Type",
    [
        "Civil",
        "Criminal",
        "Constitutional",
        "Family",
        "Property",
        "Corporate",
        "Tax",
        "Labour",
        "Banking",
        "Rent",
        "Other"
    ]
)

status = st.selectbox(
    "Case Status",
    ["Open", "Pending", "In Progress", "Closed"]
)

next_hearing = st.date_input(
    "📅 Next Hearing Date",
    value=date.today()
)

notes = st.text_area(
    "📝 Case Notes",
    placeholder=(
        "Enter important facts, previous proceedings, "
        "orders, tasks or other case notes..."
    ),
    height=150
)

st.divider()

if st.button("💾 Save Case", type="primary"):

    if not case_title.strip():
        st.warning("Please enter the case title.")

    elif not client_name.strip():
        st.warning("Please enter the client name.")
    else:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
    """
    INSERT INTO cases
    (
        case_title,
        client_name,
        case_number,
        court,
        case_type,
        status,
        notes,
        user_id
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """,
    (
        case_title,
        client_name,
        case_number,
        court,
        case_type,
        status,
        notes,
        user_id,
    )
)

        conn.commit()
        conn.close()

        st.success("Case saved successfully for this session.")


st.divider()

st.subheader("📂 Saved Cases")
search_case = st.text_input(
    "🔍 Search Cases",
    placeholder="Search by case title, client name, case number or court..."
)

conn = get_connection()
cursor = conn.cursor()

if search_case:
    search_value = f"%{search_case}%"

    cursor.execute(
        """
        SELECT id, case_title, client_name, case_number,
               court, case_type, case_status, created_at
        FROM cases
        WHERE user_id = ?
          AND (
              case_title LIKE ?
              OR client_name LIKE ?
              OR case_number LIKE ?
              OR court LIKE ?
          )
        ORDER BY id DESC
        """,
        (
            user_id,
            search_value,
            search_value,
            search_value,
            search_value,
        )
    )
else:
    cursor.execute(
        """
        SELECT id, case_title, client_name, case_number,
               court, case_type, case_status, created_at
        FROM cases
        WHERE user_id = ?
        ORDER BY id DESC
        """,
        (user_id,)
    )

cases = cursor.fetchall()
conn.close()

if cases:
    for case in cases:
        with st.expander(f"⚖️ {case[1]} — {case[3] or 'No Case Number'}"):
            col1, col2 = st.columns(2)

            with col1:
                st.write("**Client:**", case[2])
                st.write("**Case Number:**", case[3])
                st.write("**Case Type:**", case[5])

            with col2:
                st.write("**Court:**", case[4])
                st.write("**Status:**", case[6])
                st.write("**Saved:**", case[7])
            if st.button("✏️ Edit Case", key=f"edit_{case[0]}"):
               st.session_state["edit_case_id"] = case[0]
               st.rerun()

        if st.button("🗑️ Delete Case", key=f"delete_{case[0]}"):
            st.session_state["delete_case_id"] = case[0]
            st.rerun()
else:
    st.info("No cases have been saved yet.")
    # ======================
# DELETE CASE SECTION
# ======================

if "delete_case_id" in st.session_state:
    delete_id = st.session_state["delete_case_id"]

    st.divider()
    st.subheader("⚠️ Delete Case")

    st.warning(
        "Are you sure you want to permanently delete this case? "
        "This action cannot be undone."
    )

    col_yes, col_no = st.columns(2)

    with col_yes:
        if st.button("🗑️ Yes, Delete Case", type="primary"):
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                    "DELETE FROM cases WHERE id = ? AND user_id = ?",
                    (delete_id, user_id)
                )

         

            conn.commit()
            conn.close()

            del st.session_state["delete_case_id"]

            st.success("Case deleted successfully.")
            st.rerun()

    with col_no:
        if st.button("❌ Cancel Delete"):
            del st.session_state["delete_case_id"]
            st.rerun()

# =========================
# EDIT CASE SECTION
# =========================

if "edit_case_id" in st.session_state:

    edit_id = st.session_state["edit_case_id"]

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, case_title, client_name, case_number,
               court, case_type, case_status, notes
        FROM cases
       WHERE id = ? AND user_id = ?
        """,
       (edit_id, user_id) 
    )

    edit_case = cursor.fetchone()
    conn.close()

    if edit_case:

        st.divider()
        st.subheader("✏️ Edit Case")

        edit_title = st.text_input(
            "Case Title",
            value=edit_case[1],
            key="edit_title"
        )

        edit_client = st.text_input(
            "Client Name",
            value=edit_case[2] or "",
            key="edit_client"
        )

        edit_number = st.text_input(
            "Case Number",
            value=edit_case[3] or "",
            key="edit_number"
        )

        edit_court = st.text_input(
            "Court",
            value=edit_case[4] or "",
            key="edit_court"
        )

        edit_type = st.text_input(
            "Case Type",
            value=edit_case[5] or "",
            key="edit_type"
        )

        edit_status = st.text_input(
            "Case Status",
            value=edit_case[6] or "",
            key="edit_status"
        )

        edit_notes = st.text_area(
            "Case Notes",
            value=edit_case[7] or "",
            key="edit_notes"
        )

        col_update, col_cancel = st.columns(2)

        with col_update:
            if st.button("💾 Update Case", type="primary"):

                conn = get_connection()
                cursor = conn.cursor()

                cursor.execute(
                    """
                    UPDATE cases
                    SET case_title = ?,
                        client_name = ?,
                        case_number = ?,
                        court = ?,
                        case_type = ?,
                        case_status = ?,
                        notes = ?
                    WHERE id = ? AND user_id = ?
                    """,
                    (
                        edit_title,
                        edit_client,
                        edit_number,
                        edit_court,
                        edit_type,
                        edit_status,
                        edit_notes,
                        edit_id,
                        user_id
                    )
                )

                conn.commit()
                conn.close()

                del st.session_state["edit_case_id"]

                st.success("Case updated successfully.")
                st.rerun()

        with col_cancel:
            if st.button("❌ Cancel Edit"):
                del st.session_state["edit_case_id"]
                st.rerun()
st.caption(
    "LawVista Case Management helps organize case information "
    "and important legal dates."
)