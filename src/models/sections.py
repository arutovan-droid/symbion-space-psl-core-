from enum import Enum


class PSLSection(str, Enum):
    FACT = "FACT"
    TECHNIQUE = "TECHNIQUE"
    HYP = "HYP"
    ONTO = "ONTO"
    RESONANCE = "RESONANCE"
    ROLLBACK = "ROLLBACK"
    SAFETY = "SAFETY"
    CHECKLIST = "CHECKLIST"
    THREE_C = "3C"
    GLOSS = "GLOSS"
