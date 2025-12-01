import streamlit as st
from epoch_explorer.database.db.connection import get_connection
from epoch_explorer.database.models.role import RoleModel


def tcs_footer():
    st.markdown("""
    <div style='text-align: center; padding: 10px; color: gray; font-size: 12px;'>
        <hr style='border:1px solid #e6e6e6; margin-top: 10px; margin-bottom: 5px;'>
        © 2025 Tata Consultancy Services (TCS) | All Rights Reserved
    </div>
    """, unsafe_allow_html=True)


def show():
    st.title("🔑 Role Management")

    # -------------------------------
    # CHECK LOGIN
    # -------------------------------
    if "user_logged_in" not in st.session_state or not st.session_state.user_logged_in:
        st.error("⚠️ You must login first!")
        st.stop()

    conn = get_connection()
    role_model = RoleModel(conn)

    # -------------------------------
    # Only ADMIN is allowed
    # -------------------------------
    if "roles" not in st.session_state:
        st.error("❌ Could not verify your role permissions.")
        st.stop()

    roles_list = [r.lower() for r in st.session_state.roles]
    if "admin" not in roles_list:
        st.error("🚫 Only Admin can manage roles.")
        st.stop()

    # -------------------------------
    # MENU
    # -------------------------------
    menu = ["View Roles", "Create Role", "Update Role", "Delete Role"]
    action = st.radio("Choose Action", menu, horizontal=True)

    # -------------------------------
    # SUCCESS MSG
    # -------------------------------
    if "success_msg" in st.session_state:
        st.success(st.session_state.success_msg)
        del st.session_state["success_msg"]

    # -------------------------------
    # VIEW ROLES
    # -------------------------------
    if action == "View Roles":
        st.subheader("📋 Available Roles")

        roles = role_model.all()
        if roles:
            st.dataframe(roles, use_container_width=True)
        else:
            st.info("No roles found.")

    # -------------------------------
    # CREATE ROLE
    # -------------------------------
    elif action == "Create Role":
        st.subheader("➕ Create New Role")

        with st.form("create_role_form", clear_on_submit=True):
            name = st.text_input("Role Name")
            guard = st.text_input("Guard (e.g., 'web', 'api')")

            submit = st.form_submit_button("Create Role")

            if submit:
                if not (name and guard):
                    st.warning("⚠️ All fields are required")
                    st.stop()

                if role_model.find_by_name(name):
                    st.error("❌ Role already exists!")
                    st.stop()

                role_model.insert({
                    "name": name,
                    "guard": guard
                })

                st.session_state.success_msg = "✨ Role created successfully!"
                st.rerun()

    # -------------------------------
    # UPDATE ROLE
    # -------------------------------
    elif action == "Update Role":
        st.subheader("✏️ Update Existing Role")

        roles = role_model.all()

        if not roles:
            st.warning("No roles available.")
            st.stop()

        role_map = {r["name"]: r["id"] for r in roles}
        sel_role_name = st.selectbox("Select Role", list(role_map.keys()))
        sel_role_id = role_map[sel_role_name]

        role = role_model.find(sel_role_id)

        with st.form("update_role_form"):
            new_name = st.text_input("Role Name", value=role["name"])
            new_guard = st.text_input("Guard", value=role["guard"])

            submit = st.form_submit_button("Update Role")

            if submit:
                payload = {"name": new_name, "guard": new_guard}
                role_model.update(sel_role_id, payload)

                st.session_state.success_msg = "✔️ Role updated successfully!"
                st.rerun()

    # -------------------------------
    # DELETE ROLE
    # -------------------------------
    elif action == "Delete Role":
        st.subheader("🗑️ Delete Role")

        roles = role_model.all()
        if not roles:
            st.warning("No roles to delete.")
            st.stop()

        role_map = {r["name"]: r["id"] for r in roles}
        sel_role_name = st.selectbox("Select Role", list(role_map.keys()))
        sel_role_id = role_map[sel_role_name]

        if st.button("Delete Role", type="primary"):
            conn.execute("DELETE FROM roles WHERE id = ?", (sel_role_id,))
            conn.commit()
            st.session_state.success_msg = "🗑️ Role deleted successfully!"
            st.rerun()

# End of src/epoch_explorer/pages/role_crud.py
