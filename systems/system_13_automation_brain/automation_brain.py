import json

# ---- Simulated inputs from previous systems ----

def decision_engine(case_text):
    return {
        "intent": "Refund Request",
        "urgency": "high",
        "confidence": 0.6,
        "recommended_action": "Process refund"
    }

def escalation_engine(decision):
    if decision["urgency"] == "high":
        return {
            "priority": "P1",
            "escalate": True,
            "target": "Manager"
        }
    return {
        "priority": "P3",
        "escalate": False,
        "target": None
    }

def policy_check(action):
    if "refund" in action.lower():
        return {
            "approved": False,
            "reason": "Refund requires human approval"
        }
    return {
        "approved": True,
        "reason": "Action allowed"
    }

# ---- Orchestration ----

def automation_brain(trigger):
    decision = decision_engine(trigger)
    escalation = escalation_engine(decision)
    policy = policy_check(decision["recommended_action"])

    final_action = {
        "trigger": trigger,
        "decision": decision,
        "escalation": escalation,
        "policy": policy,
        "final_outcome": (
            "Escalate to human"
            if not policy["approved"]
            else decision["recommended_action"]
        )
    }

    return final_action


if __name__ == "__main__":
    trigger_event = "Customer is angry about delayed refund"

    result = automation_brain(trigger_event)

    with open("automation_output.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    print("Automation brain executed successfully.")
