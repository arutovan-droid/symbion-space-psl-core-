# src/ast/models.py
from typing import List, Dict, Optional
from pydantic import BaseModel

class Constraint(BaseModel):
    name: str
    operator: str  # <=, >=, =, etc.
    value: float
    unit: Optional[str] = None

class ThreeC(BaseModel):
    clear: bool
    cheap: bool 
    safe: bool

class PSLDocument(BaseModel):
    version: str
    context: str
    goal: str
    constraints: List[Constraint]
    resources: Optional[List[str]] = None
    skill: Optional[str] = None
    sections: Dict[str, List[str]]
    three_c: Optional[ThreeC] = None
    gloss: Optional[str] = None
