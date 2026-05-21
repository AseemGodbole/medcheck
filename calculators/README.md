# Calculator Integration

This folder is for the medicine/prescription calculator layer that sits after OCR extraction.

## Goal
Take extracted prescription text such as:
- paracetamol
- ibuprofen

and return clinical insights such as:
- anticholinergic burden
- interaction flags
- contraindication reminders
- scoring or risk notes

## Two possible approaches

### 1. Local calculator
Best when the rules are known and deterministic.

Use this when:
- the calculator logic is published or can be recreated
- you want fast offline evaluation
- you want full control over the output

### 2. API call to an external source
Best when the website exposes an API or you have permission to use one.

Use this when:
- the source already maintains the calculator logic
- you want the latest scoring rules from that source
- the site licenses API access

## Recommended flow
1. OCR extracts the prescription text.
2. Normalize drug names.
3. Map drugs to a local rules database or approved API.
4. Compute score/interaction results.
5. Send the final insights to the portal UI.

## Important note
If the website does not provide an API, scraping it may violate its terms of use. In that case, building the calculator locally is usually the safer option.
