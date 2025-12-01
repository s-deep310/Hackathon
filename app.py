import streamlit as st
from dotenv import load_dotenv
from pathlib import Path
from pages import (
    dashboard,
    incident_analysis_crew,
    reports_incidents,
    reports_alerts,
    settings,
    workflow_visual,
    login,
    logout,
    rag_qa,
    user_crud,
    department_crud,
    company_crud,
    role_crud,
    rag_matrics_report,
    rag_metadata_report,
    chunk_embedding_report
)

load_dotenv()

# --- TCS LOGO ---
logo_path = Path("/home/samyadeep/Documents/Hackathon_TCS/ai-project-scafold-main/src/epoch_explorer/tcs_logo.png")

def tcs_header():
    if logo_path.exists():
        st.image(str(logo_path), width=140)
    else:
        st.warning("TCS logo not found. Place it in /epoch_explorer/assets/tcs_logo.png")

    st.markdown("<h2 style='margin-top:-10px;'></h2>", unsafe_allow_html=True)

tcs_header()
st.set_page_config(page_title="Incident IQ", page_icon="🚨", layout="wide")

# -------------------------------------------------
# 1️⃣ Initialize session
# -------------------------------------------------
if "user_logged_in" not in st.session_state:
    st.session_state.user_logged_in = False
    st.session_state.username = None


# -------------------------------------------------
# 2️⃣ If logout request → clear and rerun
# -------------------------------------------------
if st.session_state.get("logout_triggered"):
    # clear everything safely
    for key in ["user_logged_in", "username", "id", "roles", "role"]:
        if key in st.session_state:
            del st.session_state[key]

    st.session_state.user_logged_in = False
    st.session_state.logout_triggered = False
    st.rerun()  # redirect to login instantly


# -------------------------------------------------
# 3️⃣ If NOT logged in → show ONLY login page
# -------------------------------------------------
if not st.session_state.user_logged_in:
    login.show()
    st.stop()   # IMPORTANT: stops rendering rest of UI


# -------------------------------------------------
# 4️⃣ Logged In → Main UI starts here
# -------------------------------------------------
def tcs_footer():
    st.markdown("""
    <div style='text-align: center; padding: 10px; color: gray; font-size: 12px;'>
        <hr style='border:1px solid #e6e6e6; margin-top: 10px; margin-bottom: 5px;'>
        © 2025 Tata Consultancy Services (TCS) | All Rights Reserved
    </div>
    """, unsafe_allow_html=True)

# Top right profile and logout

col1, col2, col3 = st.columns([6, 1, 1])

with col2:
    st.markdown(
        f"""
        <div style="
            background:#8B5CF6;
            color:white;
            width:32px;height:32px;
            border-radius:50%;
            display:flex;
            align-items:center;
            justify-content:center;
            font-weight:600;
            margin-top:6px;
        ">
            {st.session_state.username[0].upper() if st.session_state.username else "U"}
        </div>
        <div style="font-weight:500;">{st.session_state.username or "User"}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    logout = st.button("Logout", type="primary", key="logout_button", help="Click to logout")

if logout:
    st.session_state.clear()
    st.rerun()



# -------------------------------------------------
# Sidebar Navigation
# -------------------------------------------------

pages = [
    st.Page("pages/dashboard.py", title="Dashboard", icon="📊"),
    st.Page("pages/incident_analysis_crew.py", title="Analyze Incident", icon="🔍"),
    st.Page("pages/reports_incidents.py", title="Incidents Report", icon="📋"),
    st.Page("pages/reports_alerts.py", title="Alerts Report", icon="🔔"),
    st.Page("pages/user_crud.py", title="User Management", icon="👤"),
    st.Page("pages/role_crud.py", title="Role Management", icon="🔑"),
    st.Page("pages/department_crud.py", title="Department Management", icon="🏬"),
    st.Page("pages/company_crud.py", title="Company Management", icon="🏢"),

    st.Page("pages/rag_matrics_report.py", title="Rag Matrics", icon="📊"),
    st.Page("pages/rag_metadata_report.py", title="Rag Metadata", icon="📊"),
    st.Page("pages/chunk_embedding_report.py", title="Chunk Embedding", icon="📊"),

    st.Page("pages/workflow_visual.py", title="Workflow Visualization", icon="🧩"),
    st.Page("pages/settings.py", title="Settings", icon="⚙️"),
    st.Page("pages/rag_qa.py", title="Rag Q&A", icon="📚"),
]



page = st.navigation(pages)
title = getattr(page, "title", "Dashboard")

# -------------------------------------------------
# Routing
# -------------------------------------------------

    
if title == "Dashboard":
    dashboard.show()
elif title == "Analyze Incident":
    incident_analysis_crew.show()
elif title == "Incidents Report":
    reports_incidents.show()
elif title == "Alerts Report":
    reports_alerts.show()
elif title == "User Management":
    user_crud.show()
elif title == "Role Management":
    role_crud.show()
elif title == "Department Management":
    department_crud.show()
elif title == "Company Management":
    company_crud.show()
elif title == "Workflow Visualization":
    workflow_visual.show()
elif title == "Settings":
    settings.show()
elif title == "Rag Q&A":
    rag_qa.show()
elif page == "logout":
    logout.show()
elif title == "Rag Matrics":
    rag_matrics_report.show()
elif title == "Rag Metadata":
    rag_metadata_report.show()
elif title == "Chunk Embedding":
    chunk_embedding_report.show()


tcs_footer()
