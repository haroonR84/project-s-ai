from fastapi import FastAPI
from .schema import DecisionInput, DecisionOutput
from .logic import decide

app = FastAPI(title="System 04 — Decision Engine")

@app.post("/system_04_decision_engine", response_model=DecisionOutput)
def run_decision_engine(input: DecisionInput):
    return decide(
        input.intent_level,
        input.confidence,
        input.lead_score
    )
