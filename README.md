# Nivarak — Medication Safety Checker

A clinical decision-support web application that screens medication lists for safety risks in adults 65+. Built for pharmacists, GPs, and care coordinators to catch dangerous polypharmacy at a glance.

**Live on Render. Auto-deploys from GitHub main branch.**

---

## Background — How This Was Built

This project started as a medical OCR pipeline — the original goal was to extract drug names from prescription photographs using optical character recognition. As the drug-name extraction layer matured, it became clear that extracting drug names was only half the problem. The harder question was: *what do you do with those names?*

That led to building a calculator layer on top: a set of clinical rule engines that take a list of drug names and return structured safety analysis. Over several development phases, the system grew from a basic ACB scorer into a comprehensive polypharmacy checker:

- **Phase 1** — ACB (Anticholinergic Cognitive Burden) scorer. 527-drug database, immediate clinical utility.
- **Phase 2** — Beers Criteria checker (AGS 2023). 64 rule entries across 4 tables. STOPP/START v3 checker. 98 STOPP + 54 START rules.
- **Phase 3** — Condition-aware logic. STOPP/START rules gated to patient conditions (e.g. NSAID flagged only when CKD is present). Multi-drug interaction engine with renal risk detection.
- **Phase 4** — Cumulative risk engine. Pharmacological cluster detection (serotonin syndrome, QT prolongation, CNS depression, triple whammy AKI, bleeding). Therapeutic overlap detection across drug classes. Falls risk scoring. Clinical concern synthesis: the system generates plain-English safety summaries rather than raw rule outputs.

The web app was built alongside the calculator layer — a single-page Flask app that calls the calculator engine and renders the results in a structured, readable format designed for adults 65+ (large type, clear hierarchy, plain language).

---

## What It Does

A user enters a medication list and optional health conditions. Nivarak runs them through eight clinical analysis layers and returns a structured safety report.

### Layer 1 — Anticholinergic Cognitive Burden (ACB)

Scores every drug on the 0–3 ACB scale from acbcalc.com (updated July 2024) and sums the total burden across the medication list.

**Database: 527 drugs**
| Score | Meaning | Drugs in database |
|---|---|---|
| 3 | Definite — High burden | 74 |
| 2 | Definite — Moderate burden | 12 |
| 1 | Possible burden | 122 |
| 0 | No anticholinergic activity | 319 |

A total score ≥ 3 is clinically significant — associated with increased cognitive impairment, falls, confusion, and mortality in adults 65+.

The lookup supports both generic and brand names. Fuzzy substring matching catches partial matches (e.g. "omeprazole" matches "esomeprazole"). Drug names not found in the database are scored as 0 and flagged separately.

---

### Layer 2 — Beers Criteria (AGS 2023)

Checks each drug against the 2023 American Geriatrics Society Beers Criteria, the definitive list of potentially inappropriate medications (PIMs) for older adults.

**Source:** J Am Geriatr Soc. 2023;71(7):2052-2081. doi:10.1111/jgs.18372

**Database: 64 rule entries**

| Table | Label | Entries | What it means |
|---|---|---|---|
| Table 2 | Always Avoid | 34 | These medications are potentially inappropriate for ALL adults 65+ regardless of diagnosis. The risk consistently outweighs any benefit. |
| Table 3 | Condition-Specific | 8 | Avoid only when the patient has a specific disease or syndrome (e.g. antipsychotics in Parkinson's disease, NSAIDs in heart failure). |
| Table 4 | Use With Caution | 9 | These drugs can be used in older adults but evidence shows elevated risk. Requires active monitoring. |
| Table 6 | Renal Dose Adjustment | 13 | Dose reduction or avoidance required when kidney function is impaired. Includes CrCl thresholds for each drug. |

**Table 2 categories covered:** 1st-generation antihistamines, antiparkinson anticholinergics, antispasmodics, antithrombotics, aspirin (primary prevention), warfarin, rivaroxaban, digoxin, amiodarone, dronedarone, nifedipine IR, high-dose spironolactone, androgens, estrogens, sulfonylureas, sliding-scale insulin, megestrol, growth hormone, GI antispasmodics, metoclopramide, mineral oil, PPIs (>8 weeks), TMP-SMX in renal impairment, anticholinergic antidepressants, antipsychotics, benzodiazepines, Z-drugs, meprobamate, ergot mesylates, muscle relaxants, NSAIDs, indomethacin/ketorolac, meperidine.

**Deduplication rule:** When a drug appears in both Table 2 (Always Avoid) and Table 4 (Use With Caution), Table 2 takes precedence and the Table 4 entry is suppressed. This prevents the same drug appearing twice with conflicting labels.

---

### Layer 3 — STOPP/START v3 (2023)

**Source:** O'Mahony D et al. Eur Geriatr Med. 2023;14(4):625-632. doi:10.1007/s41999-023-00777-y (Open Access, CC BY 4.0)

STOPP (Screening Tool of Older Persons' Prescriptions) flags medications that should be stopped. START (Screening Tool to Alert to Right Treatment) flags medications that should be considered but are missing.

**STOPP: 98 rules across 12 sections**

| Section | Rules | Examples |
|---|---|---|
| A — General | 3 | No indication; prescribed too long; duplicate class |
| B — Cardiovascular | 16 | Digoxin in AF without HF; amiodarone as first-line; beta-blocker + verapamil |
| C — Coagulation | 10 | Anticoagulant in low CHADS-VASc; dabigatran in severe renal impairment |
| D — CNS/Psychotropics | ~12 | TCAs; benzodiazepines; Z-drugs; antipsychotics in dementia/Parkinson's |
| E — Renal | ~6 | NSAIDs, metformin, lithium, methotrexate in CKD |
| F — Gastrointestinal | ~5 | PPIs without indication; constipating drugs in chronic constipation |
| G — Respiratory | ~4 | Oral corticosteroids in COPD; sedatives in respiratory failure |
| H — Musculoskeletal | ~8 | NSAIDs in peptic ulcer; corticosteroids in osteoporosis |
| I — Urogenital | ~4 | Alpha-blockers in incontinence; anticholinergics in constipation |
| J — Endocrine | ~6 | Sulfonylureas; insulin in type 2 without monitoring |
| K — Falls Risk | ~8 | Benzodiazepines, antipsychotics, opioids, alpha-blockers in patients with falls history |
| L — Analgesics | ~6 | Strong opioids as first-line in mild pain; opioids without laxative |

**START: 54 rules across 10 sections**

| Section | Rules | Examples |
|---|---|---|
| A — Cardiovascular | 10 | ACE inhibitor in HFrEF; statin in CAD; anticoagulant in AF |
| B — Coagulation | 2 | Antiplatelet in CAD; anticoagulant in VTE |
| C — CNS | 4 | Antidepressant in major depression; levodopa in Parkinson's |
| D — Renal | 2 | ACE inhibitor in diabetic nephropathy |
| E — Gastrointestinal | 2 | PPI with high-dose NSAID; laxative with regular opioid use |
| F — Respiratory | 5 | Inhaled beta-agonist in COPD/asthma; tiotropium in COPD |
| G — Musculoskeletal | 6 | Bisphosphonate in osteoporosis with steroids; calcium/vit D in osteoporosis |
| H — Urogenital | 4 | Alpha-blocker in BPH; 5-alpha reductase inhibitor |
| I — Endocrine | 6 | Metformin in type 2 diabetes; statin in diabetes with CV risk |
| J — Vaccines | 3 | Influenza; pneumococcal; shingles (herpes zoster) |

**Condition-gating:** STOPP/START rules that are condition-specific only fire when the relevant condition is present in the patient's input. For example, the rule flagging NSAIDs in CKD only triggers if the patient has listed CKD or chronic kidney disease. Rules that require co-medications (e.g. beta-blocker + verapamil) only fire when both drugs are present.

---

### Layer 4 — Drug–Drug Interactions (Pairwise)

Checks every pair of drugs in the list against an interaction database. Returns each interaction with a severity rating (Contraindicated / Major / Moderate / Minor) and a clinical description.

Results are grouped and counted by severity. Contraindicated interactions are prioritised in the Clinical Concerns summary.

---

### Layer 5 — Interaction Clusters (Pharmacological Risk Groups)

Beyond pairwise interactions, Nivarak detects multi-drug pharmacological risk clusters — patterns that only become dangerous when three or more relevant drugs are present simultaneously. These are computed from the cumulative risk engine and injected into the Interactions card so both views stay consistent.

**Five clusters detected:**

| Cluster | Drugs tracked | Risk logic |
|---|---|---|
| **Serotonin Syndrome** | 19 drugs (SSRIs, SNRIs, tramadol, MAOIs, TCAs, trazodone, bupropion) | ≥2 drugs = MODERATE; ≥2 high-severity = HIGH; ≥3 high-severity = VERY HIGH |
| **QT Prolongation / Torsades** | 12 drugs (amiodarone, methadone, ziprasidone, azithromycin, clarithromycin, haloperidol, quetiapine, domperidone, citalopram, fluconazole, metoclopramide, ondansetron) | ≥2 drugs = MODERATE; ≥2 high-severity = HIGH; ≥3 = VERY HIGH |
| **CNS Depression** | 28 drugs (benzodiazepines, opioids, Z-drugs, gabapentinoids, sedating antihistamines, antipsychotics, TCAs) | Counts high/moderate agents; ≥3 = HIGH; ≥2 high-severity = VERY HIGH |
| **Triple Whammy (AKI)** | NSAID + ACE inhibitor/ARB + diuretic | Present = HIGH risk; always shown as a concern |
| **Bleeding Risk** | 24 drugs (anticoagulants, antiplatelets, NSAIDs, SSRIs) | ≥2 high = VERY HIGH; 1 high + 1 mod = HIGH; 1 high alone = MODERATE-HIGH |

Each cluster shows the contributing drugs, individual drug roles, and a clinical explanation. LOW-risk results are suppressed from the Cumulative Risk card to reduce noise.

---

### Layer 6 — Therapeutic Overlaps

Detects cases where two or more drugs from *different* drug classes produce the same pharmacological effect. This is distinct from duplicate therapy (same class twice) — overlaps catch more subtle combinations.

**Three overlap categories:**

| Category | Classes checked |
|---|---|
| **Sedating overlap** | Benzodiazepine, Z-drug, Sedating antihistamine, Opioid, Sedating antipsychotic, Sedating antidepressant, Gabapentinoid, Muscle relaxant |
| **Anticholinergic overlap** | Bladder anticholinergic, Sedating antihistamine, Antidepressant, Antipsychotic, Antispasmodic, Antiparkinsonian |
| **Serotonergic overlap** | SSRI, SNRI, Serotonergic opioid, MAOI, TCA, Other serotonergic |

When ≥2 classes overlap in any category, the overlap is flagged with the drugs involved, their classes, and a risk rating. Shown in the Duplicate Therapies card alongside strict duplicate-class detection.

---

### Layer 7 — Falls Risk

A dedicated cumulative falls risk score — separate from CNS depression — because falls are the leading cause of serious injury in adults 65+.

**32 drugs tracked** across 7 categories:
- Benzodiazepines (high risk): diazepam, lorazepam, alprazolam, clonazepam, temazepam, nitrazepam, oxazepam
- Z-drugs (high risk): zolpidem, zaleplon, eszopiclone, zopiclone
- Opioids (high/moderate): morphine, oxycodone, fentanyl, hydromorphone, codeine, tramadol
- Gabapentinoids (moderate): gabapentin, pregabalin
- Antipsychotics (moderate): haloperidol, quetiapine, olanzapine
- Sedating antidepressants (moderate): amitriptyline, mirtazapine, nortriptyline
- Alpha-blockers (moderate, orthostatic hypotension): doxazosin, terazosin, prazosin

**Risk thresholds:** ≥2 high-risk agents = VERY HIGH; ≥3 any agents = HIGH; 2 agents = MODERATE; 1 agent = LOW (suppressed from UI).

---

### Layer 8 — Clinical Concerns Summary

The top panel of the results page synthesises all eight layers into a prioritised, plain-English list of clinical themes. It does not repeat raw rule outputs (e.g. "Diazepam — Beers Table 2") — it generates actionable summaries like "High Sedative Burden — VERY HIGH: 4 CNS depressants" or "Triple Whammy — Acute Kidney Injury Risk: ibuprofen + lisinopril + furosemide".

**Priority order (highest first):**
1. Triple Whammy (AKI risk) — always shown if present
2. Serotonin Syndrome risk (VERY HIGH / HIGH only)
3. CNS Sedative Burden (VERY HIGH / HIGH only)
4. QT Prolongation / Torsades risk (VERY HIGH / HIGH only)
5. Contraindicated drug interactions
6. Renal risk (when not already captured by Triple Whammy)
7. Bleeding risk (VERY HIGH / HIGH / MODERATE-HIGH)
8. Falls risk (VERY HIGH / HIGH)
9. High ACB score (≥ 3)
10. Anticholinergic therapeutic overlap

LOW-risk signals are not shown in the Concerns panel. The panel is intentionally brief — it surfaces what matters most.

---

## Total Clinical Coverage

| Module | Entries / Drugs |
|---|---|
| ACB database | 527 drugs |
| Beers Criteria rules | 64 rule entries |
| STOPP rules | 98 |
| START rules | 54 |
| Bleeding risk drugs | 24 |
| Serotonin syndrome drugs | 19 |
| CNS depression drugs | 28 |
| QT prolongation drugs | 12 |
| Falls risk drugs | 32 |
| Therapeutic overlap classes | 20 (across 3 categories) |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.12, Flask |
| Clinical rules | Custom Python engine — no external APIs |
| Frontend | Vanilla HTML / CSS / JS (no framework) |
| Fonts | Lora (headings) · Source Sans 3 (body) — optimised for readability in adults 65+ |
| Deployment | Render (auto-deploy from GitHub) |

All clinical rules are built and maintained in-house. There are no external API calls to drug databases at runtime — every check runs locally from the bundled Python modules. This makes the tool fast, auditable, and usable offline.

---

## Project Structure

```
calculators/
  med_checker.py          # Main API — get_structured_results(drugs, conditions)
                          # Orchestrates all eight layers, builds JSON response,
                          # generates clinical concerns, injects clusters into interactions

  cumulative_risk.py      # Cumulative risk engine
                          # Bleeding, serotonin, CNS depression, QT prolongation,
                          # falls risk, therapeutic overlaps
                          # SEDATING_CLASSES, ANTICHOLINERGIC_CLASSES, SEROTONERGIC_CLASSES dicts
                          # check_all_cumulative_risks() returns unified risk dict

  beers_criteria.py       # 2023 AGS Beers Criteria — 64 BeersDrug entries
                          # Tables 2, 3, 4, 6 — lookup by generic or brand name

  stopp_start.py          # STOPP/START v3 2023 — 98 STOPP + 54 START entries
                          # STOPPEntry: requires_conditions, requires_drugs fields
                          # for condition-gated and co-medication-gated rules

  acb_calculator.py       # ACB database — 527 drugs with 0–3 scores
                          # Fuzzy match: exact → brand → substring
                          # calculate_acb(drug_names) → per-drug + total

  web_app/
    app.py                # Flask entry point — POST /check, GET /
    templates/
      index.html          # Single-page UI
                          # renderInteractions(): pairwise + cluster sections
                          # renderDuplicates(): strict duplicates + therapeutic overlap
                          # renderCumulative(): ACB, bleeding, serotonin, CNS,
                          #   QT, falls — LOW suppressed
                          # renderBeers(): Table 2/3/4/6 grouped sections
                          # renderSTOPP() / renderSTART()
                          # buildSummary(): badge counts for header
                          # renderConcerns(): clinical theme panel
    static/
      style.css           # Stylesheet — navy/teal palette, Lora + Source Sans 3
                          # Large 18px base type for readability
      Nivarak Logo - RGB.jpg.jpeg   # Brand logo
    requirements.txt      # Flask, gunicorn

brand_mapping_preview/    # Data preview folder (not used in production)
```

---

## API

`POST /check`

Request body (JSON):
```json
{
  "drugs": ["warfarin", "aspirin", "ibuprofen", "omeprazole"],
  "conditions": ["atrial fibrillation", "chronic kidney disease"]
}
```

Response (JSON):
```json
{
  "acb": { "total_acb_score": 1, "high_risk": false, "drugs": [...] },
  "beers": { "flagged": 3, "results": [...] },
  "stopp": { "flagged": [...] },
  "start": { "recommended": [...] },
  "interactions": { "interactions": [...], "clusters": [...], "counts": {...} },
  "duplicates": [...],
  "cumulative": {
    "bleeding": { "risk_level": "VERY HIGH", "drugs": [...] },
    "serotonin": { ... },
    "cns_depression": { ... },
    "qt_prolongation": { ... },
    "falls": { ... },
    "triple_whammy": { ... },
    "overlaps": [...]
  },
  "concerns": ["Triple Whammy — Acute Kidney Injury Risk: ibuprofen + lisinopril + furosemide", ...]
}
```

---

## Running Locally

```bash
cd calculators/web_app
pip install -r requirements.txt
python app.py
```

Open [http://localhost:5000](http://localhost:5000)

Each calculator module can also be run standalone from the command line:

```bash
# ACB only
python calculators/acb_calculator.py warfarin amitriptyline diphenhydramine

# Beers Criteria only
python calculators/beers_criteria.py diazepam aspirin omeprazole

# STOPP/START only
python calculators/stopp_start.py
```

---

## Deployment (Render)

Auto-deploys on every push to `main` branch.

| Setting | Value |
|---|---|
| Build command | `pip install -r requirements.txt` |
| Start command | `python app.py` |
| Branch | `main` |
| Python version | 3.12 |

---

## Clinical Sources

| Source | Version | Reference |
|---|---|---|
| ACB Scale | July 2024 | acbcalc.com |
| AGS Beers Criteria | 2023 | J Am Geriatr Soc. 71(7):2052-2081 |
| STOPP/START | Version 3, 2023 | Eur Geriatr Med. 14(4):625-632 |

---

## Disclaimer

This tool is for educational and decision-support purposes only. It is not a substitute for clinical judgment. Always consult a qualified healthcare professional before making prescribing decisions. Drug interaction and safety data is based on published guidelines and may not reflect the most recent labelling changes.
