import streamlit as st
import sqlite3
import pandas as pd
import re
from datetime import datetime
import random

# Page config
st.set_page_config(page_title="🏦 Smart Banking Assistant", page_icon="🏦", layout="wide")

# Beautiful Light Theme CSS (No Black Colors)
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
@import url('https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css');
* { margin: 0; padding: 0; box-sizing: border-box; }
.stApp { 
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 50%, #e8eaf6 100%); 
    color: #2c3e50; 
    font-family: 'Poppins', sans-serif;
}
.main-header { 
    font-size: 2.8rem; 
    background: linear-gradient(45deg, #667eea, #764ba2, #f093fb); 
    -webkit-background-clip: text; 
    -webkit-text-fill-color: transparent; 
    text-align: center;
    margin-bottom: 2rem;
}
.chat-bubble-user { 
    background: linear-gradient(135deg, #667eea, #764ba2); 
    color: white; 
    border-radius: 20px 20px 5px 20px; 
    padding: 15px 20px; 
    margin: 10px 0; 
    max-width: 75%;
    box-shadow: 0 5px 15px rgba(102,126,234,0.4);
}
.chat-bubble-bot { 
    background: linear-gradient(135deg, #fff, #f8f9ff); 
    color: #2c3e50; 
    border-radius: 20px 20px 20px 5px; 
    padding: 15px 20px; 
    margin: 10px 0; 
    max-width: 75%;
    border-left: 4px solid #667eea;
    box-shadow: 0 5px 20px rgba(0,0,0,0.1);
}
.metric-card { 
    background: rgba(255,255,255,0.9); 
    border-radius: 20px; 
    padding: 2rem; 
    text-align: center;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    transition: all 0.3s ease;
    border: 1px solid rgba(255,255,255,0.5);
}
.metric-card:hover { transform: translateY(-5px); box-shadow: 0 15px 40px rgba(0,0,0,0.15); }
.btn-gradient { 
    background: linear-gradient(45deg, #667eea, #764ba2); 
    color: white; 
    border: none; 
    border-radius: 25px; 
    padding: 12px 30px; 
    font-weight: 600;
    font-size: 16px;
    transition: all 0.3s ease;
}
.btn-gradient:hover { transform: translateY(-2px); box-shadow: 0 10px 25px rgba(102,126,234,0.4); }
.section-card {
    background: rgba(255,255,255,0.95); 
    border-radius: 20px; 
    padding: 2rem; 
    box-shadow: 0 15px 35px rgba(0,0,0,0.08);
    backdrop-filter: blur(10px);
}
</style>
""", unsafe_allow_html=True)

# Enhanced Database with more features
@st.cache_resource
def init_db():
    conn = sqlite3.connect('smart_banking.db', check_same_thread=False)
    c = conn.cursor()
    
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  name TEXT UNIQUE, 
                  account_number TEXT UNIQUE, 
                  balance REAL DEFAULT 0, 
                  account_type TEXT DEFAULT 'savings',
                  phone TEXT,
                  email TEXT,
                  last_login TEXT,
                  status TEXT DEFAULT 'active')''')
    
    # Enhanced Transactions
    c.execute('''CREATE TABLE IF NOT EXISTS transactions 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  from_account TEXT,
                  to_account TEXT,
                  amount REAL,
                  type TEXT,
                  status TEXT DEFAULT 'completed',
                  timestamp TEXT)''')
    
    # Chat history with sentiment
    c.execute('''CREATE TABLE IF NOT EXISTS chat_history 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_message TEXT,
                  bot_response TEXT,
                  intent TEXT,
                  sentiment TEXT,
                  timestamp TEXT)''')
    
    # Sample data
    users_data = [
        ('Sai Kumar', 'ACC001', 25000.0, 'savings', '9876543210', 'sai@email.com', 'active'),
        ('Ram Reddy', 'ACC002', 45000.0, 'current', '9876543211', 'ram@email.com', 'active'),
        ('Priya Sharma', 'ACC003', 18000.0, 'savings', '9876543212', 'priya@email.com', 'active'),
        ('You', 'ACC004', 35000.0, 'savings', '9876543213', 'you@email.com', 'active')
    ]
    c.executemany("""INSERT OR IGNORE INTO users 
                     (name, account_number, balance, account_type, phone, email, status) 
                     VALUES (?, ?, ?, ?, ?, ?, ?)""", users_data)
    conn.commit()
    return conn

# Smart conversational responses
GREETINGS = ['hi', 'hello', 'hey', 'good morning', 'good afternoon', 'namaste']
GREETING_RESPONSES = [
    "Hi there! 👋 How can I assist you with your banking today?",
    "Hello! 😊 Welcome to Smart Banking Assistant. What can I do for you?",
    "Hey! 🙌 Ready to help with all your banking needs!",
    "Namaste! 🌟 How may I serve you today?"
]

BANKING_INTENTS = {
    'greeting': GREETINGS,
    'balance': ['balance', 'check balance', 'my balance', 'account balance', 'how much money'],
    'transfer': ['transfer', 'send money', 'pay', 'send', 'transaction', 'money transfer'],
    'loan': ['loan', 'apply loan', 'loan eligibility', 'personal loan', 'home loan'],
    'atm': ['atm', 'find atm', 'atm near me', 'nearest atm'],
    'card': ['block card', 'card block', 'lost card', 'stolen card', 'block my card'],
    'branch': ['branch', 'bank branch', 'nearest branch'],
    'help': ['help', 'support', 'assistance']
}

def detect_intent(query):
    query_lower = query.lower()
    best_intent = 'unknown'
    max_score = 0
    
    for intent, keywords in BANKING_INTENTS.items():
        score = sum(1 for keyword in keywords if keyword in query_lower)
        if score > max_score:
            max_score = score
            best_intent = intent
    
    return best_intent, max_score / len(keywords) if keywords else 0

def extract_entities(query):
    entities = {}
    amount_match = re.search(r'rs?\.?(\d+(?:,\d{3})*(?:\.\d{2})?|\d+)', query, re.IGNORECASE)
    if amount_match:
        entities['amount'] = float(amount_match.group(1).replace(',', ''))
    
    account_match = re.search(r'acc(?:ount)?[:\-]?\s*(\w+)', query, re.IGNORECASE)
    if account_match:
        entities['account'] = account_match.group(1)
    
    return entities

def get_smart_response(intent, entities, conn):
    if intent == 'greeting':
        return random.choice(GREETING_RESPONSES)
    
    elif intent == 'balance':
        df = pd.read_sql_query("SELECT name, account_number, balance, account_type FROM users WHERE status='active'", conn)
        if not df.empty:
            total = df['balance'].sum()
            return f"💰 **Account Summary**\n\n{df[['name', 'balance', 'account_type']].to_string(index=False)}\n\n**Total Balance: ₹{total:,.2f}**"
        return "No active accounts found. Please contact support."
    
    elif intent == 'transfer':
        if 'amount' in entities:
            return f"✅ **Transfer Request**\n₹{entities['amount']:,.2f} transfer initiated!\n\n👥 **Select recipient:**\n• Sai Kumar (ACC001)\n• Ram Reddy (ACC002)\n• Priya Sharma (ACC003)"
        return "💸 Please specify amount: 'transfer ₹5000 to Sai'"
    
    elif intent == 'loan':
        return """🏦 **Loan Options Available:**
        
| Loan Type | Interest Rate | Max Amount | Tenure |
|-----------|---------------|------------|--------|
| Personal  | 10.5% p.a.    | ₹5,00,000  | 5 yrs  |
| Home      | 8.2% p.a.     | ₹1 Cr      | 30 yrs |
| Car       | 9.8% p.a.     | ₹25,00,000 | 7 yrs  |

Type **'apply personal loan'** to proceed!"""
    
    elif intent == 'atm':
        return """📍 **Nearest ATMs:**
        
• **Main Branch ATM** - 1.2 km (24x7)
• **Mall ATM** - 2.5 km (8AM-10PM)  
• **Railway Station** - 800 m (24x7)
• **24x7 ATM** - 500 m (Cash + Cheque)"""
    
    elif intent == 'card':
        return "🔒 **Card blocked successfully!**\n✅ New card will be delivered in 3-5 working days.\n📞 Call 1800-XXX-XXXX for status."
    
    elif intent == 'branch':
        return """🏛️ **Branch Locations:**
        
• **Main Branch**: MG Road, 10AM-5PM
• **Tirupati Branch**: Temple Road, 9:30AM-4PM  
• **Chennai Branch**: Anna Nagar, 9AM-5PM"""
    
    elif intent == 'help':
        return """🆘 **How I can help:**
        
• 💰 Check balance
• 💸 Transfer money  
• 🏦 Loan applications
• 📍 Find ATM/Branch
• 🔒 Block card
• ℹ️ Account details

Just type naturally! 😊"""
    
    else:
        return random.choice([
            "🤔 I understand you're asking about banking. Try: 'check balance', 'transfer ₹1000', 'find ATM'",
            "💡 Quick commands: balance, transfer, loan, ATM, help",
            "😊 I'm here for all banking queries! What specifically can I help with?",
            "🚀 Type 'help' for all available banking services!"
        ])

# Main Banking App
conn = init_db()

st.markdown('<h1 class="main-header animate__animated animate__fadeInDown">🏦 Smart Banking Assistant</h1>', unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.markdown("## 🌟 Quick Navigation")
page = st.sidebar.radio("Select Page:", ["💬 Chatbot", "👥 Accounts", "💳 Transactions", "📊 Dashboard"], index=0)

if page == "💬 Chatbot":
    st.markdown('<div class="section-card animate__animated animate__fadeInUp">', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align:center; color:#667eea;">🤖 Your Personal Banking Assistant</h2>', unsafe_allow_html=True)
    
    # Chat interface
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    chat_container = st.container(height=600)
    with chat_container:
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f'<div class="chat-bubble-user animate__animated animate__slideInRight">{message["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-bubble-bot animate__animated animate__slideInLeft"><strong>🏦 Assistant:</strong> {message["content"]}</div>', unsafe_allow_html=True)
    
    # Chat input
    if prompt := st.chat_input("Say 'Hi' or ask about banking services..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(f'<div class="chat-bubble-user">{prompt}</div>', unsafe_allow_html=True)
        
        with st.chat_message("assistant"):
            intent, confidence = detect_intent(prompt)
            entities = extract_entities(prompt)
            response = get_smart_response(intent, entities, conn)
            
            st.markdown(f'<div class="chat-bubble-bot">{response}</div>', unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            # Save to database
            c = conn.cursor()
            c.execute("INSERT INTO chat_history (user_message, bot_response, intent, sentiment, timestamp) VALUES (?, ?, ?, ?, ?)",
                     (prompt, response, intent, 'positive' if '✅' in response else 'neutral', datetime.now().isoformat()))
            conn.commit()
    
    st.markdown('</div>', unsafe_allow_html=True)

elif page == "👥 Accounts":
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<h2>👥 Manage Accounts</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        df_users = pd.read_sql_query("SELECT * FROM users WHERE status='active'", conn)
        st.dataframe(df_users, use_container_width=True, hide_index=True)
    
    with col2:
        st.subheader("🔄 Quick Actions")
        action = st.selectbox("Action:", ["Update Balance", "Add User", "Block User"])
        
        if action == "Update Balance":
            user = st.selectbox("Select User:", df_users['name'].tolist())
            new_balance = st.number_input("New Balance:", value=25000.0)
            if st.button("💾 Update", key="update"):
                c = conn.cursor()
                c.execute("UPDATE users SET balance=?, last_login=? WHERE name=?", 
                         (new_balance, datetime.now().isoformat(), user))
                conn.commit()
                st.success("✅ Balance updated!")
                st.rerun()
        
        elif action == "Add User":
            new_name = st.text_input("Name:")
            new_acc = st.text_input("Account No:")
            if st.button("➕ Add", key="add"):
                c = conn.cursor()
                c.execute("INSERT INTO users (name, account_number, balance, last_login) VALUES (?, ?, 10000, ?)",
                         (new_name, new_acc, datetime.now().isoformat()))
                conn.commit()
                st.success("✅ User added!")
    
    st.markdown('</div>', unsafe_allow_html=True)

elif page == "💳 Transactions":
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<h2>💳 Recent Transactions</h2>', unsafe_allow_html=True)
    
    # Sample transactions display
    df_trans = pd.read_sql_query("SELECT * FROM transactions ORDER BY timestamp DESC LIMIT 20", conn)
    if df_trans.empty:
        st.info("👆 Send money through chatbot to see transactions here!")
    else:
        st.dataframe(df_trans, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

elif page == "📊 Dashboard":
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<h2>📊 Banking Dashboard</h2>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    total_users = pd.read_sql_query("SELECT COUNT(*) as count FROM users WHERE status='active'", conn).iloc[0]['count']
    total_balance = pd.read_sql_query("SELECT SUM(balance) as total FROM users", conn).iloc[0]['total']
    chat_count = pd.read_sql_query("SELECT COUNT(*) as count FROM chat_history", conn).iloc[0]['count']
    
    with col1:
        st.metric("👥 Active Users", total_users)
    with col2:
        st.metric("💰 Total Balance", f"₹{total_balance:,.0f}")
    with col3:
        st.metric("💬 Total Chats", chat_count)
    with col4:
        st.metric("⭐ Satisfaction", "98%")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div style='text-align:center; padding:2rem; color:#7f8c8d;'>
    <p>🛡️ Secure • ⚡ Fast • 🤖 AI-Powered | Built for Smart Banking</p>
</div>
""", unsafe_allow_html=True)

