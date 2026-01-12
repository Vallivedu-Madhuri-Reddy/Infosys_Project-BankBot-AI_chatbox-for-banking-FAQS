from database.db import get_connection

def create_account(username, password, account_type, balance):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO users(username,password,account_type,balance) VALUES (?,?,?,?)",
            (username, password, account_type, balance)
        )
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def authenticate_user(username, password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM users WHERE username=? AND password=? AND is_active=1",
        (username, password)
    )
    user = cur.fetchone()
    conn.close()
    return user

def get_balance(username):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT balance FROM users WHERE username=?", (username,))
    row = cur.fetchone()
    conn.close()
    return row["balance"] if row else None

def transfer_money(sender, receiver, amount):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT balance FROM users WHERE username=?", (sender,))
    bal = cur.fetchone()
    if not bal or bal["balance"] < amount:
        conn.close()
        return False

    cur.execute("UPDATE users SET balance=balance-? WHERE username=?", (amount, sender))
    cur.execute("UPDATE users SET balance=balance+? WHERE username=?", (amount, receiver))
    cur.execute(
        "INSERT INTO transactions(sender,receiver,amount) VALUES (?,?,?)",
        (sender, receiver, amount)
    )

    conn.commit()
    conn.close()
    return True

def delete_user(username):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE username=?", (username,))
    conn.commit()
    conn.close()

def get_all_users():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT username,account_type,balance FROM users")
    rows = cur.fetchall()
    conn.close()
    return rows

def get_transactions():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM transactions ORDER BY timestamp DESC")
    rows = cur.fetchall()
    conn.close()
    return rows
def save_chat(user, message, role):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO transactions(sender, receiver, amount) VALUES (?,?,?)",
        (user if role=="user" else "BankBot", role, 0)
    )
    conn.commit()
    conn.close()
