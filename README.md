# Nivarak — Medication Safety Checker

A clinical decision-support web application that screens medication lists for safety risks in adults 65+. Built for pharmacists, GPs, and care coordinators.

---

## What It Does

The user enters a list of medications and optional health conditions. Nivarak runs them through a multi-layer clinical safety engine and returns a structured report covering:

- **Beers Criteria** — flags medications that are potentially inappropriate for older adults (Always Avoid, Use With Caution, Condition-Specific, Renal Dose Adjustment)
- **STOPP/START Criteria** — identifies medications to stop and medications that should be started given the patient's conditions
- **Anticholinergic Burden (ACB)** — scores the cumulative anticholinergic load across all drugs
- **Drug–Drug Interactions** — pairwise interaction checks with severity ratings
- **Interaction Clusters** — flags multi-drug pharmacological risk groups: Serotonin Syndrome, QT Prolongation, CNS Depression, Triple Whammy (AKI risk), Bleeding Risk
- **Therapeutic Overlaps** — detects overlapping pharmacological effects across different drug classes (e.g. two sedating agents from different classes)
- **Duplicate Therapy** — identifies cases where the same drug class is prescribed twice
- **Falls Risk** — cumulative falls risk scoring from CNS depressants, anticholinergics, and other high-risk agents
- **Clinical Concerns Summary** — a prioritised, plain-English summary of the most important safety signals

---

## Clinical Rules Engine

### Beers Criteria (AGS 2023)
| Table | Meaning |
|---|---|
| Table 2 | Always Avoid — inappropriate for all adults 65+ regardless of diagnosis |
| Table 3 | Condition-Specific — avoid when a specific condition is present |
| Table 4 | Use With Caution — usable with monitoring, elevated risk with age |
| Table 6 | Renal Dose Adjustment — dose reduction or avoidance when kidney function is impaired |

### STOPP/START v2
- STOPP rules flag medications that should be stopped (e.g. NSAIDs in CKD, benzodiazepines in falls risk)
- START rules flag medications that should be considered but are missing from the list
- Rules are gated to the patient's conditions and co-medications

### Interaction Clusters
Five pharmacological risk clusters are detected when three or more relevant drugs are present:
- **Serotonin Syndrome** — SSRIs, SNRIs, tramadol, linezolid, lithium, etc.
- **QT Prolongation / Torsades** — antipsychotics, macrolides, antiarrhythmics, etc.
- **CNS Depression** — benzodiazepines, opioids, antihistamines, antipsychotics, z-drugs
- **Triple Whammy (AKI)** — NSAID + ACE inhibitor/ARB + diuretic combination
- **Bleeding Risk** — anticoagulants, antiplatelets, NSAIDs, SSRIs

### Falls Risk
A dedicated cumulative falls risk score based on the number and severity of fall-promoting agents: benzodiazepines, z-drugs, opioids, antipsychotics, anticholinergics, gabapentinoids, alpha blockers.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3, Flask |
| Clinical rules | Custom Python engine (`calculators/`) |
| Frontend | Vanilla HTML/CSS/JS (no framework) |
| Fonts | Lora (headings) + Source Sans 3 (body) |
| Deployment | Render (auto-deploy from GitHub) |

---

## Project Structure

```
calculators/
  med_checker.py          # Main API: get_structured_results(drugs, conditions)
  cumulative_risk.py      # ACB, interactions, clusters, falls, overlaps
  beers_criteria.py       # Beers Criteria rules (Tables 2, 3, 4, 6)
  stopp_start.py          # STOPP/START v2 rules
  acb_calculator.py       # Anticholinergic Burden scoring
  web_app/
    app.py                # Flask app entry point
    templates/index.html  # Single-page UI
    static/style.css      # Stylesheet
    requirements.txt      # Python dependencies
```

---

## Running Locally

```bash
cd calculators/web_app
pip install -r requirements.txt
python app.py
```

Open [http://localhost:5000](http://localhost:5000)

---

## Deployment (Render)

The app is deployed on [Render](https://render.com) with auto-deploy from GitHub main branch.

| Setting | Value |
|---|---|
| Build command | `pip install -r requirements.txt` |
| Start command | `python app.py` |
| Branch | `main` |

Push to main → Render redeploys automatically.

---

## Disclaimer

This tool is for educational and decision-support purposes only. It is not a substitute for clinical judgment. Always consult a qualified healthcare professional before making prescribing decisions.
