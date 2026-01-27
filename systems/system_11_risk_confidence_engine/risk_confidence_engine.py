import json

def calculate_risk(decision, escalation):
    risk_score = 0

    if decision["urgency"] == "high":
        risk_score += 40
    elif decision["urgency"] == "medium":
        risk_score += 20

    if escalation["escalate"]:
        risk_score += 30

    confidence = decision.get("confidence", 0.5)
    confidence_penalty = int((1 - confidence) * 30)
    risk_score += confidence_penalty

    risk_score = min(risk_score, 100)

    if risk_score >= 70:
        level = "High"
    elif risk_score >= 40:
        level = "Medium"
    else:
        level = "Low"

    adjusted_confidence = max(confidence - (risk_score / 200), 0)

    return {
        "risk_score": risk_score,
        "risk_level": level,
        "confidence_adjusted": round(adjusted_confidence, 2),
        "handling_guidance": (
            "Human review required" if level == "High"
            else "Monitor closely" if level == "Medium"
            else "Auto-handle allowed"
        )
    }


if __name__ == "__main__":
    sample_decision = {
        "intent": "Refund Request",
        "urgency": "high",
        "confidence": 0.6
    }

    sample_escalation = {
        "escalate": True
    }

    result = calculate_risk(sample_decision, sample_escalation)

    with open("risk_confidence_output.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    print("Risk & confidence scoring completed.")
