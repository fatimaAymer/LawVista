import streamlit as st
from datetime import date, time,datetime
from database import get_connection
from auth import require_login
require_login()
user_id = st.session_state.user_id

st.title("🗓️ Court Schedule")

st.write(
    "Manage hearing dates, court appearances, reminders and case schedules."
)

st.divider()

st.subheader("➕ Add Court Hearing")

case_title = st.text_input(
    "📁 Case Title",
    placeholder="Example: Ali vs Ahmed"
)

case_number = st.text_input(
    "🔢 Case Number",
    placeholder="Example: Civil Suit 123/2026"
)

col1, col2 = st.columns(2)

with col1:
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

    hearing_date = st.date_input(
        "📅 Hearing Date",
        value=date.today()
    )

with col2:
    hearing_type = st.selectbox(
        "📌 Hearing Type",
        [
            "Regular Hearing",
            "Arguments",
            "Evidence",
            "Cross Examination",
            "Bail Hearing",
            "Final Arguments",
            "Judgment",
            "Other"
        ]
    )

    hearing_time = st.time_input(
        "⏰ Hearing Time",
        value=time(9, 0)
    )

lawyer_name = st.text_input(
    "👨‍⚖️ Lawyer / Counsel",
    placeholder="Enter lawyer name"
)

notes = st.text_area(
    "📝 Hearing Notes",
    placeholder="Enter preparation notes, required documents or hearing details...",
    height=120
)

reminder = st.selectbox(
    "🔔 Reminder",
    [
        "No Reminder",
        "1 Day Before",
        "2 Days Before",
        "3 Days Before",
        "7 Days Before"
    ]
)

st.divider()

if st.button("💾 Save Hearing", type="primary"):

    if not case_title.strip():
        st.warning("Please enter the case title.")

    else:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO hearings
            (user_id, case_title, case_number, court, hearing_type,
             hearing_date, hearing_time, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            
                (
                 user_id,
                 case_title,
                 case_number,
                 court,
                 hearing_type,
                 str(hearing_date),
                 str(hearing_time),
                 notes
            )
        )

        conn.commit()
        conn.close()
        st.success("Court hearing added successfully for this session.")

        st.subheader("📅 Hearing Summary")

        st.write("**Case:**", case_title)
        st.write("**Case Number:**", case_number)
        st.write("**Court:**", court)
        st.write("**Hearing Type:**", hearing_type)
        st.write("**Date:**", hearing_date)
        st.write("**Time:**", hearing_time)
        st.write("**Lawyer:**", lawyer_name)
        st.write("**Reminder:**", reminder)

        if notes:
            st.write("**Notes:**", notes)

st.divider()

st.subheader("📋 Upcoming Hearings")
search_hearing = st.text_input(
    "🔍 Search Hearings",
    placeholder="Search by case title, case number, or court..."
)

conn = get_connection()
cursor = conn.cursor()

if search_hearing.strip():
    search_value = f"%{search_hearing.strip()}%"

    cursor.execute(
        """
        SELECT id, case_title, case_number, court,
               hearing_type, hearing_date, hearing_time, notes
        FROM hearings 
        WHERE user_id = ?
AND (
    case_title LIKE ?
           OR case_number LIKE ?
           OR court LIKE ?
        (user_id, search_value, search_value, search_value)
        (search_value, search_value, search_value)
        """
    )
else:
    cursor.execute(
        """
        SELECT id, case_title, case_number, court,
               hearing_type, hearing_date, hearing_time, notes
        FROM hearings
        WHERE user_id = ?
        ORDER BY hearing_date ASC, hearing_time ASC
        """,
        (user_id,)
    )

hearings = cursor.fetchall()
conn.close()
if hearings:
    for hearing in hearings:
        with st.expander(
            f"⚖️ {hearing[1]} — {hearing[5]} at {hearing[6]}"
        ):
            st.write("**Case Number:**", hearing[2])
            st.write("**Court:**", hearing[3])
            st.write("**Hearing Type:**", hearing[4])
            st.write("**Date:**", hearing[5])
            st.write("**Time:**", hearing[6])

            if hearing[7]:
                st.write("**Notes:**", hearing[7])
                col1, col2 = st.columns(2)
            

            with col1:
                if st.button(
                    "✏️ Edit Hearing",
                    key=f"edit_hearing_{hearing[0]}"
                ):
                    st.session_state["edit_hearing_id"] = hearing[0]
                    st.rerun()

            with col2:
                if st.button(
                    "🗑️ Delete Hearing",
                    key=f"delete_hearing_{hearing[0]}"
                ):
                    conn = get_connection()
                    cursor = conn.cursor()

                    cursor.execute(
                        "DELETE FROM hearings WHERE id = ? AND user_id = ?",
                        (hearing[0], user_id)
                    )

                    conn.commit()
                    conn.close()

                    st.success("Hearing deleted successfully.")
                    st.rerun()
else:
    st.info("No upcoming hearings have been saved yet.")


st.caption(
    "LawVista Court Schedule helps organize hearing dates "
    "and important case reminders."
)


# =========================
# EDIT HEARING
# =========================

if "edit_hearing_id" in st.session_state:
    edit_id = st.session_state["edit_hearing_id"]

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
       "SELECT * FROM hearings WHERE id = ? AND user_id = ?",
        (edit_id, user_id)
    )

    edit_hearing = cursor.fetchone()
    conn.close()
    if edit_hearing is None:
        st.session_state.pop("edit_hearing_id", None)
        st.warning("This hearing no longer exists. Please select a hearing again.")
        st.rerun()
    if "edit_hearing_id" in st.session_state:
        st.divider()
        st.subheader("✏️ Edit Hearing")
       

        new_case_title = st.text_input(
            "Case Title",
            value=edit_hearing[1],
            key="edit_case_title"
        )

        new_case_number = st.text_input(
            "Case Number",
            value=edit_hearing[2] or "",
            key="edit_case_number"
        )

        new_court = st.text_input(
            "Court",
            value=edit_hearing[3] or "",
            key="edit_court"
        )

        new_hearing_type = st.text_input(
            "Hearing Type",
            value=edit_hearing[4] or "",
            key="edit_hearing_type"
        )

        new_hearing_date = st.text_input(
            "Hearing Date",
            value=edit_hearing[5] or "",
            key="edit_hearing_date"
        )

        new_hearing_time = st.text_input(
            "Hearing Time",
            value=edit_hearing[6] or "",
            key="edit_hearing_time"
        )

        new_notes = st.text_area(
            "Notes",
            value=edit_hearing[7] or "",
            key="edit_notes"
        )
        if st.button("💾 Save Changes", type="primary"):
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                UPDATE hearings
                SET case_title = ?,
                    case_number = ?,
                    court = ?,
                    hearing_type = ?,
                    hearing_date = ?,
                    hearing_time = ?,
                    notes = ?
                WHERE id = ?
                """,
                (
                    new_case_title,
                    new_case_number,
                    new_court,
                    new_hearing_type,
                    new_hearing_date,
                    new_hearing_time,
                    new_notes,
                    edit_id,
                )
            )

            conn.commit()
            conn.close()

            del st.session_state["edit_hearing_id"]

            st.success("Hearing updated successfully.")
            st.rerun()