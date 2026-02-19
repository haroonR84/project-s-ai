import json

SCENARIOS = [
    {
        "name": "Normal Operations",
        "cases": 50,
        "high_urgency_rate": 0.1
    },
    {
        "name": "Refund Spike",
        "cases": 120,
        "high_urgency_rate": 0.4
    },
    {
        "name": "System Outage",
        "cases": 200,
        "high_urgency_rate": 0.6
    }
]

def simulate(scenario):
    escalations = int(scenario["cases"] * scenario["high_urgency_rate"])
    avg_sla = 2 if scenario["high_urgency_rate"] > 0.3 else 8

    risk = "High" if escalations > 50 else "Medium" if escalations > 20 else "Low"

    return {
        "scenario": scenario["name"],
        "total_cases": scenario["cases"],
        "estimated_escalations": escalations,
        "average_sla_hours": avg_sla,
        "risk_level": risk,
        "recommendation": "Increase staff" if risk == "High" else "Normal staffing"
    }

if __name__ == "__main__":
    report = [simulate(s) for s in SCENARIOS]

    with open("what_if_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print("What-if simulation completed and saved.")
