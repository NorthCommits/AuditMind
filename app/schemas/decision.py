from pydantic import BaseModel
from typing import Dict


class DecisionCreate(BaseModel):
    decision_key: str
    input_payload: Dict
    output_payload: Dict
    decision_made_by: str


class DecisionResponse(BaseModel):
    id: str
    decision_key: str
    version: int
