import streamlit as st
from database.db import init_db
import os

# --------------------------------------------------
# INIT
# --------------------------------------------------
st.set_page_config(
    page_title="BankBot AI",
    page_icon="🏦",
    layout="wide"
)

init_db()

# --------------------------------------------------
# SESSION DEFAULTS
# --------------------------------------------------
st.session_state.setdefault("logged_in", False)
st.session_state.setdefault("user", None)
st.session_state.setdefault("role", "user")  # admin / user

# --------------------------------------------------
# LOAD CSS
# --------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSS_PATH = os.path.join(BASE_DIR, "assets", "styles.css")

if os.path.exists(CSS_PATH):
    with open(CSS_PATH, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Enhanced CSS for Admin Panel
st.markdown("""
<style>
/* Admin Panel Animations */
@keyframes slideIn {
    from { transform: translateX(-100%); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes glow {
    0%, 100% { box-shadow: 0 0 5px rgba(79, 172, 254, 0.5); }
    50% { box-shadow: 0 0 20px rgba(79, 172, 254, 0.8), 0 0 30px rgba(79, 172, 254, 0.6); }
}

@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.05); }
}

/* Admin Cards */
.admin-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 25px;
    border-radius: 15px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    margin: 15px 0;
    animation: fadeIn 0.6s ease-out;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.admin-card:hover {
    transform: translateY(-5px) scale(1.02);
    box-shadow: 0 15px 40px rgba(0,0,0,0.4);
}

.stat-card {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    color: white;
    animation: fadeIn 0.8s ease-out;
    box-shadow: 0 8px 25px rgba(0,0,0,0.2);
}

.stat-card h2 {
    margin: 0;
    font-size: 2.5em;
    font-weight: bold;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}

.stat-card p {
    margin: 5px 0 0 0;
    font-size: 1.1em;
}

.intent-card {
    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    padding: 20px;
    border-radius: 10px;
    margin: 10px 0;
    animation: slideIn 0.5s ease-out;
    box-shadow: 0 5px 15px rgba(0,0,0,0.2);
}

.success-badge {
    background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
    color: white;
    padding: 8px 15px;
    border-radius: 20px;
    display: inline-block;
    font-weight: bold;
    box-shadow: 0 4px 10px rgba(0,0,0,0.2);
}

.warning-badge {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    color: white;
    padding: 8px 15px;
    border-radius: 20px;
    display: inline-block;
    font-weight: bold;
    box-shadow: 0 4px 10px rgba(0,0,0,0.2);
}

.info-badge {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 8px 15px;
    border-radius: 20px;
    display: inline-block;
    font-weight: bold;
    box-shadow: 0 4px 10px rgba(0,0,0,0.2);
}

/* Navigation Enhancement */
.nav-button {
    animation: glow 2s infinite;
    transition: all 0.3s ease;
}

/* Dashboard Grid */
.dashboard-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
    margin: 20px 0;
}

/* 3D Card Effect */
.card-3d {
    transform-style: preserve-3d;
    transition: transform 0.6s;
}

.card-3d:hover {
    transform: rotateY(10deg) rotateX(5deg);
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# IMPORT UI
# --------------------------------------------------
from ui.home import home_ui
from ui.login import login_ui
from ui.chatbot import chatbot_ui
from ui.user_query import user_query_ui
from ui.database import database_ui
from ui.history import history_ui
from ui.analytics import analytics_ui
from ui.help import help_ui
from admin.dashboard import admin_dashboard
from admin.training import training_ui
from admin.intents import intent_manager_ui
from admin.logs import logs_ui
from admin.chat_analytics import chat_analytics_ui
from admin.query_analysis import query_analysis_ui
from admin.faqs import faq_manager_ui
from admin.knowledge_base import knowledge_base_ui

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
st.sidebar.markdown("""
<div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; margin-bottom: 20px;'>
    <h2 style='color: white; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>🏦 BankBot AI</h2>
    <p style='color: rgba(255,255,255,0.9); margin: 5px 0 0 0; font-size: 0.9em;'>AI-Powered Banking Assistant</p>
</div>
""", unsafe_allow_html=True)

# Navigation
menu = [
    "🏠 Home",
    "🔐 Login",
    "💬 Chatbot",
    "🧠 User Query",
    "📊 Analytics",
    "🆘 Help"
]

if st.session_state.logged_in:
    menu += [
        "🗄️ Database",
        "📜 History"
    ]

# Admin pages with sub-navigation
if st.session_state.role == "admin":
    st.sidebar.markdown("""
    <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                padding: 10px; border-radius: 8px; margin: 10px 0; text-align: center;'>
        <p style='color: white; margin: 0; font-weight: bold;'>⚙️ ADMIN PANEL</p>
    </div>
    """, unsafe_allow_html=True)
    
    menu += [
        "📊 Admin Dashboard",
        "🧠 Training Manager",
        "✏️ Intent Manager",
        "💬 Chat Analytics",
        "📈 Query Analysis",
        "❓ FAQ Manager",
        "📚 Knowledge Base",
        "📁 Export Logs"
    ]

menu.append("🚪 Logout")

page = st.sidebar.radio("Navigation", menu, label_visibility="collapsed")

# User info display
if st.session_state.logged_in:
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"""
    <div style='background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); 
                padding: 15px; border-radius: 8px; text-align: center;'>
        <p style='color: white; margin: 0; font-weight: bold;'>👤 {st.session_state.user}</p>
        <p style='color: rgba(255,255,255,0.9); margin: 5px 0 0 0; font-size: 0.85em;'>
            Role: {st.session_state.role.upper()}
        </p>
    </div>
    """, unsafe_allow_html=True)

# --------------------------------------------------
# ROUTING
# --------------------------------------------------
if page == "🏠 Home":
    home_ui()

elif page == "🔐 Login":
    login_ui()

elif page == "💬 Chatbot":
    chatbot_ui()

elif page == "🧠 User Query":
    user_query_ui()

elif page == "📊 Analytics":
    analytics_ui()

elif page == "🆘 Help":
    help_ui()

elif page == "🗄️ Database":
    database_ui()

elif page == "📜 History":
    history_ui()

# -------- ADMIN --------
elif page == "📊 Admin Dashboard":
    admin_dashboard()

elif page == "🧠 Training Manager":
    training_ui()

elif page == "✏️ Intent Manager":
    intent_manager_ui()

elif page == "💬 Chat Analytics":
    chat_analytics_ui()

elif page == "📈 Query Analysis":
    query_analysis_ui()

elif page == "❓ FAQ Manager":
    faq_manager_ui()

elif page == "📚 Knowledge Base":
    knowledge_base_ui()

elif page == "📁 Export Logs":
    logs_ui()

elif page == "🚪 Logout":
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.role = "user"
    st.success("Logged out successfully")
    st.rerun()

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.markdown(
    """
    <hr>
    <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                border-radius: 10px; margin-top: 30px;'>
        <p style='color: white; margin: 0;'>© 2025 BankBot AI | Vallivedu Madhuri Reddy</p>
        <p style='color: rgba(255,255,255,0.8); margin: 5px 0 0 0; font-size: 0.85em;'>
            Powered by AI & Machine Learning
        </p>
    </div>
    """,
    unsafe_allow_html=True
)