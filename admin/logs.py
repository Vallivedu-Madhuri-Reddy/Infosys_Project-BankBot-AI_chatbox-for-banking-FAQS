import streamlit as st
from database.db import get_connection
import pandas as pd
from datetime import datetime
import csv
import io

def logs_ui():
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 30px; border-radius: 15px; margin-bottom: 30px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);'>
        <h1 style='color: white; margin: 0; text-align: center;'>📁 Export Logs & Data</h1>
        <p style='color: rgba(255,255,255,0.9); text-align: center; margin: 10px 0 0 0;'>
            Download System Data & Analytics Reports
        </p>
    </div>
    """, unsafe_allow_html=True)

    tabs = st.tabs([
        "💬 Chat Logs",
        "📚 Training Data",
        "👥 User Data",
        "📊 Analytics Report"
    ])

    conn = get_connection()
    cur = conn.cursor()

    # TAB 1: Chat Logs Export
    with tabs[0]:
        st.markdown("""
        <div class='admin-card'>
            <h3>💬 Export Chat Logs</h3>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
            <div style='background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px;'>
                <h4 style='color: white;'>Export Options</h4>
            """, unsafe_allow_html=True)
            
            # Date range
            export_all = st.checkbox("Export all logs", value=True)
            
            if not export_all:
                from datetime import date, timedelta
                col_a, col_b = st.columns(2)
                with col_a:
                    start_date = st.date_input("From", value=date.today() - timedelta(days=30))
                with col_b:
                    end_date = st.date_input("To", value=date.today())
            
            # Intent filter
            cur.execute("SELECT DISTINCT intent FROM chat_logs")
            intents = ["All"] + [row['intent'] for row in cur.fetchall() if row['intent']]
            filter_intent = st.selectbox("Filter by Intent", intents)
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style='background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; text-align: center;'>
                <h4 style='color: white;'>Statistics</h4>
            """, unsafe_allow_html=True)
            
            cur.execute("SELECT COUNT(*) FROM chat_logs")
            total = cur.fetchone()[0]
            
            st.markdown(f"""
            <div class='stat-card' style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); margin: 10px 0;'>
                <h2>{total}</h2>
                <p>Total Logs</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Export button
        if st.button("📥 Export Chat Logs as CSV", use_container_width=True):
            # Build query
            query = "SELECT * FROM chat_logs WHERE 1=1"
            params = []
            
            if not export_all:
                query += " AND DATE(timestamp) BETWEEN ? AND ?"
                params.extend([start_date, end_date])
            
            if filter_intent != "All":
                query += " AND intent = ?"
                params.append(filter_intent)
            
            query += " ORDER BY timestamp DESC"
            
            # Execute and fetch
            cur.execute(query, params)
            logs = cur.fetchall()
            
            if logs:
                # Convert to DataFrame
                df = pd.DataFrame(logs, columns=['id', 'user', 'message', 'intent', 'response', 'confidence', 'timestamp'])
                
                # Create CSV
                csv_buffer = io.StringIO()
                df.to_csv(csv_buffer, index=False)
                
                # Download button
                st.download_button(
                    label="⬇️ Download CSV File",
                    data=csv_buffer.getvalue(),
                    file_name=f"chat_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
                
                st.success(f"✅ Prepared {len(logs)} records for export!")
                
                # Preview
                with st.expander("Preview Data"):
                    st.dataframe(df.head(10))
            else:
                st.warning("No logs found for the selected criteria")
        
        st.markdown("</div>", unsafe_allow_html=True)

    # TAB 2: Training Data Export
    with tabs[1]:
        st.markdown("""
        <div class='admin-card' style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);'>
            <h3 style='color: white;'>📚 Export Training Data</h3>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
            <div style='background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px;'>
                <h4 style='color: white;'>Training Data Options</h4>
            """, unsafe_allow_html=True)
            
            # Intent selection
            cur.execute("SELECT DISTINCT intent FROM training_data")
            intents = ["All"] + [row['intent'] for row in cur.fetchall()]
            selected_intents = st.multiselect("Select Intents to Export", intents, default=["All"])
            
            export_format = st.radio("Export Format", ["CSV", "JSON"])
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            cur.execute("SELECT COUNT(*) FROM training_data")
            total_examples = cur.fetchone()[0]
            
            cur.execute("SELECT COUNT(DISTINCT intent) FROM training_data")
            total_intents = cur.fetchone()[0]
            
            st.markdown(f"""
            <div style='background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; text-align: center;'>
                <h4 style='color: white;'>Dataset Info</h4>
                <div class='stat-card' style='background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); margin: 10px 0;'>
                    <h2>{total_examples}</h2>
                    <p>Examples</p>
                </div>
                <div class='stat-card' style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); margin: 10px 0;'>
                    <h2>{total_intents}</h2>
                    <p>Intents</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        if st.button("📥 Export Training Data", use_container_width=True):
            # Build query
            if "All" in selected_intents or len(selected_intents) == 0:
                cur.execute("SELECT intent, example, created_at FROM training_data ORDER BY intent")
            else:
                placeholders = ','.join('?' * len(selected_intents))
                cur.execute(f"SELECT intent, example, created_at FROM training_data WHERE intent IN ({placeholders}) ORDER BY intent", selected_intents)
            
            data = cur.fetchall()
            
            if data:
                df = pd.DataFrame(data, columns=['intent', 'example', 'created_at'])
                
                if export_format == "CSV":
                    csv_buffer = io.StringIO()
                    df.to_csv(csv_buffer, index=False)
                    file_data = csv_buffer.getvalue()
                    file_ext = "csv"
                    mime_type = "text/csv"
                else:  # JSON
                    json_data = df.to_json(orient='records', indent=2)
                    file_data = json_data
                    file_ext = "json"
                    mime_type = "application/json"
                
                st.download_button(
                    label=f"⬇️ Download {export_format} File",
                    data=file_data,
                    file_name=f"training_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{file_ext}",
                    mime=mime_type
                )
                
                st.success(f"✅ Prepared {len(data)} training examples for export!")
                
                with st.expander("Preview Data"):
                    st.dataframe(df.head(20))
            else:
                st.warning("No training data found")
        
        st.markdown("</div>", unsafe_allow_html=True)

    # TAB 3: User Data Export
    with tabs[2]:
        st.markdown("""
        <div class='admin-card' style='background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);'>
            <h3 style='color: white;'>👥 Export User Data</h3>
        """, unsafe_allow_html=True)
        
        st.warning("⚠️ User data export includes sensitive information. Handle with care!")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            export_type = st.radio(
                "Select Data Type",
                ["Users Only", "Users + Transactions", "Users + Chat History"]
            )
            
            include_inactive = st.checkbox("Include inactive users")
        
        with col2:
            cur.execute("SELECT COUNT(*) FROM users")
            total_users = cur.fetchone()[0]
            
            cur.execute("SELECT COUNT(*) FROM transactions")
            total_trans = cur.fetchone()[0]
            
            st.markdown(f"""
            <div style='background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px; text-align: center;'>
                <p style='color: white; margin: 5px 0;'>👥 Users: {total_users}</p>
                <p style='color: white; margin: 5px 0;'>💸 Transactions: {total_trans}</p>
            </div>
            """, unsafe_allow_html=True)
        
        if st.button("📥 Export User Data", use_container_width=True):
            if export_type == "Users Only":
                query = "SELECT username, account_type, balance, is_active FROM users"
                if not include_inactive:
                    query += " WHERE is_active = 1"
                cur.execute(query)
                data = cur.fetchall()
                df = pd.DataFrame(data, columns=['username', 'account_type', 'balance', 'is_active'])
            
            elif export_type == "Users + Transactions":
                query = """
                    SELECT u.username, u.account_type, u.balance, 
                           t.sender, t.receiver, t.amount, t.timestamp
                    FROM users u
                    LEFT JOIN transactions t ON u.username = t.sender OR u.username = t.receiver
                """
                if not include_inactive:
                    query += " WHERE u.is_active = 1"
                cur.execute(query)
                data = cur.fetchall()
                df = pd.DataFrame(data, columns=['username', 'account_type', 'balance', 'sender', 'receiver', 'amount', 'timestamp'])
            
            else:  # Users + Chat History
                query = """
                    SELECT u.username, u.account_type, 
                           c.message, c.intent, c.timestamp
                    FROM users u
                    LEFT JOIN chat_logs c ON u.username = c.user
                """
                if not include_inactive:
                    query += " WHERE u.is_active = 1"
                cur.execute(query)
                data = cur.fetchall()
                df = pd.DataFrame(data, columns=['username', 'account_type', 'message', 'intent', 'timestamp'])
            
            if not df.empty:
                csv_buffer = io.StringIO()
                df.to_csv(csv_buffer, index=False)
                
                st.download_button(
                    label="⬇️ Download CSV File",
                    data=csv_buffer.getvalue(),
                    file_name=f"user_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
                
                st.success(f"✅ Prepared {len(df)} records for export!")
                
                with st.expander("Preview Data"):
                    st.dataframe(df.head(10))
            else:
                st.warning("No data found")
        
        st.markdown("</div>", unsafe_allow_html=True)

    # TAB 4: Analytics Report
    with tabs[3]:
        st.markdown("""
        <div class='admin-card' style='background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);'>
            <h3 style='color: white;'>📊 Generate Analytics Report</h3>
        """, unsafe_allow_html=True)
        
        st.write("Generate a comprehensive analytics report with all system statistics")
        
        include_options = st.multiselect(
            "Include in Report",
            ["System Overview", "Intent Statistics", "User Engagement", "Training Data Summary", "Recent Activity"],
            default=["System Overview", "Intent Statistics"]
        )
        
        report_format = st.radio("Report Format", ["PDF", "HTML", "Markdown"])
        
        if st.button("📄 Generate Report", use_container_width=True):
            # Generate report content
            report = []
            report.append("# BankBot AI - Analytics Report")
            report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            report.append("\n---\n")
            
            if "System Overview" in include_options:
                cur.execute("SELECT COUNT(*) FROM users")
                users = cur.fetchone()[0]
                cur.execute("SELECT COUNT(*) FROM chat_logs")
                chats = cur.fetchone()[0]
                cur.execute("SELECT COUNT(*) FROM training_data")
                examples = cur.fetchone()[0]
                
                report.append("## System Overview")
                report.append(f"- Total Users: {users}")
                report.append(f"- Total Chats: {chats}")
                report.append(f"- Training Examples: {examples}")
                report.append("")
            
            if "Intent Statistics" in include_options:
                cur.execute("SELECT intent, count FROM intent_stats ORDER BY count DESC")
                intent_stats = cur.fetchall()
                
                report.append("## Intent Statistics")
                for intent in intent_stats:
                    report.append(f"- {intent['intent'].replace('_', ' ').title()}: {intent['count']} uses")
                report.append("")
            
            if "Training Data Summary" in include_options:
                cur.execute("SELECT intent, COUNT(*) as count FROM training_data GROUP BY intent")
                training = cur.fetchall()
                
                report.append("## Training Data Summary")
                for t in training:
                    report.append(f"- {t['intent'].replace('_', ' ').title()}: {t['count']} examples")
                report.append("")
            
            report_text = "\n".join(report)
            
            # Create download
            if report_format == "Markdown":
                st.download_button(
                    label="⬇️ Download Report (MD)",
                    data=report_text,
                    file_name=f"analytics_report_{datetime.now().strftime('%Y%m%d')}.md",
                    mime="text/markdown"
                )
            elif report_format == "HTML":
                html_content = f"<html><body><pre>{report_text}</pre></body></html>"
                st.download_button(
                    label="⬇️ Download Report (HTML)",
                    data=html_content,
                    file_name=f"analytics_report_{datetime.now().strftime('%Y%m%d')}.html",
                    mime="text/html"
                )
            else:  # PDF
                st.info("PDF generation requires additional libraries. Downloading as text instead.")
                st.download_button(
                    label="⬇️ Download Report (TXT)",
                    data=report_text,
                    file_name=f"analytics_report_{datetime.now().strftime('%Y%m%d')}.txt",
                    mime="text/plain"
                )
            
            st.success("✅ Report generated successfully!")
            
            with st.expander("Preview Report"):
                st.markdown(report_text)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    conn.close()