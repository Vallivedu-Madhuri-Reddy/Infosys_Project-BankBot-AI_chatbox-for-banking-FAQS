"""
main_app.py

Streamlit UI for BANKBOT NLU:
- Left: editor for intents.json + training controls
- Right: NLU visualizer: query -> intents + entities
"""

import streamlit as st
import os
import json
import sys
import subprocess
from pathlib import Path
from html import escape

st.session_state.pop("intent_classifier", None)

# Make local packages importable
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

# Import entity extractor (safe)
from nlu_engine.entity_extractor import extract as extract_entities  # noqa: E402

# ----------------------- Paths -----------------------

INTENTS_PATH = BASE_DIR / "nlu_engine" / "intents.json"
MODEL_DIR = BASE_DIR / "models" / "intent_model"
LOG_PATH = BASE_DIR / "models" / "training.log"
os.makedirs(MODEL_DIR.parent, exist_ok=True)

# -------------------- Page config --------------------

st.set_page_config(page_title="BankBot NLU", layout="wide")
import streamlit as st

# Page configuration
st.set_page_config(
    page_title="bankbot nlu",
    layout="wide"
)

# Full-page 3D gradient background CSS
st.markdown(
    """
    <style>
    /* Full page 3D/gradient background */
    body, .stApp {
        background: linear-gradient(135deg, #ff9a9e, #fad0c4, #a1c4fd, #c2e9fb);
        background-size: 400% 400%;
        animation: gradientBG 20s ease infinite;
        color: #000;
    }

    @keyframes gradientBG {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }

    /* Make all Streamlit elements have transparent background so gradient shows */
    .stButton>button, .stTextInput>div>input, .stSlider>div>input, .stTextArea>div>textarea {
        background: rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        color: #000 !important;
        border: none !important;
        backdrop-filter: blur(10px);
    }

    /* Optional: remove default margins/paddings for full effect */
    .css-18e3th9 {padding: 0rem 1rem 0rem 1rem;}
    </style>
    """,
    unsafe_allow_html=True
)


st.markdown("Vallivedu Madhuri Reddy")
st.markdown("## BankBot NLU – Intent & Entity Engine")

# --------------------- Utilities ---------------------


def load_intents_file() -> dict:
    if not INTENTS_PATH.exists():
        return {"intents": []}
    with open(INTENTS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_intents_file(data: dict) -> None:
    with open(INTENTS_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def model_exists() -> bool:
    return os.path.isdir(MODEL_DIR) and any(Path(MODEL_DIR).iterdir())


def start_training_subprocess(epochs: int, batch_size: int, lr: float) -> subprocess.Popen:
    cmd = [
        sys.executable,
        str(BASE_DIR / "nlu_engine" / "train_intent.py"),
        "--intents",
        str(INTENTS_PATH),
        "--output_dir",
        str(MODEL_DIR),
        "--epochs",
        str(epochs),
        "--batch_size",
        str(batch_size),
        "--lr",
        str(lr),
        "--model_name",
        "distilbert-base-uncased",
    ]
    return subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)


# ---------------------- Layout -----------------------

left_col, right_col = st.columns([1.2, 1.0])

# ===================== Left: Trainer =====================

with left_col:
    st.subheader("1. Edit & Train Intents")

    data = load_intents_file()
    intents = data.get("intents", [])

    for idx, intent in enumerate(intents):
        name = intent.get("name", f"intent_{idx}")
        examples = intent.get("examples", [])

        with st.expander(f"{name} ({len(examples)} examples)", expanded=False):
            new_name = st.text_input("Intent name", value=name, key=f"name_{idx}")

            examples_text = "\n".join(examples)
            new_examples_text = st.text_area(
                "Examples (one per line)",
                value=examples_text,
                height=150,
                key=f"examples_{idx}",
            )

            intents[idx]["name"] = new_name
            intents[idx]["examples"] = [
                line.strip()
                for line in new_examples_text.split("\n")
                if line.strip()
            ]

    st.markdown("---")
    st.subheader("Create new intent")

    new_intent_name = st.text_input("New intent name", key="new_intent_name")

    new_intent_examples_raw = st.text_area(
        "Examples (one per line)",
        key="new_intent_examples",
        height=150,
        placeholder="Example:\nCheck my balance\nHow much money is in my account\n...",
    )

    if st.button("Add intent"):
        cleaned_name = new_intent_name.strip()
        if not cleaned_name:
            st.error("Please enter an intent name.")
        else:
            existing_names = {it.get("name", "") for it in intents}
            if cleaned_name in existing_names:
                st.error(f"Intent '{cleaned_name}' already exists.")
            else:
                examples = [
                    line.strip()
                    for line in new_intent_examples_raw.splitlines()
                    if line.strip()
                ]
                if not examples:
                    st.error("Please add at least one example sentence.")
                else:
                    intents.append({"name": cleaned_name, "examples": examples})
                    save_intents_file({"intents": intents})
                    st.success(f"Intent '{cleaned_name}' added and saved to intents.json.")

    if st.button("Save intents.json"):
        try:
            save_intents_file({"intents": intents})
            st.success("intents.json saved.")
        except Exception as e:
            st.error(f"Could not save intents.json: {e}")

    st.markdown("---")
    st.subheader("Train intent model")

    epochs = st.number_input("Epochs", min_value=1, max_value=20, value=3)
    batch_size = st.number_input("Batch size", min_value=4, max_value=64, value=16)
    lr = st.number_input("Learning rate", min_value=1e-5, max_value=1e-2, value=5e-5, format="%.5f")

    if st.button("Train intent model"):
        proc = start_training_subprocess(int(epochs), int(batch_size), float(lr))
        st.info("Training started. Streaming logs below...")
        log_lines = []
        placeholder = st.empty()
        for line in proc.stdout:
            log_lines.append(line.rstrip())
            placeholder.text("\n".join(log_lines[-50:]))
        proc.wait()
        if proc.returncode == 0:
            st.success("Training finished. Model saved to models/intent_model.")
        else:
            st.error(f"Training failed with return code {proc.returncode}. See logs above.")

    if LOG_PATH.exists():
        with st.expander("View latest training.log"):
            with open(LOG_PATH, "r", encoding="utf-8") as f:
                st.text(f.read())

# ===================== Right: NLU Tester =====================

with right_col:
    st.subheader("NLU Visualizer")

    # Inject neuromorphic styles
    st.markdown(
        """
        <style>
        .intent-box {
            padding: 12px 18px;
            margin-bottom: 10px;
            border-radius: 12px;
            background: #f0f2f6;
            box-shadow: inset 2px 2px 5px #d1d9e6, inset -3px -3px 7px #ffffff;
            font-size: 16px;
        }
        .entity-chip {
            display:inline-block;
            padding: 6px 12px;
            margin: 4px;
            background:#e3f2fd;
            color:#0d47a1;
            border-radius: 8px;
            font-size:14px;
            font-weight:600;
            box-shadow: 1px 1px 4px #bbdefb;
        }
        .block-card {
            padding: 15px;
            margin-top: 10px;
            border-radius: 16px;
            background: #f8f9fb;
            box-shadow: 3px 3px 8px #d1d9e6, -3px -3px 8px #ffffff;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Try loading classifier
    IntentClassifier = None
    try:
        from nlu_engine.infer_intent import IntentClassifier as _IC
        IntentClassifier = _IC
    except Exception:
        IntentClassifier = None

    if IntentClassifier is None:
        st.info("Intent classifier module could not be loaded. Using rule-based fallback.")
    else:
        if "intent_classifier" not in st.session_state:
            try:
                st.session_state.intent_classifier = IntentClassifier(str(MODEL_DIR))
            except Exception as e:
                st.warning(f"Could not load model; using fallback. ({e})")
                try:
                    st.session_state.intent_classifier = IntentClassifier(str(MODEL_DIR))
                except Exception:
                    st.session_state.intent_classifier = None

    ic = st.session_state.get("intent_classifier", None)

    user_text = st.text_area(
        "User Query",
        value="Show balance for my savings account, I want to send 1000 rupees to account 9876543210.",
        height=120,
    )
    top_k = st.slider("Top intents to show", 1, 5, 4)

    run = st.button("Analyze")

    intents_pred = []
    entities = {}

    if run:
        if ic is None:
            intents_data = load_intents_file()
            intents_pred = []
            txt_low = user_text.lower()
            for intent in intents_data.get("intents", []):
                name = intent.get("name")
                examples = intent.get("examples", [])[:6]
                score = 0.0
                for ex in examples:
                    s = ex.lower().split()
                    for w in s:
                        if w and w in txt_low:
                            score += 0.03
                intents_pred.append(
                    {"intent": name, "score": round(min(0.99, score), 3)}
                )

            if intents_pred:
                ssum = sum(x["score"] for x in intents_pred) or 1.0
                intents_pred = sorted(
                    [{"intent": x["intent"], "score": float(x["score"] / ssum)} for x in intents_pred],
                    key=lambda z: z["score"],
                    reverse=True,
                )[:top_k]
        else:
            try:
                intents_pred = ic.predict(user_text, top_k=int(top_k))
            except Exception as e:
                st.error(f"Intent prediction error: {e}")
                intents_pred = []

        try:
            entities = extract_entities(user_text) or {}
        except Exception as e:
            st.error(f"Entity extraction error: {e}")
            entities = {}

    # Show results
    if intents_pred:
        st.markdown("### **Intent Recognition**")
        st.markdown('<div class="block-card">', unsafe_allow_html=True)

        for item in intents_pred:
            st.markdown(
                f"""
                <div class="intent-box">
                    <b>{escape(item['intent'].replace('_', ' ').title())}</b>
                    <span style='float:right;color:#1976d2;'>{item['score']:.2f}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("### **Entity Extraction**")
        st.markdown('<div class="block-card">', unsafe_allow_html=True)

        if entities:
            for key, vals in entities.items():
                for v in vals:
                    st.markdown(
                        f"<span class='entity-chip'>{escape(key.title())} : {escape(str(v))}</span>",
                        unsafe_allow_html=True,
                    )
        else:
            st.write("No entities found.")

        st.markdown("</div>", unsafe_allow_html=True)

    elif run:
        st.info("No intents returned (empty input or low confidence).")



from database.db import init_db

init_db()   # call once at app start



