# # nlu_engine/infer_intent.py

# import os
# import joblib
# import numpy as np

# MODEL_DIR = "models"
# MODEL_PATH = os.path.join(MODEL_DIR, "intent_model.pkl")
# VECTORIZER_PATH = os.path.join(MODEL_DIR, "vectorizer.pkl")
# LABEL_ENCODER_PATH = os.path.join(MODEL_DIR, "label_encoder.pkl")


# def models_exist():
#     return (
#         os.path.exists(MODEL_PATH)
#         and os.path.exists(VECTORIZER_PATH)
#         and os.path.exists(LABEL_ENCODER_PATH)
#     )


# class IntentClassifier:
#     """
#     Central NLU Engine used by:
#     - Chatbot
#     - Dialogue Manager
#     - Admin Visualizer
#     """

#     def __init__(self):
#         if not models_exist():
#             self.model = None
#             self.vectorizer = None
#             self.label_encoder = None
#             return

#         self.model = joblib.load(MODEL_PATH)
#         self.vectorizer = joblib.load(VECTORIZER_PATH)
#         self.label_encoder = joblib.load(LABEL_ENCODER_PATH)

#     def predict(self, text: str):
#         if not self.model:
#             return None, 0.0

#         X = self.vectorizer.transform([text])
#         probs = self.model.predict_proba(X)[0]

#         max_idx = np.argmax(probs)
#         intent = self.label_encoder.inverse_transform([max_idx])[0]
#         confidence = float(probs[max_idx])

#         return intent, confidence

#     def predict_all(self, text: str):
#         """
#         Returns all intents with confidence
#         """
#         if not self.model:
#             return []

#         X = self.vectorizer.transform([text])
#         probs = self.model.predict_proba(X)[0]

#         intents = self.label_encoder.inverse_transform(
#             np.arange(len(probs))
#         )

#         results = []
#         for intent, prob in zip(intents, probs):
#             results.append({
#                 "Intent": intent,
#                 "Confidence": float(prob)
#             })

#         results.sort(key=lambda x: x["Confidence"], reverse=True)
#         return results


# # ---------- ADMIN / VISUALIZER SUPPORT ----------

# def predict_with_confidence(text: str):
#     clf = IntentClassifier()
#     return clf.predict_all(text)
import json

class IntentClassifier:
    def __init__(self, model_path=None):
        """
        Lightweight intent classifier.
        `model_path` is ignored, included only to avoid errors.
        """
        with open("nlu_engine/intents.json", "r", encoding="utf-8") as f:
            self.intents = json.load(f)["intents"]

    def predict(self, text, top_k=1):
        text = text.lower()

        for intent in self.intents:
            patterns = intent.get("patterns", [])
            for p in patterns:
                if p.lower() in text:
                    return [{"intent": intent.get("tag", intent.get("name", "fallback"))}]

        return [{"intent": "fallback"}]
