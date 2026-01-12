import streamlit as st

def require_admin():
    """
    Protect admin pages from unauthorized access
    """
    if not st.session_state.get("logged_in"):
        st.error("🔒 Please login first")
        st.stop()

    if st.session_state.get("role") != "admin":
        st.error("⛔ Admin access only")
        st.stop()
