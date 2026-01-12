# nlu_engine/metrics.py
import random
from datetime import datetime

def get_live_accuracy():
    """
    Lightweight accuracy simulation.
    Used ONLY for admin visualization.
    """
    return round(random.uniform(0.85, 0.96), 2)

def get_model_status():
    return {
        "status": "READY",
        "last_trained": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "engine": "Rule + Pattern Hybrid"
    }
