import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path("database/bankbot.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # Users table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        account_type TEXT,
        balance REAL,
        is_active INTEGER DEFAULT 1
    )
    """)

    # Transactions table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS transactions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sender TEXT,
        receiver TEXT,
        amount REAL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Training data table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS training_data(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        intent TEXT NOT NULL,
        example TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Chat logs table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS chat_logs(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT,
        message TEXT,
        intent TEXT,
        response TEXT,
        confidence REAL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # FAQs table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS faqs(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT NOT NULL,
        answer TEXT NOT NULL,
        category TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Knowledge base table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS knowledge_base(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        category TEXT,
        tags TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Intent statistics table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS intent_stats(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        intent TEXT NOT NULL,
        count INTEGER DEFAULT 0,
        last_used DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Initialize default intents if not exists
    default_intents = ['check_balance', 'find_atm', 'transfer_money', 'card_block']
    for intent in default_intents:
        cur.execute("""
            INSERT OR IGNORE INTO intent_stats (intent, count)
            VALUES (?, 0)
        """, (intent,))

    # Initialize sample training data if empty
    cur.execute("SELECT COUNT(*) FROM training_data")
    if cur.fetchone()[0] == 0:
        sample_data = [
            ('check_balance', 'What is my account balance'),
            ('check_balance', 'Show me my balance'),
            ('check_balance', 'How much money do I have'),
            ('check_balance', 'Check my balance'),
            ('check_balance', 'Account balance please'),
            ('find_atm', 'Where is the nearest ATM'),
            ('find_atm', 'Find ATM near me'),
            ('find_atm', 'ATM locations'),
            ('find_atm', 'Show nearby ATMs'),
            ('find_atm', 'I need to find an ATM'),
            ('transfer_money', 'I want to transfer money'),
            ('transfer_money', 'Send money to someone'),
            ('transfer_money', 'Transfer funds'),
            ('transfer_money', 'Make a payment'),
            ('transfer_money', 'Send money'),
            ('card_block', 'Block my card'),
            ('card_block', 'I lost my card'),
            ('card_block', 'Disable my debit card'),
            ('card_block', 'Card blocking'),
            ('card_block', 'My card was stolen')
        ]
        cur.executemany("INSERT INTO training_data (intent, example) VALUES (?, ?)", sample_data)

    # Initialize sample FAQs if empty
    cur.execute("SELECT COUNT(*) FROM faqs")
    if cur.fetchone()[0] == 0:
        sample_faqs = [
            ('What are the bank working hours?', 'Our bank is open Monday to Friday from 9 AM to 5 PM, and Saturday from 9 AM to 1 PM.', 'General'),
            ('How do I reset my password?', 'You can reset your password by clicking on "Forgot Password" on the login page or visiting your nearest branch.', 'Account'),
            ('What is the minimum balance required?', 'The minimum balance for savings account is ₹5000 and for current account is ₹10000.', 'Account'),
            ('How can I apply for a loan?', 'You can apply for loans online through our website or visit your nearest branch with required documents.', 'Loans'),
            ('What are the loan interest rates?', 'Home Loan: 8-10%, Gold Loan: 7-12%, Land Loan: 9-14%. Rates subject to change.', 'Loans')
        ]
        cur.executemany("INSERT INTO faqs (question, answer, category) VALUES (?, ?, ?)", sample_faqs)

    conn.commit()
    conn.close()

def fetch_all(query, params=()):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, params)
    rows = cur.fetchall()
    conn.close()
    return rows

def execute(query, params=()):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, params)
    conn.commit()
    conn.close()

# Helper functions for admin panel
def log_chat_interaction(user, message, intent, response, confidence):
    """Log chat interaction for analytics"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO chat_logs (user, message, intent, response, confidence)
        VALUES (?, ?, ?, ?, ?)
    """, (user, message, intent, response, confidence))
    
    # Update intent statistics
    cur.execute("""
        UPDATE intent_stats 
        SET count = count + 1, last_used = CURRENT_TIMESTAMP
        WHERE intent = ?
    """, (intent,))
    
    conn.commit()
    conn.close()

def get_intent_statistics():
    """Get statistics for all intents"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT intent, count, last_used 
        FROM intent_stats 
        ORDER BY count DESC
    """)
    rows = cur.fetchall()
    conn.close()
    return rows

def get_chat_logs(limit=100):
    """Get recent chat logs"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT * FROM chat_logs 
        ORDER BY timestamp DESC 
        LIMIT ?
    """, (limit,))
    rows = cur.fetchall()
    conn.close()
    return rows