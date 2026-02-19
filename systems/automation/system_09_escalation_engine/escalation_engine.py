import json

def escalate(decision):
    urgency = decision.get("urgency", "low")
    confidence = decision.get("confidence", 0.5)

    if urgency == "high":
        return {
            "priority_level": "P1",
            "escalate": True,
            "escalation_target": "Senior Support / Manager",
            "sla_hours": 1,
            "escalation_reason": "High urgency case"
        }

    if urgency == "medium" and confidence < 0.6:
        return {
            "priority_level": "P2",
            "escalate": True,
            "escalation_target": "Support Team",
            "sla_hours": 4,
            "escalation_reason": "Medium urgency with low confidence"
        }

    return {
        "priority_level": "P3",
        "escalate": False,
        "escalation_target": "None",
        "sla_hours": 24,
        "escalation_reason": "Low risk case"
    }


if __name__ == "__main__":
    sample_decision = {
        "intent": "Refund Request",
        "urgency": "high",
        "confidence": 0.95,
        "recommended_action": "Escalate to billing team",
        "source": "rule"
    }

    escalation = escalate(sample_decision)

    with open("escalation_output.json", "w", encoding="utf-8") as f:
        json.dump(escalation, f, indent=2)

    print("Escalation decision generated and saved.")
