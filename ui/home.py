import streamlit as st

def home_ui():
    st.markdown("<h1 class='home-title'>🏦 BankBot AI</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p class='home-subtitle'>Your smart AI-powered banking assistant</p>",
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div class="feature-card card-chat">
                💬 <h3>AI Chatbot</h3>
                <p>WhatsApp-style smart banking conversations.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            """
            <div class="feature-card card-transfer">
                💸 <h3>Money Transfer</h3>
                <p>Secure, guided money transfer flow.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            """
            <div class="feature-card card-atm">
                📍 <h3>ATM Finder</h3>
                <p>Find nearby ATMs using live location.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    col4, col5, col6 = st.columns(3)

    with col4:
        st.markdown(
            """
            <div class="feature-card card-balance">
                💰 <h3>Check Balance</h3>
                <p>Instantly view your account balance.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col5:
        st.markdown(
            """
            <div class="feature-card card-loan">
                🏦 <h3>Loan Details</h3>
                <p>Explore Home, Gold & Land loans.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col6:
        st.markdown(
            """
            <div class="feature-card card-block">
                🚫 <h3>Card Block</h3>
                <p>Instantly block your debit/credit card.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.success("👉 Use the sidebar to start chatting with BankBot AI")


