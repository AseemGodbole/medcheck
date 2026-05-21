"""
2023 AGS Beers Criteria Checker
Based on: American Geriatrics Society 2023 Updated AGS Beers Criteria
          J Am Geriatr Soc. 2023;71(7):2052-2081. doi:10.1111/jgs.18372

For use in adults aged 65 years and older.

Tables covered:
  Table 2   Potentially Inappropriate Medications (PIMs)  always avoid
  Table 3   PIMs in patients with certain diseases/syndromes
  Table 4   Use with Caution
  Table 5   Drug-Drug Interactions to Avoid
  Table 6   Renal Dose Adjustment needed

  For educational/informational purposes only. Not a substitute for clinical judgment.
"""

from dataclasses import dataclass, field

#  Data structures 

@dataclass
class BeersDrug:
    names: list[str]           # generic + brand names (all lowercase)
    table: str                 # "2", "3", "4", "5", "6"
    category: str              # organ system or drug class
    recommendation: str        # Avoid / Use with Caution / Avoid in [condition]
    rationale: str             # why it's on the list
    concern: str               # primary adverse effect concern
    quality_of_evidence: str   # High / Moderate / Low
    strength: str              # Strong / Weak
    conditions: list[str] = field(default_factory=list)  # for Table 3
    renal_threshold: str = ""  # for Table 6 (e.g. "CrCl < 30 mL/min")


#  Database 
# Table 2 = always PIMs; Table 3 = condition-specific; Table 4 = caution;
# Table 6 = renal adjustment.

BEERS_DATABASE: list[BeersDrug] = [

    #  TABLE 2: Always Potentially Inappropriate 

    # Anticholinergics
    BeersDrug(
        names=["first-generation antihistamines", "brompheniramine", "carbinoxamine",
               "chlorpheniramine", "chlorpheniramine maleate", "clemastine", "cyproheptadine",
               "dexbrompheniramine", "dexchlorpheniramine", "dimenhydrinate", "diphenhydramine",
               "benadryl", "doxylamine", "hydroxyzine", "meclizine", "promethazine",
               "phenergan", "pyrilamine", "triprolidine"],
        table="2", category="Anticholinergics  1st gen antihistamines",
        recommendation="Avoid",
        rationale="Highly anticholinergic; clearance reduced with advanced age, increasing risk of confusion, dry mouth, constipation, and other anticholinergic effects.",
        concern="Confusion, dry mouth, constipation, urinary retention; risk of falls",
        quality_of_evidence="Moderate", strength="Strong",
    ),
    BeersDrug(
        names=["antiparkinson agents", "benztropine", "cogentin", "trihexyphenidyl", "artane",
               "biperiden", "procyclidine"],
        table="2", category="Anticholinergics  Antiparkinson agents",
        recommendation="Avoid",
        rationale="Not recommended for prevention of EPS with antipsychotics; more effective agents available.",
        concern="Anticholinergic adverse effects; confusion",
        quality_of_evidence="Moderate", strength="Strong",
    ),
    BeersDrug(
        names=["antispasmodics", "belladonna alkaloids", "belladonna", "clidinium-chlordiazepoxide",
               "librax", "dicyclomine", "bentyl", "dicycloverine", "hyoscyamine", "levsin",
               "methscopolamine", "propantheline", "pro-banthine", "scopolamine"],
        table="2", category="Anticholinergics  Antispasmodics",
        recommendation="Avoid (except short-term palliative use)",
        rationale="Highly anticholinergic; uncertain effectiveness.",
        concern="Anticholinergic effects; unclear benefit",
        quality_of_evidence="Moderate", strength="Strong",
    ),
    BeersDrug(
        names=["antithrombotics", "dipyridamole", "persantine", "ticlopidine"],
        table="2", category="Antithrombotics",
        recommendation="Avoid",
        rationale="Safer alternatives available; dipyridamole may cause orthostatic hypotension.",
        concern="Orthostatic hypotension; safer alternatives available",
        quality_of_evidence="Moderate", strength="Strong",
    ),
    BeersDrug(
        names=["aspirin for primary prevention"],
        table="2", category="Cardiovascular  Aspirin",
        recommendation="Avoid initiating for primary cardiovascular prevention",
        rationale="Lack of net benefit; increased risk of major bleeding; consistent with USPSTF 2022 guidance.",
        concern="Major bleeding risk without clear cardiovascular benefit in primary prevention",
        quality_of_evidence="High", strength="Strong",
    ),
    BeersDrug(
        names=["warfarin", "coumadin"],
        table="2", category="Anticoagulants",
        recommendation="Avoid initiating; prefer DOACs unless contraindicated",
        rationale="DOACs have a more favorable benefit-risk profile; long-term warfarin users may continue based on clinical judgment.",
        concern="Bleeding risk; complex monitoring; drug/food interactions",
        quality_of_evidence="High", strength="Strong",
    ),
    BeersDrug(
        names=["rivaroxaban", "xarelto"],
        table="2", category="Anticoagulants",
        recommendation="Avoid for long-term treatment of NVAF or VTE; consider alternatives",
        rationale="Higher risk of major and GI bleeding vs other DOACs. Consider if once-daily dosing is required.",
        concern="Higher GI bleeding risk compared with other DOACs",
        quality_of_evidence="Moderate", strength="Strong",
    ),
    BeersDrug(
        names=["digoxin", "lanoxin"],
        table="2", category="Cardiovascular  Antiarrhythmics",
        recommendation="Avoid as first-line for AF or HF; if used, keep dose 0.125 mg/day",
        rationale="High risk of toxicity; low therapeutic index; decreased renal clearance. Caution when discontinuing in HFrEF.",
        concern="Digoxin toxicity; narrow therapeutic index",
        quality_of_evidence="Moderate", strength="Strong",
    ),
    BeersDrug(
        names=["amiodarone", "cordarone"],
        table="2", category="Cardiovascular  Antiarrhythmics",
        recommendation="Avoid as first-line for AF unless HF or LVH",
        rationale="Multiple toxicities (thyroid, pulmonary, hepatic, GI, ocular, skin); safer alternatives exist for most patients.",
        concern="Pulmonary, thyroid, hepatic, ocular toxicity",
        quality_of_evidence="High", strength="Strong",
    ),
    BeersDrug(
        names=["dronedarone", "multaq"],
        table="2", category="Cardiovascular  Antiarrhythmics",
        recommendation="Avoid in patients with NYHA class III or IV HF or recent decompensation",
        rationale="Increased risk of mortality and stroke in patients with permanent AF or severe HF.",
        concern="Increased mortality and stroke risk in severe HF",
        quality_of_evidence="High", strength="Strong",
    ),
    BeersDrug(
        names=["nifedipine", "procardia", "adalat"],
        table="2", category="Cardiovascular  CCBs",
        recommendation="Avoid immediate-release formulation",
        rationale="Potential for hypotension; risk of precipitating myocardial ischemia.",
        concern="Hypotension; myocardial ischemia",
        quality_of_evidence="High", strength="Strong",
    ),
    BeersDrug(
        names=["spironolactone > 25mg/day"],
        table="2", category="Cardiovascular",
        recommendation="Avoid doses > 25 mg/day in HF",
        rationale="Risk of hyperkalemia in HF patients; higher doses increase risk.",
        concern="Hyperkalemia",
        quality_of_evidence="Moderate", strength="Strong",
    ),
    BeersDrug(
        names=["androgens", "methyltestosterone", "testosterone", "testosterone topical"],
        table="2", category="Endocrine",
        recommendation="Avoid unless indicated for moderate-to-severe hypogonadism",
        rationale="Potential for cardiac adverse effects; may worsen benign prostatic hyperplasia and prostate cancer. Updated: potential risks (not contraindicated) in prostate cancer.",
        concern="Cardiac adverse effects; worsening BPH; prostate cancer risk",
        quality_of_evidence="Moderate", strength="Weak",
    ),
    BeersDrug(
        names=["desiccated thyroid", "thyroid extract"],
        table="2", category="Endocrine",
        recommendation="Avoid",
        rationale="Concerns about cardiac effects; safer alternatives available.",
        concern="Cardiac effects; erratic absorption",
        quality_of_evidence="Low", strength="Strong",
    ),
    BeersDrug(
        names=["estrogen systemic", "conjugated estrogens", "estradiol oral", "estropipate",
               "medroxyprogesterone"],
        table="2", category="Endocrine  Estrogens",
        recommendation="Avoid systemic estrogen (oral and patch); vaginal topical is acceptable",
        rationale="Evidence of carcinogenic potential; lack of cardioprotective effect. Risks > benefits for women starting HRT after age 60.",
        concern="Breast cancer, cardiovascular events, DVT",
        quality_of_evidence="High", strength="Strong",
    ),
    BeersDrug(
        names=["sulfonylureas", "chlorpropamide", "diabinese", "glibenclamide", "glyburide",
               "diabeta", "micronase", "glimepiride", "amaryl", "glipizide", "glucotrol",
               "gliclazide"],
        table="2", category="Endocrine  Sulfonylureas",
        recommendation="Avoid; if necessary, short-acting preferred",
        rationale="Prolonged hypoglycemia; also associated with CV events, all-cause mortality, CV death, and ischemic stroke; safer alternatives available.",
        concern="Prolonged hypoglycemia; CV events; all-cause mortality",
        quality_of_evidence="High", strength="Strong",
    ),
    BeersDrug(
        names=["sliding scale insulin"],
        table="2", category="Endocrine  Insulin",
        recommendation="Avoid in long-term care; use only in acute settings",
        rationale="Higher risk of hypoglycemia; no improvement in hyperglycemia management.",
        concern="Hypoglycemia",
        quality_of_evidence="Moderate", strength="Strong",
    ),
    BeersDrug(
        names=["megestrol", "megace"],
        table="2", category="Endocrine",
        recommendation="Avoid",
        rationale="Minimal effect on weight in older adults; increases risk of thrombotic events and possibly death.",
        concern="Thrombotic events; fluid retention; adrenal suppression",
        quality_of_evidence="Moderate", strength="Strong",
    ),
    BeersDrug(
        names=["growth hormone", "somatropin"],
        table="2", category="Endocrine",
        recommendation="Avoid except as hormone replacement after pituitary gland removal",
        rationale="Effect on body composition is small; risk of edema, arthralgia, carpal tunnel, gynecomastia, glucose intolerance.",
        concern="Edema, arthralgia, glucose intolerance",
        quality_of_evidence="High", strength="Strong",
    ),
    BeersDrug(
        names=["gastrointestinal antispasmodics", "hyoscine butylbromide", "buscopan",
               "clidinium", "dicyclomine", "bentyl", "hyoscyamine", "levsin",
               "methscopolamine", "propantheline", "belladonna"],
        table="2", category="GI  Antispasmodics",
        recommendation="Avoid (except in palliative care)",
        rationale="Highly anticholinergic with uncertain effectiveness.",
        concern="Anticholinergic adverse effects",
        quality_of_evidence="Moderate", strength="Strong",
    ),
    BeersDrug(
        names=["metoclopramide", "reglan"],
        table="2", category="GI",
        recommendation="Avoid unless for gastroparesis",
        rationale="Risk of EPS including tardive dyskinesia; risk may be greater and recovery less likely in older adults.",
        concern="EPS; tardive dyskinesia",
        quality_of_evidence="Moderate", strength="Strong",
    ),
    BeersDrug(
        names=["mineral oil oral"],
        table="2", category="GI  Laxatives",
        recommendation="Avoid",
        rationale="Potential for aspiration and adverse effects; safer alternatives available.",
        concern="Aspiration pneumonia",
        quality_of_evidence="Moderate", strength="Strong",
    ),
    BeersDrug(
        names=["proton pump inhibitors", "ppi", "omeprazole", "prilosec", "pantoprazole",
               "protonix", "lansoprazole", "prevacid", "esomeprazole", "nexium",
               "rabeprazole", "aciphex", "dexlansoprazole", "dexilant"],
        table="2", category="GI  PPIs",
        recommendation="Avoid scheduled use > 8 weeks unless indicated (GERD, Barrett's, high-risk NSAID use)",
        rationale="Risk of C. difficile, fractures, pneumonia, GI malignancies; risk may increase with duration.",
        concern="C. difficile; bone fractures; pneumonia; GI malignancies",
        quality_of_evidence="Moderate", strength="Strong",
    ),
    BeersDrug(
        names=["trimethoprim-sulfamethoxazole", "tmp-smx", "sulfamethoxazole-trimethoprim",
               "co-trimoxazole", "bactrim", "septra"],
        table="2", category="GI / Anti-infective",
        recommendation="Avoid in patients with CrCl < 30 mL/min",
        rationale="Risk of hyperkalemia, especially in patients on ACE inhibitors, ARBs, or potassium-sparing diuretics.",
        concern="Hyperkalemia; renal impairment",
        quality_of_evidence="Moderate", strength="Strong",
        renal_threshold="CrCl < 30 mL/min"
    ),
    BeersDrug(
        names=["antidepressants highly anticholinergic", "amitriptyline", "elavil",
               "amoxapine", "asendin", "clomipramine", "anafranil", "desipramine",
               "norpramin", "doxepin >6mg/day", "imipramine", "tofranil",
               "nortriptyline", "pamelor", "protriptyline", "trimipramine", "surmontil",
               "paroxetine", "paxil"],
        table="2", category="CNS  Antidepressants (anticholinergic)",
        recommendation="Avoid",
        rationale="Highly anticholinergic; sedating; cause orthostatic hypotension. Specifically applies to highly anticholinergic antidepressants per 2023 update.",
        concern="Anticholinergic effects; sedation; orthostatic hypotension; falls",
        quality_of_evidence="High", strength="Strong",
    ),
    BeersDrug(
        names=["antipsychotics", "haloperidol", "haldol", "olanzapine", "zyprexa",
               "risperidone", "risperdal", "quetiapine", "seroquel", "aripiprazole",
               "abilify", "ziprasidone", "geodon", "chlorpromazine", "thorazine",
               "thioridazine", "mellaril", "perphenazine", "fluphenazine",
               "typical antipsychotics", "atypical antipsychotics"],
        table="2", category="CNS  Antipsychotics",
        recommendation="Avoid for behavioral problems of dementia/delirium unless non-pharmacological options have failed and patient is a threat to self or others",
        rationale="Increased risk of cerebrovascular accident, cognitive decline, and mortality in older adults with dementia. 2023: strengthened language on dementia/delirium risk.",
        concern="Stroke; cognitive decline; mortality in dementia; EPS; falls",
        quality_of_evidence="Moderate", strength="Strong",
    ),
    BeersDrug(
        names=["benzodiazepines", "alprazolam", "xanax", "clonazepam", "klonopin",
               "clorazepate", "tranxene", "diazepam", "valium", "flurazepam",
               "lorazepam", "ativan", "oxazepam", "temazepam", "triazolam", "halcion",
               "chlordiazepoxide"],
        table="2", category="CNS  Benzodiazepines",
        recommendation="Avoid",
        rationale="Older adults have increased sensitivity to benzodiazepines and slower metabolism. Cognitive impairment, delirium, falls, fractures, MVA. 2023: increased warning for opioid co-administration.",
        concern="Cognitive impairment; delirium; falls; fractures; MVA; overdose risk with opioids",
        quality_of_evidence="High", strength="Strong",
    ),
    BeersDrug(
        names=["z-drugs", "eszopiclone", "lunesta", "zaleplon", "sonata", "zolpidem",
               "ambien", "zopiclone"],
        table="2", category="CNS  Non-BZD hypnotics (Z-drugs)",
        recommendation="Avoid",
        rationale="Similar adverse effects to benzodiazepines in older adults; increased ER visits/hospitalizations; MVA; falls/fractures.",
        concern="Delirium; falls; fractures; MVA; cognitive impairment",
        quality_of_evidence="Moderate", strength="Strong",
    ),
    BeersDrug(
        names=["meprobamate", "equanil"],
        table="2", category="CNS  Barbiturates/anxiolytics",
        recommendation="Avoid",
        rationale="High rate of physical dependence; sedating; many safety concerns.",
        concern="Dependence; sedation",
        quality_of_evidence="Moderate", strength="Strong",
    ),
    BeersDrug(
        names=["ergot mesylates", "isoxsuprine"],
        table="2", category="CNS  Ergot mesylates",
        recommendation="Avoid",
        rationale="Lack of efficacy.",
        concern="Lack of efficacy",
        quality_of_evidence="High", strength="Strong",
    ),
    BeersDrug(
        names=["skeletal muscle relaxants", "carisoprodol", "soma", "chlorzoxazone",
               "cyclobenzaprine", "flexeril", "metaxalone", "skelaxin", "methocarbamol",
               "robaxin", "orphenadrine", "norflex"],
        table="2", category="Musculoskeletal  Muscle Relaxants",
        recommendation="Avoid (does not apply to baclofen/tizanidine for spasticity)",
        rationale="Poorly tolerated; anticholinergic adverse effects; sedation; increased fractures. 2023: clarified that baclofen/tizanidine for spasticity are excluded.",
        concern="Anticholinergic effects; sedation; fractures",
        quality_of_evidence="Moderate", strength="Strong",
    ),
    BeersDrug(
        names=["nsaids oral", "nsaid", "aspirin analgesic", "celecoxib", "celebrex",
               "diclofenac", "voltaren", "etodolac", "fenoprofen", "ibuprofen", "advil",
               "motrin", "indomethacin", "indocin", "ketoprofen", "ketorolac", "toradol",
               "mefenamic acid", "meloxicam", "mobic", "nabumetone", "naproxen",
               "aleve", "naprosyn", "oxaprozin", "piroxicam", "feldene", "sulindac",
               "tolmetin"],
        table="2", category="Pain  NSAIDs",
        recommendation="Avoid chronic use unless alternatives inadequate; use PPI if necessary. Avoid short-term use when drug interactions present.",
        rationale="GI bleeding/peptic ulcer disease; acute kidney injury; fluid retention; worsening heart failure. 2023: moved from Table 6, added renal dose consideration.",
        concern="GI bleeding; AKI; fluid retention; HF exacerbation; hypertension",
        quality_of_evidence="Moderate", strength="Strong",
    ),
    BeersDrug(
        names=["indomethacin", "indocin", "ketorolac oral or parenteral", "toradol"],
        table="2", category="Pain  NSAIDs (high risk)",
        recommendation="Avoid",
        rationale="Increased risk of GI bleeding/peptic ulcer disease and AKI; of all NSAIDs, indomethacin and ketorolac have most adverse effects in older adults.",
        concern="Highest GI bleeding and AKI risk among NSAIDs",
        quality_of_evidence="Moderate", strength="Strong",
    ),
    BeersDrug(
        names=["meperidine", "demerol", "pethidine"],
        table="2", category="Pain  Opioids",
        recommendation="Avoid",
        rationale="Not effective oral analgesic at commonly used doses; may cause neurotoxicity (normeperidine); safer alternatives exist.",
        concern="Neurotoxicity; seizures; confusion",
        quality_of_evidence="Moderate", strength="Strong",
    ),

    #  TABLE 3: Condition-Specific PIMs 

    BeersDrug(
        names=["anticholinergics", "diphenhydramine", "benadryl", "oxybutynin", "ditropan",
               "tolterodine", "detrol", "solifenacin", "vesicare", "darifenacin", "enablex",
               "fesoterodine", "toviaz", "trospium", "sanctura",
               "first-generation antihistamines", "tricyclic antidepressants",
               "amitriptyline", "benztropine", "cogentin"],
        table="3", category="Condition-specific  Dementia/Cognitive Impairment",
        recommendation="Avoid in patients with dementia or cognitive impairment",
        rationale="Adverse CNS effects; may induce or worsen delirium.",
        concern="Worsening cognitive function; delirium",
        quality_of_evidence="Moderate", strength="Strong",
        conditions=["Dementia", "Cognitive impairment"],
    ),
    BeersDrug(
        names=["antipsychotics", "haloperidol", "haldol", "olanzapine", "zyprexa",
               "risperidone", "risperdal", "quetiapine", "seroquel", "dextromethorphan-quinidine",
               "nuedexta"],
        table="3", category="Condition-specific  Delirium",
        recommendation="Avoid in patients with/at risk of delirium",
        rationale="May worsen or precipitate delirium. 2023: dextromethorphan/quinidine added.",
        concern="Delirium",
        quality_of_evidence="Moderate", strength="Strong",
        conditions=["Delirium", "Dementia"],
    ),
    BeersDrug(
        names=["benzodiazepines", "alprazolam", "xanax", "diazepam", "valium",
               "lorazepam", "ativan", "opioids", "z-drugs", "zolpidem", "ambien",
               "eszopiclone", "lunesta", "anticholinergics", "antiepileptics",
               "gabapentin", "neurontin", "pregabalin", "lyrica",
               "first-generation antihistamines", "skeletal muscle relaxants",
               "tricyclic antidepressants", "antipsychotics", "alcohol"],
        table="3", category="Condition-specific  Falls/Fractures",
        recommendation="Avoid in patients with history of falls or fractures",
        rationale="Increases falls risk due to sedation/CNS depression, orthostatic hypotension, or gait instability. 2023: anticholinergics added.",
        concern="Falls; fractures",
        quality_of_evidence="High", strength="Strong",
        conditions=["History of falls", "Fractures"],
    ),
    BeersDrug(
        names=["heart failure drugs", "nsaids", "ibuprofen", "naproxen", "celecoxib",
               "celebrex", "thiazolidinediones", "pioglitazone", "actos", "rosiglitazone",
               "avandia", "cilostazol", "pletal", "diltiazem", "verapamil",
               "dronedarone", "multaq", "dextromethorphan-quinidine", "nuedexta"],
        table="3", category="Condition-specific  Heart Failure",
        recommendation="Avoid in patients with heart failure",
        rationale="Potential to promote fluid retention and worsen HF. 2023: dextromethorphan-quinidine added.",
        concern="Fluid retention; HF exacerbation",
        quality_of_evidence="Moderate", strength="Strong",
        conditions=["Heart failure"],
    ),
    BeersDrug(
        names=["thiazolidinediones", "pioglitazone", "actos", "rosiglitazone", "avandia"],
        table="3", category="Condition-specific  Fractures",
        recommendation="Avoid in patients with a history of fractures",
        rationale="Thiazolidinediones are associated with bone fracture risk.",
        concern="Increased fracture risk",
        quality_of_evidence="High", strength="Strong",
        conditions=["History of fractures", "Osteoporosis"],
    ),
    BeersDrug(
        names=["antipsychotics", "haloperidol", "metoclopramide", "reglan",
               "prochlorperazine", "compazine"],
        table="3", category="Condition-specific  Parkinson's Disease",
        recommendation="Avoid in patients with Parkinson's disease",
        rationale="Dopamine receptor antagonists; likely to worsen Parkinson's symptoms. Exceptions: clozapine, pimavanserin, quetiapine.",
        concern="Worsening Parkinson's symptoms; EPS",
        quality_of_evidence="Moderate", strength="Strong",
        conditions=["Parkinson's disease"],
    ),
    BeersDrug(
        names=["testosterone", "androgens"],
        table="3", category="Condition-specific  BPH",
        recommendation="Avoid in men with BPH or urinary symptoms",
        rationale="May worsen urinary symptoms.",
        concern="Worsening BPH symptoms",
        quality_of_evidence="Moderate", strength="Strong",
        conditions=["Benign prostatic hyperplasia", "BPH", "Urinary obstruction"],
    ),
    BeersDrug(
        names=["cholinesterase inhibitors", "donepezil", "aricept", "rivastigmine",
               "exelon", "galantamine", "razadyne"],
        table="3", category="Condition-specific  Syncope",
        recommendation="Avoid in patients with a history of syncope",
        rationale="Cholinesterase inhibitors increase risk of orthostatic hypotension and bradycardia.",
        concern="Bradycardia; syncope",
        quality_of_evidence="Moderate", strength="Strong",
        conditions=["Syncope"],
    ),

    #  TABLE 4: Use with Caution 

    BeersDrug(
        names=["aspirin low dose", "aspirin 81mg"],
        table="4", category="Caution  Aspirin",
        recommendation="Use with caution in patients 80 years",
        rationale="Limited evidence of benefit; increased bleeding risk.",
        concern="Bleeding risk",
        quality_of_evidence="Low", strength="Weak",
    ),
    BeersDrug(
        names=["dabigatran", "pradaxa"],
        table="4", category="Caution  Anticoagulants",
        recommendation="Use with caution in patients 75 years or with CrCl 30-49 mL/min",
        rationale="Greater risk of major GI bleeding compared to warfarin.",
        concern="Major GI bleeding",
        quality_of_evidence="Moderate", strength="Strong",
    ),
    BeersDrug(
        names=["prasugrel", "effient"],
        table="4", category="Caution  Antiplatelets",
        recommendation="Use with caution; consider lower dose (5 mg) in patients 75 years",
        rationale="Greater risk of bleeding in older adults.",
        concern="Bleeding risk",
        quality_of_evidence="Moderate", strength="Weak",
    ),
    BeersDrug(
        names=["ticagrelor", "brilinta"],
        table="4", category="Caution  Antiplatelets",
        recommendation="Use with caution in patients 75 years",
        rationale="Greater risk of bleeding in older adults compared to clopidogrel.",
        concern="Bleeding risk",
        quality_of_evidence="Moderate", strength="Weak",
    ),
    BeersDrug(
        names=["sglt2 inhibitors", "empagliflozin", "jardiance", "canagliflozin",
               "invokana", "dapagliflozin", "farxiga"],
        table="4", category="Caution  SGLT2 inhibitors",
        recommendation="Use with caution; consider stopping if eGFR < 45 mL/min/1.73m",
        rationale="Increased risk of urinary tract infections; volume depletion; genital mycotic infections.",
        concern="UTI; volume depletion; DKA risk",
        quality_of_evidence="Moderate", strength="Strong",
    ),
    BeersDrug(
        names=["vasodilators", "alpha blockers", "doxazosin", "cardura", "prazosin",
               "terazosin", "hytrin"],
        table="4", category="Caution  Vasodilators",
        recommendation="Use with caution; avoid as antihypertensive",
        rationale="Risk of orthostatic hypotension and falls in older adults.",
        concern="Orthostatic hypotension; falls",
        quality_of_evidence="Moderate", strength="Strong",
    ),
    BeersDrug(
        names=["antidepressants", "ssri", "snri", "fluoxetine", "prozac", "sertraline",
               "zoloft", "paroxetine", "paxil", "citalopram", "celexa", "escitalopram",
               "lexapro", "fluvoxamine", "venlafaxine", "effexor", "duloxetine",
               "cymbalta", "mirtazapine", "remeron", "tricyclic antidepressants"],
        table="4", category="Caution  Antidepressants",
        recommendation="Use with caution; monitor for falls, fractures, hyponatremia",
        rationale="Risk of falls; SIADH/hyponatremia.",
        concern="Falls; SIADH; hyponatremia",
        quality_of_evidence="Moderate", strength="Strong",
    ),
    BeersDrug(
        names=["cholinesterase inhibitors", "donepezil", "aricept", "rivastigmine",
               "exelon", "galantamine", "razadyne"],
        table="4", category="Caution  Cholinesterase inhibitors",
        recommendation="Use with caution",
        rationale="Risk of syncope; bradycardia; may exacerbate COPD or asthma.",
        concern="Syncope; bradycardia; GI adverse effects",
        quality_of_evidence="Moderate", strength="Weak",
    ),
    BeersDrug(
        names=["carboplatin", "oxaliplatin", "paclitaxel", "taxol", "bortezomib",
               "velcade", "thalidomide", "lenalidomide", "revlimid"],
        table="4", category="Caution  Antineoplastics",
        recommendation="Use with caution; monitor for peripheral neuropathy",
        rationale="Increased risk of peripheral neuropathy.",
        concern="Peripheral neuropathy",
        quality_of_evidence="Moderate", strength="Strong",
    ),

    #  TABLE 6: Renal Dose Adjustment 

    BeersDrug(
        names=["apixaban", "eliquis"],
        table="6", category="Renal  Anticoagulants",
        recommendation="Dose reduction required per labeling based on age, weight, and SCr",
        rationale="Increased drug exposure and bleeding risk with renal impairment.",
        concern="Bleeding",
        quality_of_evidence="Moderate", strength="Strong",
        renal_threshold="Varies by age/weight/SCr  follow labeling"
    ),
    BeersDrug(
        names=["dabigatran", "pradaxa"],
        table="6", category="Renal  Anticoagulants",
        recommendation="Avoid if CrCl < 30 mL/min",
        rationale="Significantly increased drug exposure and bleeding risk.",
        concern="Bleeding; drug accumulation",
        quality_of_evidence="High", strength="Strong",
        renal_threshold="CrCl < 30 mL/min"
    ),
    BeersDrug(
        names=["rivaroxaban", "xarelto"],
        table="6", category="Renal  Anticoagulants",
        recommendation="Avoid for NVAF if CrCl < 50 mL/min; avoid for VTE if CrCl < 30 mL/min",
        rationale="Drug accumulation and bleeding risk.",
        concern="Bleeding",
        quality_of_evidence="Moderate", strength="Strong",
        renal_threshold="CrCl < 50 mL/min (NVAF); CrCl < 30 mL/min (VTE)"
    ),
    BeersDrug(
        names=["edoxaban", "savaysa"],
        table="6", category="Renal  Anticoagulants",
        recommendation="Avoid if CrCl > 95 mL/min or < 15 mL/min",
        rationale="Reduced efficacy at high CrCl; drug accumulation at very low CrCl.",
        concern="Reduced efficacy (high CrCl) or drug accumulation (very low CrCl)",
        quality_of_evidence="Moderate", strength="Strong",
        renal_threshold="CrCl > 95 mL/min OR CrCl < 15 mL/min"
    ),
    BeersDrug(
        names=["enoxaparin", "lovenox"],
        table="6", category="Renal  Anticoagulants",
        recommendation="Reduce dose if CrCl < 30 mL/min",
        rationale="Accumulation with renal impairment.",
        concern="Bleeding",
        quality_of_evidence="High", strength="Strong",
        renal_threshold="CrCl < 30 mL/min"
    ),
    BeersDrug(
        names=["baclofen", "lioresal"],
        table="6", category="Renal  Muscle relaxants",
        recommendation="Avoid or use low doses if CrCl < 30 mL/min",
        rationale="Drug accumulation; risk of encephalopathy. 2023: newly added.",
        concern="Encephalopathy; sedation",
        quality_of_evidence="Moderate", strength="Strong",
        renal_threshold="CrCl < 30 mL/min"
    ),
    BeersDrug(
        names=["colchicine", "colcrys"],
        table="6", category="Renal  Antigout",
        recommendation="Reduce dose; avoid prolonged use if CrCl < 30 mL/min",
        rationale="Accumulation may cause myopathy, neuromyopathy.",
        concern="Myopathy; neuromyopathy",
        quality_of_evidence="Moderate", strength="Strong",
        renal_threshold="CrCl < 30 mL/min"
    ),
    BeersDrug(
        names=["gabapentin", "neurontin", "gabapentin enacarbil", "horizant"],
        table="6", category="Renal  Anticonvulsants",
        recommendation="Reduce dose if CrCl < 60 mL/min",
        rationale="Risk of respiratory depression, sedation, falls, confusion.",
        concern="Respiratory depression; sedation; falls",
        quality_of_evidence="Moderate", strength="Strong",
        renal_threshold="CrCl < 60 mL/min"
    ),
    BeersDrug(
        names=["pregabalin", "lyrica"],
        table="6", category="Renal  Anticonvulsants",
        recommendation="Reduce dose if CrCl < 60 mL/min",
        rationale="Sedation; dizziness; falls; respiratory depression.",
        concern="Sedation; respiratory depression; falls",
        quality_of_evidence="Moderate", strength="Strong",
        renal_threshold="CrCl < 60 mL/min"
    ),
    BeersDrug(
        names=["duloxetine", "cymbalta"],
        table="6", category="Renal  SNRI",
        recommendation="Avoid if CrCl < 30 mL/min",
        rationale="Increased side effects due to accumulation; GI effects predominate.",
        concern="GI adverse effects; drug accumulation",
        quality_of_evidence="Moderate", strength="Strong",
        renal_threshold="CrCl < 30 mL/min"
    ),
    BeersDrug(
        names=["nsaids", "ibuprofen", "naproxen", "celecoxib", "celebrex",
               "diclofenac", "meloxicam", "indomethacin", "indocin", "ketorolac"],
        table="6", category="Renal  NSAIDs",
        recommendation="Avoid if CrCl < 30 mL/min",
        rationale="Acute kidney injury risk. 2023: added to Table 6.",
        concern="Acute kidney injury",
        quality_of_evidence="Moderate", strength="Strong",
        renal_threshold="CrCl < 30 mL/min"
    ),
    BeersDrug(
        names=["trimethoprim-sulfamethoxazole", "tmp-smx", "bactrim", "septra",
               "sulfamethoxazole-trimethoprim", "co-trimoxazole"],
        table="6", category="Renal  Antibiotics",
        recommendation="Avoid if CrCl < 30 mL/min",
        rationale="Hyperkalemia risk, especially with ACE inhibitors or ARBs.",
        concern="Hyperkalemia",
        quality_of_evidence="Moderate", strength="Strong",
        renal_threshold="CrCl < 30 mL/min"
    ),
    BeersDrug(
        names=["ranitidine", "zantac", "famotidine", "pepcid", "nizatidine"],
        table="6", category="Renal  H2 receptor antagonists",
        recommendation="Reduce dose if CrCl < 50 mL/min",
        rationale="CNS adverse effects due to accumulation.",
        concern="CNS adverse effects; confusion",
        quality_of_evidence="Moderate", strength="Strong",
        renal_threshold="CrCl < 50 mL/min"
    ),
]


#  Lookup logic 

def lookup_drug(name: str) -> list[BeersDrug]:
    """Return all Beers entries that match a drug name (generic or brand)."""
    key = name.strip().lower()
    matches = []
    seen_ids = set()

    for entry in BEERS_DATABASE:
        entry_id = id(entry)
        if entry_id in seen_ids:
            continue
        for n in entry.names:
            if key == n or key in n or n in key:
                matches.append(entry)
                seen_ids.add(entry_id)
                break

    return matches


TABLE_LABELS = {
    "2": "Table 2  Potentially Inappropriate Medication (avoid)",
    "3": "Table 3  Avoid in specific disease/syndrome",
    "4": "Table 4  Use with Caution",
    "5": "Table 5  Drug-Drug Interaction",
    "6": "Table 6  Renal Dose Adjustment Required",
}


def check_drugs(drug_names: list[str]) -> dict:
    all_results = []
    flagged_count = 0

    for name in drug_names:
        matches = lookup_drug(name)
        if matches:
            flagged_count += 1
        all_results.append({
            "input": name,
            "flagged": bool(matches),
            "entries": matches,
        })

    return {
        "results": all_results,
        "total_drugs": len(drug_names),
        "flagged": flagged_count,
    }


def print_report(data: dict):
    print("\n" + "=" * 70)
    print("   2023 AGS Beers Criteria Checker  (Adults 65 years)")
    print("=" * 70)

    for drug in data["results"]:
        print(f"\n   {drug['input'].upper()} ")
        if not drug["flagged"]:
            print("   Not found on Beers Criteria list")
        else:
            for entry in drug["entries"]:
                print(f"\n    [{TABLE_LABELS.get(entry.table, 'Table ' + entry.table)}]")
                print(f"     Category     : {entry.category}")
                print(f"     Recommendation: {entry.recommendation}")
                print(f"     Concern       : {entry.concern}")
                print(f"     Rationale     : {entry.rationale}")
                if entry.conditions:
                    print(f"     Conditions    : {', '.join(entry.conditions)}")
                if entry.renal_threshold:
                    print(f"     Renal cutoff  : {entry.renal_threshold}")
                print(f"     Evidence      : {entry.quality_of_evidence} quality / {entry.strength} recommendation")

    print("\n" + "-" * 70)
    flagged = data["flagged"]
    total = data["total_drugs"]
    print(f"  Summary: {flagged}/{total} drug(s) flagged on Beers Criteria")
    if flagged:
        print("    Review flagged medications. Consider safer alternatives or")
        print("     deprescribing where clinically appropriate.")
    else:
        print("   No Beers Criteria concerns identified for the drugs checked.")
    print("\n    For adults 65 years. For educational use only.")
    print("     Not a substitute for clinical judgment.")
    print("     Source: AGS Beers Criteria 2023, J Am Geriatr Soc. 71(7):2052-2081")
    print("=" * 70 + "\n")


#  Main 

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        drugs = sys.argv[1:]
    else:
        print("2023 Beers Criteria Checker  enter drug names separated by commas:")
        raw = input("> ")
        drugs = [d.strip() for d in raw.split(",") if d.strip()]

    if not drugs:
        print("No drugs entered.")
        sys.exit(0)

    result = check_drugs(drugs)
    print_report(result)
