def decide(intent_level: str, confidence: float, lead_score: int):
    if intent_level == "HOT" and confidence >= 0.7:
        return {
            "action": "notify_sales",
            "reason": "High confidence buying intent"
        }

    return {
        "action": "ignore",
        "reason": "Low or unclear intent"
    }
