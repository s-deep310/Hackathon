import streamlit as st

def show():
    st.title("Logout")

    st.warning("Are you sure you want to logout?")

    col1, col2 = st.columns(2)

    # ONE CLICK logout
    with col1:
        if st.button("Yes, Logout"):
            # Clear session completely
            for key in list(st.session_state.keys()):
                del st.session_state[key]

            st.session_state.user_logged_in = False
            st.session_state.username = None

            st.success("Logged out successfully!")
            st.rerun()

    with col2:
        if st.button("Cancel"):
            # return to previous page
            st.session_state.page = None
            st.rerun()
