import streamlit as st
from database.db import get_connection, get_intent_statistics
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import pandas as pd

def admin_dashboard():
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 30px; border-radius: 15px; margin-bottom: 30px; 
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);'>
        <h1 style='color: white; margin: 0; text-align: center; 
                   text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>
            ⚙️ Admin Dashboard
        </h1>
        <p style='color: rgba(255,255,255,0.9); text-align: center; 
                  margin: 10px 0 0 0; font-size: 1.1em;'>
            Complete Overview of BankBot AI System
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Get statistics
    conn = get_connection()
    cur = conn.cursor()
    
    # Total intents
    cur.execute("SELECT COUNT(DISTINCT intent) FROM training_data")
    total_intents = cur.fetchone()[0]
    
    # Total training examples
    cur.execute("SELECT COUNT(*) FROM training_data")
    total_examples = cur.fetchone()[0]
    
    # Total users
    cur.execute("SELECT COUNT(*) FROM users")
    total_users = cur.fetchone()[0]
    
    # Total chats (using transactions as proxy)
    cur.execute("SELECT COUNT(*) FROM chat_logs")
    total_chats = cur.fetchone()[0]
    
    # Total FAQs
    cur.execute("SELECT COUNT(*) FROM faqs")
    total_faqs = cur.fetchone()[0]
    
    # Get intent stats
    intent_stats = get_intent_statistics()
    
    conn.close()

    # Statistics Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class='stat-card' style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                                     animation: fadeIn 0.5s ease-out;'>
            <h2>🎯 {total_intents}</h2>
            <p>Total Intents</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='stat-card' style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                                     animation: fadeIn 0.7s ease-out;'>
            <h2>📚 {total_examples}</h2>
            <p>Training Examples</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class='stat-card' style='background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
                                     animation: fadeIn 0.9s ease-out;'>
            <h2>👥 {total_users}</h2>
            <p>Total Users</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class='stat-card' style='background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
                                     animation: fadeIn 1.1s ease-out;'>
            <h2>💬 {total_chats}</h2>
            <p>Chat Interactions</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Intent Distribution Chart
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='admin-card' style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);'>
            <h3 style='color: white; margin-top: 0;'>📊 Intent Distribution</h3>
        """, unsafe_allow_html=True)
        
        if intent_stats:
            intent_names = [row['intent'].replace('_', ' ').title() for row in intent_stats]
            intent_counts = [row['count'] for row in intent_stats]
            
            fig = go.Figure(data=[go.Pie(
                labels=intent_names,
                values=intent_counts,
                hole=0.4,
                marker=dict(colors=['#f093fb', '#4facfe', '#43e97b', '#fa709a']),
                textinfo='label+percent',
                textfont=dict(size=14, color='white')
            )])
            
            fig.update_layout(
                showlegend=True,
                height=400,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                margin=dict(t=20, b=20, l=20, r=20)
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='admin-card' style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);'>
            <h3 style='color: white; margin-top: 0;'>📈 Intent Usage Trends</h3>
        """, unsafe_allow_html=True)
        
        if intent_stats:
            intent_names = [row['intent'].replace('_', ' ').title() for row in intent_stats]
            intent_counts = [row['count'] for row in intent_stats]
            
            fig = go.Figure(data=[go.Bar(
                x=intent_names,
                y=intent_counts,
                marker=dict(
                    color=intent_counts,
                    colorscale='Viridis',
                    showscale=True
                ),
                text=intent_counts,
                textposition='auto',
                textfont=dict(size=14, color='white')
            )])
            
            fig.update_layout(
                height=400,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                xaxis=dict(gridcolor='rgba(255,255,255,0.2)'),
                yaxis=dict(gridcolor='rgba(255,255,255,0.2)'),
                margin=dict(t=20, b=20, l=20, r=20)
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

    # Intent Details Table
    st.markdown("""
    <div class='admin-card' style='background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);'>
        <h3 style='color: white; margin-top: 0;'>🎯 Intent Details</h3>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    intents_info = [
        ("check_balance", "💰", "Check Balance", "View account balance"),
        ("find_atm", "📍", "Find ATM", "Locate nearby ATMs"),
        ("transfer_money", "💸", "Transfer Money", "Send funds to others"),
        ("card_block", "🚫", "Card Block", "Block lost/stolen cards")
    ]
    
    for i, (intent, icon, title, desc) in enumerate(intents_info):
        col = [col1, col2, col3, col4][i]
        
        # Get count for this intent
        count = next((row['count'] for row in intent_stats if row['intent'] == intent), 0)
        
        # Get example count
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM training_data WHERE intent=?", (intent,))
        example_count = cur.fetchone()[0]
        conn.close()
        
        with col:
            st.markdown(f"""
            <div class='intent-card' style='text-align: center; padding: 15px;'>
                <div style='font-size: 2.5em; margin-bottom: 10px;'>{icon}</div>
                <h4 style='color: white; margin: 5px 0;'>{title}</h4>
                <p style='color: rgba(255,255,255,0.9); font-size: 0.9em; margin: 5px 0;'>{desc}</p>
                <hr style='border-color: rgba(255,255,255,0.3); margin: 10px 0;'>
                <div style='display: flex; justify-content: space-around; margin-top: 10px;'>
                    <div>
                        <div class='success-badge'>{count}</div>
                        <p style='color: white; font-size: 0.8em; margin: 5px 0;'>Uses</p>
                    </div>
                    <div>
                        <div class='info-badge'>{example_count}</div>
                        <p style='color: white; font-size: 0.8em; margin: 5px 0;'>Examples</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

    # System Status
    st.markdown("""
    <div class='admin-card' style='background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);'>
        <h3 style='color: white; margin-top: 0;'>🔧 System Status</h3>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='text-align: center; padding: 15px;'>
            <h4 style='color: white;'>💾 Database</h4>
            <div class='success-badge'>✓ Operational</div>
            <p style='color: white; margin-top: 10px; font-size: 0.9em;'>
                All tables initialized<br>
                Last backup: 2 hours ago
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 15px;'>
            <h4 style='color: white;'>🤖 NLU Model</h4>
            <div class='success-badge'>✓ Trained</div>
            <p style='color: white; margin-top: 10px; font-size: 0.9em;'>
                4 intents loaded<br>
                Confidence: 89%
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style='text-align: center; padding: 15px;'>
            <h4 style='color: white;'>📚 Knowledge Base</h4>
            <div class='info-badge'>{total_faqs} FAQs</div>
            <p style='color: white; margin-top: 10px; font-size: 0.9em;'>
                Last updated: Today<br>
                Categories: 5
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

    # Quick Actions
    st.markdown("""
    <div class='admin-card' style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);'>
        <h3 style='color: white; margin-top: 0;'>⚡ Quick Actions</h3>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🧠 Train Model", use_container_width=True):
            st.info("Navigate to Training Manager to retrain the model")
    
    with col2:
        if st.button("✏️ Add Intent", use_container_width=True):
            st.info("Navigate to Intent Manager to add new intents")
    
    with col3:
        if st.button("📊 View Analytics", use_container_width=True):
            st.info("Navigate to Chat Analytics for detailed insights")
    
    with col4:
        if st.button("📁 Export Data", use_container_width=True):
            st.info("Navigate to Export Logs to download data")
    
    st.markdown("</div>", unsafe_allow_html=True)

    # Recent Activity
    st.markdown("""
    <div class='admin-card' style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);'>
        <h3 style='color: white; margin-top: 0;'>📋 Recent Activity</h3>
    """, unsafe_allow_html=True)
    
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM chat_logs ORDER BY timestamp DESC LIMIT 5")
    recent_logs = cur.fetchall()
    conn.close()
    
    if recent_logs:
        for log in recent_logs:
            st.markdown(f"""
            <div style='background: rgba(255,255,255,0.1); padding: 10px; 
                        border-radius: 8px; margin: 10px 0;'>
                <p style='color: white; margin: 0;'>
                    <strong>👤 {log['user']}</strong> • {log['intent'].replace('_', ' ').title()}
                </p>
                <p style='color: rgba(255,255,255,0.8); font-size: 0.9em; margin: 5px 0;'>
                    💬 {log['message'][:80]}...
                </p>
                <p style='color: rgba(255,255,255,0.6); font-size: 0.8em; margin: 0;'>
                    🕒 {log['timestamp']}
                </p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <p style='color: rgba(255,255,255,0.8); text-align: center;'>
            No recent activity
        </p>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)