"""
ACB (Anticholinergic Cognitive Burden) Calculator
Data sourced from acbcalc.com (updated July 2024)

ACB Score meaning:
  0 = No anticholinergic burden
  1 = Possible anticholinergic burden
  2 = Definite anticholinergic burden (moderate)
  3 = Definite anticholinergic burden (high)

Total score >= 3  HIGH RISK: associated with increased confusion, falls, and mortality
"""

# Full ACB drug database from acbcalc.com
# Format: { "drug_name_lowercase": (score, [brand_names]) }
ACB_DATABASE = {
    "5-hydroxytryptophan": (0, []),
    "abacavir": (0, []),
    "abiraterone": (0, []),
    "acamprosate": (0, []),
    "acarbose": (0, []),
    "acebutolol": (0, []),
    "acetaminophen": (0, []),
    "acetazolamide": (0, []),
    "acetic acid": (0, []),
    "acetohexamide": (0, []),
    "acetylcarnitine": (0, []),
    "acetylcysteine": (0, []),
    "aciclovir": (0, []),
    "acidophilus": (0, []),
    "acitretin": (0, []),
    "aclidinium": (0, []),
    "acyclovir": (0, []),
    "adalimumab": (0, []),
    "adenosine": (0, []),
    "adrenaline": (0, []),
    "agomelatine": (0, []),
    "albumin human": (0, []),
    "albuterol": (0, []),
    "alclometasone topical": (0, []),
    "alendronate": (0, ["alendronic acid"]),
    "alfuzosin": (0, []),
    "alginic acid": (0, []),
    "alimemazine": (1, ["theralen", "alfrased", "itzenal"]),
    "aliskiren": (0, []),
    "allopurinol": (0, []),
    "aloe vera": (0, []),
    "alprazolam": (1, ["xanax"]),
    "alprostadil": (0, []),
    "alteplase": (0, []),
    "alverine": (1, ["spasmonal", "audmonal"]),
    "amantadine": (1, ["symmetrel"]),
    "amiloride": (0, []),
    "aminophylline": (1, []),
    "amiodarone": (0, []),
    "amitriptyline": (3, ["elavil"]),
    "amlodipine": (0, []),
    "amoxapine": (3, ["asendin"]),
    "amoxicillin": (0, []),
    "amoxicillin-clavulanate": (0, ["co-amoxiclav"]),
    "amphetamine": (0, []),
    "amphotericin b": (0, []),
    "ampicillin": (1, []),
    "anagrelide": (0, []),
    "anakinra": (0, []),
    "anastrozole": (0, []),
    "apixaban": (0, []),
    "aripiprazole": (1, ["abilify", "arpoya"]),
    "ascorbic acid": (0, []),
    "asenapine": (1, ["saphris"]),
    "aspirin": (0, []),
    "atazanavir": (0, []),
    "atenolol": (0, ["tenormin"]),
    "atomoxetine": (0, []),
    "atorvastatin": (0, []),
    "atropine": (3, ["sal-tropine"]),
    "azatadine": (3, ["optimine"]),
    "azathioprine": (0, []),
    "azelastine nasal": (1, []),
    "azelastine ophthalmic": (1, []),
    "azithromycin": (0, []),
    "bacitracin": (0, []),
    "baclofen": (0, []),
    "balsalazide": (0, []),
    "barberry": (1, []),
    "belladonna": (3, []),
    "benzonatate": (0, []),
    "benztropine": (3, ["cogentin"]),
    "betahistine": (0, []),
    "betamethasone": (0, []),
    "betaxolol": (0, []),
    "bethanechol": (0, []),
    "bevacizumab": (0, []),
    "bicalutamide": (0, []),
    "bilastine": (0, []),
    "biperiden": (3, []),
    "bisacodyl": (0, []),
    "bismuth subsalicylate": (0, []),
    "bisoprolol": (0, []),
    "bosentan": (0, []),
    "bromocriptine": (1, []),
    "brompheniramine": (3, ["dimetapp", "bromfed", "bromfenax", "dimetane", "lodrone"]),
    "buclizine": (3, []),
    "budesonide": (0, []),
    "bumetanide": (0, []),
    "buprenorphine": (0, []),
    "bupropion": (1, ["wellbutrin", "zyban"]),
    "buspirone": (0, []),
    "cabergoline": (0, []),
    "caffeine": (0, []),
    "calcitonin": (0, []),
    "calcitriol": (0, []),
    "calcium carbonate": (0, []),
    "canagliflozin": (0, []),
    "candesartan": (0, []),
    "cannabidiol": (0, []),
    "capecitabine": (0, []),
    "captopril": (1, ["capoten"]),
    "carbamazepine": (0, ["tegretol"]),
    "carbidopa": (0, []),
    "carbidopa-levodopa": (1, []),
    "carbinoxamine": (3, ["histex", "carbihist"]),
    "carboplatin": (0, []),
    "carisoprodol": (0, []),
    "carvedilol": (0, []),
    "cefaclor": (0, []),
    "cefadroxil": (0, []),
    "cefamandole": (1, []),
    "cefazolin": (0, []),
    "cefepime": (0, []),
    "cefixime": (0, []),
    "cefotetan": (0, []),
    "cefoxitin": (1, []),
    "ceftriaxone": (0, []),
    "cefuroxime": (0, []),
    "celecoxib": (1, []),
    "cephalexin": (0, []),
    "cephalothin": (1, []),
    "cetirizine": (1, ["zyrtec"]),
    "chloral hydrate": (0, []),
    "chlorambucil": (0, []),
    "chloramphenicol": (0, []),
    "chlordiazepoxide": (1, []),
    "chloroquine": (1, []),
    "chlorothiazide": (0, []),
    "chlorphenamine": (3, ["piriton", "chlorpheniramine", "chlor-trimeton"]),
    "chlorpheniramine": (3, ["piriton", "chlorpheniramine", "chlor-trimeton"]),
    "chlorpromazine": (3, ["thorazine"]),
    "chlorpropamide": (0, []),
    "chlorprothixene": (3, []),
    "chlortalidone": (1, ["hygroton", "chlorthalidone"]),
    "chlorzoxazone": (0, []),
    "cholecalciferol": (0, []),
    "cholestyramine": (0, []),
    "ciclosporin": (1, []),
    "cilostazol": (0, []),
    "cimetidine": (1, ["tagamet"]),
    "cinacalcet": (0, []),
    "cinnarizine": (3, []),
    "ciprofloxacin": (0, []),
    "citalopram": (1, []),
    "citric acid": (0, []),
    "clarithromycin": (0, []),
    "clemastine": (3, ["tavist"]),
    "clidinium": (3, ["librax"]),
    "clindamycin": (1, []),
    "clobazam": (0, []),
    "clomipramine": (3, ["anafranil"]),
    "clonazepam": (1, []),
    "clonidine": (0, []),
    "clopidogrel": (0, []),
    "clorazepate": (1, ["tranxene"]),
    "clotrimazole": (0, []),
    "clozapine": (3, ["clozaril"]),
    "co-codamol": (0, ["zapain"]),
    "codeine": (0, ["contin"]),
    "colchicine": (0, ["colcrys"]),
    "conjugated estrogens": (0, []),
    "corticosterone": (1, []),
    "cortisone": (1, []),
    "cromolyn": (0, ["sodium cromoglycate"]),
    "cyclizine": (3, []),
    "cyclobenzaprine": (3, ["flexeril"]),
    "cyclophosphamide": (0, []),
    "cycloserine": (1, []),
    "cyclosporine": (1, ["ciclosporin"]),
    "cyproheptadine": (3, ["periactin"]),
    "dabigatran": (0, []),
    "dalteparin": (0, []),
    "darifenacin": (3, ["enablex"]),
    "darunavir": (0, []),
    "desipramine": (3, ["norpramin"]),
    "desloratadine": (1, ["clarinex"]),
    "desmopressin": (0, []),
    "desvenlafaxine": (1, []),
    "dexamethasone": (1, []),
    "dexbrompheniramine": (3, []),
    "dexchlorpheniramine": (3, []),
    "dexlansoprazole": (0, []),
    "dextromethorphan": (1, []),
    "diazepam": (1, ["valium"]),
    "diclofenac": (0, []),
    "dicycloverine": (3, ["bentyl", "dicyclomine"]),
    "dicyclomine": (3, ["bentyl"]),
    "digoxin": (1, ["lanoxin"]),
    "diltiazem": (0, []),
    "dimenhydrinate": (3, ["dramamine"]),
    "dimetindene": (1, []),
    "diphenhydramine": (3, ["benadryl", "nytol", "sleepeaze"]),
    "diphenhydramine cream": (1, []),
    "diphenoxylate": (0, []),
    "disopyramide": (2, ["norpace"]),
    "disulfiram": (0, []),
    "dobutamine": (0, []),
    "docusate": (0, []),
    "domperidone": (0, []),
    "donepezil": (0, []),
    "dopamine": (0, []),
    "dosulepin": (3, ["dothiepin"]),
    "dothiepin": (3, ["dosulepin"]),
    "doxazosin": (0, []),
    "doxepin": (3, ["sinequan"]),
    "doxycycline": (0, []),
    "doxylamine": (3, ["unisom"]),
    "dronedarone": (0, []),
    "duloxetine": (0, []),
    "efavirenz": (0, []),
    "enalapril": (0, []),
    "enoxaparin": (0, []),
    "entacapone": (1, []),
    "epinephrine": (0, []),
    "ergotamine": (1, []),
    "erythromycin": (0, []),
    "escitalopram": (1, ["lexapro"]),
    "esomeprazole": (0, []),
    "estazolam": (0, []),
    "estradiol": (0, ["oestradiol", "estriol"]),
    "etanercept": (0, []),
    "ethambutol": (0, []),
    "etoricoxib": (1, []),
    "ezetimibe": (0, []),
    "famciclovir": (0, []),
    "famotidine": (0, []),
    "febuxostat": (0, []),
    "felodipine": (0, []),
    "fenofibrate": (0, []),
    "fentanyl": (1, ["duragesic", "actiq"]),
    "fentanyl topical": (1, []),
    "fesoterodine": (3, ["toviaz"]),
    "fexofenadine": (0, []),
    "finasteride": (0, []),
    "flavoxate": (3, ["urispas"]),
    "flecainide": (0, []),
    "flucloxacillin": (0, []),
    "fluconazole": (0, []),
    "flunitrazepam": (1, []),
    "fluoxetine": (1, []),
    "fluphenazine": (1, []),
    "flurazepam": (1, []),
    "fluticasone": (0, []),
    "fluvastatin": (0, []),
    "fluvoxamine": (1, ["luvox"]),
    "folic acid": (0, []),
    "formoterol": (0, []),
    "furosemide": (0, ["lasix"]),
    "gabapentin": (0, []),
    "galantamine": (0, []),
    "ganciclovir": (0, []),
    "gentamicin": (1, ["gentamycin"]),
    "glibenclamide": (0, ["glyburide"]),
    "gliclazide": (0, []),
    "glimepiride": (0, []),
    "glipizide": (0, []),
    "glucosamine": (0, []),
    "glyburide": (0, []),
    "glycopyrronium - inhaled": (1, []),
    "glycopyrronium injectable": (3, ["glycopyrrolate"]),
    "glycopyrrolate": (3, ["glycopyrronium injectable"]),
    "griseofulvin": (0, []),
    "guaifenesin": (1, []),
    "haloperidol": (1, ["haldol"]),
    "heparin": (0, []),
    "homatropine": (3, []),
    "homatropine ophthalmic": (2, []),
    "hydralazine": (1, ["apresoline"]),
    "hydrochlorothiazide": (0, []),
    "hydrocodone": (0, []),
    "hydrocortisone": (1, ["cortef", "cortaid"]),
    "hydromorphone": (0, []),
    "hydroxychloroquine": (0, []),
    "hydroxyzine": (1, ["atarax", "vistaril"]),
    "hyoscine butylbromide": (3, ["butylscopolamine"]),
    "butylscopolamine": (3, ["hyoscine butylbromide"]),
    "hyoscine hydrobromide": (3, ["kwells", "scopoderm", "scopolamine"]),
    "hyoscyamine": (3, ["anaspaz", "levsin"]),
    "ibuprofen": (0, []),
    "iloperidone": (1, []),
    "imatinib": (0, []),
    "imipramine": (3, ["tofranil"]),
    "indapamide": (0, []),
    "indomethacin": (0, []),
    "infliximab": (0, []),
    "insulin": (0, []),
    "ipratropium": (1, []),
    "ipratropium nasal": (1, []),
    "irbesartan": (0, []),
    "isoniazid": (0, []),
    "isosorbide": (1, []),
    "isosorbide dinitrate": (1, ["isordil"]),
    "isosorbide mononitrate": (1, ["ismo"]),
    "itraconazole": (0, []),
    "ketamine": (3, []),
    "ketoconazole": (0, []),
    "ketoprofen": (0, []),
    "labetalol": (0, []),
    "lactulose": (0, []),
    "lamivudine": (0, []),
    "lamotrigine": (0, []),
    "lansoprazole": (1, []),
    "latanoprost ophthalmic": (0, []),
    "leflunomide": (0, []),
    "lercanidipine": (0, []),
    "letrozole": (0, []),
    "levobunolol ophthalmic": (0, []),
    "levocetirizine": (1, ["xyzal"]),
    "levodopa": (1, []),
    "levofloxacin": (0, []),
    "levomepromazine": (3, []),
    "levothyroxine": (0, []),
    "linezolid": (0, []),
    "linagliptin": (0, []),
    "lisinopril": (0, []),
    "lithium": (1, []),
    "loperamide": (1, ["immodium"]),
    "loratadine": (1, ["claritin"]),
    "lorazepam": (1, ["ativan"]),
    "losartan": (0, []),
    "lovastatin": (0, []),
    "loxapine": (2, ["loxitane"]),
    "magnesium hydroxide": (0, []),
    "magnesium sulfate": (0, []),
    "mannitol": (0, []),
    "maprotiline": (2, []),
    "meclizine": (1, ["antivert"]),
    "medroxyprogesterone": (0, []),
    "melatonin": (0, []),
    "meloxicam": (0, []),
    "memantine": (0, []),
    "meperidine": (0, []),
    "metformin": (1, []),
    "methadone": (1, []),
    "methocarbamol": (3, ["robaxin"]),
    "methotrexate": (0, []),
    "methotrimeprazine": (2, ["levoprome"]),
    "methscopolamine": (3, []),
    "methyldopa": (0, []),
    "methylphenidate": (0, []),
    "methylprednisolone": (1, []),
    "metoclopramide": (0, []),
    "metoprolol": (0, ["lopressor", "toprol"]),
    "metronidazole": (0, []),
    "midazolam": (1, []),
    "minocycline": (0, []),
    "minoxidil": (0, []),
    "mirabegron": (0, []),
    "mirtazapine": (1, []),
    "misoprostol": (0, []),
    "modafinil": (0, []),
    "mometasone": (0, []),
    "montelukast": (0, []),
    "morphine": (1, ["ms contin", "avinza", "zomorph"]),
    "moxifloxacin": (0, []),
    "mycophenolate mofetil": (0, []),
    "nabilone": (0, []),
    "nabumetone": (0, []),
    "naloxone": (0, []),
    "naltrexone": (0, []),
    "naproxen": (0, []),
    "naratriptan": (1, []),
    "neomycin": (1, []),
    "neostigmine": (0, []),
    "nicardipine": (0, []),
    "nicotine": (0, []),
    "nifedipine": (0, ["procardia", "adalat"]),
    "nimodipine": (0, []),
    "nitrazepam": (1, []),
    "nitrofurantoin": (0, []),
    "nitroglycerin": (0, []),
    "nizatidine": (1, []),
    "norethisterone": (0, ["norethindrone"]),
    "nortriptyline": (3, ["pamelor"]),
    "nystatin": (0, []),
    "olanzapine": (3, ["zyprexa"]),
    "olmesartan": (0, []),
    "omeprazole": (1, []),
    "ondansetron": (0, []),
    "opipramol": (2, []),
    "orlistat": (0, []),
    "orphenadrine": (3, ["norflex"]),
    "oseltamivir": (0, []),
    "oxazepam": (1, []),
    "oxcarbazepine": (0, ["trileptal"]),
    "oxybutynin": (3, ["ditropan"]),
    "oxycodone": (1, []),
    "paliperidone": (0, ["invega"]),
    "pancuronium": (1, []),
    "pantoprazole": (1, []),
    "paracetamol": (0, []),
    "paroxetine": (3, ["paxil"]),
    "penicillin": (0, []),
    "perphenazine": (2, ["trilafon"]),
    "pethidine": (2, ["demerol", "meperidine"]),
    "phenelzine": (1, []),
    "phenindamine": (3, []),
    "pheniramine": (3, []),
    "pheniramine ophthalmic": (1, []),
    "phenobarbitol": (1, ["phenobarbital"]),
    "phenobarbital": (1, ["phenobarbitol"]),
    "phenylephrine": (0, []),
    "phenyltoloxamine": (3, []),
    "phenytoin": (0, []),
    "pilocarpine": (0, []),
    "pimozide": (2, ["orap"]),
    "pindolol": (0, []),
    "pioglitazone": (0, []),
    "piperacillin": (1, []),
    "piroxicam": (0, []),
    "potassium chloride": (0, []),
    "pramipexole": (1, []),
    "pravastatin": (0, []),
    "prazosin": (0, []),
    "prednisolone": (1, ["deltasone", "sterapred", "prednisone"]),
    "prednisone": (1, ["deltasone", "sterapred", "prednisolone"]),
    "pregabalin": (0, []),
    "primidone": (0, []),
    "procainamide": (1, []),
    "prochlorperazine": (1, []),
    "procyclidine": (3, []),
    "promethazine": (3, ["phenergan"]),
    "propafenone": (0, []),
    "propantheline": (3, ["pro-banthine"]),
    "propiverine": (3, ["detrunorm"]),
    "propranolol": (0, []),
    "protriptyline": (3, []),
    "pseudoephedrine": (0, []),
    "pyridostigmine": (0, []),
    "quetiapine": (3, ["seroquel"]),
    "quinapril": (0, []),
    "quinidine": (1, ["quinaglute"]),
    "quinine": (0, []),
    "rabeprazole": (0, []),
    "raloxifene": (0, []),
    "ramipril": (0, []),
    "ranitidine": (1, ["zantac"]),
    "rasagiline": (0, []),
    "ribavirin": (0, []),
    "rifampin": (0, []),
    "risperidone": (1, ["risperdal"]),
    "rivaroxaban": (0, []),
    "rivastigmine": (0, []),
    "ropinirole": (0, []),
    "rosuvastatin": (0, []),
    "rotigotine": (1, []),
    "salbutamol": (0, ["albuterol"]),
    "salmeterol": (0, []),
    "saxagliptin": (0, []),
    "scopolamine": (3, []),
    "scopolamine topical": (3, []),
    "selegiline": (1, []),
    "sertraline": (1, ["zoloft"]),
    "sildenafil": (0, []),
    "simethicone": (0, []),
    "simvastatin": (0, []),
    "sirolimus": (0, []),
    "sitagliptin": (0, []),
    "sodium bicarbonate": (0, []),
    "solifenacin": (3, ["vesicare"]),
    "sotalol": (0, []),
    "spironolactone": (0, []),
    "sucralfate": (0, []),
    "sulfamethoxazole": (0, []),
    "sulfamethoxazole-trimethoprim": (0, []),
    "sulfasalazine": (0, []),
    "sumatriptan": (1, []),
    "tacrolimus": (0, []),
    "tadalafil": (0, []),
    "tamoxifen": (0, []),
    "tamsulosin": (0, []),
    "temazepam": (1, []),
    "terazosin": (0, []),
    "terbinafine": (0, []),
    "terbutaline": (0, []),
    "testosterone": (0, []),
    "tetracycline": (0, []),
    "theophylline": (1, ["theodur", "uniphyl"]),
    "thioridazine": (3, ["mellaril"]),
    "thiothixene": (0, []),
    "tiagabine": (1, []),
    "tiotropium": (1, []),
    "tobramycin": (1, []),
    "tolterodine": (3, ["detrol"]),
    "topiramate": (0, []),
    "tramadol": (2, []),
    "trandolapril": (1, []),
    "tranylcypromine": (1, []),
    "trazodone": (0, ["desyrel"]),
    "triamcinolone": (1, []),
    "triamterene": (1, ["dyrenium"]),
    "triazolam": (1, []),
    "trifluoperazine": (2, ["stelazine"]),
    "triflupromazine": (3, []),
    "trihexyphenidyl": (3, ["artane"]),
    "trimethobenzamide": (3, []),
    "trimethoprim": (0, []),
    "trimipramine": (3, ["surmontil"]),
    "triprolidine": (3, []),
    "trospium": (3, ["sanctura", "regurin"]),
    "umeclidinium": (1, []),
    "ursodiol": (0, []),
    "valacyclovir": (0, []),
    "valproic acid": (1, ["depakote", "sodium valproate"]),
    "valsartan": (0, []),
    "vancomycin": (1, []),
    "vardenafil": (0, []),
    "varenicline": (0, []),
    "venlafaxine": (1, ["effexor"]),
    "verapamil": (0, []),
    "vigabatrin": (0, []),
    "vilazodone": (0, []),
    "vincristine": (0, []),
    "vortioxetine": (0, []),
    "warfarin": (0, ["coumadin"]),
    "zafirlukast": (0, []),
    "zaleplon": (0, []),
    "zidovudine": (0, []),
    "ziprasidone": (1, []),
    "zoledronic acid": (0, []),
    "zolmitriptan": (1, []),
    "zopiclone": (0, ["zolpidem"]),
    "zuclopenthixol": (1, []),
    "pericyazine": (3, []),
    "perindopril": (0, []),
    "nefopam": (2, ["nefogesic"]),
    "hydroxyzine": (1, ["atarax", "vistaril"]),
    "pramipexole": (1, []),
}

# Build a reverse lookup: brand name  generic name
BRAND_TO_GENERIC = {}
for generic, (score, brands) in ACB_DATABASE.items():
    for brand in brands:
        BRAND_TO_GENERIC[brand.lower()] = generic


def lookup_drug(name: str):
    """
    Look up a drug by generic or brand name.
    Returns (canonical_name, score, brands) or None if not found.
    """
    key = name.strip().lower()

    # Direct match in database
    if key in ACB_DATABASE:
        score, brands = ACB_DATABASE[key]
        return (key, score, brands)

    # Try brand name lookup
    if key in BRAND_TO_GENERIC:
        generic = BRAND_TO_GENERIC[key]
        score, brands = ACB_DATABASE[generic]
        return (generic, score, brands)

    # Fuzzy partial match (substring)
    matches = [
        drug for drug in ACB_DATABASE
        if key in drug or drug in key
    ]
    if len(matches) == 1:
        score, brands = ACB_DATABASE[matches[0]]
        return (matches[0], score, brands)
    if len(matches) > 1:
        # Return closest (shortest) match
        best = min(matches, key=len)
        score, brands = ACB_DATABASE[best]
        return (best, score, brands)

    return None


def score_label(score: int) -> str:
    if score == 0:
        return "No anticholinergic burden"
    elif score == 1:
        return "Possible anticholinergic burden"
    elif score == 2:
        return "Definite anticholinergic burden (moderate)"
    elif score == 3:
        return "Definite anticholinergic burden (high)"
    return "Unknown"


def calculate_acb(drug_names: list[str]) -> dict:
    """
    Calculate ACB score for a list of drug names.
    Returns a dict with per-drug results and totals.
    """
    results = []
    total_score = 0
    not_found = []

    for name in drug_names:
        match = lookup_drug(name)
        if match:
            canonical, score, brands = match
            total_score += score
            results.append({
                "input": name,
                "canonical_name": canonical.title(),
                "score": score,
                "score_label": score_label(score),
                "brand_names": [b.title() for b in brands],
            })
        else:
            not_found.append(name)
            results.append({
                "input": name,
                "canonical_name": None,
                "score": 0,
                "score_label": "Not found in database (assume score 0)",
                "brand_names": [],
            })

    high_risk = total_score >= 3

    return {
        "drugs": results,
        "total_acb_score": total_score,
        "high_risk": high_risk,
        "risk_summary": (
            "  HIGH RISK (score  3): Associated with increased risk of confusion, falls, and mortality. "
            "Please review medications and consider switching to lower-risk alternatives."
            if high_risk else
            " Lower risk (score < 3)"
        ),
        "not_found": not_found,
    }


def print_report(result: dict):
    print("\n" + "=" * 60)
    print("        ACB (Anticholinergic Burden) Report")
    print("=" * 60)

    for drug in result["drugs"]:
        print(f"\n  Drug:   {drug['input']}")
        if drug["canonical_name"]:
            print(f"  Match:  {drug['canonical_name']}", end="")
            if drug["brand_names"]:
                print(f"  (Brands: {', '.join(drug['brand_names'])})", end="")
            print()
        print(f"  Score:  {drug['score']}    {drug['score_label']}")

    print("\n" + "-" * 60)
    print(f"  TOTAL ACB SCORE:  {result['total_acb_score']}")
    print(f"  {result['risk_summary']}")

    if result["not_found"]:
        print(f"\n    Not found in database (scored as 0): {', '.join(result['not_found'])}")

    print("\n  Score guide:")
    print("    0 = No anticholinergic burden")
    print("    1 = Possible anticholinergic burden")
    print("    2 = Definite burden (moderate)")
    print("    3 = Definite burden (high)")
    print("    3 total = HIGH RISK")
    print("=" * 60)
    print("\n    For informational/educational use only.")
    print("  Not a substitute for professional medical advice.\n")


#  Main 

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        # Drugs passed as command-line arguments
        drugs = sys.argv[1:]
    else:
        # Interactive mode
        print("ACB Calculator  enter drug names separated by commas:")
        raw = input("> ")
        drugs = [d.strip() for d in raw.split(",") if d.strip()]

    if not drugs:
        print("No drugs entered. Exiting.")
        sys.exit(0)

    result = calculate_acb(drugs)
    print_report(result)
