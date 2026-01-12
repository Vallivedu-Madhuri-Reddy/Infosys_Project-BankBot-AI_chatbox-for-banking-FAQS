import streamlit as st
from database.db import get_connection

def faq_manager_ui():
    st.markdown("""
    <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                padding: 30px; border-radius: 15px; margin-bottom: 30px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);'>
        <h1 style='color: white; margin: 0; text-align: center;'>❓ FAQ Manager</h1>
        <p style='color: rgba(255,255,255,0.9); text-align: center; margin: 10px 0 0 0;'>
            Manage Frequently Asked Questions
        </p>
    </div>
    """, unsafe_allow_html=True)

    tabs = st.tabs([
        "📋 All FAQs",
        "➕ Add FAQ",
        "✏️ Edit FAQs",
        "📊 FAQ Analytics"
    ])

    conn = get_connection()
    cur = conn.cursor()

    # TAB 1: All FAQs
    with tabs[0]:
        st.markdown("""
        <div class='admin-card'>
            <h3>📋 Current FAQs</h3>
        """, unsafe_allow_html=True)
        
        # Get categories
        cur.execute("SELECT DISTINCT category FROM faqs")
        categories = [row['category'] for row in cur.fetchall()]
        
        filter_category = st.selectbox("Filter by Category", ["All"] + categories)
        
        # Get FAQs
        if filter_category == "All":
            cur.execute("SELECT * FROM faqs ORDER BY category, created_at DESC")
        else:
            cur.execute("SELECT * FROM faqs WHERE category=? ORDER BY created_at DESC", (filter_category,))
        
        faqs = cur.fetchall()
        
        if faqs:
            st.write(f"**{len(faqs)} FAQs found**")
            
            current_category = None
            for faq in faqs:
                if faq['category'] != current_category:
                    current_category = faq['category']
                    st.markdown(f"""
                    <div style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                                padding: 10px 20px; border-radius: 8px; margin: 20px 0 10px 0;'>
                        <h4 style='color: white; margin: 0;'>📁 {current_category}</h4>
                    </div>
                    """, unsafe_allow_html=True)
                
                with st.expander(f"❓ {faq['question']}"):
                    st.markdown(f"""
                    <div style='padding: 10px;'>
                        <p style='margin: 0 0 10px 0;'><strong>Answer:</strong></p>
                        <p style='background: rgba(0,0,0,0.1); padding: 10px; 
                                  border-radius: 8px; margin: 0;'>{faq['answer']}</p>
                        <p style='margin: 10px 0 0 0; color: gray; font-size: 0.9em;'>
                            Created: {faq['created_at']}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    col1, col2 = st.columns([1, 1])
                    with col1:
                        if st.button("🗑️ Delete", key=f"del_faq_{faq['id']}"):
                            cur.execute("DELETE FROM faqs WHERE id=?", (faq['id'],))
                            conn.commit()
                            st.success("FAQ deleted!")
                            st.rerun()
        else:
            st.info("No FAQs found. Add some to get started!")
        
        st.markdown("</div>", unsafe_allow_html=True)

    # TAB 2: Add FAQ
    with tabs[1]:
        st.markdown("""
        <div class='admin-card' style='background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);'>
            <h3 style='color: white;'>➕ Add New FAQ</h3>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            question = st.text_area("Question", height=100, placeholder="What is the minimum balance required?")
            answer = st.text_area("Answer", height=150, placeholder="The minimum balance for savings account is ₹5000...")
        
        with col2:
            cur.execute("SELECT DISTINCT category FROM faqs")
            existing_categories = [row['category'] for row in cur.fetchall()]
            
            category_option = st.radio("Category", ["Existing", "New"])
            
            if category_option == "Existing" and existing_categories:
                category = st.selectbox("Select Category", existing_categories)
            else:
                category = st.text_input("New Category", placeholder="e.g., Account, Loans, Cards")
        
        if st.button("➕ Add FAQ", use_container_width=True):
            if question and answer and category:
                cur.execute("""
                    INSERT INTO faqs (question, answer, category) 
                    VALUES (?, ?, ?)
                """, (question, answer, category))
                conn.commit()
                st.success("✅ FAQ added successfully!")
                st.balloons()
                st.rerun()
            else:
                st.warning("Please fill all fields")
        
        st.markdown("</div>", unsafe_allow_html=True)

    # TAB 3: Edit FAQs
    with tabs[2]:
        st.markdown("""
        <div class='admin-card' style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);'>
            <h3 style='color: white;'>✏️ Edit FAQs</h3>
        """, unsafe_allow_html=True)
        
        cur.execute("SELECT * FROM faqs ORDER BY category, created_at DESC")
        all_faqs = cur.fetchall()
        
        if all_faqs:
            faq_options = [f"{faq['id']} - {faq['question'][:50]}..." for faq in all_faqs]
            selected_idx = st.selectbox("Select FAQ to Edit", range(len(faq_options)), format_func=lambda x: faq_options[x])
            
            selected_faq = all_faqs[selected_idx]
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            new_question = st.text_area("Question", value=selected_faq['question'], height=100)
            new_answer = st.text_area("Answer", value=selected_faq['answer'], height=150)
            
            cur.execute("SELECT DISTINCT category FROM faqs")
            categories = [row['category'] for row in cur.fetchall()]
            
            new_category = st.selectbox(
                "Category",
                categories,
                index=categories.index(selected_faq['category']) if selected_faq['category'] in categories else 0
            )
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("💾 Save Changes", use_container_width=True):
                    cur.execute("""
                        UPDATE faqs 
                        SET question=?, answer=?, category=? 
                        WHERE id=?
                    """, (new_question, new_answer, new_category, selected_faq['id']))
                    conn.commit()
                    st.success("✅ FAQ updated!")
                    st.rerun()
            
            with col2:
                if st.button("🗑️ Delete FAQ", use_container_width=True):
                    cur.execute("DELETE FROM faqs WHERE id=?", (selected_faq['id'],))
                    conn.commit()
                    st.success("FAQ deleted!")
                    st.rerun()
        else:
            st.info("No FAQs available to edit")
        
        st.markdown("</div>", unsafe_allow_html=True)

    # TAB 4: FAQ Analytics
    with tabs[3]:
        st.markdown("""
        <div class='admin-card' style='background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);'>
            <h3 style='color: white;'>📊 FAQ Statistics</h3>
        """, unsafe_allow_html=True)
        
        # Get stats
        cur.execute("SELECT COUNT(*) FROM faqs")
        total_faqs = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(DISTINCT category) FROM faqs")
        total_categories = cur.fetchone()[0]
        
        cur.execute("""
            SELECT category, COUNT(*) as count 
            FROM faqs 
            GROUP BY category 
            ORDER BY count DESC
        """)
        category_data = cur.fetchall()
        
        # Display stats
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class='stat-card' style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);'>
                <h2>{total_faqs}</h2>
                <p>Total FAQs</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class='stat-card' style='background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);'>
                <h2>{total_categories}</h2>
                <p>Categories</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            avg_per_cat = total_faqs / max(total_categories, 1)
            st.markdown(f"""
            <div class='stat-card' style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);'>
                <h2>{avg_per_cat:.1f}</h2>
                <p>Avg per Category</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Category breakdown
        if category_data:
            st.subheader("📁 FAQs by Category")
            
            for cat in category_data:
                percentage = (cat['count'] / total_faqs) * 100
                
                st.markdown(f"""
                <div style='margin: 15px 0;'>
                    <div style='display: flex; justify-content: space-between; 
                                align-items: center; margin-bottom: 5px;'>
                        <span style='color: white; font-weight: bold;'>{cat['category']}</span>
                        <span style='color: white;'>{cat['count']} FAQs ({percentage:.1f}%)</span>
                    </div>
                    <div style='background: rgba(255,255,255,0.2); height: 8px; 
                                border-radius: 4px; overflow: hidden;'>
                        <div style='background: linear-gradient(90deg, #43e97b 0%, #38f9d7 100%); 
                                    height: 100%; width: {percentage}%; transition: width 0.3s ease;'></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    conn.close()