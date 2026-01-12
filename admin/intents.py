import streamlit as st
from database.db import get_connection
import plotly.graph_objects as go
import plotly.express as px

def intent_manager_ui():
    st.markdown("""
    <div style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                padding: 30px; border-radius: 15px; margin-bottom: 30px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);'>
        <h1 style='color: white; margin: 0; text-align: center;'>✏️ Intent Manager</h1>
        <p style='color: rgba(255,255,255,0.9); text-align: center; margin: 10px 0 0 0;'>
            Create, Read, Update, Delete Intents & Training Examples
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Tabs for different operations
    tab1, tab2, tab3, tab4 = st.tabs([
        "📋 View Intents",
        "➕ Add Intent/Example",
        "✏️ Edit Examples",
        "📊 Intent Analytics"
    ])

    # TAB 1: View Intents
    with tab1:
        st.markdown("""
        <div class='admin-card'>
            <h3>🎯 Current Intents</h3>
        """, unsafe_allow_html=True)
        
        conn = get_connection()
        cur = conn.cursor()
        
        # Get all intents with their example counts
        cur.execute("""
            SELECT intent, COUNT(*) as example_count 
            FROM training_data 
            GROUP BY intent
        """)
        intents = cur.fetchall()
        
        if intents:
            cols = st.columns(2)
            for idx, intent in enumerate(intents):
                col = cols[idx % 2]
                with col:
                    st.markdown(f"""
                    <div class='intent-card' style='margin: 10px 0;'>
                        <h4 style='color: white; margin: 0;'>
                            🎯 {intent['intent'].replace('_', ' ').title()}
                        </h4>
                        <div style='margin-top: 10px;'>
                            <span class='success-badge'>{intent['example_count']} Examples</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Show examples for this intent
                    with st.expander(f"View Examples for {intent['intent'].replace('_', ' ').title()}"):
                        cur.execute("""
                            SELECT id, example, created_at 
                            FROM training_data 
                            WHERE intent = ? 
                            ORDER BY created_at DESC
                        """, (intent['intent'],))
                        examples = cur.fetchall()
                        
                        for ex in examples:
                            col1, col2 = st.columns([4, 1])
                            with col1:
                                st.write(f"💬 {ex['example']}")
                            with col2:
                                if st.button("🗑️", key=f"del_{ex['id']}"):
                                    cur.execute("DELETE FROM training_data WHERE id=?", (ex['id'],))
                                    conn.commit()
                                    st.success("Deleted!")
                                    st.rerun()
        else:
            st.warning("No intents found. Add some intents to get started!")
        
        conn.close()
        st.markdown("</div>", unsafe_allow_html=True)

    # TAB 2: Add Intent/Example
    with tab2:
        st.markdown("""
        <div class='admin-card' style='background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);'>
            <h3 style='color: white;'>➕ Add New Training Data</h3>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🆕 Create New Intent")
            new_intent = st.text_input("Intent Name (lowercase, use underscores)")
            new_intent_example = st.text_area("First Example for this Intent")
            
            if st.button("Create Intent", use_container_width=True):
                if new_intent and new_intent_example:
                    conn = get_connection()
                    cur = conn.cursor()
                    try:
                        # Add to training data
                        cur.execute("""
                            INSERT INTO training_data (intent, example) 
                            VALUES (?, ?)
                        """, (new_intent.lower().replace(' ', '_'), new_intent_example))
                        
                        # Add to intent stats
                        cur.execute("""
                            INSERT OR IGNORE INTO intent_stats (intent, count) 
                            VALUES (?, 0)
                        """, (new_intent.lower().replace(' ', '_'),))
                        
                        conn.commit()
                        st.success(f"✅ Intent '{new_intent}' created successfully!")
                        st.balloons()
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")
                    finally:
                        conn.close()
                else:
                    st.warning("Please provide both intent name and example")
        
        with col2:
            st.subheader("📝 Add Example to Existing Intent")
            
            # Get existing intents
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT DISTINCT intent FROM training_data")
            existing_intents = [row['intent'] for row in cur.fetchall()]
            conn.close()
            
            if existing_intents:
                selected_intent = st.selectbox(
                    "Select Intent",
                    existing_intents,
                    format_func=lambda x: x.replace('_', ' ').title()
                )
                
                new_example = st.text_area("New Example")
                
                if st.button("Add Example", use_container_width=True):
                    if new_example:
                        conn = get_connection()
                        cur = conn.cursor()
                        cur.execute("""
                            INSERT INTO training_data (intent, example) 
                            VALUES (?, ?)
                        """, (selected_intent, new_example))
                        conn.commit()
                        conn.close()
                        st.success(f"✅ Example added to '{selected_intent}'!")
                        st.rerun()
                    else:
                        st.warning("Please provide an example")
            else:
                st.info("Create an intent first!")
        
        st.markdown("</div>", unsafe_allow_html=True)

    # TAB 3: Edit Examples
    with tab3:
        st.markdown("""
        <div class='admin-card' style='background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);'>
            <h3 style='color: white;'>✏️ Edit & Delete Examples</h3>
        """, unsafe_allow_html=True)
        
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT intent FROM training_data")
        existing_intents = [row['intent'] for row in cur.fetchall()]
        
        if existing_intents:
            selected_intent = st.selectbox(
                "Select Intent to Edit",
                existing_intents,
                format_func=lambda x: x.replace('_', ' ').title(),
                key="edit_intent_select"
            )
            
            cur.execute("""
                SELECT id, example, created_at 
                FROM training_data 
                WHERE intent = ? 
                ORDER BY created_at DESC
            """, (selected_intent,))
            examples = cur.fetchall()
            
            st.write(f"**{len(examples)} examples found**")
            
            for ex in examples:
                with st.container():
                    col1, col2, col3 = st.columns([5, 1, 1])
                    with col1:
                        new_text = st.text_input(
                            "Example",
                            value=ex['example'],
                            key=f"edit_{ex['id']}",
                            label_visibility="collapsed"
                        )
                    with col2:
                        if st.button("💾", key=f"save_{ex['id']}"):
                            cur.execute("""
                                UPDATE training_data 
                                SET example = ? 
                                WHERE id = ?
                            """, (new_text, ex['id']))
                            conn.commit()
                            st.success("Saved!")
                            st.rerun()
                    with col3:
                        if st.button("🗑️", key=f"delete_{ex['id']}"):
                            cur.execute("DELETE FROM training_data WHERE id=?", (ex['id'],))
                            conn.commit()
                            st.success("Deleted!")
                            st.rerun()
                    st.markdown("---")
        
        conn.close()
        st.markdown("</div>", unsafe_allow_html=True)

    # TAB 4: Intent Analytics
    with tab4:
        st.markdown("""
        <div class='admin-card' style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);'>
            <h3 style='color: white;'>📊 Intent Analytics</h3>
        """, unsafe_allow_html=True)
        
        conn = get_connection()
        cur = conn.cursor()
        
        # Get intent example counts
        cur.execute("""
            SELECT intent, COUNT(*) as count 
            FROM training_data 
            GROUP BY intent
        """)
        data = cur.fetchall()
        
        if data:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📈 Examples per Intent (Bar Chart)")
                intent_names = [row['intent'].replace('_', ' ').title() for row in data]
                counts = [row['count'] for row in data]
                
                fig = go.Figure(data=[go.Bar(
                    x=intent_names,
                    y=counts,
                    marker=dict(
                        color=['#f093fb', '#4facfe', '#43e97b', '#fa709a'],
                        line=dict(color='white', width=2)
                    ),
                    text=counts,
                    textposition='auto',
                    textfont=dict(size=16, color='white')
                )])
                
                fig.update_layout(
                    height=400,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white'),
                    xaxis=dict(gridcolor='rgba(255,255,255,0.2)'),
                    yaxis=dict(gridcolor='rgba(255,255,255,0.2)', title="Number of Examples"),
                    margin=dict(t=20, b=20, l=20, r=20)
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.subheader("🥧 Training Data Distribution")
                fig = go.Figure(data=[go.Pie(
                    labels=intent_names,
                    values=counts,
                    hole=0.4,
                    marker=dict(colors=['#f093fb', '#4facfe', '#43e97b', '#fa709a']),
                    textinfo='label+percent+value',
                    textfont=dict(size=12, color='white')
                )])
                
                fig.update_layout(
                    height=400,
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white'),
                    showlegend=True,
                    margin=dict(t=20, b=20, l=20, r=20)
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Data Quality Metrics
            st.subheader("🎯 Data Quality Metrics")
            
            total_examples = sum(counts)
            avg_examples = total_examples / len(data)
            min_examples = min(counts)
            max_examples = max(counts)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Examples", total_examples)
            with col2:
                st.metric("Average per Intent", f"{avg_examples:.1f}")
            with col3:
                st.metric("Min Examples", min_examples)
            with col4:
                st.metric("Max Examples", max_examples)
            
            # Recommendations
            st.subheader("💡 Recommendations")
            if min_examples < 5:
                st.warning(f"⚠️ Some intents have less than 5 examples. Consider adding more training data for better accuracy.")
            elif min_examples < 10:
                st.info(f"ℹ️ Good coverage! Consider adding 10+ examples per intent for optimal performance.")
            else:
                st.success(f"✅ Excellent! All intents have sufficient training data.")
        
        conn.close()
        st.markdown("</div>", unsafe_allow_html=True)