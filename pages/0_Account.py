import streamlit as st
import hashlib
import re

from database import get_connection, create_tables


create_tables()

st.set_page_config(
    page_title="Login & Register | LawVista",
    page_icon="🔐",
    layout="wide"
)

st.title("🔐 LawVista Account")
st.caption("Secure access to your LawVista legal workspace.")


# -------------------------
# PASSWORD HASHING
# -------------------------

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password, password_hash):
    return hash_password(password) == password_hash


def valid_email(email):
    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return re.match(pattern, email) is not None


# -------------------------
# SESSION STATE
# -------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "user_name" not in st.session_state:
    st.session_state.user_name = None

if "user_role" not in st.session_state:
    st.session_state.user_role = None


# -------------------------
# LOGGED-IN VIEW
# -------------------------

if st.session_state.logged_in:

    st.success(
        f"Welcome, {st.session_state.user_name}! "
        f"You are logged in as {st.session_state.user_role}."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Account Status", "Active")

    with col2:
        st.metric("Role", st.session_state.user_role.title())

    with col3:
        st.metric("LawVista Access", "Granted")

    st.info(
        "You can now use LawVista's legal research, case management, "
        "document analysis and drafting tools."
    )

    if st.button("🚪 Logout", type="primary"):
        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.user_name = None
        st.session_state.user_role = None
        st.success("Logged out successfully.")
        st.rerun()


# -------------------------
# LOGIN / REGISTER
# -------------------------

else:

    login_tab, register_tab = st.tabs(
        ["🔑 Login", "📝 Register"]
    )

    # LOGIN
    with login_tab:

        st.subheader("Login to LawVista")

        login_email = st.text_input(
            "Email",
            key="login_email"
        )

        login_password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        if st.button(
            "🔑 Login",
            type="primary",
            key="login_button"
        ):

            if not login_email or not login_password:
                st.warning("Please enter your email and password.")

            else:
                conn = get_connection()
                cursor = conn.cursor()

                cursor.execute(
                    """
                    SELECT id, full_name, email,
                           password_hash, role, is_active
                    FROM users
                    WHERE LOWER(email) = LOWER(?)
                    """,
                    (login_email.strip(),)
                )

                user = cursor.fetchone()
                conn.close()

                if user is None:
                    st.error("No account was found with this email.")

                elif not user["is_active"]:
                    st.error("This account is currently inactive.")

                elif not verify_password(
                    login_password,
                    user["password_hash"]
                ):
                    st.error("Incorrect password.")

                else:
                    st.session_state.logged_in = True
                    st.session_state.user_id = user["id"]
                    st.session_state.user_name = user["full_name"]
                    st.session_state.user_role = user["role"]

                    st.success("Login successful.")
                    st.rerun()


    # REGISTER
    with register_tab:

        st.subheader("Create a LawVista Account")

        full_name = st.text_input(
            "Full Name",
            key="register_name"
        )

        email = st.text_input(
            "Email Address",
            key="register_email"
        )

        phone = st.text_input(
            "Phone Number",
            key="register_phone"
        )

        city = st.text_input(
            "City",
            key="register_city"
        )

        role = st.selectbox(
            "Account Type",
            ["User", "Lawyer", "Law Student"],
            key="register_role"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="register_password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            key="confirm_password"
        )

        if st.button(
            "📝 Create Account",
            type="primary",
            key="register_button"
        ):

            if not full_name.strip():
                st.warning("Please enter your full name.")

            elif not valid_email(email.strip()):
                st.warning("Please enter a valid email address.")

            elif len(password) < 8:
                st.warning(
                    "Password must contain at least 8 characters."
                )

            elif password != confirm_password:
                st.warning("Passwords do not match.")

            else:
                role_map = {
                    "User": "user",
                    "Lawyer": "lawyer",
                    "Law Student": "student"
                }

                password_hash = hash_password(password)

                conn = get_connection()
                cursor = conn.cursor()

                try:
                    cursor.execute(
                        """
                        INSERT INTO users
                        (
                            full_name,
                            email,
                            password_hash,
                            role,
                            phone,
                            city
                        )
                        VALUES (?, ?, ?, ?, ?, ?)
                        """,
                        (
                            full_name.strip(),
                            email.strip().lower(),
                            password_hash,
                            role_map[role],
                            phone.strip(),
                            city.strip()
                        )
                    )

                    conn.commit()

                    st.success(
                        "Account created successfully. "
                        "You can now open the Login tab."
                    )

                except Exception as error:

                    if "UNIQUE constraint failed" in str(error):
                        st.error(
                            "An account with this email already exists."
                        )
                    else:
                        st.error(
                            f"Account could not be created: {error}"
                        )

                finally:
                    conn.close()


st.divider()

st.caption(
    "LawVista — AI-Powered Legal Assistant for Pakistan"
)