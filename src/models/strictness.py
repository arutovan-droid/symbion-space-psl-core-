from enum import Enum
from dataclasses import dataclass


class StrictnessMode(str, Enum):
    STRICT = "STRICT"
    RELAXED = "RELAXED"


@dataclass
class StrictnessContext:
    ts_emergence_score: float = 0.0
    kks_score: float = 0.0
    e_function_score: float = 0.0
    risk_tier: int = 0
    mode: str = "default"


def resolve_strictness(ctx: StrictnessContext) -> StrictnessMode:
    high_emergence = (
        ctx.ts_emergence_score >= 0.75
        or ctx.kks_score >= 0.75
        or ctx.e_function_score >= 0.75
    )
    low_operational_risk = ctx.risk_tier <= 1 and ctx.mode in {
        "meta",
        "dialogue",
        "collapse_to_dialogue",
        "ht_mode",
        "ontological",
    }

    if high_emergence and low_operational_risk:
        return StrictnessMode.RELAXED
    return StrictnessMode.STRICT
