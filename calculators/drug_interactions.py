"""
Drug-Drug Interaction Checker
Data compiled from: Medscape, drugs.com, AAFP AFP guidelines, BNF,
FDA drug labeling, and published clinical pharmacology literature.

Severity levels (matching Medscape categories):
  CONTRAINDICATED   Do not use together; risks outweigh any benefit
  SERIOUS           Avoid or use alternative; monitor closely if unavoidable
  MONITOR           Monitor closely; adjust dose or frequency as needed
  MINOR             Usually no action needed; clinically insignificant

 For educational use only. Not a substitute for clinical judgment.
"""

from dataclasses import dataclass, field

@dataclass
class Interaction:
    drugs: tuple           # (drug_a, drug_b)  canonical lowercase names
    severity: str          # CONTRAINDICATED / SERIOUS / MONITOR / MINOR
    mechanism: str         # pharmacokinetic or pharmacodynamic mechanism
    effect: str            # clinical consequence
    management: str        # what to do
    aliases_a: list = field(default_factory=list)  # brand names / synonyms for drug_a
    aliases_b: list = field(default_factory=list)  # brand names / synonyms for drug_b

#  Interaction Database 

INTERACTIONS: list[Interaction] = [

    #  MAOI interactions (mostly CONTRAINDICATED) 
    Interaction(
        drugs=("maoi", "ssri"),
        severity="CONTRAINDICATED",
        mechanism="Pharmacodynamic  additive serotonergic effect; MAO inhibition prevents serotonin breakdown",
        effect="Serotonin syndrome: hyperthermia, agitation, tachycardia, hypertension, clonus, potentially fatal",
        management="Contraindicated. Allow 14 days washout after stopping MAOI before starting SSRI; allow 14 days (or 5 weeks for fluoxetine) after stopping SSRI before starting MAOI.",
        aliases_a=["phenelzine", "nardil", "tranylcypromine", "parnate", "isocarboxazid", "marplan", "selegiline", "emsam", "rasagiline", "azilect", "moclobemide"],
        aliases_b=["fluoxetine", "prozac", "sertraline", "zoloft", "paroxetine", "paxil", "citalopram", "celexa", "escitalopram", "lexapro", "fluvoxamine", "luvox"],
    ),
    Interaction(
        drugs=("maoi", "snri"),
        severity="CONTRAINDICATED",
        mechanism="Pharmacodynamic  combined serotonin and noradrenaline excess",
        effect="Serotonin syndrome; hypertensive crisis",
        management="Contraindicated. Strict washout periods required (same as MAOI + SSRI).",
        aliases_a=["phenelzine", "nardil", "tranylcypromine", "parnate", "isocarboxazid", "moclobemide"],
        aliases_b=["venlafaxine", "effexor", "duloxetine", "cymbalta", "desvenlafaxine", "pristiq", "levomilnacipran", "fetzima"],
    ),
    Interaction(
        drugs=("maoi", "tramadol"),
        severity="CONTRAINDICATED",
        mechanism="Pharmacodynamic  tramadol inhibits serotonin and noradrenaline reuptake; MAOI prevents monoamine breakdown",
        effect="Serotonin syndrome; seizures",
        management="Contraindicated. Do not use together or within 14 days of each other.",
        aliases_a=["phenelzine", "nardil", "tranylcypromine", "parnate", "isocarboxazid", "moclobemide"],
        aliases_b=["tramadol", "ultram", "conzip"],
    ),
    Interaction(
        drugs=("maoi", "meperidine"),
        severity="CONTRAINDICATED",
        mechanism="Pharmacodynamic  meperidine inhibits serotonin reuptake; combined serotonin toxicity",
        effect="Potentially fatal serotonin syndrome; hyperpyrexia, circulatory collapse",
        management="Absolutely contraindicated. Use alternative opioids (morphine, oxycodone) with extreme caution and monitoring.",
        aliases_a=["phenelzine", "nardil", "tranylcypromine", "parnate", "moclobemide"],
        aliases_b=["meperidine", "pethidine", "demerol"],
    ),
    Interaction(
        drugs=("maoi", "linezolid"),
        severity="CONTRAINDICATED",
        mechanism="Pharmacodynamic  linezolid has weak MAOI properties; additive serotonergic and monoamine effects",
        effect="Serotonin syndrome; hypertensive crisis",
        management="Contraindicated. If linezolid absolutely necessary, stop serotonergic drugs and monitor closely.",
        aliases_a=["phenelzine", "tranylcypromine", "moclobemide", "selegiline"],
        aliases_b=["linezolid", "zyvox"],
    ),
    Interaction(
        drugs=("maoi", "sympathomimetics"),
        severity="CONTRAINDICATED",
        mechanism="Pharmacodynamic  MAO inhibition prevents breakdown of noradrenaline released by sympathomimetics",
        effect="Hypertensive crisis; severe headache; stroke risk",
        management="Contraindicated. Avoid all indirect sympathomimetics (pseudoephedrine, ephedrine, tyramine-rich foods).",
        aliases_a=["phenelzine", "tranylcypromine", "isocarboxazid", "moclobemide"],
        aliases_b=["pseudoephedrine", "sudafed", "ephedrine", "phenylephrine", "amphetamine"],
    ),
    Interaction(
        drugs=("maoi", "dextromethorphan"),
        severity="CONTRAINDICATED",
        mechanism="Pharmacodynamic  dextromethorphan inhibits serotonin reuptake; combined with MAO inhibition",
        effect="Serotonin syndrome; hyperpyrexia; psychosis",
        management="Contraindicated. Avoid all OTC cough preparations containing dextromethorphan.",
        aliases_a=["phenelzine", "tranylcypromine", "isocarboxazid", "moclobemide"],
        aliases_b=["dextromethorphan", "dm", "robitussin", "nyquil"],
    ),
    Interaction(
        drugs=("maoi", "tricyclic antidepressants"),
        severity="CONTRAINDICATED",
        mechanism="Pharmacodynamic  additive serotonergic and noradrenergic effects",
        effect="Serotonin syndrome; hypertensive crisis; seizures",
        management="Contraindicated. Do not use together.",
        aliases_a=["phenelzine", "tranylcypromine", "isocarboxazid", "moclobemide"],
        aliases_b=["amitriptyline", "elavil", "imipramine", "tofranil", "clomipramine", "anafranil", "nortriptyline", "pamelor", "doxepin"],
    ),

    #  QT Prolongation interactions 
    Interaction(
        drugs=("amiodarone", "azithromycin"),
        severity="CONTRAINDICATED",
        mechanism="Pharmacodynamic  both prolong QT interval via potassium channel blockade",
        effect="Additive QT prolongation; risk of torsades de pointes; ventricular fibrillation; sudden cardiac death",
        management="Contraindicated. Use alternative antibiotic (amoxicillin, doxycycline). If unavoidable, baseline and serial ECG monitoring required.",
        aliases_a=["amiodarone", "cordarone", "pacerone"],
        aliases_b=["azithromycin", "zithromax", "z-pak"],
    ),
    Interaction(
        drugs=("amiodarone", "sotalol"),
        severity="CONTRAINDICATED",
        mechanism="Pharmacodynamic  both prolong QT interval; class III antiarrhythmic effects",
        effect="Severe QT prolongation; torsades de pointes; cardiac arrest",
        management="Contraindicated. Do not combine two QT-prolonging antiarrhythmics.",
        aliases_a=["amiodarone", "cordarone"],
        aliases_b=["sotalol", "betapace"],
    ),
    Interaction(
        drugs=("antipsychotics", "azithromycin"),
        severity="SERIOUS",
        mechanism="Pharmacodynamic  additive QT prolongation",
        effect="QT prolongation; risk of torsades de pointes",
        management="Avoid combination if possible. If necessary, obtain baseline ECG, monitor potassium/magnesium, avoid other QT-prolonging drugs.",
        aliases_a=["haloperidol", "haldol", "quetiapine", "seroquel", "olanzapine", "zyprexa", "risperidone", "risperdal", "ziprasidone", "geodon", "thioridazine", "mellaril", "chlorpromazine"],
        aliases_b=["azithromycin", "zithromax", "z-pak"],
    ),
    Interaction(
        drugs=("antipsychotics", "antipsychotics"),
        severity="SERIOUS",
        mechanism="Pharmacodynamic  additive QT prolongation and CNS/cardiovascular depression",
        effect="QT prolongation; increased EPS; sedation; orthostatic hypotension",
        management="Avoid dual antipsychotic use unless clearly indicated (e.g. clozapine augmentation). Monitor ECG and clinical status.",
        aliases_a=["haloperidol", "quetiapine", "olanzapine", "risperidone", "aripiprazole", "ziprasidone"],
        aliases_b=["haloperidol", "quetiapine", "olanzapine", "risperidone", "aripiprazole", "ziprasidone"],
    ),
    Interaction(
        drugs=("citalopram", "azithromycin"),
        severity="SERIOUS",
        mechanism="Pharmacodynamic  both prolong QT interval; citalopram has highest QT effect among SSRIs",
        effect="QT prolongation; torsades de pointes risk",
        management="Use with caution. If unavoidable, limit citalopram to 20 mg/day; monitor ECG; check electrolytes.",
        aliases_a=["citalopram", "celexa"],
        aliases_b=["azithromycin", "zithromax"],
    ),

    #  Serotonin Syndrome (non-MAOI) 
    Interaction(
        drugs=("ssri", "tramadol"),
        severity="SERIOUS",
        mechanism="Pharmacodynamic  both increase serotonin; SSRIs inhibit CYP2D6 (especially fluoxetine/paroxetine), reducing tramadol conversion to active M1 metabolite and increasing parent drug",
        effect="Serotonin syndrome risk; reduced analgesia (CYP2D6 inhibition by fluoxetine/paroxetine)",
        management="Avoid if possible. If used together, use lowest effective tramadol dose; monitor for serotonin toxicity signs. Consider alternative analgesic.",
        aliases_a=["fluoxetine", "prozac", "sertraline", "zoloft", "paroxetine", "paxil", "citalopram", "celexa", "escitalopram", "lexapro", "fluvoxamine"],
        aliases_b=["tramadol", "ultram"],
    ),
    Interaction(
        drugs=("ssri", "triptans"),
        severity="MONITOR",
        mechanism="Pharmacodynamic  additive serotonergic effects at 5-HT1B/1D receptors",
        effect="Serotonin syndrome (weak risk in practice); monitor for signs of toxicity",
        management="FDA warns of risk; clinical evidence suggests low actual risk. Monitor patient after first dose combination; use with caution in patients with known risk factors.",
        aliases_a=["fluoxetine", "sertraline", "paroxetine", "citalopram", "escitalopram"],
        aliases_b=["sumatriptan", "imitrex", "rizatriptan", "maxalt", "zolmitriptan", "zomig", "eletriptan", "relpax"],
    ),
    Interaction(
        drugs=("ssri", "snri"),
        severity="SERIOUS",
        mechanism="Pharmacodynamic  additive serotonergic effects",
        effect="Serotonin syndrome; increased risk of bleeding (antiplatelet effect)",
        management="Avoid combination unless clearly warranted and monitored by specialist.",
        aliases_a=["fluoxetine", "sertraline", "paroxetine", "citalopram", "escitalopram", "fluvoxamine"],
        aliases_b=["venlafaxine", "effexor", "duloxetine", "cymbalta", "desvenlafaxine"],
    ),
    Interaction(
        drugs=("ssri", "linezolid"),
        severity="CONTRAINDICATED",
        mechanism="Pharmacodynamic  linezolid inhibits MAO; combined serotonin excess",
        effect="Serotonin syndrome",
        management="Contraindicated. If linezolid urgently needed, stop SSRI and allow washout (5 weeks for fluoxetine, 2 weeks for others).",
        aliases_a=["fluoxetine", "prozac", "sertraline", "zoloft", "paroxetine", "paxil", "citalopram", "escitalopram"],
        aliases_b=["linezolid", "zyvox"],
    ),
    Interaction(
        drugs=("snri", "linezolid"),
        severity="CONTRAINDICATED",
        mechanism="Pharmacodynamic  combined serotonin/noradrenaline toxicity with MAO inhibition",
        effect="Serotonin syndrome",
        management="Contraindicated. Stop SNRI with appropriate washout before linezolid.",
        aliases_a=["venlafaxine", "effexor", "duloxetine", "cymbalta"],
        aliases_b=["linezolid", "zyvox"],
    ),

    #  Anticoagulant interactions 
    Interaction(
        drugs=("warfarin", "nsaids"),
        severity="SERIOUS",
        mechanism="Pharmacodynamic  additive bleeding risk (NSAIDs inhibit platelet aggregation, damage gastric mucosa); pharmacokinetic (some NSAIDs inhibit CYP2C9 warfarin metabolism)",
        effect="Significantly increased risk of serious GI bleeding and major haemorrhage",
        management="Avoid if possible. Use paracetamol (acetaminophen) for pain relief. If NSAID necessary: use lowest dose for shortest time; add PPI; monitor INR more frequently.",
        aliases_a=["warfarin", "coumadin", "jantoven"],
        aliases_b=["ibuprofen", "advil", "motrin", "naproxen", "aleve", "naprosyn", "diclofenac", "voltaren", "indomethacin", "indocin", "celecoxib", "celebrex", "meloxicam", "mobic", "etoricoxib", "piroxicam", "ketorolac"],
    ),
    Interaction(
        drugs=("warfarin", "aspirin"),
        severity="SERIOUS",
        mechanism="Pharmacodynamic  aspirin inhibits platelet function (irreversibly) + gastric mucosal damage; high-dose aspirin also displaces warfarin from protein binding",
        effect="Increased bleeding risk; GI haemorrhage",
        management="Avoid unless specific indication (e.g. mechanical heart valve, high thromboembolic risk). If unavoidable, limit aspirin to 100 mg/day; add PPI; monitor INR; educate patient on bleeding signs.",
        aliases_a=["warfarin", "coumadin"],
        aliases_b=["aspirin", "asa", "acetylsalicylic acid"],
    ),
    Interaction(
        drugs=("warfarin", "amiodarone"),
        severity="SERIOUS",
        mechanism="Pharmacokinetic  amiodarone inhibits CYP2C9 and CYP3A4, reducing warfarin metabolism and raising warfarin concentrations significantly",
        effect="Markedly elevated INR; severe bleeding risk",
        management="Reduce warfarin dose empirically by 3050% when amiodarone initiated. Monitor INR weekly for several weeks. Note: amiodarone effect persists weeksmonths after it is stopped (very long half-life).",
        aliases_a=["warfarin", "coumadin"],
        aliases_b=["amiodarone", "cordarone", "pacerone"],
    ),
    Interaction(
        drugs=("warfarin", "fluconazole"),
        severity="SERIOUS",
        mechanism="Pharmacokinetic  fluconazole potently inhibits CYP2C9 (primary warfarin metaboliser) and CYP3A4",
        effect="Markedly elevated INR within 13 days; serious bleeding",
        management="Empirically reduce warfarin dose by 2550%. Monitor INR every 12 days during fluconazole course and after completion. Consider topical antifungal alternatives.",
        aliases_a=["warfarin", "coumadin"],
        aliases_b=["fluconazole", "diflucan"],
    ),
    Interaction(
        drugs=("warfarin", "metronidazole"),
        severity="SERIOUS",
        mechanism="Pharmacokinetic  metronidazole inhibits CYP2C9; also reduces intestinal vitamin K-producing bacteria",
        effect="Elevated INR; bleeding risk",
        management="Monitor INR closely during and for 1 week after metronidazole course. Consider dose adjustment.",
        aliases_a=["warfarin", "coumadin"],
        aliases_b=["metronidazole", "flagyl"],
    ),
    Interaction(
        drugs=("warfarin", "trimethoprim-sulfamethoxazole"),
        severity="SERIOUS",
        mechanism="Pharmacokinetic  TMP-SMX inhibits CYP2C9 (S-warfarin); also reduces vitamin K-producing gut flora",
        effect="Significantly elevated INR; major bleeding risk",
        management="Avoid if possible. If necessary, reduce warfarin dose by ~25%; check INR every 2 days during therapy and 5 days after.",
        aliases_a=["warfarin", "coumadin"],
        aliases_b=["trimethoprim-sulfamethoxazole", "tmp-smx", "bactrim", "septra", "co-trimoxazole"],
    ),
    Interaction(
        drugs=("warfarin", "ssri"),
        severity="MONITOR",
        mechanism="Pharmacodynamic  SSRIs impair platelet aggregation via serotonin depletion; pharmacokinetic  fluoxetine/fluvoxamine inhibit CYP2C9/2C19",
        effect="Increased bleeding risk; elevated INR (especially with fluoxetine/fluvoxamine)",
        management="Monitor INR more frequently. Avoid fluoxetine/fluvoxamine with warfarin if possible (highest interaction risk). Citalopram/escitalopram/sertraline are safer choices.",
        aliases_a=["warfarin", "coumadin"],
        aliases_b=["fluoxetine", "prozac", "fluvoxamine", "luvox", "sertraline", "zoloft", "paroxetine", "citalopram", "escitalopram"],
    ),
    Interaction(
        drugs=("warfarin", "statins"),
        severity="MONITOR",
        mechanism="Pharmacokinetic  fluvastatin, lovastatin, rosuvastatin, simvastatin inhibit CYP2C9; atorvastatin less so",
        effect="Increased warfarin exposure; elevated INR and bleeding risk",
        management="Monitor INR when statin initiated or dose changed. Pravastatin and atorvastatin have lowest interaction risk and are preferred.",
        aliases_a=["warfarin", "coumadin"],
        aliases_b=["simvastatin", "zocor", "lovastatin", "mevacor", "rosuvastatin", "crestor", "fluvastatin", "lescol", "atorvastatin", "lipitor"],
    ),
    Interaction(
        drugs=("warfarin", "rifampicin"),
        severity="SERIOUS",
        mechanism="Pharmacokinetic  rifampicin is potent inducer of CYP2C9, CYP3A4, and P-glycoprotein; markedly increases warfarin metabolism",
        effect="Markedly reduced INR; loss of anticoagulation; thromboembolic events",
        management="Avoid if possible. If essential, increase warfarin dose significantly (may need to double or triple); monitor INR every 12 days. After rifampicin stopped, reduce warfarin promptly or risk major bleeding.",
        aliases_a=["warfarin", "coumadin"],
        aliases_b=["rifampicin", "rifampin", "rifadin"],
    ),
    Interaction(
        drugs=("warfarin", "carbamazepine"),
        severity="SERIOUS",
        mechanism="Pharmacokinetic  carbamazepine induces CYP3A4 and CYP2C9, increasing warfarin metabolism",
        effect="Reduced anticoagulation; thromboembolic risk",
        management="Monitor INR weekly when carbamazepine started or dose changed. May need warfarin dose increase of 3050%.",
        aliases_a=["warfarin", "coumadin"],
        aliases_b=["carbamazepine", "tegretol", "carbatrol"],
    ),
    Interaction(
        drugs=("warfarin", "phenytoin"),
        severity="SERIOUS",
        mechanism="Pharmacokinetic  complex bidirectional: phenytoin initially inhibits then induces warfarin metabolism; warfarin displaces phenytoin from protein binding",
        effect="Unpredictable INR changes; also phenytoin toxicity possible",
        management="Monitor INR and phenytoin levels closely when combined. Avoid if possible.",
        aliases_a=["warfarin", "coumadin"],
        aliases_b=["phenytoin", "dilantin", "phenytek"],
    ),
    Interaction(
        drugs=("doac", "nsaids"),
        severity="SERIOUS",
        mechanism="Pharmacodynamic  additive bleeding risk; NSAIDs impair platelet function and damage GI mucosa",
        effect="Significantly increased major and GI bleeding",
        management="Avoid chronic NSAID use with any DOAC. If short-term NSAID required, consider adding PPI and use lowest dose for shortest duration.",
        aliases_a=["apixaban", "eliquis", "rivaroxaban", "xarelto", "dabigatran", "pradaxa", "edoxaban", "savaysa"],
        aliases_b=["ibuprofen", "naproxen", "diclofenac", "celecoxib", "meloxicam", "indomethacin", "ketorolac"],
    ),
    Interaction(
        drugs=("doac", "antiplatelet"),
        severity="SERIOUS",
        mechanism="Pharmacodynamic  dual antithrombotic therapy significantly increases bleeding risk",
        effect="Major bleeding; GI haemorrhage; intracranial haemorrhage",
        management="Avoid triple therapy (DOAC + aspirin + P2Y12 inhibitor) unless specific indication (recent ACS/stent). If needed, minimise duration, use PPI, and use lowest antiplatelet dose.",
        aliases_a=["apixaban", "eliquis", "rivaroxaban", "xarelto", "dabigatran", "pradaxa"],
        aliases_b=["aspirin", "clopidogrel", "plavix", "ticagrelor", "brilinta", "prasugrel", "effient"],
    ),
    Interaction(
        drugs=("doac", "strong cyp3a4 inhibitors"),
        severity="SERIOUS",
        mechanism="Pharmacokinetic  CYP3A4/P-gp inhibition increases DOAC plasma levels (especially rivaroxaban, apixaban)",
        effect="Elevated DOAC levels; increased bleeding risk",
        management="Avoid ketoconazole, itraconazole, ritonavir with rivaroxaban/apixaban. Dabigatran also affected by P-gp inhibitors (dronedarone, ketoconazole). Dose reduction may be required per labeling.",
        aliases_a=["apixaban", "eliquis", "rivaroxaban", "xarelto", "dabigatran", "pradaxa"],
        aliases_b=["ketoconazole", "itraconazole", "sporanox", "ritonavir", "norvir", "dronedarone", "multaq", "clarithromycin", "biaxin"],
    ),
    Interaction(
        drugs=("doac", "rifampicin"),
        severity="SERIOUS",
        mechanism="Pharmacokinetic  rifampicin induces CYP3A4 and P-gp; markedly reduces all DOAC levels",
        effect="Loss of anticoagulant effect; thromboembolic events",
        management="Avoid co-administration. If rifampicin required, switch to warfarin with close INR monitoring.",
        aliases_a=["apixaban", "eliquis", "rivaroxaban", "xarelto", "dabigatran", "pradaxa", "edoxaban"],
        aliases_b=["rifampicin", "rifampin", "rifadin"],
    ),
    Interaction(
        drugs=("anticoagulant", "ssri"),
        severity="MONITOR",
        mechanism="Pharmacodynamic  SSRIs inhibit platelet serotonin uptake, impairing platelet aggregation",
        effect="Increased bleeding risk, particularly GI haemorrhage",
        management="Monitor for signs of bleeding. Consider adding PPI, especially with history of GI bleeding. Monitor INR if on warfarin.",
        aliases_a=["warfarin", "apixaban", "rivaroxaban", "dabigatran"],
        aliases_b=["fluoxetine", "sertraline", "paroxetine", "citalopram", "escitalopram", "fluvoxamine"],
    ),

    #  Opioid interactions 
    Interaction(
        drugs=("opioids", "benzodiazepines"),
        severity="CONTRAINDICATED",
        mechanism="Pharmacodynamic  synergistic CNS and respiratory depression via different receptor systems",
        effect="Profound sedation; respiratory depression; coma; death. FDA black box warning.",
        management="Avoid combination. If both essential (e.g. cancer pain + anxiety): use lowest effective doses; short-acting benzodiazepine; naloxone available; educate patient. NEVER combine with alcohol.",
        aliases_a=["morphine", "oxycodone", "oxycontin", "fentanyl", "duragesic", "hydromorphone", "dilaudid", "codeine", "tramadol", "buprenorphine", "methadone"],
        aliases_b=["diazepam", "valium", "lorazepam", "ativan", "alprazolam", "xanax", "clonazepam", "klonopin", "temazepam", "midazolam"],
    ),
    Interaction(
        drugs=("opioids", "z-drugs"),
        severity="SERIOUS",
        mechanism="Pharmacodynamic  combined CNS and respiratory depression",
        effect="Serious respiratory depression; sedation; falls; death risk",
        management="Avoid combination. If required, use lowest doses; monitor closely; patient education.",
        aliases_a=["morphine", "oxycodone", "fentanyl", "hydromorphone", "codeine", "tramadol", "buprenorphine"],
        aliases_b=["zolpidem", "ambien", "zopiclone", "eszopiclone", "lunesta", "zaleplon"],
    ),
    Interaction(
        drugs=("opioids", "gabapentinoids"),
        severity="SERIOUS",
        mechanism="Pharmacodynamic  additive CNS and respiratory depression; gabapentinoids enhance opioid-induced respiratory depression disproportionately",
        effect="Respiratory depression; overdose risk; death  especially with high opioid doses",
        management="Use with caution. Use minimum effective doses of both. Caution in patients with COPD, sleep apnoea, elderly. Monitor respiratory rate.",
        aliases_a=["morphine", "oxycodone", "fentanyl", "codeine", "tramadol", "hydromorphone"],
        aliases_b=["gabapentin", "neurontin", "pregabalin", "lyrica"],
    ),
    Interaction(
        drugs=("methadone", "ssri"),
        severity="SERIOUS",
        mechanism="Pharmacokinetic + pharmacodynamic  fluoxetine/fluvoxamine inhibit CYP2D6/3A4, raising methadone levels; also QT prolongation and serotonin risk",
        effect="QT prolongation; torsades de pointes; serotonin toxicity",
        management="Monitor ECG (QTc). Avoid fluoxetine and fluvoxamine. Citalopram/escitalopram preferred but also monitor QT.",
        aliases_a=["methadone", "dolophine"],
        aliases_b=["fluoxetine", "prozac", "fluvoxamine", "sertraline", "citalopram"],
    ),
    Interaction(
        drugs=("fentanyl", "cyp3a4 inhibitors"),
        severity="SERIOUS",
        mechanism="Pharmacokinetic  CYP3A4 inhibitors reduce fentanyl metabolism, increasing plasma concentrations",
        effect="Opioid toxicity; respiratory depression; sedation",
        management="Avoid or reduce fentanyl dose. Monitor closely for respiratory depression. Common inhibitors: azole antifungals, macrolide antibiotics, HIV protease inhibitors, grapefruit juice.",
        aliases_a=["fentanyl", "duragesic", "actiq", "abstral"],
        aliases_b=["ketoconazole", "itraconazole", "fluconazole", "clarithromycin", "biaxin", "erythromycin", "ritonavir", "verapamil", "diltiazem"],
    ),
    Interaction(
        drugs=("naloxone", "opioids"),
        severity="MONITOR",
        mechanism="Pharmacodynamic  competitive opioid receptor antagonism; reverses opioid effects",
        effect="Acute opioid withdrawal; reversal of analgesia; tachycardia; pulmonary oedema in overdose",
        management="Use cautiously in opioid-dependent patients. Titrate dose carefully. Repeat doses may be required due to short naloxone half-life.",
        aliases_a=["naloxone", "narcan"],
        aliases_b=["morphine", "oxycodone", "fentanyl", "heroin", "methadone", "buprenorphine"],
    ),
    Interaction(
        drugs=("codeine", "cyp2d6 inhibitors"),
        severity="SERIOUS",
        mechanism="Pharmacokinetic  CYP2D6 converts codeine to morphine (active); inhibitors reduce conversion, reducing analgesia; poor CYP2D6 metabolisers get no analgesia",
        effect="Reduced analgesia; analgesia failure",
        management="Avoid codeine in poor CYP2D6 metabolisers and with strong CYP2D6 inhibitors. Use alternative opioid (morphine, oxycodone).",
        aliases_a=["codeine"],
        aliases_b=["fluoxetine", "prozac", "paroxetine", "paxil", "bupropion", "wellbutrin", "duloxetine"],
    ),

    #  Cardiovascular interactions 
    Interaction(
        drugs=("statins", "cyp3a4 inhibitors"),
        severity="SERIOUS",
        mechanism="Pharmacokinetic  CYP3A4 inhibitors reduce metabolism of simvastatin/lovastatin/atorvastatin, markedly increasing statin exposure",
        effect="Myopathy; rhabdomyolysis; acute renal failure",
        management="Contraindicated: simvastatin/lovastatin + itraconazole/ketoconazole/HIV protease inhibitors. Serious: simvastatin 20 mg with diltiazem/verapamil/amiodarone. Switch to pravastatin or rosuvastatin (not CYP3A4 substrates) with strong inhibitors.",
        aliases_a=["simvastatin", "zocor", "lovastatin", "mevacor", "atorvastatin", "lipitor"],
        aliases_b=["itraconazole", "sporanox", "ketoconazole", "posaconazole", "clarithromycin", "biaxin", "erythromycin", "diltiazem", "cardizem", "verapamil", "calan", "ritonavir", "cyclosporine"],
    ),
    Interaction(
        drugs=("statins", "gemfibrozil"),
        severity="SERIOUS",
        mechanism="Pharmacokinetic  gemfibrozil inhibits CYP2C8 and glucuronidation, dramatically raising statin levels (especially simvastatin, cerivastatin)",
        effect="Rhabdomyolysis; severe myopathy",
        management="Avoid combination. If fibrate required with statin, use fenofibrate (safer than gemfibrozil). Avoid simvastatin + any fibrate.",
        aliases_a=["simvastatin", "lovastatin", "atorvastatin", "rosuvastatin", "pravastatin"],
        aliases_b=["gemfibrozil", "lopid"],
    ),
    Interaction(
        drugs=("digoxin", "amiodarone"),
        severity="SERIOUS",
        mechanism="Pharmacokinetic  amiodarone inhibits P-glycoprotein and CYP enzymes, reducing digoxin renal/non-renal clearance by ~50%",
        effect="Digoxin toxicity: nausea, bradycardia, heart block, ventricular arrhythmias",
        management="Reduce digoxin dose by 50% when amiodarone initiated. Monitor digoxin levels and ECG. Be aware of long delay due to amiodarone's long half-life.",
        aliases_a=["digoxin", "lanoxin"],
        aliases_b=["amiodarone", "cordarone"],
    ),
    Interaction(
        drugs=("digoxin", "verapamil"),
        severity="SERIOUS",
        mechanism="Pharmacokinetic  verapamil inhibits P-glycoprotein-mediated renal digoxin excretion; pharmacodynamic  additive AV node depression",
        effect="Digoxin toxicity; heart block; bradycardia",
        management="Reduce digoxin dose by 3350% when verapamil added. Monitor digoxin levels, heart rate, and ECG.",
        aliases_a=["digoxin", "lanoxin"],
        aliases_b=["verapamil", "calan", "isoptin", "verelan"],
    ),
    Interaction(
        drugs=("beta-blockers", "verapamil"),
        severity="SERIOUS",
        mechanism="Pharmacodynamic  additive suppression of AV node conduction; combined negative chronotropy and inotropy",
        effect="Severe bradycardia; heart block; acute heart failure; hypotension",
        management="Avoid IV combination (high risk of cardiac arrest). Oral combination requires close monitoring; use only with specialist supervision.",
        aliases_a=["atenolol", "metoprolol", "lopressor", "bisoprolol", "propranolol", "carvedilol"],
        aliases_b=["verapamil", "calan", "isoptin"],
    ),
    Interaction(
        drugs=("beta-blockers", "diltiazem"),
        severity="SERIOUS",
        mechanism="Pharmacodynamic  additive AV node depression and negative chronotropy",
        effect="Bradycardia; heart block; hypotension",
        management="Avoid IV combination. Oral combination: monitor heart rate and ECG; use lower doses.",
        aliases_a=["atenolol", "metoprolol", "bisoprolol", "propranolol", "carvedilol"],
        aliases_b=["diltiazem", "cardizem", "tiazac"],
    ),
    Interaction(
        drugs=("ace inhibitors", "potassium-sparing diuretics"),
        severity="SERIOUS",
        mechanism="Pharmacodynamic  additive potassium retention; ACE-I reduces aldosterone, sparing potassium; K+-sparing diuretics do the same",
        effect="Hyperkalaemia; potentially life-threatening cardiac arrhythmias",
        management="Monitor serum potassium and renal function closely (before starting, then 12 weeks later, and with any dose change). Avoid in patients with CKD or diabetes where hyperkalaemia risk is high.",
        aliases_a=["lisinopril", "ramipril", "enalapril", "perindopril", "captopril", "trandolapril", "quinapril"],
        aliases_b=["spironolactone", "aldactone", "eplerenone", "amiloride", "triamterene"],
    ),
    Interaction(
        drugs=("ace inhibitors", "arb"),
        severity="SERIOUS",
        mechanism="Pharmacodynamic  dual renin-angiotensin blockade; additive hyperkalaemia and renal impairment",
        effect="Acute kidney injury; severe hyperkalaemia; hypotension",
        management="Contraindicated in most situations. The ONTARGET trial showed no benefit and increased harm. Rarely justified (some HF/proteinuria cases under specialist care).",
        aliases_a=["lisinopril", "ramipril", "enalapril", "captopril"],
        aliases_b=["losartan", "cozaar", "valsartan", "diovan", "irbesartan", "avapro", "candesartan", "telmisartan"],
    ),
    Interaction(
        drugs=("ace inhibitors", "nsaids"),
        severity="SERIOUS",
        mechanism="Pharmacodynamic  NSAIDs block prostaglandin-mediated vasodilation; reduce antihypertensive effect and cause renal afferent arteriolar vasoconstriction",
        effect="Acute kidney injury (especially with diuretic  'triple whammy'); reduced antihypertensive efficacy; hyperkalaemia",
        management="Avoid triple combination (ACE-I + diuretic + NSAID). Use paracetamol instead. Monitor renal function and blood pressure if NSAID unavoidable.",
        aliases_a=["lisinopril", "ramipril", "enalapril", "perindopril", "captopril"],
        aliases_b=["ibuprofen", "naproxen", "diclofenac", "celecoxib", "etoricoxib", "indomethacin"],
    ),
    Interaction(
        drugs=("arb", "nsaids"),
        severity="SERIOUS",
        mechanism="Pharmacodynamic  same mechanism as ACE-I + NSAIDs; triple whammy risk",
        effect="Acute kidney injury; reduced antihypertensive effect",
        management="Same as ACE-I + NSAIDs. Avoid triple combination with diuretic.",
        aliases_a=["losartan", "valsartan", "irbesartan", "candesartan", "telmisartan"],
        aliases_b=["ibuprofen", "naproxen", "diclofenac", "celecoxib", "indomethacin"],
    ),

    #  Antidiabetic interactions 
    Interaction(
        drugs=("sulfonylureas", "fluconazole"),
        severity="SERIOUS",
        mechanism="Pharmacokinetic  fluconazole inhibits CYP2C9, reducing sulfonylurea metabolism and raising drug levels",
        effect="Severe prolonged hypoglycaemia",
        management="Avoid combination if possible. If essential, monitor blood glucose closely; consider dose reduction of sulfonylurea.",
        aliases_a=["glibenclamide", "glyburide", "glipizide", "glimepiride", "gliclazide", "tolbutamide", "chlorpropamide"],
        aliases_b=["fluconazole", "diflucan"],
    ),
    Interaction(
        drugs=("metformin", "iodinated contrast media"),
        severity="SERIOUS",
        mechanism="Pharmacodynamic  contrast-induced nephropathy can impair metformin excretion, leading to accumulation",
        effect="Lactic acidosis (rare but potentially fatal)",
        management="Withhold metformin on day of contrast administration and for 48 hours after. Restart only if renal function remains normal.",
        aliases_a=["metformin", "glucophage"],
        aliases_b=["iodinated contrast", "contrast dye", "radiocontrast"],
    ),
    Interaction(
        drugs=("insulin", "beta-blockers"),
        severity="MONITOR",
        mechanism="Pharmacodynamic  beta-blockers mask most hypoglycaemia symptoms (tachycardia, tremor, anxiety) except sweating; may also prolong hypoglycaemia by blocking glycogenolysis",
        effect="Masked hypoglycaemia; prolonged hypoglycaemic episodes",
        management="Use cardioselective beta-blockers (atenolol, metoprolol, bisoprolol) where possible. Educate patient on sweating as hypoglycaemia warning sign. Monitor blood glucose carefully.",
        aliases_a=["insulin", "glargine", "lantus", "detemir", "aspart", "lispro", "glulisine"],
        aliases_b=["propranolol", "atenolol", "tenormin", "metoprolol", "bisoprolol", "carvedilol"],
    ),
    Interaction(
        drugs=("sglt2 inhibitors", "loop diuretics"),
        severity="MONITOR",
        mechanism="Pharmacodynamic  additive volume depletion and risk of dehydration",
        effect="Volume depletion; acute kidney injury; hypotension; DKA risk with insulin",
        management="Monitor for dehydration. Ensure adequate hydration. Hold SGLT2i before surgery or procedures. Reduce diuretic if needed.",
        aliases_a=["empagliflozin", "jardiance", "dapagliflozin", "farxiga", "canagliflozin", "invokana"],
        aliases_b=["furosemide", "lasix", "bumetanide", "torasemide"],
    ),

    #  Antibiotic interactions 
    Interaction(
        drugs=("fluoroquinolones", "antacids"),
        severity="MONITOR",
        mechanism="Pharmacokinetic  divalent/trivalent cations (Mg, Al, Ca, Fe, Zn) chelate fluoroquinolones in gut, reducing absorption by up to 90%",
        effect="Markedly reduced fluoroquinolone plasma levels; treatment failure",
        management="Administer fluoroquinolone 2 hours before or 46 hours after antacids, iron, zinc, or calcium supplements. Same applies to dairy products.",
        aliases_a=["ciprofloxacin", "cipro", "levofloxacin", "levaquin", "moxifloxacin", "avelox", "norfloxacin"],
        aliases_b=["antacids", "aluminium hydroxide", "magnesium hydroxide", "gaviscon", "calcium carbonate", "iron", "ferrous sulphate", "ferrous gluconate"],
    ),
    Interaction(
        drugs=("fluoroquinolones", "nsaids"),
        severity="MONITOR",
        mechanism="Pharmacodynamic  both lower seizure threshold; NSAID competition at GABA receptor",
        effect="Increased risk of seizures, especially in elderly patients or those with epilepsy",
        management="Avoid combining if patient has seizure history. Monitor closely if unavoidable.",
        aliases_a=["ciprofloxacin", "cipro", "norfloxacin"],
        aliases_b=["ibuprofen", "naproxen", "indomethacin"],
    ),
    Interaction(
        drugs=("metronidazole", "alcohol"),
        severity="SERIOUS",
        mechanism="Pharmacodynamic  metronidazole inhibits aldehyde dehydrogenase (ALDH); acetaldehyde accumulates",
        effect="Disulfiram-like reaction: severe flushing, nausea, vomiting, tachycardia, hypotension",
        management="Avoid all alcohol during and for 48 hours after metronidazole course. Counsel patients explicitly.",
        aliases_a=["metronidazole", "flagyl"],
        aliases_b=["alcohol", "ethanol"],
    ),
    Interaction(
        drugs=("rifampicin", "oral contraceptives"),
        severity="SERIOUS",
        mechanism="Pharmacokinetic  rifampicin is a potent inducer of CYP3A4 and P-gp; markedly reduces oestrogen/progestogen plasma levels",
        effect="Contraceptive failure; unwanted pregnancy",
        management="Use additional non-hormonal contraception (barrier method) during rifampicin course and for 28 days after. Consider alternative antibiotic if appropriate.",
        aliases_a=["rifampicin", "rifampin"],
        aliases_b=["oral contraceptive", "combined oral contraceptive", "pill", "ocp", "ethinylestradiol", "levonorgestrel", "desogestrel"],
    ),
    Interaction(
        drugs=("clarithromycin", "statins"),
        severity="SERIOUS",
        mechanism="Pharmacokinetic  clarithromycin potently inhibits CYP3A4, raising simvastatin/lovastatin/atorvastatin levels dramatically",
        effect="Rhabdomyolysis; myopathy; acute renal failure",
        management="Temporarily withhold simvastatin/lovastatin/atorvastatin during clarithromycin course. Use azithromycin as alternative (does not inhibit CYP3A4 significantly). Pravastatin or rosuvastatin are safer alternatives.",
        aliases_a=["clarithromycin", "biaxin"],
        aliases_b=["simvastatin", "zocor", "lovastatin", "mevacor", "atorvastatin", "lipitor"],
    ),

    #  Psychiatric drug interactions 
    Interaction(
        drugs=("lithium", "nsaids"),
        severity="SERIOUS",
        mechanism="Pharmacokinetic  NSAIDs reduce renal prostaglandin synthesis, impairing lithium excretion and raising serum lithium levels",
        effect="Lithium toxicity: tremor, confusion, seizures, cardiac arrhythmias, coma",
        management="Avoid NSAIDs in patients on lithium. Use paracetamol for analgesia. If NSAID unavoidable, reduce lithium dose by 2550% and monitor levels closely.",
        aliases_a=["lithium", "priadel", "camcolit", "lithonate"],
        aliases_b=["ibuprofen", "naproxen", "diclofenac", "celecoxib", "indomethacin"],
    ),
    Interaction(
        drugs=("lithium", "diuretics"),
        severity="SERIOUS",
        mechanism="Pharmacokinetic  thiazide and loop diuretics cause sodium depletion; kidney compensates by reabsorbing more lithium (competes with Na+)",
        effect="Lithium toxicity",
        management="Avoid thiazide diuretics with lithium if possible. If necessary, monitor lithium levels every 27 days after diuretic initiation or dose change. Maintain adequate salt and fluid intake.",
        aliases_a=["lithium", "priadel", "camcolit"],
        aliases_b=["hydrochlorothiazide", "hctz", "bendroflumethiazide", "furosemide", "lasix", "bumetanide"],
    ),
    Interaction(
        drugs=("lithium", "ace inhibitors"),
        severity="SERIOUS",
        mechanism="Pharmacokinetic  ACE-I reduce aldosterone, causing sodium loss; compensatory lithium retention in kidney tubules",
        effect="Lithium toxicity",
        management="Monitor lithium levels closely within 12 weeks of starting/stopping ACE-I. Dose reduction may be required.",
        aliases_a=["lithium", "priadel"],
        aliases_b=["lisinopril", "ramipril", "enalapril", "perindopril"],
    ),
    Interaction(
        drugs=("clozapine", "carbamazepine"),
        severity="SERIOUS",
        mechanism="Pharmacodynamic  both suppress bone marrow; additive agranulocytosis risk; also pharmacokinetic  carbamazepine induces CYP, reducing clozapine levels",
        effect="Severe agranulocytosis; neutropenia; fatal infection risk",
        management="Contraindicated by most guidelines. Do not combine. Use valproate or lamotrigine as alternative mood stabilisers with clozapine.",
        aliases_a=["clozapine", "clozaril"],
        aliases_b=["carbamazepine", "tegretol"],
    ),
    Interaction(
        drugs=("clozapine", "fluvoxamine"),
        severity="SERIOUS",
        mechanism="Pharmacokinetic  fluvoxamine potently inhibits CYP1A2, raising clozapine levels by 310 fold",
        effect="Clozapine toxicity: seizures, sedation, hypersalivation, agranulocytosis",
        management="Avoid combination if possible. If used, reduce clozapine dose by 6775% and monitor levels and clinical status closely.",
        aliases_a=["clozapine", "clozaril"],
        aliases_b=["fluvoxamine", "luvox"],
    ),
    Interaction(
        drugs=("antipsychotics", "anticholinergics"),
        severity="MONITOR",
        mechanism="Pharmacodynamic  additive anticholinergic effects",
        effect="Urinary retention; constipation; confusion; delirium; increased anticholinergic burden",
        management="Minimise concurrent use. Regularly reassess need for anticholinergic co-prescription (e.g. procyclidine with antipsychotic for EPS).",
        aliases_a=["haloperidol", "chlorpromazine", "olanzapine", "quetiapine"],
        aliases_b=["procyclidine", "kemadrin", "benztropine", "cogentin", "trihexyphenidyl", "artane", "oxybutynin", "ditropan"],
    ),
    Interaction(
        drugs=("ssri", "nsaids"),
        severity="MONITOR",
        mechanism="Pharmacodynamic  both impair platelet function via different mechanisms; additive GI bleeding risk",
        effect="Increased GI bleeding risk (315x); particularly upper GI haemorrhage",
        management="Consider adding PPI if both required long-term. Educate on GI bleeding symptoms. Consider alternative analgesic.",
        aliases_a=["fluoxetine", "sertraline", "paroxetine", "citalopram", "escitalopram"],
        aliases_b=["ibuprofen", "naproxen", "diclofenac", "celecoxib", "aspirin"],
    ),

    #  Immunosuppressant interactions 
    Interaction(
        drugs=("ciclosporin", "statins"),
        severity="SERIOUS",
        mechanism="Pharmacokinetic  ciclosporin inhibits OATP1B1, CYP3A4, and P-gp; greatly increases statin exposure",
        effect="Severe myopathy; rhabdomyolysis",
        management="Contraindicated with simvastatin and lovastatin. Use lowest possible dose of pravastatin (max 20 mg) or fluvastatin. Rosuvastatin max 5 mg. Monitor CK levels.",
        aliases_a=["ciclosporin", "cyclosporine", "neoral", "sandimmune"],
        aliases_b=["simvastatin", "lovastatin", "atorvastatin", "pravastatin", "rosuvastatin"],
    ),
    Interaction(
        drugs=("tacrolimus", "cyp3a4 inhibitors"),
        severity="SERIOUS",
        mechanism="Pharmacokinetic  CYP3A4/P-gp inhibition raises tacrolimus levels; narrow therapeutic index",
        effect="Tacrolimus toxicity: nephrotoxicity, neurotoxicity, hyperglycaemia",
        management="Monitor tacrolimus levels closely. Reduce dose. Common culprits: azole antifungals, macrolide antibiotics, diltiazem, verapamil.",
        aliases_a=["tacrolimus", "prograf", "advagraf"],
        aliases_b=["fluconazole", "itraconazole", "ketoconazole", "clarithromycin", "erythromycin", "diltiazem", "verapamil"],
    ),
    Interaction(
        drugs=("methotrexate", "nsaids"),
        severity="SERIOUS",
        mechanism="Pharmacokinetic  NSAIDs compete for renal tubular secretion of methotrexate; also reduce GFR",
        effect="Methotrexate toxicity: myelosuppression, mucositis, nephrotoxicity, hepatotoxicity",
        management="Avoid NSAIDs around high-dose methotrexate. With low-dose (RA): cautious short-term use with monitoring; hold NSAIDs on methotrexate day if possible.",
        aliases_a=["methotrexate"],
        aliases_b=["ibuprofen", "naproxen", "diclofenac", "indomethacin", "aspirin"],
    ),

    #  Herbal/Supplement interactions 
    Interaction(
        drugs=("st john's wort", "ssri"),
        severity="SERIOUS",
        mechanism="Pharmacodynamic  St John's Wort has serotonergic properties; additive serotonin toxicity",
        effect="Serotonin syndrome",
        management="Avoid combination. Discontinue St John's Wort before starting any antidepressant.",
        aliases_a=["st john's wort", "hypericum", "hypericum perforatum"],
        aliases_b=["fluoxetine", "sertraline", "paroxetine", "citalopram", "escitalopram"],
    ),
    Interaction(
        drugs=("st john's wort", "warfarin"),
        severity="SERIOUS",
        mechanism="Pharmacokinetic  St John's Wort induces CYP2C9, CYP3A4, and P-gp; reduces warfarin levels",
        effect="Reduced anticoagulation; thromboembolic events",
        management="Avoid combination. Patient should disclose all herbal supplements. If stopped, INR may rise  monitor closely.",
        aliases_a=["st john's wort", "hypericum"],
        aliases_b=["warfarin", "coumadin"],
    ),
    Interaction(
        drugs=("st john's wort", "oral contraceptives"),
        severity="SERIOUS",
        mechanism="Pharmacokinetic  CYP3A4/P-gp induction reduces hormonal contraceptive levels",
        effect="Contraceptive failure",
        management="Avoid combination. Use additional non-hormonal contraception. Consider stopping St John's Wort.",
        aliases_a=["st john's wort", "hypericum"],
        aliases_b=["oral contraceptive", "pill", "ocp", "ethinylestradiol"],
    ),
    Interaction(
        drugs=("st john's wort", "doac"),
        severity="SERIOUS",
        mechanism="Pharmacokinetic  P-gp/CYP3A4 induction reduces all DOAC levels",
        effect="Loss of anticoagulant effect; stroke or VTE risk",
        management="Contraindicated with all DOACs. Discontinue St John's Wort.",
        aliases_a=["st john's wort", "hypericum"],
        aliases_b=["apixaban", "eliquis", "rivaroxaban", "xarelto", "dabigatran", "pradaxa", "edoxaban"],
    ),
    Interaction(
        drugs=("grapefruit juice", "statins"),
        severity="MONITOR",
        mechanism="Pharmacokinetic  grapefruit inhibits intestinal CYP3A4 and OATP1B1; increases simvastatin/lovastatin/atorvastatin bioavailability",
        effect="Raised statin plasma levels; myopathy risk",
        management="Avoid grapefruit/pomelo juice with simvastatin or lovastatin. Moderate caution with atorvastatin. Pravastatin and rosuvastatin not significantly affected.",
        aliases_a=["grapefruit juice", "grapefruit"],
        aliases_b=["simvastatin", "zocor", "lovastatin", "atorvastatin", "lipitor"],
    ),
    Interaction(
        drugs=("grapefruit juice", "calcium channel blockers"),
        severity="MONITOR",
        mechanism="Pharmacokinetic  intestinal CYP3A4 inhibition raises felodipine/nifedipine/amlodipine levels",
        effect="Enhanced antihypertensive effect; hypotension; tachycardia; oedema",
        management="Advise patients to avoid grapefruit juice. Effect most pronounced with felodipine (up to 3-fold increase).",
        aliases_a=["grapefruit juice", "grapefruit"],
        aliases_b=["felodipine", "nifedipine", "procardia", "amlodipine", "norvasc", "nimodipine"],
    ),
]


#  Lookup engine 

def build_alias_map():
    """Build flat name  list[Interaction] lookup."""
    lookup = {}
    for iact in INTERACTIONS:
        all_names_a = [iact.drugs[0]] + iact.aliases_a
        all_names_b = [iact.drugs[1]] + iact.aliases_b
        for name in all_names_a + all_names_b:
            key = name.strip().lower()
            if key not in lookup:
                lookup[key] = []
            if iact not in lookup[key]:
                lookup[key].append(iact)
    return lookup

ALIAS_MAP = build_alias_map()


def normalise(name: str) -> str:
    return name.strip().lower()


def find_drugs_matching(name: str) -> list[str]:
    """Return all keys in ALIAS_MAP that match the query (exact or substring)."""
    key = normalise(name)
    direct = [key] if key in ALIAS_MAP else []
    partial = [k for k in ALIAS_MAP if key in k or k in key]
    seen = set()
    result = []
    for k in direct + partial:
        if k not in seen:
            seen.add(k)
            result.append(k)
    return result


def check_interactions(drug_names: list) -> dict:
    """
    Given a list of drug names, return all pairwise interactions found.
    Returns dict with 'pairs' list and severity summary.
    """
    results = []
    seen_pairs = set()
    resolved = {}  # input name  matched alias keys

    for name in drug_names:
        matched = find_drugs_matching(name)
        resolved[name] = matched

    drug_list = list(drug_names)
    for i in range(len(drug_list)):
        for j in range(i + 1, len(drug_list)):
            a, b = drug_list[i], drug_list[j]
            keys_a = resolved.get(a, [])
            keys_b = resolved.get(b, [])
            for ka in keys_a:
                for kb in keys_b:
                    for iact in ALIAS_MAP.get(ka, []):
                        pair_id = id(iact)
                        all_a = [iact.drugs[0]] + iact.aliases_a
                        all_b = [iact.drugs[1]] + iact.aliases_b
                        all_names = [n.lower() for n in all_a + all_b]
                        if ka in all_names and kb in all_names and ka != kb:
                            if pair_id not in seen_pairs:
                                seen_pairs.add(pair_id)
                                results.append({
                                    "drug_a": a,
                                    "drug_b": b,
                                    "interaction": iact,
                                })

    severity_order = {"CONTRAINDICATED": 0, "SERIOUS": 1, "MONITOR": 2, "MINOR": 3}
    results.sort(key=lambda x: severity_order.get(x["interaction"].severity, 99))

    counts = {"CONTRAINDICATED": 0, "SERIOUS": 0, "MONITOR": 0, "MINOR": 0}
    for r in results:
        sev = r["interaction"].severity
        if sev in counts:
            counts[sev] += 1

    return {
        "drugs": drug_names,
        "pairs_checked": len(drug_list) * (len(drug_list) - 1) // 2,
        "interactions_found": results,
        "counts": counts,
        "resolved": resolved,
    }


SEVERITY_ICON = {
    "CONTRAINDICATED": "",
    "SERIOUS": "",
    "MONITOR": " ",
    "MINOR": " ",
}

def print_report(result: dict):
    SEP = "=" * 72
    print(f"\n{SEP}")
    print("  DRUG INTERACTION CHECKER")
    print(f"  Drugs: {', '.join(d.title() for d in result['drugs'])}")
    print(SEP)

    if not result["interactions_found"]:
        print("\n   No interactions found between the listed drugs.")
        print("     Note: absence from this database does not guarantee safety.")
    else:
        for r in result["interactions_found"]:
            sev = r["interaction"].severity
            icon = SEVERITY_ICON.get(sev, "")
            print(f"\n  {icon} [{sev}]  {r['drug_a'].title()}    {r['drug_b'].title()}")
            print(f"     Mechanism  : {r['interaction'].mechanism}")
            print(f"     Effect     : {r['interaction'].effect}")
            print(f"     Management : {r['interaction'].management}")

    c = result["counts"]
    print(f"\n  {''*70}")
    print(f"  Summary: {len(result['interactions_found'])} interaction(s) found in {result['pairs_checked']} pair(s) checked")
    if c["CONTRAINDICATED"]: print(f"     CONTRAINDICATED : {c['CONTRAINDICATED']}")
    if c["SERIOUS"]:         print(f"     SERIOUS         : {c['SERIOUS']}")
    if c["MONITOR"]:         print(f"      MONITOR         : {c['MONITOR']}")
    if c["MINOR"]:           print(f"      MINOR           : {c['MINOR']}")
    print(f"\n    For educational use only. Not a substitute for clinical judgment.")
    print(f"  Sources: Medscape, BNF, AAFP AFP, FDA drug labeling, published literature.")
    print(SEP + "\n")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        drugs = sys.argv[1:]
    else:
        print("Drug Interaction Checker")
        raw = input("Enter drug names (comma-separated): ")
        drugs = [d.strip() for d in raw.split(",") if d.strip()]
    if drugs:
        result = check_interactions(drugs)
        print_report(result)
