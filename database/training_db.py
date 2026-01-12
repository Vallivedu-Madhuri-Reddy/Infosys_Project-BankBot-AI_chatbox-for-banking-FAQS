# database/training_db.py
from database.db import get_connection

def add_training_example(intent, example):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS training_data (intent TEXT, example TEXT)"
    )
    cur.execute(
        "INSERT INTO training_data (intent, example) VALUES (?, ?)",
        (intent, example)
    )
    conn.commit()
    conn.close()

def get_training_data():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS training_data (intent TEXT, example TEXT)"
    )
    cur.execute("SELECT intent, example FROM training_data")
    rows = cur.fetchall()
    conn.close()
    return rows

def delete_training_example(intent, example):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM training_data WHERE intent=? AND example=?",
        (intent, example)
    )
    conn.commit()
    conn.close()
