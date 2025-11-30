import streamlit as st
from epoch_explorer.database.db.connection import get_connection
from epoch_explorer.database.models.user import UserModel, _hash
from epoch_explorer.database.models.companies import CompaniesModel
from epoch_explorer.database.models.department import DepartmentModel
from epoch_explorer.database.models.company_users import CompanyUserModel
from epoch_explorer.database.models.user_role import UserRoleModel
from epoch_explorer.database.models.department_user import DepartmentUserModel


def show():
    st.title("👥 U  ser Management")

    # -------------------------------
    # CHECK LOGIN
    # -------------------------------
    if "user_logged_in" not in st.session_state or not st.session_state.user_logged_in:
        st.error("⚠️ You must login first!")
        st.stop()

    conn = get_connection()
    user_model = UserModel(conn)
    company_model = CompaniesModel(conn)
    department_model = DepartmentModel(conn)
    comp_user_model = CompanyUserModel(conn)
    dept_user_model = DepartmentUserModel(conn)
    role_model = UserRoleModel(conn)

    # -------------------------------
    # Determine roles
    # -------------------------------
    profile_roles = [r["role_name"].lower() for r in user_model.find_user_with_roles(st.session_state.id)]
    is_admin = "admin" in profile_roles
    is_manager = "manager" in profile_roles

    # -------------------------------
    # MENU
    # -------------------------------
    menu = ["View Users"]  # everyone can view
    if is_admin or is_manager:
        menu.append("Create User")
    if is_admin:
        menu += ["Update User", "Delete User"]
    menu.append("My Profile")

    action = st.radio("Choose Action", menu, horizontal=True)

    if "success_msg" in st.session_state:
        st.success(st.session_state.success_msg)
        del st.session_state["success_msg"]

    # -------------------------------
    # CREATE USER
    # -------------------------------
    if action == "Create User":
        if not (is_admin or is_manager):
            st.error("🚫 You do not have permission to create users.")
            st.stop()
        st.subheader("➕ Create New User")

        companies = company_model.all()
        departments = department_model.all()
        roles = role_model.conn.execute("SELECT * FROM roles").fetchall()

        company_map = {c["name"]: c["id"] for c in companies}
        department_map = {d["name"]: d["id"] for d in departments}
        role_map = {r["name"]: r["id"] for r in roles}

        with st.form("create_user_form", clear_on_submit=True):
            name = st.text_input("👤 Full Name")
            email = st.text_input("📧 Email Address")
            password = st.text_input("🔑 Password", type="password")
            company_name = st.selectbox("🏭 Company", list(company_map.keys()))
            department_name = st.selectbox("🏬 Department", list(department_map.keys()))
            role_name = st.selectbox("🔑 Role", list(role_map.keys()))

            submit = st.form_submit_button("Create User")

            if submit:
                # Email uniqueness check
                if user_model.find_by_email(email):
                    st.error("❌ Email already exists.")
                    st.stop()
                if not (name and email and password):
                    st.warning("⚠️ All fields are required")
                    st.stop()

                user_id = user_model.insert({
                    "name": name,
                    "email": email,
                    "password": _hash(password)
                })

                # Assign company, department, role
                comp_user_model.insert({"user_id": user_id, "company_id": company_map[company_name], "role": role_name})
                dept_user_model.insert({"user_id": user_id, "department_id": department_map[department_name]})
                role_model.assign(user_id, role_map[role_name])

                st.session_state.success_msg = "✨ User created successfully!"
                st.rerun()

    # -------------------------------
    # VIEW USERS
    # -------------------------------
    elif action == "View Users":
        st.subheader("📋 All Users")
        users = user_model.user_full_profile()
        if users:
            st.dataframe(users, use_container_width=True)
        else:
            st.info("No users found.")

    # -------------------------------
    # UPDATE USER
    # -------------------------------
    elif action == "Update User":
        if not is_admin:
            st.error("🚫 Only admin can update users.")
            st.stop()
        st.subheader("✏️ Update User Info & Assignments")

        users = user_model.all()
        if not users:
            st.warning("No users to update.")
            st.stop()

        user_map = {u["email"]: u["id"] for u in users}
        selected_email = st.selectbox("Select User", list(user_map.keys()))
        user_id = user_map[selected_email]

        user = user_model.find(user_id)

        # Current assignments
        user_companies = comp_user_model.for_user(user_id)
        user_departments = dept_user_model.for_user(user_id)
        user_roles = role_model.for_user(user_id)

        companies = company_model.all()
        departments = department_model.all()
        roles = role_model.conn.execute("SELECT * FROM roles").fetchall()

        company_map = {c["name"]: c["id"] for c in companies}
        department_map = {d["name"]: d["id"] for d in departments}
        role_map = {r["name"]: r["id"] for r in roles}

        with st.form("update_user_form"):
            new_name = st.text_input("Name", value=user["name"])
            new_email = st.text_input("Email", value=user["email"])
            new_pass = st.text_input("New Password (optional)", type="password")
            company_name = st.selectbox(
                "🏭 Company",
                list(company_map.keys()),
                index=0 if not user_companies else list(company_map.values()).index(user_companies[0]["company_id"])
            )
            department_name = st.selectbox(
                "🏬 Department",
                list(department_map.keys()),
                index=0 if not user_departments else list(department_map.values()).index(user_departments[0]["department_id"])
            )
            role_name = st.selectbox(
                "🔑 Role",
                list(role_map.keys()),
                index=0 if not user_roles else list(role_map.values()).index(user_roles[0]["role_id"])
            )

            submit = st.form_submit_button("Update User")
            if submit:
                payload = {"name": new_name, "email": new_email}
                if new_pass.strip():
                    payload["password"] = _hash(new_pass)
                user_model.update(user_id, payload)

                # Update assignments
                if user_companies:
                    comp_user_model.update(user_companies[0]["id"], {"company_id": company_map[company_name], "role": role_name})
                else:
                    comp_user_model.insert({"user_id": user_id, "company_id": company_map[company_name], "role": role_name})

                if user_departments:
                    dept_user_model.update(user_departments[0]["id"], {"department_id": department_map[department_name]})
                else:
                    dept_user_model.insert({"user_id": user_id, "department_id": department_map[department_name]})

                if user_roles:
                    role_model.update(user_roles[0]["id"], {"role_id": role_map[role_name]})
                else:
                    role_model.assign(user_id, role_map[role_name])

                st.session_state.success_msg = "✔️ User info & assignments updated successfully!"
                st.rerun()

    # -------------------------------
    # DELETE USER
    # -------------------------------
    elif action == "Delete User":
        if not is_admin:
            st.error("🚫 Only admin can delete users.")
            st.stop()
        st.subheader("🗑️ Delete User")

        user_map = {u["email"]: u["id"] for u in user_model.all()}
        selected = st.selectbox("Select User", list(user_map.keys()))
        user_id = user_map[selected]

        if st.button("Delete User", type="primary"):
            conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
            conn.commit()
            st.session_state.success_msg = "🗑️ User deleted successfully!"
            st.rerun()

    # -------------------------------
    # MY PROFILE
    # -------------------------------
    elif action == "My Profile":
        st.subheader("👤 My Full Profile")
        profile_rows = user_model.find_user_full_profile(st.session_state.id)
        if not profile_rows:
            st.warning("No profile data found.")
            st.stop()

        basic = profile_rows[0]
        st.info(f"### 👋 Welcome, **{basic['name']}**")
        st.write(f"📧 Email: **{basic['email']}**")
        st.write("---")

        # Companies
        companies = [{"Company": r["company_name"]} for r in profile_rows if r["company_id"]]
        if companies:
            st.markdown("### 🏭 Companies")
            st.table(companies)

        # Departments
        departments = [{"Department": r["department_name"]} for r in profile_rows if r["department_id"]]
        if departments:
            st.markdown("### 🏬 Departments")
            st.table(departments)

        # Roles
        roles = [{"Role": r["role_name"], "Guard": r["guard"]} for r in profile_rows if r["role_name"]]
        if roles:
            st.markdown("### 🔑 Roles & Permissions")
            st.table(roles)

    # tcs_footer()
