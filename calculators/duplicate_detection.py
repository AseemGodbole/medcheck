"""
Duplicate Therapy Detector

Identifies drugs that belong to the same therapeutic class.
Warns about duplicate anticoagulants, antiplatelet agents, NSAIDs, benzos, SSRIs, etc.

This is a DEFINITE rule - no patient context needed.
"""

from dataclasses import dataclass


@dataclass
class TherapeuticClass:
    """Definition of a therapeutic drug class."""
    class_name: str              # e.g. "Anticoagulant"
    class_type: str              # "anticoagulant", "nsaid", "benzo", etc.
    members: list[str]           # drug names (lowercase)
    risk_level: str              # "CONTRAINDICATED", "SERIOUS", "MODERATE", "MONITOR"
    warning_text: str            # user-friendly warning


#  Therapeutic Classes Database 

THERAPEUTIC_CLASSES = [
    TherapeuticClass(
        class_name="Anticoagulants",
        class_type="anticoagulant",
        members=[
            "warfarin", "coumadin", "jantoven",
            "apixaban", "eliquis",
            "rivaroxaban", "xarelto",
            "dabigatran", "pradaxa",
            "edoxaban", "savaysa",
            "enoxaparin", "lovenox", "enoxaparine",
            "heparin", "dalteparin", "fragmin", "tinzaparin", "innohep"
        ],
        risk_level="CONTRAINDICATED",
        warning_text="Duplicate anticoagulants may cause serious bleeding. Review indication and discontinue one if not medically necessary."
    ),
    
    TherapeuticClass(
        class_name="Antiplatelet Agents",
        class_type="antiplatelet",
        members=[
            "aspirin", "acetylsalicylic acid", "asa",
            "clopidogrel", "plavix",
            "ticagrelor", "brilinta",
            "prasugrel", "effient",
            "ticlopidine", "ticlid"
        ],
        risk_level="SERIOUS",
        warning_text="Duplicate antiplatelet agents increase bleeding risk. Confirm dual therapy is indicated."
    ),
    
    TherapeuticClass(
        class_name="NSAIDs",
        class_type="nsaid",
        members=[
            "ibuprofen", "advil", "motrin", "midol",
            "naproxen", "aleve", "naprosyn", "naproxen sodium",
            "diclofenac", "voltaren",
            "meloxicam", "mobic",
            "celecoxib", "celebrex",
            "indomethacin", "indocin",
            "ketorolac", "toradol",
            "piroxicam", "feldene",
            "etoricoxib", "arcoxia",
            "flurbiprofen", "ansaid",
            "nabumetone", "relafen",
            "ketoprofen", "orudis"
        ],
        risk_level="SERIOUS",
        warning_text="Duplicate NSAIDs increase risk of GI bleeding, ulcers, and kidney damage. Use only one NSAID."
    ),
    
    TherapeuticClass(
        class_name="Benzodiazepines",
        class_type="benzodiazepine",
        members=[
            "diazepam", "valium",
            "lorazepam", "ativan",
            "alprazolam", "xanax",
            "clonazepam", "klonopin", "clonopin",
            "temazepam", "restoril",
            "oxazepam", "serax",
            "midazolam", "versed",
            "flurazepam", "dalmane",
            "estazolam", "prosom",
            "triazolam", "halcion",
            "chlordiazepoxide", "librium"
        ],
        risk_level="SERIOUS",
        warning_text="Duplicate benzodiazepines increase risk of over-sedation, falls, and respiratory depression. Use only one."
    ),
    
    TherapeuticClass(
        class_name="SSRIs",
        class_type="ssri",
        members=[
            "fluoxetine", "prozac", "sarafem",
            "sertraline", "zoloft",
            "paroxetine", "paxil", "pexeva",
            "citalopram", "celexa",
            "escitalopram", "lexapro",
            "fluvoxamine", "luvox"
        ],
        risk_level="SERIOUS",
        warning_text="Duplicate SSRIs increase risk of serotonin syndrome and other adverse effects. Use only one SSRI."
    ),
    
    TherapeuticClass(
        class_name="SNRIs",
        class_type="snri",
        members=[
            "venlafaxine", "effexor", "effexor xr",
            "duloxetine", "cymbalta",
            "desvenlafaxine", "pristiq",
            "levomilnacipran", "fetzima",
            "milnacipran", "savella"
        ],
        risk_level="SERIOUS",
        warning_text="Duplicate SNRIs increase risk of serotonin syndrome. Use only one SNRI."
    ),
    
    TherapeuticClass(
        class_name="ACE Inhibitors",
        class_type="ace_inhibitor",
        members=[
            "lisinopril", "zestril", "prinivil",
            "enalapril", "vasotec",
            "ramipril", "altace",
            "perindopril", "aceon",
            "captopril", "capoten",
            "benazepril", "lotensin",
            "trandolapril", "mavik",
            "quinapril", "accupril",
            "moexipril", "univasc",
            "fosinopril", "monopril"
        ],
        risk_level="SERIOUS",
        warning_text="Duplicate ACE inhibitors are not indicated. Use only one ACE inhibitor."
    ),
    
    TherapeuticClass(
        class_name="Angiotensin II Receptor Blockers (ARBs)",
        class_type="arb",
        members=[
            "losartan", "cozaar",
            "valsartan", "diovan",
            "irbesartan", "avapro",
            "candesartan", "atacand",
            "telmisartan", "micardis",
            "olmesartan", "benicar",
            "azilsartan", "edarbi",
            "eprosartan", "teveten"
        ],
        risk_level="SERIOUS",
        warning_text="Duplicate ARBs are not indicated. Use only one ARB."
    ),
    
    TherapeuticClass(
        class_name="Beta-Blockers",
        class_type="beta_blocker",
        members=[
            "metoprolol", "lopressor", "toprol",
            "atenolol", "tenormin",
            "bisoprolol", "zebeta",
            "carvedilol", "coreg",
            "labetalol", "trandate",
            "propranolol", "inderal",
            "nadolol", "corgard",
            "pindolol", "visken",
            "acebutolol", "sectral",
            "betaxolol", "kerlone",
            "esmolol", "brevibloc",
            "penbutolol", "levatol",
            "nebivolol", "bystolic"
        ],
        risk_level="MODERATE",
        warning_text="Duplicate beta-blockers are not indicated. Use only one beta-blocker."
    ),
    
    TherapeuticClass(
        class_name="Calcium Channel Blockers",
        class_type="ccb",
        members=[
            "amlodipine", "norvasc",
            "nifedipine", "procardia", "adalat",
            "diltiazem", "cardizem", "tiazac",
            "verapamil", "calan", "isoptin", "verelan",
            "felodipine", "plendil",
            "isradipine", "dynacirc",
            "lercanidipine", "zanidip",
            "nicardipine", "cardene"
        ],
        risk_level="MODERATE",
        warning_text="Duplicate calcium channel blockers are not indicated. Use only one CCB."
    ),
    
    TherapeuticClass(
        class_name="Diuretics (Loop)",
        class_type="loop_diuretic",
        members=[
            "furosemide", "lasix", "frusemide",
            "bumetanide", "bumex",
            "torasemide", "demadex",
            "ethacrynic acid", "edacrin"
        ],
        risk_level="MODERATE",
        warning_text="Duplicate loop diuretics are not indicated. Use only one loop diuretic."
    ),
    
    TherapeuticClass(
        class_name="Thiazide Diuretics",
        class_type="thiazide_diuretic",
        members=[
            "hydrochlorothiazide", "hctz", "microzide", "esidrix",
            "chlorthalidone", "thalitone",
            "indapamide", "lozol",
            "metolazone", "zaroxolyn",
            "bendroflumethiazide", "naturetin"
        ],
        risk_level="MODERATE",
        warning_text="Duplicate thiazide diuretics are not indicated. Use only one thiazide."
    ),
    
    TherapeuticClass(
        class_name="Statins",
        class_type="statin",
        members=[
            "atorvastatin", "lipitor",
            "simvastatin", "zocor",
            "rosuvastatin", "crestor",
            "pravastatin", "pravachol",
            "lovastatin", "mevacor",
            "fluvastatin", "lescol",
            "pitavastatin", "livalo"
        ],
        risk_level="MODERATE",
        warning_text="Duplicate statins are not indicated. Use only one statin."
    ),
    
    TherapeuticClass(
        class_name="Proton Pump Inhibitors (PPIs)",
        class_type="ppi",
        members=[
            "omeprazole", "prilosec",
            "esomeprazole", "nexium",
            "lansoprazole", "prevacid",
            "pantoprazole", "protonix",
            "rabeprazole", "aciphex",
            "dexlansoprazole", "dexilant"
        ],
        risk_level="MONITOR",
        warning_text="Duplicate PPIs are not indicated. Long-term use of multiple PPIs increases risk of deficiencies and infections."
    ),
]


def normalize_drug_name(name: str) -> str:
    """Normalize drug name for matching."""
    return name.strip().lower()


def find_therapeutic_class(drug_name: str) -> TherapeuticClass:
    """Find which therapeutic class a drug belongs to (if any)."""
    normalized = normalize_drug_name(drug_name)
    
    for tc in THERAPEUTIC_CLASSES:
        for member in tc.members:
            if normalized == member or normalized in member or member in normalized:
                return tc
    
    return None


def check_duplicates(drug_names: list[str]) -> dict:
    """
    Check for duplicate therapeutic classes.
    
    Returns:
        {
            "duplicates": [
                {
                    "class_name": "Anticoagulants",
                    "drugs": ["warfarin", "apixaban"],
                    "risk_level": "CONTRAINDICATED",
                    "warning": "..."
                }
            ],
            "total_checked": N,
            "duplicates_found": N
        }
    """
    
    # Map each drug to its therapeutic class
    drug_to_class = {}
    for drug in drug_names:
        tc = find_therapeutic_class(drug)
        if tc:
            if tc.class_type not in drug_to_class:
                drug_to_class[tc.class_type] = {
                    "class_name": tc.class_name,
                    "drugs": [],
                    "risk_level": tc.risk_level,
                    "warning": tc.warning_text
                }
            drug_to_class[tc.class_type]["drugs"].append(drug)
    
    # Find duplicates (class with >1 drug)
    duplicates = [
        info for info in drug_to_class.values()
        if len(info["drugs"]) > 1
    ]
    
    # Sort by risk level
    risk_order = {"CONTRAINDICATED": 0, "SERIOUS": 1, "MODERATE": 2, "MONITOR": 3}
    duplicates.sort(key=lambda x: risk_order.get(x["risk_level"], 99))
    
    return {
        "duplicates": duplicates,
        "total_checked": len(drug_names),
        "duplicates_found": len(duplicates),
    }


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        drugs = sys.argv[1:]
    else:
        print("Duplicate Therapy Detector")
        raw = input("Enter drug names (comma-separated): ")
        drugs = [d.strip() for d in raw.split(",") if d.strip()]
    
    if drugs:
        result = check_duplicates(drugs)
        
        print("\n" + "=" * 70)
        print("  DUPLICATE THERAPEUTIC CLASS DETECTION")
        print("=" * 70)
        
        if not result["duplicates"]:
            print("\n   No duplicate therapeutic classes detected.")
        else:
            for dup in result["duplicates"]:
                print(f"\n    {dup['risk_level']}: {dup['class_name']}")
                print(f"     Drugs: {', '.join(dup['drugs'])}")
                print(f"     {dup['warning']}")
        
        print(f"\n  Summary: {result['duplicates_found']} duplicate class(es) in {result['total_checked']} drugs checked")
        print("=" * 70 + "\n")
