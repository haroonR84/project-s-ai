import streamlit as st

# ---- Simulated system calls (from Systems 7–13) ----

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

def risk_engine(decision, escalation):
    score = 80 if escalation["escalate"] else 20
    return {
        "risk_score": score,
        "risk_level": "High" if score > 50 else "Low"
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

def automation_brain(case_text):
    decision = decision_engine(case_text)
    escalation = escalation_engine(decision)
    risk = risk_engine(decision, escalation)
    policy = policy_check(decision["recommended_action"])

    final_outcome = (
        "Escalate to human"
        if not policy["approved"]
        else decision["recommended_action"]
    )

    return {
        "decision": decision,
        "escalation": escalation,
        "risk": risk,
        "policy": policy,
        "final_outcome": final_outcome
    }

# ---- Streamlit UI ----

st.set_page_config(page_title="Unified AI Systems Dashboard", layout="wide")

st.title("🧠 Unified AI Systems Dashboard")

case_text = st.text_area(
    "Enter customer case / message:",
    height=120,
    placeholder="Customer is asking for a refund due to delay"
)

if st.button("Run AI Systems"):
    result = automation_brain(case_text)

    st.subheader("📌 Decision Engine")
    st.json(result["decision"])

    st.subheader("🚨 Escalation Engine")
    st.json(result["escalation"])

    st.subheader("⚠️ Risk & Confidence")
    st.json(result["risk"])

    st.subheader("📜 Policy Check")
    st.json(result["policy"])

    st.subheader("✅ Final Outcome")
    st.success(result["final_outcome"])
