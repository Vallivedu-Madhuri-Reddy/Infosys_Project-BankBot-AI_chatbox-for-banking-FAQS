import streamlit as st
from database.db import get_connection
from datetime import datetime

def knowledge_base_ui():
    st.markdown("""
    <div style='background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); 
                padding: 30px; border-radius: 15px; margin-bottom: 30px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);'>
        <h1 style='color: white; margin: 0; text-align: center;'>📚 Knowledge Base</h1>
        <p style='color: rgba(255,255,255,0.9); text-align: center; margin: 10px 0 0 0;'>
            Manage Banking Information & Documentation
        </p>
    </div>
    """, unsafe_allow_html=True)

    tabs = st.tabs([
        "📖 Browse Knowledge Base",
        "➕ Add Article",
        "✏️ Edit Articles",
        "📊 KB Statistics"
    ])

    conn = get_connection()
    cur = conn.cursor()

    # TAB 1: Browse Knowledge Base
    with tabs[0]:
        st.markdown("""
        <div class='admin-card'>
            <h3>📖 Knowledge Base Articles</h3>
        """, unsafe_allow_html=True)
        
        # Search and filter
        col1, col2 = st.columns([3, 1])
        
        with col1:
            search_term = st.text_input("🔍 Search articles", placeholder="Search by title or content...")
        
        with col2:
            cur.execute("SELECT DISTINCT category FROM knowledge_base")
            categories = [row['category'] for row in cur.fetchall() if row['category']]
            filter_cat = st.selectbox("Category", ["All"] + categories)
        
        # Get articles
        if search_term:
            cur.execute("""
                SELECT * FROM knowledge_base 
                WHERE title LIKE ? OR content LIKE ?
                ORDER BY updated_at DESC
            """, (f'%{search_term}%', f'%{search_term}%'))
        elif filter_cat != "All":
            cur.execute("""
                SELECT * FROM knowledge_base 
                WHERE category = ?
                ORDER BY updated_at DESC
            """, (filter_cat,))
        else:
            cur.execute("SELECT * FROM knowledge_base ORDER BY updated_at DESC")
        
        articles = cur.fetchall()
        
        if articles:
            st.write(f"**{len(articles)} articles found**")
            
            for article in articles:
                with st.expander(f"📄 {article['title']}"):
                    st.markdown(f"""
                    <div style='background: rgba(0,0,0,0.1); padding: 15px; border-radius: 8px;'>
                        <div style='margin-bottom: 10px;'>
                            <span class='info-badge'>{article['category'] or 'Uncategorized'}</span>
                            {f"<span class='success-badge' style='margin-left: 10px;'>{article['tags']}</span>" if article['tags'] else ""}
                        </div>
                        <div style='background: white; padding: 15px; border-radius: 8px; 
                                    color: #333; margin: 10px 0;'>
                            {article['content']}
                        </div>
                        <div style='margin-top: 10px; font-size: 0.9em; color: gray;'>
                            <p style='margin: 0;'>Created: {article['created_at']}</p>
                            <p style='margin: 0;'>Updated: {article['updated_at']}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button("🗑️ Delete", key=f"del_kb_{article['id']}"):
                        cur.execute("DELETE FROM knowledge_base WHERE id=?", (article['id'],))
                        conn.commit()
                        st.success("Article deleted!")
                        st.rerun()
        else:
            st.info("No articles found. Add some knowledge base content!")
        
        st.markdown("</div>", unsafe_allow_html=True)

    # TAB 2: Add Article
    with tabs[1]:
        st.markdown("""
        <div class='admin-card' style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);'>
            <h3 style='color: white;'>➕ Add New Article</h3>
        """, unsafe_allow_html=True)
        
        title = st.text_input("Article Title", placeholder="e.g., How to Apply for Home Loan")
        
        col1, col2 = st.columns(2)
        
        with col1:
            cur.execute("SELECT DISTINCT category FROM knowledge_base")
            existing_categories = [row['category'] for row in cur.fetchall() if row['category']]
            
            category_type = st.radio("Category", ["Existing", "New"])
            
            if category_type == "Existing" and existing_categories:
                category = st.selectbox("Select Category", existing_categories)
            else:
                category = st.text_input("New Category", placeholder="e.g., Loans, Cards, Accounts")
        
        with col2:
            tags = st.text_input("Tags (comma-separated)", placeholder="loan, home, eligibility")
        
        content = st.text_area(
            "Article Content",
            height=300,
            placeholder="Write your article content here. You can include detailed information, steps, requirements, etc."
        )
        
        if st.button("📝 Publish Article", use_container_width=True):
            if title and content:
                cur.execute("""
                    INSERT INTO knowledge_base (title, content, category, tags) 
                    VALUES (?, ?, ?, ?)
                """, (title, content, category or "General", tags))
                conn.commit()
                st.success("✅ Article published successfully!")
                st.balloons()
                st.rerun()
            else:
                st.warning("Please provide at least a title and content")
        
        st.markdown("</div>", unsafe_allow_html=True)

    # TAB 3: Edit Articles
    with tabs[2]:
        st.markdown("""
        <div class='admin-card' style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);'>
            <h3 style='color: white;'>✏️ Edit Articles</h3>
        """, unsafe_allow_html=True)
        
        cur.execute("SELECT * FROM knowledge_base ORDER BY updated_at DESC")
        all_articles = cur.fetchall()
        
        if all_articles:
            article_options = [f"{art['id']} - {art['title']}" for art in all_articles]
            selected_idx = st.selectbox(
                "Select Article to Edit",
                range(len(article_options)),
                format_func=lambda x: article_options[x]
            )
            
            selected_article = all_articles[selected_idx]
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            new_title = st.text_input("Title", value=selected_article['title'])
            
            col1, col2 = st.columns(2)
            
            with col1:
                cur.execute("SELECT DISTINCT category FROM knowledge_base")
                categories = [row['category'] for row in cur.fetchall() if row['category']]
                new_category = st.selectbox(
                    "Category",
                    categories,
                    index=categories.index(selected_article['category']) if selected_article['category'] in categories else 0
                )
            
            with col2:
                new_tags = st.text_input("Tags", value=selected_article['tags'] or "")
            
            new_content = st.text_area("Content", value=selected_article['content'], height=300)
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("💾 Save Changes", use_container_width=True):
                    cur.execute("""
                        UPDATE knowledge_base 
                        SET title=?, content=?, category=?, tags=?, updated_at=CURRENT_TIMESTAMP
                        WHERE id=?
                    """, (new_title, new_content, new_category, new_tags, selected_article['id']))
                    conn.commit()
                    st.success("✅ Article updated!")
                    st.rerun()
            
            with col2:
                if st.button("🗑️ Delete Article", use_container_width=True):
                    cur.execute("DELETE FROM knowledge_base WHERE id=?", (selected_article['id'],))
                    conn.commit()
                    st.success("Article deleted!")
                    st.rerun()
        else:
            st.info("No articles available to edit")
        
        st.markdown("</div>", unsafe_allow_html=True)

    # TAB 4: KB Statistics
    with tabs[3]:
        st.markdown("""
        <div class='admin-card' style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);'>
            <h3 style='color: white;'>📊 Knowledge Base Statistics</h3>
        """, unsafe_allow_html=True)
        
        # Get stats
        cur.execute("SELECT COUNT(*) FROM knowledge_base")
        total_articles = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(DISTINCT category) FROM knowledge_base WHERE category IS NOT NULL")
        total_categories = cur.fetchone()[0]
        
        cur.execute("""
            SELECT SUM(LENGTH(content)) FROM knowledge_base
        """)
        total_words = (cur.fetchone()[0] or 0) // 5  # Approximate word count
        
        # Recent articles
        cur.execute("""
            SELECT COUNT(*) FROM knowledge_base 
            WHERE DATE(created_at) >= DATE('now', '-7 days')
        """)
        recent_articles = cur.fetchone()[0]
        
        # Display stats
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class='stat-card' style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);'>
                <h2>{total_articles}</h2>
                <p>Total Articles</p>
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
            st.markdown(f"""
            <div class='stat-card' style='background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);'>
                <h2>{total_words:,}</h2>
                <p>Total Words</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class='stat-card' style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);'>
                <h2>{recent_articles}</h2>
                <p>New This Week</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Category breakdown
        cur.execute("""
            SELECT category, COUNT(*) as count 
            FROM knowledge_base 
            WHERE category IS NOT NULL
            GROUP BY category 
            ORDER BY count DESC
        """)
        category_data = cur.fetchall()
        
        if category_data:
            st.subheader("📁 Articles by Category")
            
            for cat in category_data:
                percentage = (cat['count'] / total_articles) * 100 if total_articles > 0 else 0
                
                st.markdown(f"""
                <div style='margin: 15px 0;'>
                    <div style='display: flex; justify-content: space-between; 
                                align-items: center; margin-bottom: 5px;'>
                        <span style='color: white; font-weight: bold;'>📁 {cat['category']}</span>
                        <span style='color: white;'>{cat['count']} articles ({percentage:.1f}%)</span>
                    </div>
                    <div style='background: rgba(255,255,255,0.2); height: 10px; 
                                border-radius: 5px; overflow: hidden;'>
                        <div style='background: linear-gradient(90deg, #43e97b 0%, #38f9d7 100%); 
                                    height: 100%; width: {percentage}%; transition: width 0.3s ease;'></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Recent activity
        st.subheader("📅 Recent Articles")
        cur.execute("""
            SELECT title, category, created_at 
            FROM knowledge_base 
            ORDER BY created_at DESC 
            LIMIT 5
        """)
        recent = cur.fetchall()
        
        for art in recent:
            st.markdown(f"""
            <div style='background: rgba(255,255,255,0.1); padding: 10px; 
                        border-radius: 8px; margin: 8px 0;'>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <div>
                        <strong style='color: white;'>📄 {art['title']}</strong>
                        <span class='info-badge' style='margin-left: 10px;'>{art['category']}</span>
                    </div>
                    <span style='color: rgba(255,255,255,0.7); font-size: 0.9em;'>{art['created_at']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    conn.close()