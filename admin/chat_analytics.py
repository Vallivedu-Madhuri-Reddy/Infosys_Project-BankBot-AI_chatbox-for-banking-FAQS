import streamlit as st
from database.db import get_connection, get_intent_statistics, get_chat_logs
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta

def chat_analytics_ui():
    st.markdown("""
    <div style='background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); 
                padding: 30px; border-radius: 15px; margin-bottom: 30px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);'>
        <h1 style='color: white; margin: 0; text-align: center;'>💬 Chat Analytics</h1>
        <p style='color: rgba(255,255,255,0.9); text-align: center; margin: 10px 0 0 0;'>
            Real-time Analysis of User Conversations
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Get data
    conn = get_connection()
    cur = conn.cursor()
    
    # Total chats
    cur.execute("SELECT COUNT(*) FROM chat_logs")
    total_chats = cur.fetchone()[0]
    
    # Unique users
    cur.execute("SELECT COUNT(DISTINCT user) FROM chat_logs")
    unique_users = cur.fetchone()[0]
    
    # Average confidence
    cur.execute("SELECT AVG(confidence) FROM chat_logs WHERE confidence IS NOT NULL")
    avg_confidence = cur.fetchone()[0] or 0
    
    # Today's chats
    cur.execute("""
        SELECT COUNT(*) FROM chat_logs 
        WHERE DATE(timestamp) = DATE('now')
    """)
    today_chats = cur.fetchone()[0]
    
    # Stats Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class='stat-card' style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);'>
            <h2>{total_chats}</h2>
            <p>Total Conversations</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='stat-card' style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);'>
            <h2>{unique_users}</h2>
            <p>Unique Users</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class='stat-card' style='background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);'>
            <h2>{avg_confidence:.1f}%</h2>
            <p>Avg Confidence</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class='stat-card' style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);'>
            <h2>{today_chats}</h2>
            <p>Today's Chats</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Intent Usage Over Time
    st.markdown("""
    <div class='admin-card'>
        <h3>📊 Intent Usage Distribution</h3>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🥧 Intent Breakdown")
        intent_stats = get_intent_statistics()
        
        if intent_stats:
            intent_names = [row['intent'].replace('_', ' ').title() for row in intent_stats]
            intent_counts = [row['count'] for row in intent_stats]
            
            fig = go.Figure(data=[go.Pie(
                labels=intent_names,
                values=intent_counts,
                hole=0.4,
                marker=dict(colors=['#f093fb', '#4facfe', '#43e97b', '#fa709a']),
                textinfo='label+percent',
                textfont=dict(size=12)
            )])
            
            fig.update_layout(
                height=400,
                showlegend=True,
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(t=20, b=20, l=20, r=20)
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📈 Usage Trends")
        
        if intent_stats:
            intent_names = [row['intent'].replace('_', ' ').title() for row in intent_stats]
            intent_counts = [row['count'] for row in intent_stats]
            
            fig = go.Figure(data=[go.Bar(
                y=intent_names,
                x=intent_counts,
                orientation='h',
                marker=dict(
                    color=intent_counts,
                    colorscale='Viridis',
                    showscale=True
                ),
                text=intent_counts,
                textposition='auto'
            )])
            
            fig.update_layout(
                height=400,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(gridcolor='rgba(200,200,200,0.2)'),
                yaxis=dict(gridcolor='rgba(200,200,200,0.2)'),
                margin=dict(t=20, b=20, l=20, r=20)
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

    # Chat Volume Timeline
    st.markdown("""
    <div class='admin-card' style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);'>
        <h3 style='color: white;'>📅 Chat Volume Timeline</h3>
    """, unsafe_allow_html=True)
    
    # Simulated timeline data
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    volumes = [15, 18, 22, 19, 25, 30, 28, 24, 26, 32, 29, 27, 31, 35, 33, 
               30, 34, 38, 36, 32, 35, 40, 38, 35, 37, 42, 40, 38, 41, 45]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=dates,
        y=volumes,
        mode='lines+markers',
        name='Chat Volume',
        line=dict(color='#43e97b', width=3),
        fill='tonexty',
        fillcolor='rgba(67, 233, 123, 0.3)',
        marker=dict(size=6)
    ))
    
    fig.update_layout(
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        xaxis=dict(gridcolor='rgba(255,255,255,0.2)', title="Date"),
        yaxis=dict(gridcolor='rgba(255,255,255,0.2)', title="Number of Chats"),
        margin=dict(t=20, b=20, l=20, r=20)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # User Engagement
    st.markdown("""
    <div class='admin-card' style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);'>
        <h3 style='color: white;'>👥 User Engagement Metrics</h3>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("💬 Avg Messages/User")
        avg_msgs = total_chats / max(unique_users, 1)
        st.metric("", f"{avg_msgs:.1f}")
        
        # Progress bar
        progress = min(avg_msgs / 10, 1.0)
        st.progress(progress)
        
        if avg_msgs < 5:
            st.caption("🔴 Low engagement")
        elif avg_msgs < 10:
            st.caption("🟡 Moderate engagement")
        else:
            st.caption("🟢 High engagement")
    
    with col2:
        st.subheader("⏱️ Peak Hours")
        st.metric("", "2PM - 4PM")
        
        # Simulated hourly data
        hours = list(range(24))
        activity = [2, 1, 1, 0, 0, 1, 3, 5, 8, 10, 12, 15, 18, 22, 20, 16, 14, 12, 10, 8, 6, 5, 4, 3]
        
        fig = go.Figure(data=go.Bar(
            x=hours,
            y=activity,
            marker=dict(color=activity, colorscale='Blues')
        ))
        
        fig.update_layout(
            height=200,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            xaxis=dict(gridcolor='rgba(255,255,255,0.2)', title="Hour"),
            yaxis=dict(gridcolor='rgba(255,255,255,0.2)', showticklabels=False),
            margin=dict(t=10, b=10, l=10, r=10),
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col3:
        st.subheader("🔥 Busiest Day")
        st.metric("", "Monday")
        
        # Day of week data
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        day_activity = [45, 38, 42, 40, 35, 28, 22]
        
        fig = go.Figure(data=go.Bar(
            x=days,
            y=day_activity,
            marker=dict(color=day_activity, colorscale='Reds')
        ))
        
        fig.update_layout(
            height=200,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            xaxis=dict(gridcolor='rgba(255,255,255,0.2)'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.2)', showticklabels=False),
            margin=dict(t=10, b=10, l=10, r=10),
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

    # Recent Conversations
    st.markdown("""
    <div class='admin-card' style='background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);'>
        <h3 style='color: white;'>💬 Recent Conversations</h3>
    """, unsafe_allow_html=True)
    
    chat_logs = get_chat_logs(limit=10)
    
    if chat_logs:
        for log in chat_logs:
            confidence_color = '#43e97b' if log['confidence'] > 0.8 else '#fa709a' if log['confidence'] < 0.5 else '#fee140'
            
            st.markdown(f"""
            <div style='background: rgba(255,255,255,0.1); padding: 15px; 
                        border-radius: 10px; margin: 10px 0; border-left: 4px solid {confidence_color};'>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <div>
                        <strong style='color: white; font-size: 1.1em;'>👤 {log['user']}</strong>
                        <span class='info-badge' style='margin-left: 10px;'>
                            {log['intent'].replace('_', ' ').title()}
                        </span>
                    </div>
                    <span style='color: rgba(255,255,255,0.7);'>
                        🕒 {log['timestamp']}
                    </span>
                </div>
                <p style='color: white; margin: 10px 0 5px 0;'>
                    <strong>User:</strong> {log['message']}
                </p>
                <p style='color: rgba(255,255,255,0.9); margin: 5px 0;'>
                    <strong>Bot:</strong> {log['response']}
                </p>
                <div style='margin-top: 10px;'>
                    <span style='color: rgba(255,255,255,0.7); font-size: 0.9em;'>
                        Confidence: {log['confidence']*100:.1f}%
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No chat logs available yet")
    
    conn.close()
    st.markdown("</div>", unsafe_allow_html=True)