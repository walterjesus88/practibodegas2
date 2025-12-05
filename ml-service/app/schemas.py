from pydantic import BaseModel
from typing import List, Any

class AprioriRun(BaseModel):
    min_support: float = 0.01
    min_confidence: float = 0.3

class Rule(BaseModel):
    antecedents: List[str]
    consequents: List[str]
    support: float
    confidence: float
    lift: float
