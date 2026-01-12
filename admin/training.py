
# training.py

import streamlit as st
from database.db import get_connection
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

# Your additional code goes here...


def training_ui():
    st.markdown("""
    <div style='background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); 
                padding: 30px; border-radius: 15px; margin-bottom: 30px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);'>
        <h1 style='color: white; margin: 0; text-align: center;'>🧠 Training Manager</h1>
        <p style='color: rgba(255,255,255,0.9); text-align: center; margin: 10px 0 0 0;'>
            Train and Manage NLU Models
        </p>
    </div>
    """, unsafe_allow_html=True)

    tabs = st.tabs([
        "📚 Training Data Overview",
        "🎯 Train Model",
        "📊 Model Analytics",
        "⚡ Quick Add Examples"
    ])

    # TAB 1: Training Data Overview
    with tabs[0]:
        st.markdown("""
        <div class='admin-card'>
            <h3>📚 Current Training Dataset</h3>
        """, unsafe_allow_html=True)
        
        conn = get_connection()
        cur = conn.cursor()
        
        # Get all training data
        cur.execute("""
            SELECT intent, COUNT(*) as count 
            FROM training_data 
            GROUP BY intent
        """)
        intent_data = cur.fetchall()
        
        # Display stats
        col1, col2, col3, col4 = st.columns(4)
        
        total_examples = sum([row['count'] for row in intent_data])
        total_intents = len(intent_data)
        avg_examples = total_examples / total_intents if total_intents > 0 else 0
        
        with col1:
            st.markdown(f"""
            <div class='stat-card' style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);'>
                <h2>{total_intents}</h2>
                <p>Total Intents</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class='stat-card' style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);'>
                <h2>{total_examples}</h2>
                <p>Total Examples</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class='stat-card' style='background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);'>
                <h2>{avg_examples:.1f}</h2>
                <p>Avg per Intent</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            ready = "✓" if total_examples >= 20 else "⚠"
            st.markdown(f"""
            <div class='stat-card' style='background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);'>
                <h2>{ready}</h2>
                <p>Training Ready</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Intent breakdown
        st.subheader("🎯 Intent Breakdown")
        
        for intent_row in intent_data:
            intent = intent_row['intent']
            count = intent_row['count']
            
            # Get examples
            cur.execute("""
                SELECT example 
                FROM training_data 
                WHERE intent = ? 
                LIMIT 3
            """, (intent,))
            examples = cur.fetchall()
            
            with st.expander(f"🎯 {intent.replace('_', ' ').title()} ({count} examples)"):
                st.write("**Sample Examples:**")
                for ex in examples:
                    st.write(f"• {ex['example']}")
                
                if count < 5:
                    st.warning(f"⚠️ Only {count} examples. Add at least 5 for better accuracy.")
                elif count < 10:
                    st.info(f"ℹ️ {count} examples. Consider adding more for optimal performance.")
                else:
                    st.success(f"✅ {count} examples. Good coverage!")
        
        conn.close()
        st.markdown("</div>", unsafe_allow_html=True)

    # TAB 2: Train Model
    with tabs[1]:
        st.markdown("""
        <div class='admin-card' style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);'>
            <h3 style='color: white;'>🎯 Model Training</h3>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
            <div style='background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px;'>
                <h4 style='color: white;'>Training Configuration</h4>
            """, unsafe_allow_html=True)
            
            model_type = st.selectbox(
                "Model Type",
                ["Naive Bayes", "Logistic Regression", "SVM", "Neural Network"]
            )
            
            test_size = st.slider("Test Split (%)", 10, 40, 20)
            
            max_features = st.number_input("Max Features", 100, 1000, 500, 50)
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style='background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; text-align: center;'>
                <h4 style='color: white;'>Model Status</h4>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class='success-badge' style='margin: 10px 0;'>✓ Ready to Train</div>
            <p style='color: white; font-size: 0.9em;'>Last trained: 2 hours ago</p>
            <p style='color: white; font-size: 0.9em;'>Accuracy: 89.5%</p>
            """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("🚀 Start Training", use_container_width=True, type="primary"):
            with st.spinner("Training model..."):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                import time
                
                # Simulate training process
                steps = [
                    ("Loading training data...", 20),
                    ("Preprocessing text...", 40),
                    ("Training model...", 70),
                    ("Evaluating performance...", 90),
                    ("Saving model...", 100)
                ]
                
                for step, progress in steps:
                    status_text.text(step)
                    progress_bar.progress(progress)
                    time.sleep(0.5)
                
                st.success("✅ Model trained successfully!")
                st.balloons()
                
                # Show results
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Accuracy", "89.5%", "2.3%")
                with col2:
                    st.metric("Precision", "87.2%", "1.8%")
                with col3:
                    st.metric("Recall", "88.9%", "2.1%")
        
        st.markdown("</div>", unsafe_allow_html=True)

    # TAB 3: Model Analytics
    with tabs[2]:
        st.markdown("""
        <div class='admin-card' style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);'>
            <h3 style='color: white;'>📊 Model Performance Analytics</h3>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🎯 Per-Intent Accuracy")
            
            # Simulated accuracy data
            intents = ['Check Balance', 'Find ATM', 'Transfer Money', 'Card Block']
            accuracies = [92, 87, 89, 85]
            
            fig = go.Figure(data=[go.Bar(
                x=intents,
                y=accuracies,
                marker=dict(
                    color=accuracies,
                    colorscale='RdYlGn',
                    showscale=True,
                    cmin=80,
                    cmax=95
                ),
                text=[f"{a}%" for a in accuracies],
                textposition='auto',
                textfont=dict(size=14, color='white')
            )])
            
            fig.update_layout(
                height=400,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                yaxis=dict(gridcolor='rgba(255,255,255,0.2)', title="Accuracy (%)"),
                margin=dict(t=20, b=20, l=20, r=20)
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("📈 Training History")
            
            # Simulated training history
            epochs = list(range(1, 11))
            train_acc = [70, 75, 80, 83, 85, 87, 88, 89, 89.5, 90]
            val_acc = [68, 73, 78, 81, 83, 85, 86, 87.5, 88, 89]
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=epochs,
                y=train_acc,
                mode='lines+markers',
                name='Training',
                line=dict(color='#43e97b', width=3),
                marker=dict(size=8)
            ))
            
            fig.add_trace(go.Scatter(
                x=epochs,
                y=val_acc,
                mode='lines+markers',
                name='Validation',
                line=dict(color='#f093fb', width=3),
                marker=dict(size=8)
            ))
            
            fig.update_layout(
                height=400,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                xaxis=dict(gridcolor='rgba(255,255,255,0.2)', title="Epoch"),
                yaxis=dict(gridcolor='rgba(255,255,255,0.2)', title="Accuracy (%)"),
                legend=dict(bgcolor='rgba(0,0,0,0.3)'),
                margin=dict(t=20, b=20, l=20, r=20)
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Confusion Matrix
        st.subheader("🔥 Confusion Matrix")
        
        confusion_data = [
            [45, 2, 1, 2],
            [1, 42, 3, 4],
            [2, 3, 44, 1],
            [3, 2, 1, 44]
        ]
        
        fig = go.Figure(data=go.Heatmap(
            z=confusion_data,
            x=['Check Balance', 'Find ATM', 'Transfer Money', 'Card Block'],
            y=['Check Balance', 'Find ATM', 'Transfer Money', 'Card Block'],
            colorscale='Blues',
            text=confusion_data,
            texttemplate='%{text}',
            textfont={"size": 14},
            showscale=True
        ))
        
        fig.update_layout(
            height=500,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            xaxis=dict(title="Predicted"),
            yaxis=dict(title="Actual"),
            margin=dict(t=20, b=20, l=20, r=20)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

    # TAB 4: Quick Add Examples
    with tabs[3]:
        st.markdown("""
        <div class='admin-card' style='background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);'>
            <h3 style='color: white;'>⚡ Quick Add Examples</h3>
        """, unsafe_allow_html=True)
        
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT intent FROM training_data")
        intents = [row['intent'] for row in cur.fetchall()]
        
        selected_intent = st.selectbox(
            "Select Intent",
            intents,
            format_func=lambda x: x.replace('_', ' ').title()
        )
        
        cur.execute("""
            SELECT COUNT(*) as count 
            FROM training_data 
            WHERE intent = ?
        """, (selected_intent,))
        current_count = cur.fetchone()['count']
        
        st.info(f"Current examples for **{selected_intent.replace('_', ' ').title()}**: {current_count}")
        
        # Bulk add
        st.subheader("📝 Add Multiple Examples")
        examples_text = st.text_area(
            "Enter examples (one per line)",
            height=200,
            placeholder="What is my balance\nShow my account balance\nHow much money do I have"
        )
        
        if st.button("➕ Add All Examples", use_container_width=True):
            if examples_text:
                examples = [e.strip() for e in examples_text.split('\n') if e.strip()]
                
                for example in examples:
                    cur.execute("""
                        INSERT INTO training_data (intent, example) 
                        VALUES (?, ?)
                    """, (selected_intent, example))
                
                conn.commit()
                st.success(f"✅ Added {len(examples)} examples to '{selected_intent}'!")
                st.balloons()
                st.rerun()
            else:
                st.warning("Please enter at least one example")
        
        conn.close()
        st.markdown("</div>", unsafe_allow_html=True)