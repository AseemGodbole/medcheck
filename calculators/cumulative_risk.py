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
    
    # Opioids - MODERATE/HIGH
    "morphine": "high",
    "oxycodone": "high",
    "fentanyl": "high",
    
    # Sedating antihistamines - MODERATE
    "diphenhydramine": "moderate",
    "hydroxyzine": "moderate",
    
    # Antipsychotics - MODERATE
    "haloperidol": "moderate",
    "quetiapine": "moderate",
    
    # Anticholinergics - MODERATE
    "benztropine": "moderate",
    "trihexyphenidyl": "moderate",
    
    # Sedating antidepressants - MODERATE
    "amitriptyline": "moderate",
    "mirtazapine": "moderate",
    
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
    
    if len(serotonin_drugs) <= 1:
        risk = "LOW"
        urgency = "Minimal"
    elif len(serotonin_drugs) == 2:
        risk = "MODERATE"
        urgency = "Medium"
    else:
        risk = "HIGH"
        urgency = "High"
    
    return {
        "risk_level": risk,
        "urgency": urgency,
        "drugs": serotonin_drugs,
        "message": f"Serotonin syndrome risk from {len(serotonin_drugs)} medication(s): {risk}"
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


def check_all_cumulative_risks(drug_names: list[str]) -> dict:
    """Run all cumulative risk checks."""
    return {
        "bleeding": check_cumulative_bleeding_risk(drug_names),
        "serotonin": check_cumulative_serotonin_risk(drug_names),
        "cns_depression": check_cumulative_cns_depression(drug_names),
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
