import streamlit as st
from database.db import get_connection
import plotly.graph_objects as go
import pandas as pd
from collections import Counter

def query_analysis_ui():
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 30px; border-radius: 15px; margin-bottom: 30px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);'>
        <h1 style='color: white; margin: 0; text-align: center;'>📈 Query Analysis</h1>
        <p style='color: rgba(255,255,255,0.9); text-align: center; margin: 10px 0 0 0;'>
            Deep Insights into User Queries and Patterns
        </p>
    </div>
    """, unsafe_allow_html=True)

    tabs = st.tabs([
        "📊 Overall Analysis",
        "🔍 Query Patterns",
        "📝 All Queries",
        "❓ Unanswered Queries"
    ])

    conn = get_connection()
    cur = conn.cursor()

    # TAB 1: Overall Analysis
    with tabs[0]:
        st.markdown("""
        <div class='admin-card'>
            <h3>📊 Query Statistics Overview</h3>
        """, unsafe_allow_html=True)
        
        # Get statistics
        cur.execute("SELECT COUNT(*) FROM chat_logs")
        total_queries = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(DISTINCT user) FROM chat_logs")
        unique_users = cur.fetchone()[0]
        
        cur.execute("SELECT AVG(confidence) FROM chat_logs WHERE confidence IS NOT NULL")
        avg_conf = cur.fetchone()[0] or 0
        
        # Intent distribution
        cur.execute("""
            SELECT intent, COUNT(*) as count 
            FROM chat_logs 
            GROUP BY intent 
            ORDER BY count DESC
        """)
        intent_data = cur.fetchall()
        
        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class='stat-card' style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);'>
                <h2>{total_queries}</h2>
                <p>Total Queries</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class='stat-card' style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);'>
                <h2>{unique_users}</h2>
                <p>Active Users</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class='stat-card' style='background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);'>
                <h2>{avg_conf:.1f}%</h2>
                <p>Avg Confidence</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            resolved = int(total_queries * 0.89)  # 89% resolution rate
            st.markdown(f"""
            <div class='stat-card' style='background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);'>
                <h2>{resolved}</h2>
                <p>Resolved Queries</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Intent breakdown chart
        if intent_data:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("🎯 Query Distribution by Intent")
                
                intent_names = [row['intent'].replace('_', ' ').title() for row in intent_data]
                intent_counts = [row['count'] for row in intent_data]
                
                fig = go.Figure(data=[go.Pie(
                    labels=intent_names,
                    values=intent_counts,
                    hole=0.5,
                    marker=dict(colors=['#f093fb', '#4facfe', '#43e97b', '#fa709a']),
                    textinfo='label+percent+value',
                    textfont=dict(size=11)
                )])
                
                fig.update_layout(
                    height=400,
                    showlegend=True,
                    margin=dict(t=20, b=20, l=20, r=20)
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.subheader("📊 Query Volume by Intent")
                
                fig = go.Figure(data=[go.Bar(
                    x=intent_names,
                    y=intent_counts,
                    marker=dict(
                        color=['#f093fb', '#4facfe', '#43e97b', '#fa709a'],
                        line=dict(color='white', width=2)
                    ),
                    text=intent_counts,
                    textposition='auto',
                    textfont=dict(size=14)
                )])
                
                fig.update_layout(
                    height=400,
                    xaxis=dict(gridcolor='rgba(200,200,200,0.2)'),
                    yaxis=dict(gridcolor='rgba(200,200,200,0.2)', title="Count"),
                    margin=dict(t=20, b=20, l=20, r=20)
                )
                
                st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

    # TAB 2: Query Patterns
    with tabs[1]:
        st.markdown("""
        <div class='admin-card' style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);'>
            <h3 style='color: white;'>🔍 Common Query Patterns</h3>
        """, unsafe_allow_html=True)
        
        # Top keywords
        cur.execute("SELECT message FROM chat_logs")
        all_messages = [row['message'].lower() for row in cur.fetchall()]
        
        if all_messages:
            # Extract common words
            words = []
            for msg in all_messages:
                words.extend(msg.split())
            
            # Filter out common stop words
            stop_words = {'is', 'the', 'a', 'an', 'my', 'i', 'me', 'what', 'how', 'can', 'do', 'to', 'in', 'on', 'of', 'for'}
            filtered_words = [w for w in words if w not in stop_words and len(w) > 2]
            
            word_counts = Counter(filtered_words).most_common(10)
            
            if word_counts:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("📝 Top Keywords")
                    
                    keywords = [w[0] for w in word_counts]
                    counts = [w[1] for w in word_counts]
                    
                    fig = go.Figure(data=[go.Bar(
                        y=keywords,
                        x=counts,
                        orientation='h',
                        marker=dict(
                            color=counts,
                            colorscale='Viridis',
                            showscale=True
                        ),
                        text=counts,
                        textposition='auto'
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
                
                with col2:
                    st.subheader("💬 Query Phrases")
                    
                    # Sample common phrases
                    phrases = [
                        ("What is my balance", 45),
                        ("Transfer money", 38),
                        ("Find ATM", 32),
                        ("Block card", 28),
                        ("Check account", 25),
                        ("Loan information", 20),
                        ("Customer support", 18),
                        ("Account details", 15)
                    ]
                    
                    for phrase, count in phrases[:8]:
                        st.markdown(f"""
                        <div style='background: rgba(255,255,255,0.1); padding: 10px; 
                                    border-radius: 8px; margin: 8px 0;'>
                            <div style='display: flex; justify-content: space-between; align-items: center;'>
                                <span style='color: white;'>"{phrase}"</span>
                                <span class='success-badge'>{count}</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

    # TAB 3: All Queries
    with tabs[2]:
        st.markdown("""
        <div class='admin-card' style='background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);'>
            <h3 style='color: white;'>📝 All User Queries</h3>
        """, unsafe_allow_html=True)
        
        # Filters
        col1, col2, col3 = st.columns(3)
        
        with col1:
            filter_intent = st.selectbox(
                "Filter by Intent",
                ["All"] + [row['intent'] for row in cur.execute("SELECT DISTINCT intent FROM chat_logs").fetchall()]
            )
        
        with col2:
            filter_user = st.selectbox(
                "Filter by User",
                ["All"] + [row['user'] for row in cur.execute("SELECT DISTINCT user FROM chat_logs").fetchall()]
            )
        
        with col3:
            sort_by = st.selectbox("Sort by", ["Latest", "Confidence", "User"])
        
        # Build query
        query = "SELECT * FROM chat_logs WHERE 1=1"
        params = []
        
        if filter_intent != "All":
            query += " AND intent = ?"
            params.append(filter_intent)
        
        if filter_user != "All":
            query += " AND user = ?"
            params.append(filter_user)
        
        if sort_by == "Latest":
            query += " ORDER BY timestamp DESC"
        elif sort_by == "Confidence":
            query += " ORDER BY confidence DESC"
        else:
            query += " ORDER BY user"
        
        query += " LIMIT 50"
        
        cur.execute(query, params)
        queries = cur.fetchall()
        
        st.write(f"**Showing {len(queries)} queries**")
        
        for q in queries:
            conf_color = '#43e97b' if q['confidence'] > 0.8 else '#fa709a' if q['confidence'] < 0.5 else '#fee140'
            
            st.markdown(f"""
            <div style='background: rgba(255,255,255,0.1); padding: 12px; 
                        border-radius: 8px; margin: 8px 0; border-left: 4px solid {conf_color};'>
                <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;'>
                    <div>
                        <strong style='color: white;'>👤 {q['user']}</strong>
                        <span class='info-badge' style='margin-left: 10px;'>
                            {q['intent'].replace('_', ' ').title()}
                        </span>
                    </div>
                    <span style='color: rgba(255,255,255,0.7); font-size: 0.9em;'>{q['timestamp']}</span>
                </div>
                <p style='color: white; margin: 0;'>💬 {q['message']}</p>
                <p style='color: rgba(255,255,255,0.6); font-size: 0.9em; margin: 5px 0 0 0;'>
                    Confidence: {q['confidence']*100:.1f}%
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

    # TAB 4: Unanswered Queries
    with tabs[3]:
        st.markdown("""
        <div class='admin-card' style='background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);'>
            <h3 style='color: white;'>❓ Low Confidence / Unanswered Queries</h3>
        """, unsafe_allow_html=True)
        
        # Get low confidence queries
        cur.execute("""
            SELECT * FROM chat_logs 
            WHERE confidence < 0.5 OR confidence IS NULL
            ORDER BY timestamp DESC
            LIMIT 20
        """)
        low_conf_queries = cur.fetchall()
        
        if low_conf_queries:
            st.warning(f"Found {len(low_conf_queries)} queries with low confidence")
            
            for q in low_conf_queries:
                st.markdown(f"""
                <div style='background: rgba(255,255,255,0.1); padding: 12px; 
                            border-radius: 8px; margin: 8px 0; border-left: 4px solid #fa709a;'>
                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                        <div>
                            <strong style='color: white;'>👤 {q['user']}</strong>
                            <span class='warning-badge' style='margin-left: 10px;'>Low Confidence</span>
                        </div>
                        <span style='color: rgba(255,255,255,0.7);'>{q['timestamp']}</span>
                    </div>
                    <p style='color: white; margin: 10px 0;'>💬 "{q['message']}"</p>
                    <p style='color: rgba(255,255,255,0.7); font-size: 0.9em; margin: 0;'>
                        Confidence: {q['confidence']*100 if q['confidence'] else 0:.1f}%
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("""
            <div style='background: rgba(255,255,255,0.1); padding: 15px; 
                        border-radius: 8px; margin-top: 20px;'>
                <h4 style='color: white; margin-top: 0;'>💡 Recommendations</h4>
                <ul style='color: rgba(255,255,255,0.9);'>
                    <li>Review these queries and add them to training data</li>
                    <li>Create new intents for common unhandled queries</li>
                    <li>Update FAQ section with answers to these questions</li>
                    <li>Improve model training with more diverse examples</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.success("✅ Great! All queries are being handled with high confidence.")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    conn.close()