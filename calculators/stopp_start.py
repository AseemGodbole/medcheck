"""
STOPP/START Version 3 Criteria Checker (2023)
Source: O'Mahony D et al. Eur Geriatr Med. 2023;14(4):625-632
        doi:10.1007/s41999-023-00777-y  (Open Access, CC BY 4.0)

STOPP = Screening Tool of Older Persons' Prescriptions (drugs to STOP)
START = Screening Tool to Alert to Right Treatment (drugs to START / consider)

For adults aged 65 years and older.
  For educational/informational purposes only.
"""

from dataclasses import dataclass, field

@dataclass
class STOPPEntry:
    names: list          # drug names / classes (all lowercase)
    section: str         # e.g. "A  Cardiovascular"
    criterion_id: str    # e.g. "A1"
    condition: str       # when does this apply?
    rationale: str       # why stop
    brand_examples: list = field(default_factory=list)

@dataclass
class STARTEntry:
    drug_class: str      # what should be started
    section: str
    criterion_id: str
    indication: str      # when is it indicated?
    rationale: str
    examples: list = field(default_factory=list)


#  STOPP DATABASE 
# Section A: General/Overarching
# Section B: Cardiovascular
# Section C: Coagulation / Anticoagulation
# Section D: CNS / Psychotropics
# Section E: Renal
# Section F: Gastrointestinal
# Section G: Respiratory
# Section H: Musculoskeletal
# Section I: Urogenital
# Section J: Endocrine
# Section K: Falls Risk-Increasing Drugs
# Section L: Analgesics
# Section M: Anticholinergic Burden

STOPP_DATABASE: list[STOPPEntry] = [

    #  Section A: General 
    STOPPEntry(
        names=["any drug"],
        section="A  General", criterion_id="A1",
        condition="No clear clinical indication for the drug",
        rationale="Any drug prescribed without an evidence-based clinical indication should be stopped.",
    ),
    STOPPEntry(
        names=["any drug"],
        section="A  General", criterion_id="A2",
        condition="Prescribed beyond the recommended duration",
        rationale="Drug prescribed beyond the recommended treatment duration should be reviewed and stopped if appropriate.",
    ),
    STOPPEntry(
        names=["duplicate drug class"],
        section="A  General", criterion_id="A3",
        condition="Duplicate drug classes prescribed (e.g. two NSAIDs, two SSRIs)",
        rationale="Duplicate prescribing within a drug class increases adverse drug reaction risk without therapeutic benefit.",
    ),

    #  Section B: Cardiovascular 
    STOPPEntry(
        names=["digoxin", "lanoxin"],
        section="B  Cardiovascular", criterion_id="B1",
        condition="Atrial fibrillation without heart failure  used for rate control",
        rationale="Digoxin is not recommended for rate control in AF without heart failure; safer alternatives (beta-blockers, CCBs) are available.",
    ),
    STOPPEntry(
        names=["amiodarone", "cordarone"],
        section="B  Cardiovascular", criterion_id="B2",
        condition="Atrial fibrillation  as first-line rate or rhythm control",
        rationale="Amiodarone has significant long-term toxicities (thyroid, pulmonary, hepatic, ocular, peripheral neuropathy) compared to safer alternatives.",
    ),
    STOPPEntry(
        names=["loop diuretics", "furosemide", "lasix", "frusemide", "bumetanide", "torasemide"],
        section="B  Cardiovascular", criterion_id="B3",
        condition="As first-line monotherapy for hypertension",
        rationale="Safer, more effective first-line antihypertensives available (ACE-I, ARB, CCB, thiazide).",
    ),
    STOPPEntry(
        names=["loop diuretics", "furosemide", "lasix", "frusemide", "bumetanide"],
        section="B  Cardiovascular", criterion_id="B4",
        condition="Dependent ankle oedema without clinical, biochemical or radiological evidence of heart failure, liver failure, nephrotic syndrome or renal failure",
        rationale="Leg elevation or compression stockings are safer; loop diuretics cause electrolyte imbalance and dehydration.",
    ),
    STOPPEntry(
        names=["thiazide diuretics", "bendroflumethiazide", "hydrochlorothiazide", "hctz",
                "chlortalidone", "indapamide", "metolazone"],
        section="B  Cardiovascular", criterion_id="B5",
        condition="History of gout",
        rationale="Thiazides can exacerbate gout; safer antihypertensives available.",
    ),
    STOPPEntry(
        names=["beta-blockers", "atenolol", "tenormin", "metoprolol", "lopressor", "toprol",
                "bisoprolol", "carvedilol", "propranolol", "nadolol", "nebivolol"],
        section="B  Cardiovascular", criterion_id="B6",
        condition="In combination with verapamil or diltiazem",
        rationale="Risk of heart block, bradycardia, and cardiac arrest.",
    ),
    STOPPEntry(
        names=["diltiazem", "cardizem", "verapamil", "calan", "isoptin",
                "non-dihydropyridine calcium channel blockers"],
        section="B  Cardiovascular", criterion_id="B7",
        condition="Heart failure with reduced ejection fraction (HFrEF)",
        rationale="May worsen heart failure and increase mortality in HFrEF.",
    ),
    STOPPEntry(
        names=["calcium channel blockers", "nifedipine", "procardia", "amlodipine", "norvasc",
                "felodipine", "lercanidipine", "diltiazem", "verapamil"],
        section="B  Cardiovascular", criterion_id="B8",
        condition="Chronic constipation",
        rationale="Calcium channel blockers worsen constipation.",
    ),
    STOPPEntry(
        names=["alpha-1 blockers", "doxazosin", "cardura", "prazosin", "terazosin", "hytrin",
                "tamsulosin", "alfuzosin"],
        section="B  Cardiovascular", criterion_id="B9",
        condition="Orthostatic hypotension or frequent falls",
        rationale="Alpha-1 blockers worsen orthostatic hypotension and increase falls risk.",
    ),
    STOPPEntry(
        names=["aspirin", "clopidogrel", "plavix", "prasugrel", "effient",
                "ticagrelor", "brilinta", "antiplatelet"],
        section="B  Cardiovascular", criterion_id="B10",
        condition="Concurrent use of oral anticoagulant  no clear indication for dual therapy",
        rationale="Increased risk of major bleeding without clear incremental antithrombotic benefit in most cases.",
    ),
    STOPPEntry(
        names=["aspirin"],
        section="B  Cardiovascular", criterion_id="B11",
        condition="No history of coronary, cerebrovascular or peripheral arterial disease (primary prevention)",
        rationale="No clear net benefit in primary cardiovascular prevention in older adults; increased bleeding risk.",
    ),
    STOPPEntry(
        names=["digoxin", "lanoxin"],
        section="B  Cardiovascular", criterion_id="B12",
        condition="Chronic kidney disease with eGFR < 30 mL/min/1.73m",
        rationale="Drug accumulation, increased risk of toxicity.",
        brand_examples=["Lanoxin"],
    ),
    STOPPEntry(
        names=["aldosterone antagonists", "spironolactone", "aldactone", "eplerenone",
                "inspra"],
        section="B  Cardiovascular", criterion_id="B13",
        condition="Concurrent potassium-sparing diuretics or potassium supplements  without monitoring of serum potassium",
        rationale="Risk of hyperkalemia.",
    ),
    STOPPEntry(
        names=["phosphodiesterase-5 inhibitors", "sildenafil", "viagra", "tadalafil", "cialis",
                "vardenafil", "avanafil"],
        section="B  Cardiovascular", criterion_id="B14",
        condition="Concurrent long-acting nitrate therapy (e.g. isosorbide mononitrate, nitrate patch)",
        rationale="Risk of severe hypotension.",
    ),
    STOPPEntry(
        names=["statin", "simvastatin", "zocor", "atorvastatin", "lipitor", "rosuvastatin",
                "crestor", "pravastatin", "fluvastatin", "lovastatin"],
        section="B  Cardiovascular", criterion_id="B15",
        condition="Life expectancy less than 1 year or in the setting of frailty/terminal illness",
        rationale="No benefit in short life-expectancy; risk of adverse effects including myopathy.",
    ),
    STOPPEntry(
        names=["warfarin", "coumadin"],
        section="B  Cardiovascular", criterion_id="B16",
        condition="Patient has well-controlled atrial fibrillation on warfarin and DOAC is clinically appropriate",
        rationale="DOACs have superior safety profiles to warfarin for AF in most patients.",
    ),

    #  Section C: Coagulation 
    STOPPEntry(
        names=["anticoagulants", "warfarin", "coumadin", "apixaban", "eliquis",
                "rivaroxaban", "xarelto", "dabigatran", "pradaxa", "edoxaban"],
        section="C  Coagulation", criterion_id="C1",
        condition="Non-valvular atrial fibrillation with CHADS-VASc score of 0 (males) or 1 (females)",
        rationale="Bleeding risk outweighs thromboembolic risk at these scores.",
    ),
    STOPPEntry(
        names=["warfarin", "coumadin"],
        section="C  Coagulation", criterion_id="C2",
        condition="DVT or PE without ongoing thrombotic risk factors  beyond recommended duration (typically 6 months)",
        rationale="Extended anticoagulation beyond recommended duration increases bleeding risk without benefit.",
    ),
    STOPPEntry(
        names=["antiplatelet agents", "aspirin", "clopidogrel", "plavix",
                "ticagrelor", "brilinta"],
        section="C  Coagulation", criterion_id="C3",
        condition="Concurrent use of two or more antiplatelet agents without a clear indication for dual antiplatelet therapy",
        rationale="Additive bleeding risk.",
    ),
    STOPPEntry(
        names=["dabigatran", "pradaxa"],
        section="C  Coagulation", criterion_id="C4",
        condition="eGFR < 30 mL/min/1.73m",
        rationale="Dabigatran is predominantly renally excreted; accumulation causes increased bleeding risk.",
    ),
    STOPPEntry(
        names=["rivaroxaban", "xarelto"],
        section="C  Coagulation", criterion_id="C5",
        condition="eGFR < 15 mL/min/1.73m or on dialysis",
        rationale="Not studied in severe renal impairment; risk of drug accumulation and bleeding.",
    ),
    STOPPEntry(
        names=["apixaban", "eliquis"],
        section="C  Coagulation", criterion_id="C6",
        condition="eGFR < 15 mL/min/1.73m",
        rationale="Not studied in severe renal impairment.",
    ),
    STOPPEntry(
        names=["edoxaban", "savaysa", "lixiana"],
        section="C  Coagulation", criterion_id="C7",
        condition="eGFR > 95 mL/min/1.73m",
        rationale="Risk of reduced efficacy at high CrCl; consider alternative DOAC.",
    ),
    STOPPEntry(
        names=["heparin", "lmwh", "low molecular weight heparin", "enoxaparin", "lovenox",
                "dalteparin", "fragmin", "tinzaparin"],
        section="C  Coagulation", criterion_id="C8",
        condition="eGFR < 30 mL/min/1.73m without dose reduction",
        rationale="Accumulation causing increased bleeding risk; dose reduction needed.",
    ),
    STOPPEntry(
        names=["thrombolytics", "alteplase", "tenecteplase", "streptokinase"],
        section="C  Coagulation", criterion_id="C9",
        condition="Concurrent anticoagulant use  unless life-threatening indication (e.g. massive PE, STEMI)",
        rationale="Markedly increased risk of serious or fatal bleeding.",
    ),
    STOPPEntry(
        names=["anticoagulant", "warfarin", "doac", "apixaban", "rivaroxaban",
                "dabigatran", "edoxaban"],
        section="C  Coagulation", criterion_id="C10",
        condition="Patient with HAS-BLED score  3  without regular review/monitoring",
        rationale="High bleeding risk requires regular reassessment and possible deprescribing.",
    ),

    #  Section D: CNS / Psychotropics 
    STOPPEntry(
        names=["tricyclic antidepressants", "amitriptyline", "elavil", "imipramine",
                "tofranil", "clomipramine", "anafranil", "desipramine", "norpramin",
                "nortriptyline", "pamelor", "doxepin", "sinequan", "trimipramine"],
        section="D  CNS/Psychotropics", criterion_id="D1",
        condition="Depression, anxiety, or insomnia in older adult",
        rationale="Highly anticholinergic; sedating; cause orthostatic hypotension; safer alternatives available.",
    ),
    STOPPEntry(
        names=["benzodiazepines", "diazepam", "valium", "lorazepam", "ativan",
                "alprazolam", "xanax", "clonazepam", "klonopin", "oxazepam",
                "temazepam", "nitrazepam", "flurazepam", "chlordiazepoxide"],
        section="D  CNS/Psychotropics", criterion_id="D2",
        condition="Anxiety, agitation, insomnia or other CNS conditions",
        rationale="Cognitive impairment, falls, fractures, delirium, dependence; safer alternatives available.",
    ),
    STOPPEntry(
        names=["z-drugs", "zolpidem", "ambien", "eszopiclone", "lunesta",
                "zaleplon", "sonata", "zopiclone", "zimovane"],
        section="D  CNS/Psychotropics", criterion_id="D3",
        condition="Insomnia",
        rationale="Similar adverse effects to benzodiazepines; increased ER visits, falls, fractures, motor vehicle accidents in older adults.",
    ),
    STOPPEntry(
        names=["typical antipsychotics", "haloperidol", "haldol", "chlorpromazine",
                "thorazine", "trifluoperazine", "stelazine", "perphenazine",
                "thioridazine", "fluphenazine", "zuclopenthixol", "flupenthixol"],
        section="D  CNS/Psychotropics", criterion_id="D4",
        condition="Parkinsonism (not as antipsychotic for psychosis in Parkinson's disease)",
        rationale="Dopamine antagonists worsen parkinsonian symptoms.",
    ),
    STOPPEntry(
        names=["antipsychotics", "haloperidol", "haldol", "olanzapine", "zyprexa",
                "risperidone", "risperdal", "quetiapine", "seroquel", "aripiprazole",
                "chlorpromazine", "thorazine"],
        section="D  CNS/Psychotropics", criterion_id="D5",
        condition="Behavioural and psychological symptoms of dementia  unless non-pharmacological options have failed",
        rationale="Risk of stroke, cognitive decline, mortality. Non-pharmacological approaches preferred.",
    ),
    STOPPEntry(
        names=["antipsychotics", "phenothiazines", "haloperidol", "haldol",
                "olanzapine", "zyprexa", "risperidone", "risperdal",
                "chlorpromazine", "thorazine"],
        section="D  CNS/Psychotropics", criterion_id="D6",
        condition="History of falls or current high falls risk",
        rationale="Increased risk of falls due to sedation, orthostatic hypotension, EPS.",
    ),
    STOPPEntry(
        names=["antipsychotics"],
        section="D  CNS/Psychotropics", criterion_id="D7",
        condition="QTc interval > 450ms or concurrent QT-prolonging drugs",
        rationale="Risk of torsades de pointes and ventricular arrhythmias.",
    ),
    STOPPEntry(
        names=["ssri", "selective serotonin reuptake inhibitors", "fluoxetine", "prozac",
                "sertraline", "zoloft", "citalopram", "celexa", "escitalopram", "lexapro",
                "paroxetine", "paxil", "fluvoxamine"],
        section="D  CNS/Psychotropics", criterion_id="D8",
        condition="Current or recent (within 3 months) significant hyponatraemia (Na < 130 mmol/L)",
        rationale="SSRIs cause SIADH; hyponatraemia risk especially in frail older adults.",
    ),
    STOPPEntry(
        names=["anticonvulsants", "phenytoin", "dilantin", "phenobarbitone", "phenobarbital",
                "carbamazepine", "tegretol", "valproate", "valproic acid", "depakote",
                "primidone"],
        section="D  CNS/Psychotropics", criterion_id="D9",
        condition="Non-epileptic indication (e.g. anxiety, insomnia, pain)  safer alternatives available",
        rationale="Cognitive impairment, falls, gait disorders; avoid for non-epileptic use.",
    ),
    STOPPEntry(
        names=["opioids", "morphine", "oxycodone", "fentanyl", "duragesic",
                "hydromorphone", "codeine", "tramadol", "buprenorphine"],
        section="D  CNS/Psychotropics", criterion_id="D10",
        condition="Concurrent benzodiazepine use",
        rationale="Risk of profound sedation, respiratory depression, coma, death.",
    ),
    STOPPEntry(
        names=["methylphenidate", "ritalin", "modafinil", "provigil",
                "dextroamphetamine", "amphetamines"],
        section="D  CNS/Psychotropics", criterion_id="D11",
        condition="Insomnia, anxiety, or as a stimulant without clear indication",
        rationale="CNS stimulants can worsen agitation, anxiety, insomnia and have cardiovascular risks.",
    ),
    STOPPEntry(
        names=["opioids", "morphine", "oxycodone", "codeine", "fentanyl",
                "tramadol", "hydromorphone", "buprenorphine"],
        section="D  CNS/Psychotropics", criterion_id="D12",
        condition="History of falls or current fall risk",
        rationale="Sedation, postural instability; increased falls and fractures.",
    ),

    #  Section E: Renal 
    STOPPEntry(
        names=["nsaids", "ibuprofen", "advil", "motrin", "naproxen", "aleve", "naprosyn",
                "diclofenac", "voltaren", "indomethacin", "indocin", "celecoxib",
                "meloxicam", "mobic", "etoricoxib", "ketorolac", "toradol",
                "piroxicam", "sulindac"],
        section="E  Renal", criterion_id="E1",
        condition="eGFR < 50 mL/min/1.73m",
        rationale="Risk of renal failure; worsening pre-existing chronic kidney disease.",
    ),
    STOPPEntry(
        names=["metformin", "glucophage"],
        section="E  Renal", criterion_id="E2",
        condition="eGFR < 30 mL/min/1.73m",
        rationale="Risk of lactic acidosis.",
    ),
    STOPPEntry(
        names=["ace inhibitors", "ace-i", "lisinopril", "zestril", "ramipril", "altace",
                "enalapril", "vasotec", "perindopril", "captopril", "trandolapril",
                "quinapril", "fosinopril", "benazepril"],
        section="E  Renal", criterion_id="E3",
        condition="eGFR < 30 mL/min/1.73m  without monitoring of renal function and potassium",
        rationale="Risk of hyperkalaemia and renal failure without monitoring.",
    ),
    STOPPEntry(
        names=["arb", "angiotensin receptor blockers", "losartan", "cozaar",
                "valsartan", "diovan", "irbesartan", "avapro", "candesartan",
                "olmesartan", "telmisartan"],
        section="E  Renal", criterion_id="E4",
        condition="eGFR < 30 mL/min/1.73m  without monitoring of renal function and potassium",
        rationale="Risk of hyperkalaemia and renal failure without monitoring.",
    ),
    STOPPEntry(
        names=["potassium-sparing diuretics", "spironolactone", "aldactone",
                "amiloride", "triamterene", "eplerenone", "inspra"],
        section="E  Renal", criterion_id="E5",
        condition="eGFR < 30 mL/min/1.73m or concurrent potassium-raising medications without monitoring",
        rationale="Hyperkalemia risk; may be severe or life-threatening.",
    ),
    STOPPEntry(
        names=["colchicine", "colcrys"],
        section="E  Renal", criterion_id="E6",
        condition="eGFR < 10 mL/min/1.73m",
        rationale="Risk of severe colchicine toxicity.",
    ),
    STOPPEntry(
        names=["sglt2 inhibitors", "dapagliflozin", "farxiga", "empagliflozin",
                "jardiance", "canagliflozin", "invokana"],
        section="E  Renal", criterion_id="E7",
        condition="eGFR < 45 mL/min/1.73m",
        rationale="Reduced effectiveness and increased adverse effects (UTI, DKA) at lower eGFR.",
    ),
    STOPPEntry(
        names=["lithium", "priadel", "camcolit"],
        section="E  Renal", criterion_id="E8",
        condition="eGFR < 30 mL/min/1.73m",
        rationale="Risk of lithium toxicity due to accumulation.",
    ),
    STOPPEntry(
        names=["nitrofurantoin", "macrobid"],
        section="E  Renal", criterion_id="E9",
        condition="eGFR < 30 mL/min/1.73m  as treatment or prophylaxis",
        rationale="Inadequate urinary concentration; risk of pulmonary toxicity.",
    ),
    STOPPEntry(
        names=["trimethoprim", "trimethoprim-sulfamethoxazole", "bactrim", "septra",
                "co-trimoxazole"],
        section="E  Renal", criterion_id="E10",
        condition="eGFR < 30 mL/min/1.73m",
        rationale="Risk of life-threatening hyperkalemia.",
    ),

    #  Section F: Gastrointestinal 
    STOPPEntry(
        names=["proton pump inhibitors", "ppi", "omeprazole", "prilosec",
                "lansoprazole", "prevacid", "esomeprazole", "nexium",
                "pantoprazole", "protonix", "rabeprazole", "dexlansoprazole"],
        section="F  Gastrointestinal", criterion_id="F1",
        condition="Uncomplicated peptic ulcer or GORD  used for > 8 weeks at full dose",
        rationale="Risk of C. difficile, osteoporosis, fractures, pneumonia; dose reduction or step-down preferred.",
    ),
    STOPPEntry(
        names=["prokinetics", "metoclopramide", "reglan", "domperidone",
                "erythromycin"],
        section="F  Gastrointestinal", criterion_id="F2",
        condition="Parkinson's disease or Parkinsonism",
        rationale="Dopamine antagonists worsen Parkinson's disease symptoms.",
    ),
    STOPPEntry(
        names=["anticholinergics", "hyoscine butylbromide", "buscopan", "dicyclomine",
                "bentyl", "propantheline", "pro-banthine"],
        section="F  Gastrointestinal", criterion_id="F3",
        condition="Chronic constipation",
        rationale="Anticholinergics worsen constipation.",
    ),
    STOPPEntry(
        names=["antidiarrhoeals", "loperamide", "immodium", "codeine", "diphenoxylate"],
        section="F  Gastrointestinal", criterion_id="F4",
        condition="Diarrhoea  unknown cause",
        rationale="May delay diagnosis and appropriate treatment; risk of toxic megacolon in inflammatory bowel disease.",
    ),
    STOPPEntry(
        names=["antacids", "aluminium hydroxide", "magnesium trisilicate"],
        section="F  Gastrointestinal", criterion_id="F5",
        condition="Regular scheduled use",
        rationale="PPIs or H2 antagonists are more effective; aluminum antacids cause constipation.",
    ),
    STOPPEntry(
        names=["oral bisphosphonates", "alendronate", "fosamax", "risedronate",
                "actonel", "ibandronate"],
        section="F  Gastrointestinal", criterion_id="F6",
        condition="Active or recent (last 6 months) upper GI problems (dysphagia, oesophagitis, gastritis, peptic ulcer disease)",
        rationale="Risk of oesophageal ulceration; worsening of GI disease.",
    ),
    STOPPEntry(
        names=["stimulant laxatives", "senna", "bisacodyl", "dulcolax", "cascara"],
        section="F  Gastrointestinal", criterion_id="F7",
        condition="Chronic use in absence of organic cause of constipation",
        rationale="Risk of dependence, electrolyte imbalance; osmotic laxatives preferred.",
    ),
    STOPPEntry(
        names=["iron supplements", "ferrous sulphate", "ferrous gluconate",
                "ferrous fumarate"],
        section="F  Gastrointestinal", criterion_id="F8",
        condition="Without clear evidence of iron deficiency anaemia",
        rationale="Unnecessary use; GI adverse effects including constipation and nausea.",
    ),

    #  Section G: Respiratory 
    STOPPEntry(
        names=["theophylline", "aminophylline"],
        section="G  Respiratory", criterion_id="G1",
        condition="COPD or asthma  as monotherapy",
        rationale="Safer, more effective inhaled bronchodilators available; narrow therapeutic index; drug interactions.",
    ),
    STOPPEntry(
        names=["systemic corticosteroids", "prednisolone", "prednisone",
                "methylprednisolone", "dexamethasone"],
        section="G  Respiratory", criterion_id="G2",
        condition="COPD  as long-term monotherapy instead of inhaled therapy",
        rationale="Significant systemic side effects (osteoporosis, diabetes, adrenal suppression); inhaled steroids preferred.",
    ),
    STOPPEntry(
        names=["ipratropium", "atrovent", "tiotropium", "spiriva", "glycopyrronium",
                "umeclidinium", "aclidinium", "inhaled anticholinergics"],
        section="G  Respiratory", criterion_id="G3",
        condition="Concurrent closed angle glaucoma",
        rationale="Risk of exacerbating glaucoma.",
    ),
    STOPPEntry(
        names=["sedating antihistamines", "promethazine", "phenergan",
                "chlorphenamine", "diphenhydramine", "benadryl",
                "hydroxyzine", "atarax", "ketotifen"],
        section="G  Respiratory", criterion_id="G4",
        condition="COPD or asthma",
        rationale="Risk of bronchospasm, increased secretion viscosity, respiratory depression.",
    ),

    #  Section H: Musculoskeletal 
    STOPPEntry(
        names=["nsaids", "ibuprofen", "naproxen", "diclofenac", "celecoxib",
                "etoricoxib", "meloxicam", "indomethacin"],
        section="H  Musculoskeletal", criterion_id="H1",
        condition="eGFR < 50 mL/min/1.73m, or heart failure, or on anticoagulants",
        rationale="Increased risk of acute kidney injury, fluid retention, worsening heart failure, GI bleeding.",
    ),
    STOPPEntry(
        names=["corticosteroids systemic", "prednisolone", "prednisone",
                "methylprednisolone", "dexamethasone"],
        section="H  Musculoskeletal", criterion_id="H2",
        condition="As long-term (> 3 months) monotherapy for rheumatoid arthritis",
        rationale="Disease-modifying drugs are preferred; systemic corticosteroids cause significant long-term adverse effects.",
    ),
    STOPPEntry(
        names=["nsaids", "cox-2 inhibitors", "celecoxib", "celebrex", "etoricoxib",
                "ibuprofen", "naproxen", "diclofenac"],
        section="H  Musculoskeletal", criterion_id="H3",
        condition="Peptic ulcer disease or upper GI bleeding  without concurrent PPI",
        rationale="Risk of serious GI bleeding recurrence.",
    ),
    STOPPEntry(
        names=["bisphosphonates", "alendronate", "fosamax", "risedronate",
                "ibandronate", "zoledronic acid"],
        section="H  Musculoskeletal", criterion_id="H4",
        condition="Chronic kidney disease with eGFR < 30 mL/min/1.73m",
        rationale="Risk of adynamic bone disease.",
    ),
    STOPPEntry(
        names=["colchicine", "colcrys"],
        section="H  Musculoskeletal", criterion_id="H5",
        condition="eGFR < 30 mL/min/1.73m or concurrent statin therapy",
        rationale="Risk of colchicine toxicity (myopathy, neuromyopathy).",
    ),
    STOPPEntry(
        names=["hydroxychloroquine", "plaquenil", "chloroquine"],
        section="H  Musculoskeletal", criterion_id="H6",
        condition="Long-term use without ophthalmological review",
        rationale="Risk of retinal toxicity; requires 6-monthly ophthalmological monitoring.",
    ),

    #  Section I: Urogenital 
    STOPPEntry(
        names=["bladder antimuscarinics", "oxybutynin", "ditropan", "tolterodine",
                "detrol", "solifenacin", "vesicare", "darifenacin", "enablex",
                "fesoterodine", "toviaz", "trospium", "sanctura", "regurin"],
        section="I  Urogenital", criterion_id="I1",
        condition="Dementia or cognitive impairment",
        rationale="Risk of increased cognitive impairment and worsening delirium.",
    ),
    STOPPEntry(
        names=["bladder antimuscarinics", "oxybutynin", "ditropan", "tolterodine",
                "detrol", "solifenacin", "vesicare", "darifenacin", "fesoterodine"],
        section="I  Urogenital", criterion_id="I2",
        condition="Chronic constipation",
        rationale="Anticholinergics worsen constipation.",
    ),
    STOPPEntry(
        names=["bladder antimuscarinics", "oxybutynin", "tolterodine", "solifenacin",
                "darifenacin", "fesoterodine"],
        section="I  Urogenital", criterion_id="I3",
        condition="Closed angle glaucoma",
        rationale="May precipitate acute glaucoma.",
    ),
    STOPPEntry(
        names=["alpha-1 blockers", "tamsulosin", "flomax", "alfuzosin", "uroxatral",
                "doxazosin", "cardura", "terazosin"],
        section="I  Urogenital", criterion_id="I4",
        condition="Orthostatic hypotension or syncope",
        rationale="Alpha-1 blockers worsen orthostatic hypotension.",
    ),
    STOPPEntry(
        names=["5-alpha reductase inhibitors", "finasteride", "proscar",
                "dutasteride", "avodart"],
        section="I  Urogenital", criterion_id="I5",
        condition="History of orthostatic hypotension",
        rationale="Can cause orthostatic hypotension, especially on initiation.",
    ),

    #  Section J: Endocrine 
    STOPPEntry(
        names=["sulfonylureas", "glibenclamide", "glyburide", "diabeta",
                "glimepiride", "amaryl", "glipizide", "glucotrol", "gliclazide",
                "chlorpropamide", "tolbutamide"],
        section="J  Endocrine", criterion_id="J1",
        condition="Type 2 diabetes  risk of prolonged hypoglycemia",
        rationale="Prolonged hypoglycemia particularly dangerous in older adults; safer hypoglycaemic agents available.",
    ),
    STOPPEntry(
        names=["thiazolidinediones", "pioglitazone", "actos", "rosiglitazone", "avandia"],
        section="J  Endocrine", criterion_id="J2",
        condition="Heart failure (any degree)",
        rationale="Promote fluid retention and worsen heart failure.",
    ),
    STOPPEntry(
        names=["beta-blockers", "propranolol", "atenolol", "tenormin",
                "metoprolol", "bisoprolol", "carvedilol"],
        section="J  Endocrine", criterion_id="J3",
        condition="Diabetes with frequent hypoglycaemia",
        rationale="Masks most symptoms of hypoglycaemia (except sweating); dangerous in older adults.",
    ),
    STOPPEntry(
        names=["estrogen", "systemic estrogen", "conjugated estrogens",
                "estradiol", "oestradiol", "hrt", "hormone replacement therapy"],
        section="J  Endocrine", criterion_id="J4",
        condition="History of breast cancer or venous thromboembolism",
        rationale="Increased risk of breast cancer recurrence and VTE.",
    ),
    STOPPEntry(
        names=["thyroid replacement", "levothyroxine", "synthroid", "thyroxine",
                "liothyronine"],
        section="J  Endocrine", criterion_id="J5",
        condition="Without regular thyroid function monitoring",
        rationale="Risk of over-treatment causing atrial fibrillation and osteoporosis.",
    ),
    STOPPEntry(
        names=["insulin", "glargine", "lantus", "detemir", "levemir",
                "lispro", "aspart", "glulisine", "isophane"],
        section="J  Endocrine", criterion_id="J6",
        condition="Inappropriate insulin regimen  sliding scale or no basal insulin in type 1 diabetes",
        rationale="Increased hypoglycaemia risk; suboptimal glycaemic control.",
    ),

    #  Section K: Falls Risk-Increasing Drugs 
    STOPPEntry(
        names=["benzodiazepines", "diazepam", "valium", "lorazepam", "ativan",
                "alprazolam", "xanax", "clonazepam", "oxazepam", "temazepam",
                "nitrazepam", "chlordiazepoxide"],
        section="K  Falls Risk", criterion_id="K1",
        condition="Patient with history of falls or current high falls risk",
        rationale="Sedation, balance impairment, cognitive effects; significantly increased falls risk.",
    ),
    STOPPEntry(
        names=["z-drugs", "zolpidem", "ambien", "eszopiclone", "lunesta",
                "zaleplon", "zopiclone"],
        section="K  Falls Risk", criterion_id="K2",
        condition="Patient with history of falls or current high falls risk",
        rationale="Sedation; falls risk comparable to benzodiazepines.",
    ),
    STOPPEntry(
        names=["antiepileptics", "carbamazepine", "tegretol", "gabapentin",
                "neurontin", "pregabalin", "lyrica", "phenytoin", "dilantin",
                "valproate", "lamotrigine", "levetiracetam", "keppra",
                "oxcarbazepine", "topiramate"],
        section="K  Falls Risk", criterion_id="K3",
        condition="Patient with history of falls or current high falls risk",
        rationale="Ataxia, sedation, dizziness causing falls.",
    ),
    STOPPEntry(
        names=["opioids", "morphine", "oxycodone", "fentanyl", "tramadol",
                "codeine", "hydromorphone", "buprenorphine"],
        section="K  Falls Risk", criterion_id="K4",
        condition="Patient with history of falls or current high falls risk",
        rationale="Sedation, postural instability, increased falls risk.",
    ),
    STOPPEntry(
        names=["antidepressants", "ssri", "snri", "tricyclic antidepressants",
                "fluoxetine", "prozac", "sertraline", "zoloft", "citalopram",
                "escitalopram", "venlafaxine", "duloxetine", "mirtazapine",
                "amitriptyline", "nortriptyline"],
        section="K  Falls Risk", criterion_id="K5",
        condition="Patient with history of falls or current high falls risk",
        rationale="Orthostatic hypotension, sedation, falls risk.",
    ),
    STOPPEntry(
        names=["antihypertensives", "alpha-1 blockers", "doxazosin", "prazosin",
                "terazosin", "loop diuretics", "furosemide", "thiazide diuretics",
                "nitrates", "isosorbide mononitrate", "isosorbide dinitrate"],
        section="K  Falls Risk", criterion_id="K6",
        condition="Patient with orthostatic hypotension",
        rationale="Worsen orthostatic hypotension and increase falls risk.",
    ),
    STOPPEntry(
        names=["antipsychotics", "haloperidol", "olanzapine", "risperidone",
                "quetiapine", "chlorpromazine"],
        section="K  Falls Risk", criterion_id="K7",
        condition="Patient with history of falls or current high falls risk",
        rationale="Sedation, EPS, orthostatic hypotension increasing falls risk.",
    ),
    STOPPEntry(
        names=["muscle relaxants", "cyclobenzaprine", "flexeril", "baclofen",
                "lioresal", "tizanidine", "zanaflex", "methocarbamol", "robaxin",
                "carisoprodol", "soma", "orphenadrine"],
        section="K  Falls Risk", criterion_id="K8",
        condition="Patient with history of falls or current high falls risk",
        rationale="Sedation, muscle weakness, increased falls risk.",
    ),
    STOPPEntry(
        names=["antihistamines first generation", "diphenhydramine", "benadryl",
                "promethazine", "phenergan", "hydroxyzine", "atarax",
                "chlorphenamine", "clemastine"],
        section="K  Falls Risk", criterion_id="K9",
        condition="Patient with history of falls or current high falls risk",
        rationale="Sedation, anticholinergic effects increasing falls risk.",
    ),
    STOPPEntry(
        names=["carbidopa-levodopa", "levodopa", "sinemet", "madopar",
                "dopamine agonists", "pramipexole", "mirapex", "ropinirole",
                "requip", "rotigotine", "neupro"],
        section="K  Falls Risk", criterion_id="K10",
        condition="Patient with orthostatic hypotension",
        rationale="Worsen orthostatic hypotension increasing falls risk.",
    ),
    STOPPEntry(
        names=["anticholinergic drugs (high burden)", "oxybutynin", "ditropan",
                "tolterodine", "solifenacin", "amitriptyline", "diphenhydramine"],
        section="K  Falls Risk", criterion_id="K11",
        condition="Patient with history of falls or current high falls risk",
        rationale="Anticholinergic burden increases falls risk.",
    ),
    STOPPEntry(
        names=["cholinesterase inhibitors", "donepezil", "aricept",
                "rivastigmine", "exelon", "galantamine", "razadyne"],
        section="K  Falls Risk", criterion_id="K12",
        condition="Concurrent use with known QT-prolonging drug",
        rationale="Additive risk of bradycardia, which may contribute to falls.",
    ),

    #  Section L: Analgesics 
    STOPPEntry(
        names=["strong opioids", "morphine", "oxycodone", "fentanyl", "duragesic",
                "hydromorphone", "buprenorphine"],
        section="L  Analgesics", criterion_id="L1",
        condition="Mild to moderate pain  without trial of weaker analgesics",
        rationale="WHO pain ladder should be followed; strong opioids are not first-line for mild/moderate pain.",
    ),
    STOPPEntry(
        names=["opioids", "morphine", "oxycodone", "fentanyl", "codeine",
                "tramadol", "hydromorphone", "buprenorphine"],
        section="L  Analgesics", criterion_id="L2",
        condition="Without concurrent laxative",
        rationale="Risk of severe constipation; all patients on regular opioids need a prophylactic laxative.",
    ),
    STOPPEntry(
        names=["opioids", "strong opioids"],
        section="L  Analgesics", criterion_id="L3",
        condition="Chronic non-cancer pain  without documented assessment and treatment plan",
        rationale="Chronic opioid therapy requires regular reassessment and review.",
    ),
    STOPPEntry(
        names=["tramadol"],
        section="L  Analgesics", criterion_id="L4",
        condition="Epilepsy or concurrent seizure risk medications",
        rationale="Tramadol lowers seizure threshold.",
    ),
    STOPPEntry(
        names=["gabapentin", "neurontin", "pregabalin", "lyrica"],
        section="L  Analgesics", criterion_id="L5",
        condition="eGFR < 60 mL/min/1.73m  without dose reduction",
        rationale="Drug accumulation causing dizziness, sedation, falls, respiratory depression.",
    ),
    STOPPEntry(
        names=["nsaids", "ibuprofen", "naproxen", "diclofenac", "celecoxib",
                "etoricoxib", "indomethacin", "ketorolac", "meloxicam"],
        section="L  Analgesics", criterion_id="L6",
        condition="Concurrent oral anticoagulant therapy",
        rationale="Increased risk of serious GI bleeding.",
    ),
]


#  START DATABASE 

START_DATABASE: list[STARTEntry] = [

    #  Section A: Cardiovascular 
    STARTEntry(
        drug_class="ACE inhibitor or ARB",
        section="A  Cardiovascular", criterion_id="A1",
        indication="Systolic heart failure (EF < 40%) or established hypertension",
        rationale="Reduces mortality and hospitalisations; essential therapy in HFrEF.",
        examples=["lisinopril", "ramipril", "enalapril", "losartan", "valsartan"],
    ),
    STARTEntry(
        drug_class="Beta-blocker",
        section="A  Cardiovascular", criterion_id="A2",
        indication="Stable systolic heart failure (EF < 40%)",
        rationale="Reduces mortality; carvedilol, metoprolol succinate, bisoprolol are evidence-based.",
        examples=["carvedilol", "bisoprolol", "metoprolol succinate"],
    ),
    STARTEntry(
        drug_class="Antiplatelet therapy (aspirin or clopidogrel)",
        section="A  Cardiovascular", criterion_id="A3",
        indication="Established coronary, cerebrovascular, or peripheral arterial disease (secondary prevention)",
        rationale="Reduces risk of further cardiovascular events.",
        examples=["aspirin 75-100mg", "clopidogrel"],
    ),
    STARTEntry(
        drug_class="Statin",
        section="A  Cardiovascular", criterion_id="A4",
        indication="Established cardiovascular disease (secondary prevention)",
        rationale="Reduces cardiovascular mortality and morbidity.",
        examples=["atorvastatin", "rosuvastatin", "simvastatin"],
    ),
    STARTEntry(
        drug_class="Oral anticoagulant",
        section="A  Cardiovascular", criterion_id="A5",
        indication="Atrial fibrillation with CHADS-VASc score  2 (males) or  3 (females)",
        rationale="Reduces risk of stroke and systemic embolism.",
        examples=["apixaban", "rivaroxaban", "dabigatran", "edoxaban", "warfarin"],
    ),
    STARTEntry(
        drug_class="SGLT-2 inhibitor (dapagliflozin or empagliflozin)",
        section="A  Cardiovascular", criterion_id="A6",
        indication="Heart failure with reduced EF (eGFR  25 mL/min/1.73m)",
        rationale="Reduces mortality and hospitalisations due to HF.",
        examples=["dapagliflozin", "empagliflozin"],
    ),
    STARTEntry(
        drug_class="ACE inhibitor, ARB, or ARNI + MRA + beta-blocker",
        section="A  Cardiovascular", criterion_id="A7",
        indication="Symptomatic HFrEF  ensure all three pillars of therapy are prescribed",
        rationale="Combination therapy with these three classes significantly reduces mortality in HFrEF.",
        examples=["sacubitril/valsartan (Entresto)", "spironolactone", "eplerenone"],
    ),
    STARTEntry(
        drug_class="Antihypertensive therapy",
        section="A  Cardiovascular", criterion_id="A8",
        indication="Systolic BP consistently > 160 mmHg or diastolic > 90 mmHg",
        rationale="Reduces risk of stroke, coronary artery disease, heart failure.",
        examples=["amlodipine", "lisinopril", "losartan", "hydrochlorothiazide"],
    ),
    STARTEntry(
        drug_class="Statin + antihypertensive",
        section="A  Cardiovascular", criterion_id="A9",
        indication="Diabetes with established cardiovascular disease or at high CV risk",
        rationale="Significant reduction in cardiovascular events.",
        examples=["atorvastatin", "rosuvastatin"],
    ),
    STARTEntry(
        drug_class="SGLT-2 inhibitor or GLP-1 agonist",
        section="A  Cardiovascular", criterion_id="A10",
        indication="Type 2 diabetes with established cardiovascular disease",
        rationale="Reduces CV mortality and hospitalisation for heart failure.",
        examples=["empagliflozin", "dapagliflozin", "semaglutide", "liraglutide"],
    ),
    STARTEntry(
        drug_class="Ivabradine",
        section="A  Cardiovascular", criterion_id="A11",
        indication="Symptomatic HFrEF on maximal tolerated beta-blocker with HR > 70 bpm in sinus rhythm",
        rationale="Reduces hospitalisation for HF.",
        examples=["ivabradine (Coralan/Procoralan)"],
    ),

    #  Section B: Coagulation 
    STARTEntry(
        drug_class="VTE prophylaxis (anticoagulant)",
        section="B  Coagulation", criterion_id="B1",
        indication="Prolonged immobility or post-surgical patient  risk of DVT/PE",
        rationale="Reduces VTE risk in high-risk patients.",
        examples=["enoxaparin", "apixaban", "rivaroxaban"],
    ),
    STARTEntry(
        drug_class="Anticoagulation therapy",
        section="B  Coagulation", criterion_id="B2",
        indication="Active deep vein thrombosis or pulmonary embolism",
        rationale="Treatment anticoagulation essential to prevent extension and PE.",
        examples=["apixaban", "rivaroxaban", "dabigatran", "warfarin"],
    ),

    #  Section C: CNS 
    STARTEntry(
        drug_class="L-DOPA / dopaminergic therapy",
        section="C  CNS", criterion_id="C1",
        indication="Parkinson's disease with functional impairment",
        rationale="Significantly improves motor function and quality of life.",
        examples=["levodopa-carbidopa (Sinemet)", "pramipexole", "ropinirole"],
    ),
    STARTEntry(
        drug_class="Cholinesterase inhibitor",
        section="C  CNS", criterion_id="C2",
        indication="Mild to moderate Alzheimer's dementia or Lewy body dementia",
        rationale="Modest but consistent improvements in cognition, function, behaviour.",
        examples=["donepezil", "rivastigmine", "galantamine"],
    ),
    STARTEntry(
        drug_class="Antidepressant",
        section="C  CNS", criterion_id="C3",
        indication="Active, moderate-to-severe depressive illness",
        rationale="Significant improvement in depression; reduces risk of suicide.",
        examples=["sertraline", "mirtazapine", "escitalopram", "venlafaxine"],
    ),
    STARTEntry(
        drug_class="SNRI or SSRI for neuropathic pain",
        section="C  CNS", criterion_id="C4",
        indication="Persistent neuropathic pain unresponsive to simple analgesia",
        rationale="Effective for diabetic neuropathy and other neuropathic pain syndromes.",
        examples=["duloxetine", "venlafaxine", "amitriptyline (low dose)"],
    ),
    STARTEntry(
        drug_class="Gabapentinoid for neuropathic pain",
        section="C  CNS", criterion_id="C5",
        indication="Persistent neuropathic or central sensitisation pain",
        rationale="Reduces neuropathic pain; note falls risk and dose adjustment needed in renal impairment.",
        examples=["gabapentin", "pregabalin"],
    ),

    #  Section D: Renal 
    STARTEntry(
        drug_class="ACE inhibitor or ARB",
        section="D  Renal", criterion_id="D1",
        indication="Diabetic nephropathy with significant proteinuria (ACR > 30 mg/mmol)",
        rationale="Slows progression of diabetic nephropathy.",
        examples=["ramipril", "lisinopril", "losartan"],
    ),
    STARTEntry(
        drug_class="Statin",
        section="D  Renal", criterion_id="D2",
        indication="Chronic kidney disease stage 3 or greater",
        rationale="Reduces CV events in CKD.",
        examples=["atorvastatin", "rosuvastatin"],
    ),
    STARTEntry(
        drug_class="Erythropoiesis-stimulating agent",
        section="D  Renal", criterion_id="D3",
        indication="Symptomatic anaemia in CKD (Hb < 100 g/L)",
        rationale="Improves anaemia and quality of life.",
        examples=["erythropoietin", "darbepoetin"],
    ),
    STARTEntry(
        drug_class="Active Vitamin D analogue",
        section="D  Renal", criterion_id="D4",
        indication="Symptomatic or biochemical vitamin D deficiency in CKD",
        rationale="Prevents renal osteodystrophy.",
        examples=["calcitriol", "alfacalcidol"],
    ),

    #  Section E: Gastrointestinal 
    STARTEntry(
        drug_class="PPI or H2 antagonist",
        section="E  Gastrointestinal", criterion_id="E1",
        indication="Chronic NSAID therapy at high risk of peptic ulcer disease (PUD)",
        rationale="Significantly reduces NSAID-induced PUD.",
        examples=["omeprazole", "lansoprazole", "pantoprazole"],
    ),
    STARTEntry(
        drug_class="Bulk-forming laxative",
        section="E  Gastrointestinal", criterion_id="E2",
        indication="Symptomatic diverticular disease with constipation",
        rationale="Prevents diverticular complications.",
        examples=["ispaghula husk", "psyllium", "methylcellulose"],
    ),
    STARTEntry(
        drug_class="Disease-modifying therapy for IBD",
        section="E  Gastrointestinal", criterion_id="E3",
        indication="Active inflammatory bowel disease (Crohn's or UC)",
        rationale="Reduces flares and prevents complications.",
        examples=["mesalazine", "azathioprine", "infliximab"],
    ),
    STARTEntry(
        drug_class="Prophylactic laxative",
        section="E  Gastrointestinal", criterion_id="E4",
        indication="Patient on regular opioid analgesics",
        rationale="Opioid-induced constipation is universal; prophylactic laxative essential.",
        examples=["macrogol", "lactulose", "senna"],
    ),
    STARTEntry(
        drug_class="Vitamin B12 replacement",
        section="E  Gastrointestinal", criterion_id="E5",
        indication="Confirmed Vitamin B12 deficiency",
        rationale="Prevents/treats megaloblastic anaemia, peripheral neuropathy, cognitive decline.",
        examples=["cyanocobalamin IM", "hydroxocobalamin IM", "cyanocobalamin oral high dose"],
    ),
    STARTEntry(
        drug_class="Folic acid",
        section="E  Gastrointestinal", criterion_id="E6",
        indication="Methotrexate therapy",
        rationale="Reduces methotrexate toxicity (mucositis, GI effects).",
        examples=["folic acid 5mg weekly"],
    ),
    STARTEntry(
        drug_class="Laxative / prokinetic for constipation",
        section="E  Gastrointestinal", criterion_id="E7",
        indication="Chronic constipation refractory to bulk-forming and osmotic laxatives",
        rationale="Reduces symptoms of refractory chronic constipation.",
        examples=["prucalopride", "linaclotide"],
    ),

    #  Section F: Respiratory 
    STARTEntry(
        drug_class="Regular inhaled long-acting bronchodilator (LABA or LAMA)",
        section="F  Respiratory", criterion_id="F1",
        indication="Moderate to severe COPD (FEV < 50% predicted)",
        rationale="Reduces exacerbations, improves exercise tolerance and quality of life.",
        examples=["tiotropium", "umeclidinium", "salmeterol", "formoterol"],
    ),
    STARTEntry(
        drug_class="Inhaled corticosteroid (ICS) + LABA",
        section="F  Respiratory", criterion_id="F2",
        indication="Moderate to severe COPD with frequent exacerbations (2/year) or eosinophilia",
        rationale="Reduces exacerbations and hospitalisation.",
        examples=["fluticasone/salmeterol", "budesonide/formoterol"],
    ),
    STARTEntry(
        drug_class="Regular inhaled bronchodilator",
        section="F  Respiratory", criterion_id="F3",
        indication="Mild to moderate asthma or COPD",
        rationale="Improves symptoms and lung function.",
        examples=["salbutamol", "ipratropium", "tiotropium"],
    ),

    #  Section G: Musculoskeletal 
    STARTEntry(
        drug_class="DMARD (Disease-Modifying Anti-Rheumatic Drug)",
        section="G  Musculoskeletal", criterion_id="G1",
        indication="Active, moderate to severe rheumatoid arthritis",
        rationale="Reduces disease progression, joint destruction, and improves function.",
        examples=["methotrexate", "hydroxychloroquine", "leflunomide", "sulfasalazine"],
    ),
    STARTEntry(
        drug_class="Bisphosphonate / anti-osteoporotic agent",
        section="G  Musculoskeletal", criterion_id="G2",
        indication="Osteoporosis  DEXA T score < -2.5 or fragility fracture",
        rationale="Reduces fracture risk.",
        examples=["alendronate", "risedronate", "zoledronic acid", "denosumab"],
    ),
    STARTEntry(
        drug_class="Vitamin D and Calcium supplementation",
        section="G  Musculoskeletal", criterion_id="G3",
        indication="Osteoporosis, care home residents, or documented deficiency",
        rationale="Reduces fracture risk especially in combination with bisphosphonate.",
        examples=["cholecalciferol + calcium carbonate", "Adcal-D3"],
    ),
    STARTEntry(
        drug_class="Xanthine-oxidase inhibitor",
        section="G  Musculoskeletal", criterion_id="G4",
        indication="Gout with 2 attacks per year",
        rationale="Prevents recurrent attacks and tophaceous gout.",
        examples=["allopurinol", "febuxostat"],
    ),
    STARTEntry(
        drug_class="Anti-RANKL agent or PTH analogue",
        section="G  Musculoskeletal", criterion_id="G5",
        indication="Severe osteoporosis or continued fractures on bisphosphonate therapy",
        rationale="Potent reduction in fracture risk.",
        examples=["denosumab", "teriparatide", "romosozumab"],
    ),
    STARTEntry(
        drug_class="Low-dose corticosteroid or hydroxychloroquine",
        section="G  Musculoskeletal", criterion_id="G6",
        indication="Polymyalgia rheumatica (PMR) or active SLE",
        rationale="First-line treatment for PMR; reduces inflammation in SLE.",
        examples=["prednisolone", "hydroxychloroquine"],
    ),
    STARTEntry(
        drug_class="Topical NSAID or capsaicin",
        section="G  Musculoskeletal", criterion_id="G7",
        indication="Mild-to-moderate osteoarthritis of knee or hand",
        rationale="Effective local analgesia with lower systemic adverse effects.",
        examples=["diclofenac gel", "ibuprofen gel", "capsaicin cream"],
    ),
    STARTEntry(
        drug_class="IL-6 or TNF-alpha inhibitor",
        section="G  Musculoskeletal", criterion_id="G8",
        indication="Persistent active rheumatoid arthritis despite DMARDs",
        rationale="Significantly reduces joint damage and improves function.",
        examples=["tocilizumab", "adalimumab", "etanercept"],
    ),
    STARTEntry(
        drug_class="Colchicine or NSAIDs for acute gout",
        section="G  Musculoskeletal", criterion_id="G9",
        indication="Acute gout attack",
        rationale="Effective rapid treatment of acute gout.",
        examples=["colchicine", "indomethacin", "naproxen", "prednisolone"],
    ),

    #  Section H: Urogenital 
    STARTEntry(
        drug_class="Alpha-1 blocker or 5-alpha reductase inhibitor",
        section="H  Urogenital", criterion_id="H1",
        indication="Symptomatic benign prostatic hyperplasia (BPH) causing bother",
        rationale="Improves urinary symptoms and quality of life; 5-alpha reductase inhibitors reduce long-term risk of acute retention.",
        examples=["tamsulosin", "alfuzosin", "finasteride", "dutasteride"],
    ),
    STARTEntry(
        drug_class="Topical vaginal oestrogen",
        section="H  Urogenital", criterion_id="H2",
        indication="Symptomatic vaginal atrophy (dyspareunia, recurrent UTIs)",
        rationale="Effective for vaginal symptoms; minimal systemic absorption at low doses.",
        examples=["oestradiol cream", "estriol pessary", "vaginal oestrogen ring"],
    ),
    STARTEntry(
        drug_class="Antimuscarinics or mirabegron",
        section="H  Urogenital", criterion_id="H3",
        indication="Overactive bladder (OAB)  after failure of bladder training",
        rationale="Reduces urgency incontinence and frequency.",
        examples=["solifenacin", "fesoterodine", "mirabegron"],
    ),
    STARTEntry(
        drug_class="5-alpha reductase inhibitor",
        section="H  Urogenital", criterion_id="H4",
        indication="Moderate to severe BPH to prevent disease progression and acute retention",
        rationale="Reduces prostate volume and risk of acute urinary retention.",
        examples=["finasteride", "dutasteride"],
    ),
    STARTEntry(
        drug_class="Desmopressin (if no hyponatraemia risk)",
        section="H  Urogenital", criterion_id="H5",
        indication="Nocturia due to nocturnal polyuria  without hyponatraemia",
        rationale="Reduces nocturia frequency; avoid in patients at risk of hyponatraemia.",
        examples=["desmopressin"],
    ),

    #  Section I: Endocrine 
    STARTEntry(
        drug_class="Metformin (if tolerated and eGFR  30)",
        section="I  Endocrine", criterion_id="I1",
        indication="Type 2 diabetes mellitus, first-line",
        rationale="Reduces cardiovascular events and mortality; weight-neutral.",
        examples=["metformin"],
    ),
    STARTEntry(
        drug_class="ACE inhibitor or ARB",
        section="I  Endocrine", criterion_id="I2",
        indication="Diabetes with hypertension",
        rationale="Renal and cardiovascular protection in diabetic hypertension.",
        examples=["ramipril", "lisinopril", "losartan"],
    ),
    STARTEntry(
        drug_class="Statin",
        section="I  Endocrine", criterion_id="I3",
        indication="Diabetes without cardiovascular disease  at high CV risk",
        rationale="Primary prevention of cardiovascular events in high-risk diabetic patients.",
        examples=["atorvastatin", "rosuvastatin"],
    ),
    STARTEntry(
        drug_class="Thyroid hormone replacement",
        section="I  Endocrine", criterion_id="I4",
        indication="Confirmed hypothyroidism",
        rationale="Essential replacement therapy; prevents cognitive decline, cardiac effects, metabolic complications.",
        examples=["levothyroxine"],
    ),

    #  Section J: Vaccines 
    STARTEntry(
        drug_class="Annual influenza vaccine",
        section="J  Vaccines", criterion_id="J1",
        indication="All adults aged  65 years",
        rationale="Reduces influenza-related morbidity and mortality.",
        examples=["seasonal flu vaccine"],
    ),
    STARTEntry(
        drug_class="Pneumococcal vaccine",
        section="J  Vaccines", criterion_id="J2",
        indication="Adults  65 years or those with chronic disease",
        rationale="Reduces pneumococcal pneumonia and invasive disease.",
        examples=["PPSV23 / PCV13 / PCV15 / PCV20"],
    ),
    STARTEntry(
        drug_class="Herpes zoster (shingles) vaccine",
        section="J  Vaccines", criterion_id="J3",
        indication="Adults aged  65 years",
        rationale="Reduces incidence and severity of herpes zoster and post-herpetic neuralgia.",
        examples=["Shingrix (recombinant, preferred)", "Zostavax"],
    ),
    STARTEntry(
        drug_class="COVID-19 booster vaccine",
        section="J  Vaccines", criterion_id="J4",
        indication="All older adults per current immunisation schedule",
        rationale="Reduces severe COVID-19, hospitalisation, and mortality.",
        examples=["mRNA COVID-19 vaccine (Pfizer/Moderna)"],
    ),
]


#  Lookup logic 

def lookup_stopp(name: str) -> list[STOPPEntry]:
    key = name.strip().lower()
    matches = []
    seen = set()
    for entry in STOPP_DATABASE:
        if id(entry) in seen:
            continue
        for n in entry.names:
            if key == n or key in n or n in key:
                matches.append(entry)
                seen.add(id(entry))
                break
    return matches


def check_drugs_stopp(drug_names: list) -> dict:
    results = []
    for name in drug_names:
        hits = lookup_stopp(name)
        results.append({"input": name, "flagged": bool(hits), "entries": hits})
    return {"results": results, "total": len(drug_names),
            "flagged": sum(1 for r in results if r["flagged"])}


def print_stopp_report(data: dict):
    print("\n" + "=" * 70)
    print("   STOPP v3 (2023)  Potentially Inappropriate Prescriptions")
    print("   Drugs to CONSIDER STOPPING in adults 65 years")
    print("=" * 70)
    for drug in data["results"]:
        print(f"\n   {drug['input'].upper()} ")
        if not drug["flagged"]:
            print("   No STOPP flags found")
        else:
            for e in drug["entries"]:
                print(f"\n   [{e.criterion_id}] {e.section}")
                print(f"     Condition : {e.condition}")
                print(f"     Rationale : {e.rationale}")
    flagged = data["flagged"]
    total = data["total"]
    print(f"\n  Summary: {flagged}/{total} drug(s) have STOPP flags")
    print("=" * 70)


def get_start_suggestions(conditions: list) -> list[STARTEntry]:
    """Return START suggestions for given condition keywords."""
    hits = []
    seen = set()
    for entry in START_DATABASE:
        if id(entry) in seen:
            continue
        for cond in conditions:
            key = cond.strip().lower()
            if key in entry.indication.lower() or key in entry.rationale.lower():
                hits.append(entry)
                seen.add(id(entry))
                break
    return hits


def print_start_report(conditions: list):
    hits = get_start_suggestions(conditions)
    print("\n" + "=" * 70)
    print("   START v3 (2023)  Prescribing Omissions to Consider")
    print("   Drugs to consider STARTING for documented conditions")
    print("=" * 70)
    if not conditions:
        print("    No conditions provided  START criteria require known diagnoses.")
        print("     Pass conditions with --conditions flag when using combined_checker.py")
    elif not hits:
        print(f"    No START criteria matched for: {', '.join(conditions)}")
    else:
        for e in hits:
            print(f"\n   [{e.criterion_id}] {e.section}")
            print(f"     Consider  : {e.drug_class}")
            print(f"     Indication: {e.indication}")
            print(f"     Rationale : {e.rationale}")
            if e.examples:
                print(f"     Examples  : {', '.join(e.examples)}")
    print("=" * 70)


#  Main 

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        drugs = sys.argv[1:]
    else:
        print("STOPP/START v3 Checker")
        print("Enter current medications (comma-separated):")
        raw = input("Drugs > ")
        drugs = [d.strip() for d in raw.split(",") if d.strip()]

    if not drugs:
        print("No drugs entered.")
        sys.exit(0)

    result = check_drugs_stopp(drugs)
    print_stopp_report(result)

    print("\nOptional: enter patient conditions to get START suggestions")
    print("(e.g. 'heart failure, diabetes, osteoporosis') or press Enter to skip:")
    cond_raw = input("Conditions > ").strip()
    conditions = [c.strip() for c in cond_raw.split(",") if c.strip()] if cond_raw else []
    print_start_report(conditions)
    print("\n    For adults 65 years. For educational use only.")
    print("     Source: STOPP/START v3, O'Mahony D et al., Eur Geriatr Med 2023")
