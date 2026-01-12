import streamlit as st
from database.bank_crud import get_balance, transfer_money, delete_user
from nlu_engine.infer_intent import IntentClassifier
from nlu_engine.entity_extractor import extract
from experiments.llm_local import grok_answer
from nlu_engine.infer_intent import IntentClassifier
# dialogue_manager/dialogue_handler.py
from nlu_engine.infer_intent import IntentClassifier
from nlu_engine.entity_extractor import extract
from experiments.llm_local import grok_answer

intent_classifier = IntentClassifier("models/intent_model")

from nlu_engine.infer_intent import IntentClassifier


def handle_user_message(message: str):
    clf = IntentClassifier()

    intent, confidence = clf.predict(message)

    if intent is None:
        return "⚠️ Model not trained yet. Please contact admin."

    # Example routing
    if intent == "check_balance":
        return "Your balance is ₹25,000"
    elif intent == "loan_info":
        return "We offer home, gold and personal loans"
    else:
        return "Sorry, I didn't understand your request."


# Load model ONCE
intent_classifier = IntentClassifier("models/intent_model")


def handle_user_message(message: str) -> str:
    msg = message.strip().lower()

    st.session_state.setdefault("flow", None)
    st.session_state.setdefault("data", {})

    # ---------------- GREETING ----------------
    if msg in ["hi", "hello", "hey"]:
        return "👋 Hi! Options: balance | transfer | atm | loan | block card"

    # ---------------- NLU ----------------
    intents = intent_classifier.predict(msg, top_k=1)
    intent = intents[0]["intent"] if intents else "fallback"
    entities = extract(msg)

    # ---------------- BANKING ----------------
    if intent == "check_balance":
        user = st.session_state.get("user")
        if not user:
            return "🔐 Please login first."
        balance = get_balance(user)
        return f"💰 Your account balance is ₹{balance}"

    if intent == "transfer_money":
        amount = entities.get("amount", [0])[0]
        return f"💸 Transfer request detected for ₹{amount}"

    if intent == "find_atm":
        return "📍 Please enable location access to find nearby ATMs."

    if intent == "card_block":
        return "⚠️ Please visit the bank branch to block your card."

    # ---------------- EDUCATIONAL ----------------
    if intent in ["define_datascience", "define_deep_learning"]:
        return grok_answer(msg)

    if msg == "loan":
        return (
            "💰 Loan Details:\n"
            "• Gold Loan: 7% – 12%\n"
            "• Land Loan: 9% – 14%\n"
            "• Home Loan: 8% – 10%"
        )

    # ---------------- FALLBACK ----------------
    return grok_answer(msg)
