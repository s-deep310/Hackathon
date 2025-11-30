import streamlit as st
from epoch_explorer.database.db.connection import get_connection
from epoch_explorer.database.models.companies import CompaniesModel


def show():

    st.title("🏢 Company Management")

    # Check login
    if "user_logged_in" not in st.session_state or not st.session_state.user_logged_in:
        st.error("⚠️ You must login first!")
        st.stop()

    conn = get_connection()
    company_model = CompaniesModel(conn)

    # -----------------------------
    # Roles & Permissions
    # -----------------------------
    role = st.session_state.get("role", "user")
    is_admin = role == "admin"

    # Menu
    menu = ["View Companies"]
    if is_admin:
        menu += ["Create Company", "Update Company", "Delete Company"]

    action = st.radio("Choose Action", menu, horizontal=True)

    st.write("----")

    # -----------------------------
    # Success message handler
    # -----------------------------
    if "success_msg" in st.session_state:
        st.success(st.session_state.success_msg)
        del st.session_state["success_msg"]

    # -----------------------------
    # CREATE COMPANY
    # -----------------------------
    if action == "Create Company":
        if not is_admin:
            st.error("🚫 Only admin can create companies.")
            st.stop()

        st.subheader("➕ Create New Company")
        with st.form("create_company_form", clear_on_submit=True):
            name = st.text_input("🏢 Company Name")
            submit = st.form_submit_button("Create Company")

            if submit:
                if not name.strip():
                    st.warning("⚠️ Company name is required")
                else:
                    try:
                        company_model.insert({"name": name.strip()})
                        st.session_state.success_msg = "✨ Company created successfully!"
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error: {e}")

    # -----------------------------
    # VIEW COMPANIES
    # -----------------------------
    elif action == "View Companies":
        st.subheader("📋 All Companies")
        companies = company_model.all()
        if companies:
            st.dataframe(companies, use_container_width=True, hide_index=True)
        else:
            st.info("No companies found.")

    # -----------------------------
    # UPDATE COMPANY
    # -----------------------------
    elif action == "Update Company":
        if not is_admin:
            st.error("🚫 Only admin can update companies.")
            st.stop()

        st.subheader("✏️ Update Company")

        companies = company_model.all()
        if not companies:
            st.warning("No companies to update.")
            st.stop()

        company_map = {c["name"]: c["id"] for c in companies}
        selected = st.selectbox("Select Company", list(company_map.keys()))
        company_id = company_map[selected]
        company = company_model.find(company_id)

        with st.form("update_company_form"):
            new_name = st.text_input("New Company Name", value=company["name"])
            submit = st.form_submit_button("Update Company")

            if submit:
                if not new_name.strip():
                    st.warning("⚠️ Company name cannot be empty")
                else:
                    try:
                        company_model.update(company_id, {"name": new_name.strip()})
                        st.session_state.success_msg = "✔️ Company updated successfully!"
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error: {e}")

    # -----------------------------
    # DELETE COMPANY
    # -----------------------------
    elif action == "Delete Company":
        if not is_admin:
            st.error("🚫 Only admin can delete companies.")
            st.stop()

        st.subheader("🗑️ Delete Company")

        companies = company_model.all()
        if not companies:
            st.warning("No companies to delete.")
            st.stop()

        company_map = {c["name"]: c["id"] for c in companies}
        selected = st.selectbox("Select Company to Delete", list(company_map.keys()))
        company_id = company_map[selected]

        if st.button("Delete Company", type="primary"):
            try:
                company_model.delete(company_id)
                st.session_state.success_msg = "🗑️ Company deleted successfully!"
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error: {e}")

