"""
Local ACB (Anticholinergic Burden) calculator module.

Simple, offline scoring engine with a minimal drug->score map and
helper functions to compute ACB score for a list of medications.

Usage:
    from calculators.acb_local import compute_acb
    result = compute_acb(["paracetamol", "ibuprofen", "amitriptyline"])

    # CLI
    python calculators/acb_local.py "paracetamol, ibuprofen"

This is intentionally small and easy to extend with a fuller drug database
or to map brand names to generics.
"""
from typing import List, Dict
import re

# Minimal example mapping. Extend this mapping with authoritative sources.
DEFAULT_ACB_SCORES = {
    "amitriptyline": 3,
    "oxybutynin": 3,
    "doxepin": 3,
    "chlorpromazine": 2,
    "olanzapine": 2,
    "chlorpheniramine": 1,
    "promethazine": 1,
    "trazodone": 1,
    "diphenhydramine": 1,
    "paracetamol": 0,
    "acetaminophen": 0,
    "ibuprofen": 0,
    "aspirin": 0,
}

# Simple brand -> generic aliases (add as needed)
BRAND_ALIASES = {
    "tylenol": "acetaminophen",
    "panadol": "paracetamol",
    "benadryl": "diphenhydramine",
}

_normalize_re = re.compile(r"[^a-z0-9]+")

def normalize_name(name: str) -> str:
    s = name.lower().strip()
    s = _normalize_re.sub(" ", s).strip()
    # map brand to generic
    if s in BRAND_ALIASES:
        return BRAND_ALIASES[s]
    return s


def compute_acb(drugs: List[str]) -> Dict:
    """Compute the ACB score for a list of drug names.

    Returns a dict with `total` score and `details` list.
    Each detail contains `input`, `normalized`, and `score`.
    """
    details = []
    total = 0
    for raw in drugs:
        norm = normalize_name(raw)
        score = DEFAULT_ACB_SCORES.get(norm, 0)
        details.append({"input": raw, "normalized": norm, "score": score})
        total += score
    return {"total": total, "details": details}


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python calculators/acb_local.py \"drug1, drug2\"")
        sys.exit(1)
    raw = sys.argv[1]
    meds = [m.strip() for m in raw.split(",") if m.strip()]
    out = compute_acb(meds)
    print(f"Total ACB score: {out['total']}")
    for d in out["details"]:
        print(f"- {d['input']} -> {d['normalized']}: {d['score']}")
