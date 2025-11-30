from pathlib import Path
import streamlit as st
from epoch_explorer.database.db.connection import get_connection
from epoch_explorer.database.models.user import UserModel

def show():
    st.title("🔐 Login to the system")

    email = st.text_input("Email", value="souvik@example.com")
    password = st.text_input("Password", type="password", value="Password@123")

    if st.button("Login"):
        conn = get_connection()
        user = UserModel(conn)
        user_data = user.authenticate(email, password)

        st.write(user_data)

        if user_data['is_loggedin']:
            # Fetch roles
            rows = user.find_user_full_profile(user_data["id"])
            roles = list({r["role_name"].lower() for r in rows if r.get("role_name")})

            # Primary role
            if "admin" in roles: primary = "admin"
            elif "manager" in roles: primary = "manager"
            else: primary = "user"


            st.session_state.user_logged_in = user_data['is_loggedin']
            st.session_state.username = user_data['name']
            st.session_state.id = user_data['id']
            st.session_state.roles = roles
            st.session_state.role = primary
            st.success("✅ Login successful")
            st.rerun()  # redirect to dashboard
        else:
            st.error("❌ Invalid email or password")