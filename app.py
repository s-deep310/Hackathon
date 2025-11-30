import streamlit as st
from dotenv import load_dotenv
from pages import (
    dashboard,
    incident_analysis_crew,
    reports_incidents,
    reports_alerts,
    settings,
    workflow_visual,
    login,
    rag_qa,
    user_crud,
    department_crud,
    company_crud
)

load_dotenv()
st.set_page_config(page_title="Incident IQ", page_icon="🚨", layout="wide")

if 'user_logged_in' not in st.session_state:
    st.session_state.user_logged_in = False
    st.session_state.username = None

# if not logged in, show login page only
if not st.session_state.user_logged_in:
    login.show()
    st.stop()

def tcs_footer():
    st.markdown("""
    <div style='text-align: center; padding: 10px; color: gray; font-size: 12px;'>
        <hr style='border:1px solid #e6e6e6; margin-top: 10px; margin-bottom: 5px;'>
        © 2025 Tata Consultancy Services (TCS) | All Rights Reserved
    </div>
    """, unsafe_allow_html=True)

# Top user info (kept minimal)
col1, col2 = st.columns([6, 1])
with col2:
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:8px;">
      <div style="background:#8B5CF6;color:white;width:32px;height:32px;border-radius:50%;
                  display:flex;align-items:center;justify-content:center;font-weight:600;">
        {st.session_state.username[0].upper() if st.session_state.username else "U"}
      </div>
      <div style="font-weight:500;">{st.session_state.username or "User"}</div>
    </div>
    """, unsafe_allow_html=True)

pages = [
    st.Page("pages/dashboard.py", title="Dashboard", icon="📊"),
    st.Page("pages/incident_analysis_crew.py", title="Analyze Incident", icon="🔍"),
    st.Page("pages/reports_incidents.py", title="Incidents Report", icon="📋"),
    st.Page("pages/reports_alerts.py", title="Alerts Report", icon="🔔"),
    st.Page("pages/user_crud.py", title="User Management", icon="👤"),
    st.Page("pages/department_crud.py", title="Department Management", icon="🏬"),
    st.Page("pages/company_crud.py", title="Company Management", icon="🏢"),
    st.Page("pages/workflow_visual.py", title="Workflow Visualization", icon="🧩"),
    st.Page("pages/settings.py", title="Settings", icon="⚙️"),
    st.Page("pages/rag_qa.py", title="Rag Q&A", icon="📚"),
]

with st.sidebar:
    st.markdown("<h1 style='font-size:20px'>Application</h1>", unsafe_allow_html=True)
    st.divider()

page = st.navigation(pages)
title = getattr(page, "title", "Dashboard")

# Route by title and call each module's .show()
if title == "Dashboard":
    dashboard.show()
    tcs_footer()
elif title == "Rag Q&A":
    rag_qa.show()
    tcs_footer()
elif title == "Analyze Incident":
    incident_analysis_crew.show()
    tcs_footer()
elif title == "Incidents Report":
    reports_incidents.show()
    tcs_footer()
elif title == "Approve Suggestions":
    admin_approvals.show()
    tcs_footer()
elif title == "Alerts Report":
    reports_alerts.show()
    tcs_footer()
elif title == "User Management":
    user_crud.show()
    tcs_footer()
elif title == "Department Management":
    department_crud.show()
    tcs_footer()
elif title == "Company Management":
    company_crud.show()
    tcs_footer()
elif title == "Workflow Visualization":
    workflow_visual.show()
    tcs_footer()
elif title == "Settings":
    settings.show()
    tcs_footer()
elif title == "Logout" or title == "🔐 Logout":
    st.session_state.user_logged_in = False
    st.session_state.username = None
    st.experimental_rerun()
