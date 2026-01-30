from pydantic import BaseModel

class DecisionInput(BaseModel):
    intent_level: str
    confidence: float
    lead_score: int

class DecisionOutput(BaseModel):
    action: str
    reason: str
