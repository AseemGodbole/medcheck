#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comprehensive Geriatric Medication Checker

Combines three validated screening tools for older adults (>=65):

1. ACB Calculator  - Anticholinergic Cognitive Burden score (acbcalc.com)
2. Beers Criteria  - AGS 2023 Potentially Inappropriate Medications
3. STOPP/START v3  - European Inappropriate Prescribing Tool
4. Drug Interactions - Clinically significant interactions
5. Duplicate Detection - Duplicate therapeutic classes
6. Cumulative Risk Assessment - Aggregated risks across drugs
7. START Suggestions - Medicines to consider starting

For educational/informational use only. Not a substitute for clinical judgment.

Usage:
    python med_checker.py amitriptyline diazepam omeprazole lisinopril
    python med_checker.py amitriptyline diazepam --conditions "heart failure, diabetes"
    python med_checker.py  # Interactive mode
"""

import sys
import os

#  Pull in the modules 
sys.path.insert(0, os.path.dirname(__file__))
from acb_calculator import calculate_acb, score_label as acb_score_label
from beers_criteria import check_drugs as check_beers, TABLE_LABELS
from drug_interactions import check_interactions
from stopp_start import (
    check_drugs_stopp, get_start_suggestions,
    STOPPEntry, STARTEntry
)
from duplicate_detection import check_duplicates
from cumulative_risk import check_all_cumulative_risks
from drug_name_resolver import resolve_drug_names

# --- Colour helpers (ANSI, graceful fallback) ----------------------------------
def _c(code, text):
    try:
        if sys.stdout.isatty():
            return f"\033[{code}m{text}\033[0m"
    except Exception:
        pass
    return text

RED    = lambda t: _c("31", t)
YELLOW = lambda t: _c("33", t)
GREEN  = lambda t: _c("32", t)
CYAN   = lambda t: _c("36", t)
BOLD   = lambda t: _c("1",  t)
DIM    = lambda t: _c("2",  t)

# --- Safe unicode converter for Windows compatibility --------------------------
def safe_text(text):
    """Sanitize text to ensure it can be printed on Windows without encoding errors."""
    if not isinstance(text, str):
        return text
    try:
        # Try to encode/decode as ASCII to catch any non-ASCII chars
        return text.encode('ascii').decode('ascii')
    except (UnicodeEncodeError, UnicodeDecodeError):
        # If it has non-ASCII, use ignore mode
        return text.encode('ascii', 'ignore').decode('ascii')

def sanitize_entry_data(entry):
    """Sanitize all string fields in a Beers/STOPP entry to be ASCII-safe."""
    if hasattr(entry, '__dict__'):
        # It's a dataclass
        for attr_name in dir(entry):
            if not attr_name.startswith('_'):
                attr_val = getattr(entry, attr_name, None)
                if isinstance(attr_val, str):
                    # Replace common problematic Unicode characters
                    attr_val = attr_val.replace('\u2265', '>=')  # >=
                    attr_val = attr_val.replace('\u2264', '<=')  # <=
                    attr_val = attr_val.replace('\u00b1', '+/-') # +-
                    attr_val = attr_val.replace('\u2013', '-')   # en-dash
                    attr_val = attr_val.replace('\u2014', '--')  # em-dash
                    try:
                        setattr(entry, attr_name, attr_val.encode('ascii', 'ignore').decode('ascii'))
                    except:
                        pass
    return entry

def safe_print(*args, **kwargs):
    """Safe print that gracefully handles Unicode encoding issues."""
    try:
        print(*args, **kwargs)
    except UnicodeEncodeError:
        # Convert all args to safe ASCII strings
        safe_args = []
        for arg in args:
            if isinstance(arg, str):
                safe_args.append(safe_text(arg))
            else:
                safe_args.append(str(arg))
        print(*safe_args, **kwargs)


#  Main report 

def run_full_check(drug_names: list, conditions: list = None):
    conditions = conditions or []
    resolved_drug_names, resolution_notes = resolve_drug_names(drug_names)
    SEP  = "=" * 72
    SEP2 = "-" * 72

    print(f"\n{BOLD(SEP)}")
    print(BOLD("  COMPREHENSIVE GERIATRIC MEDICATION CHECKER"))
    print(f"  Drugs reviewed: {CYAN(', '.join(d.title() for d in resolved_drug_names))}")
    if conditions:
        print(f"  Conditions    : {CYAN(', '.join(c.title() for c in conditions))}")
    if resolution_notes:
        print(f"  Brand names   : {DIM('; '.join(resolution_notes))}")
    print(BOLD(SEP))

    # -- 1. ACB Score -------------------------------------------------------
    acb_result = calculate_acb(resolved_drug_names)
    total_acb  = acb_result["total_acb_score"]
    acb_flag   = total_acb >= 3

    print(f"\n{BOLD('--- 1. ACB - Anticholinergic Cognitive Burden ---')}")
    for d in acb_result["drugs"]:
        if d["score"] > 0:
            icon = RED("") if d["score"] >= 3 else YELLOW("")
            print(f"  {icon}  {d['input'].title():<25} ACB = {d['score']}  -- {d['score_label']}")
        else:
            print(f"  {GREEN('*')}  {d['input'].title():<25} ACB = 0   -- No burden")

    acb_colour = RED if acb_flag else GREEN
    print(f"\n  {BOLD('Total ACB Score: ')} {acb_colour(str(total_acb))}")
    if acb_flag:
        print(f"  {RED('HIGH RISK (3): confusion, falls, and mortality risk elevated')}")
    else:
        print(f"  {GREEN('Lower risk (score < 3)')}")
    if acb_result["not_found"]:
        print(f"  {DIM('Not in ACB database (scored 0): ' + ', '.join(acb_result['not_found']))}")

    #  2. Beers Criteria 
    beers_result = check_beers(resolved_drug_names)

    print(f"\n{BOLD('--- 2. Beers Criteria 2023 - Potentially Inappropriate Meds ---')}")
    # Show only entries that are DEFINITE or match provided patient conditions
    displayed_beers_flags = 0
    bt = beers_result["total_drugs"]
    provided_conditions = [c.lower() for c in conditions]
    for drug in beers_result["results"]:
        if not drug["flagged"]:
            print(f"  {GREEN('')}  {drug['input'].title():<25} No Beers flags")
        else:
            # Filter entries by condition match: if entry.conditions empty -> definite flag, show it
            shown_any = False
            for entry in drug["entries"]:
                entry_conditions = [ec.lower() for ec in (entry.conditions or [])]
                condition_match = False
                if not entry_conditions:
                    condition_match = True
                else:
                    for pc in provided_conditions:
                        for ec in entry_conditions:
                            if pc and (ec in pc or pc in ec or ec.split()[0] == pc.split()[0]):
                                condition_match = True
                                break
                        if condition_match:
                            break

                if not condition_match:
                    # skip condition-specific entry when patient conditions not provided/matching
                    continue

                tbl_short = f"T{entry.table}"
                icon = RED("") if entry.table == "2" else YELLOW("")
                print(f"  {icon}  {drug['input'].title():<25} [{tbl_short}] {entry.recommendation}")
                print(f"       {DIM(entry.concern)}")
                if entry.conditions:
                    print(f"       {DIM('Conditions: ' + ', '.join(entry.conditions))}")
                if entry.renal_threshold:
                    print(f"       {DIM('Renal: ' + entry.renal_threshold)}")
                shown_any = True
                displayed_beers_flags += 1

            if not shown_any:
                print(f"  {GREEN('')}  {drug['input'].title():<25} No relevant Beers flags for provided conditions")

    bf = displayed_beers_flags
    flag_colour = RED if bf > 0 else GREEN
    print(f"\n  {BOLD('Beers flags (shown): ')} {flag_colour(str(bf))}/{bt} drug(s) flagged")

    #  3. STOPP 
    stopp_result = check_drugs_stopp(resolved_drug_names)

    print(f"\n{BOLD('--- 3. STOPP v3 2023 - Drugs to Consider Stopping ---')}")
    displayed_stopp_flags = 0
    st = stopp_result["total"]
    for drug in stopp_result["results"]:
        if not drug["flagged"]:
            print(f"  {GREEN('')}  {drug['input'].title():<25} No STOPP flags")
        else:
            shown_any = False
            for e in drug["entries"]:
                # STOPP entries often have e.condition; only show if it matches provided conditions or is general
                entry_cond = (e.condition or '').lower()
                condition_match = False
                if not entry_cond.strip():
                    condition_match = True
                else:
                    for pc in provided_conditions:
                        if pc and (entry_cond in pc or pc in entry_cond or entry_cond.split()[0] == pc.split()[0]):
                            condition_match = True
                            break

                if not condition_match:
                    continue

                print(f"  {RED('')}  {drug['input'].title():<25} [{e.criterion_id}] {e.section}")
                print(f"       {DIM('Condition: ' + e.condition)}")
                print(f"       {DIM('Rationale: ' + e.rationale)}")
                shown_any = True
                displayed_stopp_flags += 1

            if not shown_any:
                print(f"  {GREEN('')}  {drug['input'].title():<25} No relevant STOPP flags for provided conditions")

    sf = displayed_stopp_flags
    sflag_colour = RED if sf > 0 else GREEN
    print(f"\n  {BOLD('STOPP flags (shown): ')} {sflag_colour(str(sf))}/{st} drug(s) flagged")

    # -- 4. Drug-Drug Interactions ----------------------------------------
    interaction_result = check_interactions(resolved_drug_names)

    print(f"\n{BOLD('--- 4. Drug-Drug Interactions ---')}")
    if not interaction_result["interactions_found"]:
        print(f"  {GREEN('')}  No clinically significant interactions found between the listed drugs")
    else:
        for item in interaction_result["interactions_found"]:
            interaction = item["interaction"]
            severity = interaction.severity
            icon = {
                "CONTRAINDICATED": RED(""),
                "SERIOUS": RED(""),
                "MONITOR": YELLOW(""),
                "MINOR": DIM(""),
            }.get(severity, YELLOW(""))
            print(f"  {icon}  {item['drug_a'].title():<25}  {item['drug_b'].title()}  [{severity}]")
            print(f"       Mechanism : {interaction.mechanism}")
            print(f"       Effect    : {interaction.effect}")
            print(f"       Management: {interaction.management}")

    ic = interaction_result["counts"]
    i_total = len(interaction_result["interactions_found"])
    i_colour = RED if i_total > 0 else GREEN
    print(f"\n  {BOLD('Interactions found: ')} {i_colour(str(i_total))}/{interaction_result['pairs_checked']} pair(s)")
    if i_total > 0:
        sev_bits = []
        for label in ("CONTRAINDICATED", "SERIOUS", "MONITOR", "MINOR"):
            if ic.get(label, 0):
                sev_bits.append(f"{label.lower()}: {ic[label]}")
        if sev_bits:
            print(f"  {DIM('Severity breakdown: ' + ', '.join(sev_bits))}")

    # -- 5. Duplicate Therapeutic Classes ---------------------------------
    dup_result = check_duplicates(resolved_drug_names)
    dup_count = dup_result["duplicates_found"]

    print(f"\n{BOLD('--- 5. Duplicate Therapeutic Classes ---')}")
    if dup_count == 0:
        print(f"  {GREEN('')}  No duplicate therapeutic classes detected")
    else:
        for dup in dup_result["duplicates"]:
            icon = RED("") if dup["risk_level"] == "CONTRAINDICATED" else YELLOW("")
            print(f"  {icon}  {BOLD(dup['class_name'])} [{dup['risk_level']}]")
            print(f"       Drugs: {', '.join(dup['drugs'])}")
            print(f"       {dup['warning']}")

    dup_colour = RED if dup_count > 0 else GREEN
    print(f"\n  {BOLD('Duplicate classes: ')} {dup_colour(str(dup_count))}/{len(drug_names)}")

    # -- 6. Cumulative Risk Assessment ------------------------------------
    cumulative_risks = check_all_cumulative_risks(resolved_drug_names)

    print(f"\n{BOLD('--- 6. Cumulative Risk Assessment ---')}")
    
    # Bleeding risk
    bleeding = cumulative_risks["bleeding"]
    bleeding_drugs_count = len(bleeding["drugs"])
    if bleeding_drugs_count > 0:
        icon = RED("") if bleeding["risk_level"] in ["VERY HIGH", "HIGH"] else YELLOW("")
        print(f"  {icon}  BLEEDING RISK: {BOLD(bleeding['risk_level'])}")
        for drug in bleeding["drugs"]:
            print(f"       - {drug['drug'].title()} ({drug['severity']})")
    
    # Serotonin risk
    serotonin = cumulative_risks["serotonin"]
    serotonin_drugs_count = len(serotonin["drugs"])
    if serotonin_drugs_count > 0:
        icon = RED("") if serotonin["risk_level"] in ["HIGH", "VERY HIGH"] else YELLOW("")
        print(f"  {icon}  SEROTONIN SYNDROME RISK: {BOLD(serotonin['risk_level'])}")
        for drug in serotonin["drugs"]:
            print(f"       - {drug['drug'].title()} ({drug['severity']})")
    
    # CNS depression risk
    cns = cumulative_risks["cns_depression"]
    cns_drugs_count = len(cns["drugs"])
    if cns_drugs_count > 0:
        icon = RED("") if cns["risk_level"] in ["VERY HIGH", "HIGH"] else YELLOW("")
        print(f"  {icon}  CNS DEPRESSION RISK: {BOLD(cns['risk_level'])}")
        for drug in cns["drugs"]:
            print(f"       - {drug['drug'].title()} ({drug['severity']})")

    # -- 7. START Suggestions -------------------------------------------
    print(f"\n{BOLD('--- 7. START v3 2023 - Medicines to Consider Starting ---')}")
    if not conditions:
        print(f"  {DIM('No conditions provided  pass conditions to see START suggestions.')}")
        print(f"  {DIM('Example: python med_checker.py [drugs] --conditions \"heart failure, diabetes\"')}")
    else:
        start_hits = get_start_suggestions(conditions)
        if not start_hits:
            print(f"  {DIM('No START criteria matched for the given conditions.')}")
        else:
            for e in start_hits:
                print(f"  {CYAN('')}  [{e.criterion_id}] {BOLD(e.drug_class)}")
                print(f"       Indication : {e.indication}")
                if e.examples:
                    print(f"       Examples   : {', '.join(e.examples)}")

    #  Summary 
    print(f"\n{BOLD(SEP)}")
    print(BOLD("  SUMMARY"))
    print(SEP2)

    total_flags = (1 if acb_flag else 0) + bf + sf
    if total_flags == 0 and i_total == 0 and dup_count == 0 and (bleeding_drugs_count + serotonin_drugs_count + cns_drugs_count) == 0:
        print(f"  {GREEN('  No major flags identified across all seven tools.')}")
    else:
        if acb_flag:
            print(f"  {RED('  ACB Score 3: High anticholinergic burden  review and reduce where possible')}")
        if bf > 0:
            t2 = sum(1 for d in beers_result["results"]
                     for e in d["entries"] if e.table == "2")
            t3 = sum(1 for d in beers_result["results"]
                     for e in d["entries"] if e.table == "3")
            t4 = sum(1 for d in beers_result["results"]
                     for e in d["entries"] if e.table == "4")
            t6 = sum(1 for d in beers_result["results"]
                     for e in d["entries"] if e.table == "6")
            detail = []
            if t2: detail.append(f"{t2} always-avoid")
            if t3: detail.append(f"{t3} condition-specific")
            if t4: detail.append(f"{t4} caution")
            if t6: detail.append(f"{t6} renal")
            print(f"  {RED('  Beers 2023: ')} {bf} drug(s) flagged ({', '.join(detail)})")
        if sf > 0:
            print(f"  {RED('  STOPP v3:   ')} {sf} drug(s) to consider deprescribing")
        if i_total > 0:
            print(f"  {RED('  Interactions: ')} {i_total} clinically significant interaction(s) found")
        if dup_count > 0:
            print(f"  {RED('  Duplicates:   ')} {dup_count} duplicate therapeutic class(es) detected")
        if bleeding_drugs_count > 0:
            print(f"  {RED('  Bleeding:     ')} Cumulative bleeding risk ({bleeding['risk_level']})")
        if serotonin_drugs_count > 0:
            print(f"  {RED('  Serotonin:    ')} Serotonin syndrome risk ({serotonin['risk_level']})")
        if cns_drugs_count > 0:
            print(f"  {RED('  CNS Depr.:    ')} CNS depression risk ({cns['risk_level']})")

    start_hits_count = len(get_start_suggestions(conditions)) if conditions else 0
    if start_hits_count > 0:
        print(f"  {CYAN('  START v3:    ')} {start_hits_count} prescribing omission(s) to consider")

    # Improved disclaimer wording and formatting
    print("\n  DISCLAIMER:")
    print(f"    This tool is for information and educational purposes only — not medical advice.")
    print(f"    Do NOT change medication without consulting a qualified healthcare professional.")
    print(f"    Apply recommendations with clinical judgment for adults aged 65 and over.")
    print("\n    Sources: ACB (acbcalc.com) | AGS Beers Criteria 2023 | STOPP/START v3 2023 | Medscape interactions")
    print(BOLD(SEP) + "\n")


def get_structured_results(drug_names: list, conditions: list = None) -> dict:
    """
    Run all checks and return structured JSON-serialisable data.
    Used by the web API instead of run_full_check().
    Shows ALL flags; the caller decides what to display.
    """
    conditions = conditions or []
    resolved_drug_names, resolution_notes = resolve_drug_names(drug_names)

    acb_result         = calculate_acb(resolved_drug_names)
    beers_result       = check_beers(resolved_drug_names)
    stopp_result       = check_drugs_stopp(resolved_drug_names)
    interaction_result = check_interactions(resolved_drug_names)
    dup_result         = check_duplicates(resolved_drug_names)
    cumulative_risks   = check_all_cumulative_risks(resolved_drug_names)
    start_hits         = get_start_suggestions(conditions, resolved_drug_names) if conditions else []

    # --- ACB ---
    acb_data = {
        "total_score": acb_result["total_acb_score"],
        "high_risk":   acb_result["high_risk"],
        "drugs": [
            {"name": d["input"], "score": d["score"], "score_label": d["score_label"]}
            for d in acb_result["drugs"]
        ],
        "not_found": acb_result["not_found"],
    }

    # --- Beers ---
    beers_data = {"results": []}
    for drug in beers_result["results"]:
        entries = []
        for entry in drug["entries"]:
            entries.append({
                "table":               entry.table,
                "category":            entry.category,
                "recommendation":      entry.recommendation,
                "concern":             entry.concern,
                "rationale":           entry.rationale,
                "conditions":          entry.conditions,
                "renal_threshold":     entry.renal_threshold,
                "quality_of_evidence": entry.quality_of_evidence,
                "strength":            entry.strength,
            })
        beers_data["results"].append({
            "drug":    drug["input"],
            "flagged": drug["flagged"],
            "entries": entries,
        })

    # --- STOPP ---
    stopp_data = {"results": []}
    for drug in stopp_result["results"]:
        entries = []
        for entry in drug["entries"]:
            entries.append({
                "criterion_id": entry.criterion_id,
                "section":      entry.section,
                "condition":    entry.condition,
                "rationale":    entry.rationale,
            })
        stopp_data["results"].append({
            "drug":    drug["input"],
            "flagged": drug["flagged"],
            "entries": entries,
        })

    # --- Interactions: deduplicate by drug pair, show all reasons, highest severity ---
    sev_order = {"CONTRAINDICATED": 0, "SERIOUS": 1, "MONITOR": 2, "MINOR": 3}
    from collections import defaultdict
    pair_groups = defaultdict(list)
    for item in interaction_result["interactions_found"]:
        key = tuple(sorted([item["drug_a"], item["drug_b"]]))
        pair_groups[key].append(item)

    interactions_data = {"found": [], "pairs_checked": interaction_result["pairs_checked"]}
    for (da, db), items in pair_groups.items():
        items.sort(key=lambda x: sev_order.get(x["interaction"].severity, 99))
        highest_sev = items[0]["interaction"].severity
        reasons = []
        seen_effects = set()
        for item in items:
            iact = item["interaction"]
            effect_key = iact.effect[:60].lower()
            if effect_key not in seen_effects:
                seen_effects.add(effect_key)
                reasons.append({
                    "severity":   iact.severity,
                    "mechanism":  iact.mechanism,
                    "effect":     iact.effect,
                    "management": iact.management,
                })
        interactions_data["found"].append({
            "drug_a":   da,
            "drug_b":   db,
            "severity": highest_sev,
            "reasons":  reasons,
        })

    interactions_data["found"].sort(key=lambda x: sev_order.get(x["severity"], 99))
    counts = {"CONTRAINDICATED": 0, "SERIOUS": 0, "MONITOR": 0, "MINOR": 0}
    for finding in interactions_data["found"]:
        sev = finding["severity"]
        if sev in counts:
            counts[sev] += 1
    interactions_data["counts"] = counts

    # --- Duplicates ---
    dup_data = {
        "found": dup_result["duplicates"],
        "count": dup_result["duplicates_found"],
    }

    # --- Cumulative ---
    cumulative_data = {
        "bleeding": {
            "risk_level": cumulative_risks["bleeding"]["risk_level"],
            "drugs":      cumulative_risks["bleeding"]["drugs"],
        },
        "serotonin": {
            "risk_level": cumulative_risks["serotonin"]["risk_level"],
            "drugs":      cumulative_risks["serotonin"]["drugs"],
        },
        "cns_depression": {
            "risk_level": cumulative_risks["cns_depression"]["risk_level"],
            "drugs":      cumulative_risks["cns_depression"]["drugs"],
        },
    }

    # --- START ---
    start_data = {
        "suggestions": [
            {
                "criterion_id": e.criterion_id,
                "section":      e.section,
                "drug_class":   e.drug_class,
                "indication":   e.indication,
                "rationale":    e.rationale,
                "examples":     e.examples,
            }
            for e in start_hits
        ]
    }

    # --- Concerns: top-level clinical summary ---
    concerns = []
    for finding in interactions_data["found"]:
        if finding["severity"] == "CONTRAINDICATED":
            effects = "; ".join(r["effect"][:100] for r in finding["reasons"][:2])
            concerns.append({
                "level": "danger",
                "text":  f"{finding['drug_a'].title()} + {finding['drug_b'].title()}: {effects}",
            })
    sero = cumulative_data["serotonin"]
    if sero["risk_level"] in ("VERY HIGH", "HIGH", "MODERATE-HIGH"):
        lvl = "danger" if "VERY HIGH" in sero["risk_level"] else "warning"
        drugs_txt = ", ".join(d["drug"].title() for d in sero["drugs"][:3])
        concerns.append({"level": lvl,
                         "text": f"Serotonin syndrome risk: {sero['risk_level']} ({drugs_txt})"})
    bleed = cumulative_data["bleeding"]
    if bleed["risk_level"] not in ("LOW", ""):
        lvl = "danger" if "VERY HIGH" in bleed["risk_level"] else \
              "warning" if bleed["risk_level"] in ("HIGH", "MODERATE-HIGH") else "caution"
        concerns.append({"level": lvl,
                         "text": f"Bleeding risk: {bleed['risk_level']}"})
    if acb_data["high_risk"]:
        concerns.append({"level": "warning",
                         "text": f"High anticholinergic burden (ACB score {acb_data['total_score']}, threshold >= 3)"})
    for r in beers_data["results"]:
        for e in r["entries"]:
            if e["table"] == "2":
                concerns.append({"level": "danger",
                                 "text": f"{r['drug'].title()} — Beers Table 2 (Always Avoid): {e['recommendation']}"})

    return {
        "drugs_checked":    resolved_drug_names,
        "conditions":       conditions,
        "resolution_notes": resolution_notes,
        "concerns":         concerns,
        "acb":              acb_data,
        "beers":            beers_data,
        "stopp":            stopp_data,
        "interactions":     interactions_data,
        "duplicates":       dup_data,
        "cumulative":       cumulative_data,
        "start":            start_data,
    }


#  CLI

def main():
    args = sys.argv[1:]

    # Parse --conditions flag
    conditions = []
    if "--conditions" in args:
        idx = args.index("--conditions")
        cond_str = args[idx + 1] if idx + 1 < len(args) else ""
        conditions = [c.strip() for c in cond_str.split(",") if c.strip()]
        args = args[:idx] + args[idx + 2:]

    drugs = [a.strip() for a in args if a.strip()]

    if not drugs:
        print("=" * 60)
        print("  COMPREHENSIVE GERIATRIC MEDICATION CHECKER")
        print("=" * 60)
        raw = input("  Enter drug names (comma-separated):\n  > ")
        drugs = [d.strip() for d in raw.split(",") if d.strip()]
        if not drugs:
            print("No drugs entered. Exiting.")
            return
        cond_raw = input("\n  Enter patient conditions for START criteria")
        print("  (e.g. 'heart failure, diabetes, osteoporosis') or press Enter to skip:")
        cond_input = input("  > ").strip()
        if cond_input:
            conditions = [c.strip() for c in cond_input.split(",") if c.strip()]

    run_full_check(drugs, conditions)


if __name__ == "__main__":
    main()
