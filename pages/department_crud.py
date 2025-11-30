import streamlit as st
from epoch_explorer.database.db.connection import get_connection
from epoch_explorer.database.models.department import DepartmentModel


def show():

    st.title("🏬 Department Management")

    # -----------------------------
    # LOGIN CHECK
    # -----------------------------
    if "user_logged_in" not in st.session_state or not st.session_state.user_logged_in:
        st.error("⚠️ You must login first!")
        st.stop()

    conn = get_connection()
    dept_model = DepartmentModel(conn)

    # -----------------------------
    # ROLES & PERMISSIONS
    # -----------------------------
    roles = st.session_state.roles if "roles" in st.session_state else []
    is_admin = "admin" in roles
    is_manager = "manager" in roles

    # -----------------------------
    # MENU OPTIONS
    # -----------------------------
    menu = ["View Departments"]

    if is_admin or is_manager:
        menu.append("Create Department")

    if is_admin:
        menu += ["Update Department", "Delete Department"]

    action = st.radio("Choose Action", menu, horizontal=True)
    st.write("-----")

    # -----------------------------
    # SUCCESS MESSAGE
    # -----------------------------
    if "success_msg" in st.session_state:
        st.success(st.session_state.success_msg)
        del st.session_state["success_msg"]

    # ============================================================
    # CREATE DEPARTMENT
    # ============================================================
    if action == "Create Department":
        if not (is_admin or is_manager):
            st.error("🚫 You do not have permission to create departments.")
            st.stop()

        st.subheader("➕ Create New Department")

        with st.form("create_dept_form", clear_on_submit=True):
            company_id = st.number_input("🏢 Company ID", min_value=1)
            name = st.text_input("🏬 Department Name")

            submit = st.form_submit_button("Create Department")

            if submit:
                if not company_id or not name.strip():
                    st.warning("⚠️ All fields are required.")
                else:
                    dept_model.insert({
                        "company_id": company_id,
                        "name": name,
                    })
                    st.session_state.success_msg = "✨ Department created successfully!"
                    st.rerun()

    # ============================================================
    # VIEW DEPARTMENTS
    # ============================================================
    elif action == "View Departments":
        st.subheader("📋 All Departments")
        departments = dept_model.for_company_with_name()

        if departments:
            st.dataframe(departments, use_container_width=True)
        else:
            st.info("No departments found.")

    # ============================================================
    # UPDATE DEPARTMENT
    # ============================================================
    elif action == "Update Department":
        if not is_admin:
            st.error("🚫 Only admin can update departments.")
            st.stop()

        st.subheader("✏️ Update Department")

        departments = dept_model.all()
        if not departments:
            st.warning("No departments to update.")
            st.stop()

        dept_map = {f"{d['id']} - {d['name']}": d["id"] for d in departments}
        selected = st.selectbox("Select Department", list(dept_map.keys()))
        dept_id = dept_map[selected]

        dept = dept_model.find(dept_id)

        with st.form("update_dept_form"):
            new_company_id = st.number_input("Company ID", min_value=1, value=dept["company_id"])
            new_name = st.text_input("Department Name", value=dept["name"])

            submit = st.form_submit_button("Update Department")

            if submit:
                dept_model.update(dept_id, {
                    "company_id": new_company_id,
                    "name": new_name
                })
                st.session_state.success_msg = "✔️ Department updated successfully!"
                st.rerun()

    # ============================================================
    # DELETE DEPARTMENT
    # ============================================================
    elif action == "Delete Department":
        if not is_admin:
            st.error("🚫 Only admin can delete departments.")
            st.stop()

        st.subheader("🗑️ Delete Department")

        departments = dept_model.all()
        if not departments:
            st.warning("No departments to delete.")
            st.stop()

        dept_map = {f"{d['id']} - {d['name']}": d["id"] for d in departments}
        selected = st.selectbox("Select Department", list(dept_map.keys()))
        dept_id = dept_map[selected]

        if st.button("Delete Department", type="primary"):
            dept_model.delete(dept_id)
            st.session_state.success_msg = "🗑 Department deleted successfully!"
            st.rerun()

