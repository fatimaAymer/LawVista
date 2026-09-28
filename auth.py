import streamlit as st


def initialize_session():
    """Create authentication session variables if they do not exist."""

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if "user_id" not in st.session_state:
        st.session_state.user_id = None

    if "user_name" not in st.session_state:
        st.session_state.user_name = None

    if "user_role" not in st.session_state:
        st.session_state.user_role = None


def require_login():
    """Block a page until the user logs in."""

    initialize_session()

    if not st.session_state.logged_in:
        st.warning("🔐 Please login to access this feature.")
        st.info(
            "Open **login register** from the sidebar and login "
            "to continue."
        )
        st.stop()


def require_role(allowed_roles):
    """Allow access only to selected account roles."""

    require_login()

    if st.session_state.user_role not in allowed_roles:
        st.error("⛔ You do not have permission to access this page.")
        st.stop()


def current_user_id():
    initialize_session()
    return st.session_state.user_id


def current_user_name():
    initialize_session()
    return st.session_state.user_name


def current_user_role():
    initialize_session()
    return st.session_state.user_role


def logout_user():
    """Clear the current LawVista login session."""

    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.user_name = None
    st.session_state.user_role = None 