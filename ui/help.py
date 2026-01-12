import streamlit as st

def help_ui():
    st.markdown("<h2>🆘 Help & User Guide</h2>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="help-card help-transfer">
        <h3>💸 Money Transfer</h3>
        <p>
        Type <b>transfer</b><br>
        ➜ Enter receiver username<br>
        ➜ Enter amount<br>
        ➜ Transfer completed
        </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="help-card help-balance">
        <h3>💰 Check Balance</h3>
        <p>
        Type <b>balance</b><br>
        ➜ Your account balance is displayed instantly
        </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="help-card help-atm">
        <h3>📍 ATM Finder</h3>
        <p>
        Type <b>atm</b><br>
        ➜ Enable live location<br>
        ➜ Nearby ATMs will be shown
        </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="help-card help-loan">
        <h3>🏦 Loan Details</h3>
        <p>
        Type <b>loan</b><br>
        ➜ Home Loan<br>
        ➜ Gold Loan<br>
        ➜ Land Loan
        </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="help-card help-block">
        <h3>🚫 Card Block</h3>
        <p>
        Type <b>block card</b><br>
        ➜ Enter account number<br>
        ➜ Card blocked successfully
        </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")
    st.info(
        "📞 **Need Help?**\n\n"
        "📧 Email: support@bankbot.ai\n"
        "📱 Phone: +91-90000-00000"
    )
