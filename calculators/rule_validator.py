"""
Rule Validator Utility

Provides reusable logic for separating DEFINITE from CONDITIONAL rules.
Prevents over-triggering of warnings without sufficient patient context.
"""

from dataclasses import dataclass
from enum import Enum

class RuleType(Enum):
    """Classification of rule applicability."""
    DEFINITE = "definite"          # Always applies; no patient data needed
    CONDITIONAL = "conditional"    # Requires specific patient conditions/labs


class ConditionRequirement:
    """Specifies what patient data is needed to evaluate a rule."""
    
    def __init__(self):
        self.requires_eGFR = False
        self.requires_conditions = []
        self.requires_history = []
        self.requires_labs = []
    
    def is_satisfied(self, patient_data: dict) -> bool:
        """Check if patient_data provides all required information."""
        if self.requires_eGFR and ("eGFR" not in patient_data or patient_data["eGFR"] is None):
            return False
        
        if self.requires_conditions:
            patient_conditions = [c.lower() for c in patient_data.get("conditions", [])]
            required_conds = [c.lower() for c in self.requires_conditions]
            if not any(rc in patient_conditions for rc in required_conds):
                return False
        
        if self.requires_history:
            patient_history = [h.lower() for h in patient_data.get("history", [])]
            required_hist = [h.lower() for h in self.requires_history]
            if not any(rh in patient_history for rh in required_hist):
                return False
        
        return True
    
    def missing_fields(self) -> list[str]:
        """Return list of missing data fields needed to evaluate rule."""
        missing = []
        if self.requires_eGFR:
            missing.append("eGFR (kidney function)")
        if self.requires_conditions:
            missing.append(f"Patient conditions (looking for: {', '.join(self.requires_conditions)})")
        if self.requires_history:
            missing.append(f"Medical history (looking for: {', '.join(self.requires_history)})")
        return missing


@dataclass
class RuleContext:
    """Context for evaluating a single rule against patient data."""
    rule_id: str
    rule_type: RuleType
    patient_data: dict  # {conditions: [...], labs: {...}, history: [...], ...}
    requirement: ConditionRequirement = None
    
    def should_trigger(self) -> bool:
        """Determine if rule should trigger given current patient data."""
        if self.rule_type == RuleType.DEFINITE:
            return True
        
        # CONDITIONAL: only trigger if patient data satisfies requirement
        if self.requirement is None:
            return False
        
        return self.requirement.is_satisfied(self.patient_data)
    
    def get_warning_level(self) -> str:
        """
        Determine warning level:
        - "DEFINITE": rule triggers, show full warning
        - "POSSIBLE": rule might apply if patient data verified
        - "INSUFFICIENT_DATA": need more patient data to evaluate
        """
        if self.rule_type == RuleType.DEFINITE:
            return "DEFINITE"
        
        if self.requirement is None:
            return "INSUFFICIENT_DATA"
        
        if self.requirement.is_satisfied(self.patient_data):
            return "DEFINITE"
        
        # Patient data exists but doesn't match required conditions
        if any(self.patient_data.get(field) for field in ["conditions", "history", "labs"]):
            return "POSSIBLE"
        
        return "INSUFFICIENT_DATA"
    
    def get_message_suffix(self) -> str:
        """Return user-friendly message about missing data."""
        if self.get_warning_level() == "DEFINITE":
            return ""
        
        missing = self.requirement.missing_fields() if self.requirement else []
        if not missing:
            return ""
        
        return f"(Requires: {'; '.join(missing)})"


def build_patient_context(
    conditions: list = None,
    eGFR: int = None,
    medical_history: list = None,
    labs: dict = None
) -> dict:
    """Build a patient data context dict for rule evaluation."""
    return {
        "conditions": [c.lower().strip() for c in (conditions or [])],
        "eGFR": eGFR,
        "history": [h.lower().strip() for h in (medical_history or [])],
        "labs": labs or {},
    }


def requirement_for_renal(threshold_text: str = "CrCl < 30") -> ConditionRequirement:
    """Create requirement for renal-based rules."""
    req = ConditionRequirement()
    req.requires_eGFR = True
    return req


def requirement_for_condition(condition_keywords: list) -> ConditionRequirement:
    """Create requirement for condition-based rules."""
    req = ConditionRequirement()
    req.requires_conditions = condition_keywords
    return req


def requirement_for_history(history_keywords: list) -> ConditionRequirement:
    """Create requirement for history-based rules."""
    req = ConditionRequirement()
    req.requires_history = history_keywords
    return req


def requirement_combined(*requirements: ConditionRequirement) -> ConditionRequirement:
    """Combine multiple requirements (ALL must be satisfied)."""
    combined = ConditionRequirement()
    for req in requirements:
        combined.requires_eGFR = combined.requires_eGFR or req.requires_eGFR
        combined.requires_conditions.extend(req.requires_conditions)
        combined.requires_history.extend(req.requires_history)
    return combined
