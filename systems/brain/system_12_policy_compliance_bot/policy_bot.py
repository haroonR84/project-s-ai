import json

POLICIES = [
    {
        "name": "Refund Approval Policy",
        "condition": lambda action: "refund" in action.lower(),
        "allowed": False,
        "reason": "Refunds require human approval"
    },
    {
        "name": "Password Reset Policy",
        "condition": lambda action: "password reset" in action.lower(),
        "allowed": True,
        "reason": "Password resets are automated"
    }
]

def check_policy(recommended_action):
    for policy in POLICIES:
        if policy["condition"](recommended_action):
            return {
                "policy": policy["name"],
                "approved": policy["allowed"],
                "reason": policy["reason"]
            }

    return {
        "policy": "Default Policy",
        "approved": True,
        "reason": "No restrictions found"
    }


if __name__ == "__main__":
    sample_action = "Send password reset instructions"

    result = check_policy(sample_action)

    with open("policy_decision.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    print("Policy compliance check completed.")
