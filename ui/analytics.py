import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from database.bank_crud import get_transactions

def analytics_ui():
    st.markdown("## 📊 Analytics Dashboard")

    data = get_transactions()
    if not data:
        st.warning("No analytics data available.")
        return

    df = pd.DataFrame(data, columns=["Sender", "Receiver", "Amount", "Time"])

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🔹 Transfers Count")
        fig, ax = plt.subplots()
        df["Sender"].value_counts().plot(kind="bar", ax=ax)
        st.pyplot(fig)

    with col2:
        st.subheader("🔹 Money Distribution")
        fig2, ax2 = plt.subplots()
        df.groupby("Sender")["Amount"].sum().plot(kind="pie", autopct="%1.1f%%", ax=ax2)
        st.pyplot(fig2)
