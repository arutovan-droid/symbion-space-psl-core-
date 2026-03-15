from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from src.models.strictness import StrictnessContext, StrictnessMode, resolve_strictness


@dataclass
class ValidationIssue:
    rule: str
    level: str
    message: str


class LRuleValidator:
    """L-rules validator with ONTO/RESONANCE support and dynamic strictness."""

    ORDER = [
        "FACT",
        "TECHNIQUE",
        "HYP",
        "ONTO",
        "RESONANCE",
        "ROLLBACK",
        "SAFETY",
        "ASSUMPTIONS",
        "CHECKLIST",
        "3C",
        "GLOSS",
    ]

    def __init__(self):
        self.issues: List[Dict[str, str]] = []

    def validate(
        self,
        document: Any,
        strictness_ctx: Optional[StrictnessContext] = None,
    ) -> List[Dict[str, str]]:
        self.issues = []
        mode = resolve_strictness(strictness_ctx or StrictnessContext())

        self._validate_l01_section_order(document)
        self._validate_l02_hyp_rollback_pairing(document, mode)
        self._validate_l11_onto_resonance_legality(document, mode)

        return self.issues

    def _validate_l01_section_order(self, doc: Any):
        """L-01: section ordering with ONTO/RESONANCE support."""
        actual_sections = [s for s in doc.sections.keys() if s in self.ORDER]
        expected_actual = [s for s in self.ORDER if s in actual_sections]

        if actual_sections != expected_actual:
            self.issues.append({
                "rule": "L-01",
                "level": "error",
                "message": f"Section order violation. Expected: {expected_actual}, Got: {actual_sections}",
            })

    def _validate_l02_hyp_rollback_pairing(self, doc: Any, mode: StrictnessMode):
        """L-02: HYP requires ROLLBACK in strict mode."""
        hyp_count = len(doc.sections.get("HYP", []))
        rollback_count = len(doc.sections.get("ROLLBACK", []))

        if mode == StrictnessMode.STRICT and hyp_count > 0 and rollback_count == 0:
            self.issues.append({
                "rule": "L-02",
                "level": "error",
                "message": "HYP requires ROLLBACK in strict mode.",
            })

    def _validate_l11_onto_resonance_legality(self, doc: Any, mode: StrictnessMode):
        """L-11: ONTO/RESONANCE are legal sections; in strict mode they should coexist with SAFETY."""
        has_onto = "ONTO" in doc.sections and len(doc.sections.get("ONTO", [])) > 0
        has_resonance = "RESONANCE" in doc.sections and len(doc.sections.get("RESONANCE", [])) > 0
        has_safety = "SAFETY" in doc.sections and len(doc.sections.get("SAFETY", [])) > 0

        if (has_onto or has_resonance) and mode == StrictnessMode.STRICT and not has_safety:
            self.issues.append({
                "rule": "L-11",
                "level": "warning",
                "message": "ONTO/RESONANCE present without SAFETY in strict mode.",
            })
