"""
Cumulative Risk Detector

Aggregates risk across multiple medications.
Detects high bleeding risk, serotonin syndrome risk, CNS depression, QT prolongation, etc.

This adds a layer beyond pairwise interactions to catch complex polypharmacy risks.
"""

from dataclasses import dataclass, field


@dataclass
class RiskFactor:
    """A medication-related risk factor."""
    risk_type: str           # "bleeding", "serotonin", "cns_depression", "qt_prolongation", "fall_risk", "anticholinergic"
    drug: str
    severity: str            # "high", "moderate", "low"
    mechanism: str


#  Risk Factor Database 

BLEEDING_RISK_DRUGS = {
    # Anticoagulants - HIGH
    "warfarin": ("high", "Direct vitamin K antagonist"),
    "apixaban": ("high", "Direct Factor Xa inhibitor"),
    "rivaroxaban": ("high", "Direct Factor Xa inhibitor"),
    "dabigatran": ("high", "Direct thrombin inhibitor"),
    "edoxaban": ("high", "Direct Factor Xa inhibitor"),
    "enoxaparin": ("high", "Low molecular weight heparin"),
    "heparin": ("high", "Unfractionated heparin"),
    
    # Antiplatelets - HIGH
    "aspirin": ("high", "Platelet aggregation inhibitor"),
    "clopidogrel": ("high", "P2Y12 receptor inhibitor"),
    "ticagrelor": ("high", "P2Y12 receptor inhibitor"),
    "prasugrel": ("high", "P2Y12 receptor inhibitor"),
    
    # NSAIDs - MODERATE
    "ibuprofen": ("moderate", "Inhibits platelet function; GI bleeding risk"),
    "naproxen": ("moderate", "Inhibits platelet function; GI bleeding risk"),
    "diclofenac": ("moderate", "Inhibits platelet function; GI bleeding risk"),
    "meloxicam": ("moderate", "Inhibits platelet function; GI bleeding risk"),
    "celecoxib": ("moderate", "COX-2 inhibitor; GI bleeding risk"),
    "ketorolac": ("moderate", "NSAID; high GI bleeding risk"),
    "indomethacin": ("moderate", "NSAID; GI bleeding risk"),
    
    # SSRIs - LOW (impair platelet aggregation)
    "fluoxetine": ("low", "Inhibits platelet serotonin reuptake"),
    "sertraline": ("low", "Inhibits platelet serotonin reuptake"),
    "paroxetine": ("low", "Inhibits platelet serotonin reuptake"),
    "citalopram": ("low", "Inhibits platelet serotonin reuptake"),
    "escitalopram": ("low", "Inhibits platelet serotonin reuptake"),
    "fluvoxamine": ("low", "Inhibits platelet serotonin reuptake"),
}

SEROTONIN_SYNDROME_DRUGS = {
    # SSRIs
    "fluoxetine": "high",
    "sertraline": "high",
    "paroxetine": "high",
    "citalopram": "high",
    "escitalopram": "high",
    "fluvoxamine": "high",
    
    # SNRIs
    "venlafaxine": "high",
    "duloxetine": "high",
    "desvenlafaxine": "high",
    
    # Tramadol
    "tramadol": "high",
    
    # MAOIs
    "phenelzine": "high",
    "tranylcypromine": "high",
    "isocarboxazid": "high",
    "moclobemide": "high",
    
    # TCAs
    "amitriptyline": "moderate",
    "nortriptyline": "moderate",
    "imipramine": "moderate",
    
    # Other serotonergic
    "trazodone": "moderate",
    "bupropion": "low",  # weak serotonergic effect
}

CNS_DEPRESSION_DRUGS = {
    # Benzodiazepines - HIGH
    "diazepam": "high",
    "lorazepam": "high",
    "alprazolam": "high",
    "clonazepam": "high",
    "temazepam": "high",
    "midazolam": "high",
    "triazolam": "high",
    
    # Opioids - HIGH
    "morphine": "high",
    "oxycodone": "high",
    "fentanyl": "high",
    "hydromorphone": "high",
    "codeine": "high",
    "tramadol": "moderate",
    "methadone": "high",
    
    # Gabapentinoids - MODERATE
    "gabapentin": "moderate",
    "pregabalin": "moderate",
    
    # Sedating antihistamines - MODERATE
    "diphenhydramine": "moderate",
    "doxylamine": "moderate",
    "hydroxyzine": "moderate",
    
    # Antipsychotics - MODERATE
    "quetiapine": "moderate",
    "olanzapine": "moderate",
    "haloperidol": "moderate",
    
    # TCAs - MODERATE
    "amitriptyline": "moderate",
    "nortriptyline": "moderate",
    
    # Z-drugs - HIGH
    "zolpidem": "high",
    "zaleplon": "high",
    "eszopiclone": "high",
    "zopiclone": "high",
}

QT_PROLONGATION_DRUGS = {
    "amiodarone": "high",
    "azithromycin": "moderate",
    "clarithromycin": "moderate",
    "erythromycin": "moderate",
    "haloperidol": "moderate",
    "quetiapine": "moderate",
    "ziprasidone": "high",
    "domperidone": "moderate",
    "metoclopramide": "low",
    "citalopram": "moderate",  # dose-dependent
    "fluconazole": "low",
    "methadone": "high",
}

FALL_RISK_DRUGS = {
    # Benzodiazepines - HIGH
    "diazepam": "high",
    "lorazepam": "high",
    "alprazolam": "high",
    "clonazepam": "high",
    "temazepam": "high",
    "nitrazepam": "high",
    "oxazepam": "high",

    # Z-drugs - HIGH
    "zolpidem": "high",
    "zaleplon": "high",
    "eszopiclone": "high",
    "zopiclone": "high",

    # Opioids - HIGH
    "morphine": "high",
    "oxycodone": "high",
    "fentanyl": "high",
    "hydromorphone": "high",
    "codeine": "moderate",
    "tramadol": "moderate",

    # Gabapentinoids - MODERATE
    "gabapentin": "moderate",
    "pregabalin": "moderate",

    # Sedating antihistamines - MODERATE
    "diphenhydramine": "moderate",
    "hydroxyzine": "moderate",

    # Antipsychotics - MODERATE
    "haloperidol": "moderate",
    "quetiapine": "moderate",
    "olanzapine": "moderate",

    # Anticholinergics - MODERATE
    "benztropine": "moderate",
    "trihexyphenidyl": "moderate",

    # Sedating antidepressants - MODERATE
    "amitriptyline": "moderate",
    "mirtazapine": "moderate",
    "nortriptyline": "moderate",

    # Alpha-blockers - MODERATE (orthostatic hypotension)
    "doxazosin": "moderate",
    "terazosin": "moderate",
    "prazosin": "moderate",
}


def normalize(name: str) -> str:
    """Normalize drug name for matching."""
    return name.strip().lower()


def check_cumulative_bleeding_risk(drug_names: list[str]) -> dict:
    """Assess cumulative bleeding risk from drug combination."""
    drugs_normalized = [normalize(d) for d in drug_names]
    
    bleeding_drugs = []
    high_count = 0
    moderate_count = 0
    low_count = 0
    
    for drug in drugs_normalized:
        for risk_drug, (severity, mechanism) in BLEEDING_RISK_DRUGS.items():
            if drug == risk_drug or drug in risk_drug or risk_drug in drug:
                bleeding_drugs.append({
                    "drug": drug,
                    "severity": severity,
                    "mechanism": mechanism
                })
                
                if severity == "high":
                    high_count += 1
                elif severity == "moderate":
                    moderate_count += 1
                else:
                    low_count += 1
                break
    
    # Determine cumulative risk level
    if high_count >= 2:
        cumulative_risk = "VERY HIGH"
        urgency = "Critical"
    elif high_count == 1 and moderate_count >= 2:
        cumulative_risk = "VERY HIGH"
        urgency = "Critical"
    elif high_count == 1 and moderate_count >= 1:
        cumulative_risk = "HIGH"
        urgency = "High"
    elif high_count == 1 or (moderate_count >= 2):
        cumulative_risk = "MODERATE-HIGH"
        urgency = "Medium"
    elif moderate_count >= 1 or low_count >= 2:
        cumulative_risk = "MODERATE"
        urgency = "Low"
    else:
        cumulative_risk = "LOW"
        urgency = "Minimal"
    
    return {
        "risk_level": cumulative_risk,
        "urgency": urgency,
        "high_count": high_count,
        "moderate_count": moderate_count,
        "low_count": low_count,
        "drugs": bleeding_drugs,
        "message": f"Cumulative bleeding risk from {len(bleeding_drugs)} medication(s): {cumulative_risk}"
    }


def check_cumulative_serotonin_risk(drug_names: list[str]) -> dict:
    """Assess cumulative serotonin syndrome risk."""
    drugs_normalized = [normalize(d) for d in drug_names]

    serotonin_drugs = []

    for drug in drugs_normalized:
        for risk_drug, severity in SEROTONIN_SYNDROME_DRUGS.items():
            if drug == risk_drug or drug in risk_drug or risk_drug in drug:
                serotonin_drugs.append({"drug": drug, "severity": severity})
                break

    high_count = sum(1 for d in serotonin_drugs if d["severity"] == "high")
    n = len(serotonin_drugs)

    if n <= 1:
        risk = "LOW"
        urgency = "Minimal"
    elif high_count >= 3:
        risk = "VERY HIGH"
        urgency = "Critical"
    elif high_count >= 2:
        risk = "HIGH"
        urgency = "High"
    elif n >= 3:
        risk = "HIGH"
        urgency = "High"
    else:
        risk = "MODERATE"
        urgency = "Medium"

    return {
        "risk_level": risk,
        "urgency": urgency,
        "drugs": serotonin_drugs,
        "message": f"Serotonin syndrome risk from {n} medication(s): {risk}"
    }


def check_cumulative_cns_depression(drug_names: list[str]) -> dict:
    """Assess cumulative CNS depression risk."""
    drugs_normalized = [normalize(d) for d in drug_names]
    
    cns_drugs = []
    high_count = 0
    
    for drug in drugs_normalized:
        for risk_drug, severity in CNS_DEPRESSION_DRUGS.items():
            if drug == risk_drug or drug in risk_drug or risk_drug in drug:
                cns_drugs.append({"drug": drug, "severity": severity})
                if severity == "high":
                    high_count += 1
                break
    
    if len(cns_drugs) <= 1:
        risk = "LOW"
    elif high_count >= 2:
        risk = "VERY HIGH"
    elif len(cns_drugs) >= 3:
        risk = "HIGH"
    elif len(cns_drugs) == 2:
        risk = "MODERATE"
    else:
        risk = "LOW"
    
    return {
        "risk_level": risk,
        "drugs": cns_drugs,
        "message": f"CNS depression risk from {len(cns_drugs)} medication(s): {risk}"
    }


# ── Drug class sets for multi-drug cluster detection ──────────────────────────

_ACE_ARB = {
    "lisinopril", "zestril", "ramipril", "altace", "enalapril", "vasotec",
    "perindopril", "captopril", "trandolapril", "quinapril", "fosinopril", "benazepril",
    "losartan", "cozaar", "valsartan", "diovan", "irbesartan", "avapro",
    "candesartan", "olmesartan", "telmisartan", "eprosartan", "azilsartan",
    "ace inhibitor", "ace-i", "arb", "angiotensin",
}

_DIURETIC = {
    "furosemide", "frusemide", "lasix", "bumetanide", "torasemide",
    "hydrochlorothiazide", "hctz", "bendroflumethiazide", "chlortalidone", "indapamide",
    "spironolactone", "aldactone", "amiloride", "triamterene", "eplerenone",
    "loop diuretic", "thiazide", "diuretic",
}

_NSAID = {
    "ibuprofen", "advil", "motrin", "naproxen", "aleve", "naprosyn",
    "diclofenac", "voltaren", "indomethacin", "indocin", "celecoxib", "celebrex",
    "meloxicam", "mobic", "etoricoxib", "ketorolac", "toradol", "piroxicam", "sulindac",
    "nsaid",
}

_QT_HIGH = {"amiodarone", "cordarone", "methadone", "ziprasidone", "geodon"}
_QT_MODERATE = {
    "azithromycin", "zithromax", "clarithromycin", "biaxin", "erythromycin",
    "haloperidol", "haldol", "quetiapine", "seroquel", "domperidone", "motilium",
    "metoclopramide", "reglan", "citalopram", "celexa", "fluconazole", "diflucan",
    "ondansetron", "zofran",
}

# ── Drug class membership for therapeutic overlap detection ───────────────────

SEDATING_CLASSES = {
    "Benzodiazepine": {
        "diazepam", "lorazepam", "alprazolam", "clonazepam", "temazepam",
        "midazolam", "triazolam", "nitrazepam", "oxazepam", "chlordiazepoxide",
    },
    "Z-drug": {
        "zolpidem", "zaleplon", "eszopiclone", "zopiclone",
    },
    "Sedating antihistamine": {
        "diphenhydramine", "doxylamine", "hydroxyzine", "promethazine", "chlorphenamine",
    },
    "Opioid": {
        "morphine", "oxycodone", "fentanyl", "hydromorphone", "codeine",
        "tramadol", "methadone", "hydrocodone", "buprenorphine", "pethidine",
    },
    "Sedating antipsychotic": {
        "quetiapine", "olanzapine", "haloperidol", "chlorpromazine", "clozapine", "risperidone",
    },
    "Sedating antidepressant": {
        "amitriptyline", "nortriptyline", "doxepin", "trimipramine", "mirtazapine",
    },
    "Gabapentinoid": {
        "gabapentin", "pregabalin",
    },
    "Muscle relaxant": {
        "baclofen", "cyclobenzaprine", "carisoprodol", "methocarbamol",
    },
}

ANTICHOLINERGIC_CLASSES = {
    "Bladder anticholinergic": {
        "oxybutynin", "tolterodine", "solifenacin", "darifenacin", "trospium", "fesoterodine",
    },
    "Sedating antihistamine": {
        "diphenhydramine", "doxylamine", "hydroxyzine", "promethazine", "chlorphenamine",
    },
    "Antidepressant": {
        "amitriptyline", "nortriptyline", "doxepin", "trimipramine", "paroxetine",
    },
    "Antipsychotic": {
        "clozapine", "olanzapine", "chlorpromazine",
    },
    "Antispasmodic": {
        "dicyclomine", "hyoscine", "scopolamine",
    },
    "Antiparkinsonian": {
        "benztropine", "trihexyphenidyl", "procyclidine",
    },
}

SEROTONERGIC_CLASSES = {
    "SSRI": {
        "fluoxetine", "sertraline", "paroxetine", "citalopram", "escitalopram", "fluvoxamine",
    },
    "SNRI": {
        "venlafaxine", "duloxetine", "desvenlafaxine", "milnacipran",
    },
    "Opioid (serotonergic)": {
        "tramadol", "meperidine", "pethidine",
    },
    "MAOI": {
        "phenelzine", "tranylcypromine", "isocarboxazid", "moclobemide",
    },
    "TCA": {
        "amitriptyline", "nortriptyline", "imipramine", "clomipramine",
    },
    "Other serotonergic": {
        "trazodone", "buspirone", "lithium", "linezolid", "dextromethorphan",
    },
}


def _drug_in_class(drug_name: str, class_set: set) -> bool:
    """Check if a normalized drug name belongs to a drug class set."""
    for cls in class_set:
        if drug_name == cls or drug_name in cls or cls in drug_name:
            return True
    return False


def check_triple_whammy(drug_names: list[str]) -> dict:
    """
    Detect the 'Triple Whammy' combination: ACE/ARB + diuretic + NSAID.
    This combination acutely reduces renal perfusion and can precipitate AKI.
    """
    drugs_normalized = [normalize(d) for d in drug_names]
    found_ace_arb  = [d for d in drugs_normalized if _drug_in_class(d, _ACE_ARB)]
    found_diuretic = [d for d in drugs_normalized if _drug_in_class(d, _DIURETIC)]
    found_nsaid    = [d for d in drugs_normalized if _drug_in_class(d, _NSAID)]

    if found_ace_arb and found_diuretic and found_nsaid:
        return {
            "detected": True,
            "risk_level": "VERY HIGH",
            "drugs": {
                "ace_arb":   found_ace_arb,
                "diuretic":  found_diuretic,
                "nsaid":     found_nsaid,
            },
            "message": (
                "Triple Whammy: ACE/ARB + diuretic + NSAID combination detected. "
                "Significantly increases risk of acute kidney injury (AKI) through "
                "combined haemodynamic effects on glomerular filtration."
            ),
        }
    return {"detected": False, "risk_level": "LOW", "drugs": {}, "message": ""}


def check_qt_prolongation_risk(drug_names: list[str]) -> dict:
    """Assess QT prolongation and Torsades de Pointes risk from drug combination."""
    drugs_normalized = [normalize(d) for d in drug_names]
    qt_drugs = []
    high_count = 0

    for drug in drugs_normalized:
        if any(drug == d or drug in d or d in drug for d in _QT_HIGH):
            qt_drugs.append({"drug": drug, "severity": "high"})
            high_count += 1
        elif any(drug == d or drug in d or d in drug for d in _QT_MODERATE):
            qt_drugs.append({"drug": drug, "severity": "moderate"})

    n = len(qt_drugs)
    if n == 0:
        risk = "LOW"
    elif high_count >= 2 or n >= 3:
        risk = "VERY HIGH"
    elif high_count == 1 or n == 2:
        risk = "HIGH"
    else:
        risk = "MODERATE"

    return {
        "risk_level": risk,
        "drugs": qt_drugs,
        "message": f"QT prolongation risk from {n} medication(s): {risk}",
    }


def check_renal_risk(drug_names: list[str], patient_conditions: list[str] = None) -> dict:
    """
    Assess renal injury risk. Elevated in CKD patients or Triple Whammy combinations.
    """
    drugs_normalized  = [normalize(d) for d in drug_names]
    conditions_lower  = [c.strip().lower() for c in (patient_conditions or [])]
    has_ckd = any(
        any(kw in c for kw in ("ckd", "chronic kidney", "renal failure", "renal disease",
                               "kidney disease", "kidney failure", "egfr", "nephropathy"))
        for c in conditions_lower
    )
    triple_whammy = check_triple_whammy(drug_names)

    renal_drugs = []
    for drug in drugs_normalized:
        if _drug_in_class(drug, _NSAID):
            sev = "high" if has_ckd else "moderate"
            renal_drugs.append({
                "drug": drug,
                "severity": sev,
                "mechanism": "Inhibits prostaglandin-mediated afferent arteriolar dilation; reduces GFR",
            })
        elif _drug_in_class(drug, _ACE_ARB) and has_ckd:
            renal_drugs.append({
                "drug": drug,
                "severity": "moderate",
                "mechanism": "Reduces efferent arteriolar tone; monitor potassium and creatinine in CKD",
            })

    if triple_whammy["detected"]:
        risk = "VERY HIGH"
    elif has_ckd and any(d["severity"] == "high" for d in renal_drugs):
        risk = "HIGH"
    elif renal_drugs:
        risk = "MODERATE"
    else:
        risk = "LOW"

    return {
        "risk_level": risk,
        "triple_whammy": triple_whammy["detected"],
        "ckd_context": has_ckd,
        "drugs": renal_drugs,
        "message": f"Renal injury risk: {risk}",
    }


def _drug_in_set(drug: str, drug_set: set) -> bool:
    """Check if a drug name matches any member of a set (substring match)."""
    for member in drug_set:
        if drug == member or drug in member or member in drug:
            return True
    return False


def check_fall_risk(drug_names: list[str]) -> dict:
    """Assess cumulative falls risk from drug combination."""
    drugs_normalized = [normalize(d) for d in drug_names]
    fall_drugs = []
    high_count = 0

    for drug in drugs_normalized:
        for risk_drug, severity in FALL_RISK_DRUGS.items():
            if drug == risk_drug or drug in risk_drug or risk_drug in drug:
                fall_drugs.append({"drug": drug, "severity": severity})
                if severity == "high":
                    high_count += 1
                break

    n = len(fall_drugs)
    if n <= 1:
        risk = "LOW"
    elif high_count >= 2:
        risk = "VERY HIGH"
    elif n >= 3:
        risk = "HIGH"
    elif n == 2:
        risk = "MODERATE"
    else:
        risk = "LOW"

    return {
        "risk_level": risk,
        "drugs": fall_drugs,
        "message": f"Falls risk from {n} medication(s): {risk}",
    }


def check_therapeutic_overlaps(drug_names: list[str]) -> list:
    """
    Detect pharmacological overlaps across drug classes (different classes, shared effect).
    Only flags when drugs come from 2+ distinct drug classes with the same pharmacological property.
    """
    drugs_normalized = [normalize(d) for d in drug_names]
    overlaps = []

    # Sedating burden — drugs from 2+ different sedating drug classes
    sedating_hits = {}
    for drug in drugs_normalized:
        for cls_label, members in SEDATING_CLASSES.items():
            if _drug_in_set(drug, members):
                sedating_hits[drug] = cls_label
                break
    unique_sed_classes = set(sedating_hits.values())
    if len(unique_sed_classes) >= 2 and len(sedating_hits) >= 2:
        n = len(sedating_hits)
        risk = "VERY HIGH" if n >= 4 else ("HIGH" if n >= 3 else "MODERATE")
        overlaps.append({
            "overlap_type": "sedating_burden",
            "label": "Sedating Medication Burden",
            "risk_level": risk,
            "drugs": [{"drug": d, "class": sedating_hits[d]} for d in sedating_hits],
            "drug_count": n,
            "risks": ["Falls", "Delirium", "Cognitive impairment", "Respiratory depression"],
            "description": (
                f"{n} CNS-depressing medications from {len(unique_sed_classes)} different drug classes. "
                "Combined sedative effect is additive."
            ),
        })

    # Anticholinergic overlap — 2+ drugs from different anticholinergic classes
    ach_hits = {}
    for drug in drugs_normalized:
        for cls_label, members in ANTICHOLINERGIC_CLASSES.items():
            if _drug_in_set(drug, members):
                ach_hits[drug] = cls_label
                break
    unique_ach_classes = set(ach_hits.values())
    if len(unique_ach_classes) >= 2:
        n = len(ach_hits)
        risk = "HIGH" if n >= 3 else "MODERATE"
        overlaps.append({
            "overlap_type": "anticholinergic_overlap",
            "label": "Anticholinergic Medication Overlap",
            "risk_level": risk,
            "drugs": [{"drug": d, "class": ach_hits[d]} for d in ach_hits],
            "drug_count": n,
            "risks": ["Confusion", "Urinary retention", "Constipation", "Falls"],
            "description": (
                f"{n} medications with anticholinergic properties from "
                f"{len(unique_ach_classes)} different drug classes."
            ),
        })

    # Serotonergic overlap — 2+ drugs from different serotonergic classes
    sero_hits = {}
    for drug in drugs_normalized:
        for cls_label, members in SEROTONERGIC_CLASSES.items():
            if _drug_in_set(drug, members):
                sero_hits[drug] = cls_label
                break
    unique_sero_classes = set(sero_hits.values())
    if len(unique_sero_classes) >= 2 and len(sero_hits) >= 2:
        n = len(sero_hits)
        risk = "VERY HIGH" if n >= 3 else "HIGH"
        overlaps.append({
            "overlap_type": "serotonergic_overlap",
            "label": "Serotonergic Medication Overlap",
            "risk_level": risk,
            "drugs": [{"drug": d, "class": sero_hits[d]} for d in sero_hits],
            "drug_count": n,
            "risks": ["Serotonin syndrome", "Agitation", "Hyperthermia", "Seizures"],
            "description": (
                f"{n} serotonergic agents from {len(unique_sero_classes)} different drug classes."
            ),
        })

    # QT-prolonging overlap — 2+ QT drugs
    qt_hits = {}
    for drug in drugs_normalized:
        if _drug_in_set(drug, _QT_HIGH):
            qt_hits[drug] = "High-risk QT"
        elif _drug_in_set(drug, _QT_MODERATE):
            qt_hits[drug] = "Moderate-risk QT"
    if len(qt_hits) >= 2:
        n = len(qt_hits)
        high_count = sum(1 for v in qt_hits.values() if v == "High-risk QT")
        risk = "VERY HIGH" if (high_count >= 2 or n >= 3) else "HIGH"
        overlaps.append({
            "overlap_type": "qt_overlap",
            "label": "QT-Prolonging Medication Overlap",
            "risk_level": risk,
            "drugs": [{"drug": d, "class": qt_hits[d]} for d in qt_hits],
            "drug_count": n,
            "risks": ["QT prolongation", "Torsades de Pointes", "Cardiac arrest"],
            "description": f"{n} QT-prolonging medications detected — combined risk is additive.",
        })

    return overlaps


def check_all_cumulative_risks(drug_names: list[str], patient_conditions: list[str] = None) -> dict:
    """Run all cumulative risk checks."""
    return {
        "bleeding":      check_cumulative_bleeding_risk(drug_names),
        "serotonin":     check_cumulative_serotonin_risk(drug_names),
        "cns_depression":check_cumulative_cns_depression(drug_names),
        "qt":            check_qt_prolongation_risk(drug_names),
        "renal":         check_renal_risk(drug_names, patient_conditions),
        "triple_whammy": check_triple_whammy(drug_names),
        "falls":         check_fall_risk(drug_names),
        "overlaps":      check_therapeutic_overlaps(drug_names),
    }


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        drugs = sys.argv[1:]
    else:
        print("Cumulative Risk Detector")
        raw = input("Enter drug names (comma-separated): ")
        drugs = [d.strip() for d in raw.split(",") if d.strip()]
    
    if drugs:
        risks = check_all_cumulative_risks(drugs)
        
        print("\n" + "=" * 70)
        print("  CUMULATIVE RISK ASSESSMENT")
        print("=" * 70)
        
        for risk_type, result in risks.items():
            print(f"\n  {risk_type.upper()}: {result['message']}")
            for drug_info in result["drugs"]:
                print(f"    - {drug_info['drug']} ({drug_info['severity']})")
        
        print("\n" + "=" * 70 + "\n")
