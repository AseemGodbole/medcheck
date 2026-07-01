# Nivarak Web App

Flask web application for the Nivarak medication safety checker. See the root README for full feature documentation.

## Local Setup

```bash
cd calculators/web_app
pip install -r requirements.txt
python app.py
```

Open [http://localhost:5000](http://localhost:5000)

## Deploy to Render

1. Push to GitHub (main branch).
2. Go to [render.com](https://render.com) and create a **Web Service**.
3. Connect the GitHub repo and set:
   - **Build command:** `pip install -r requirements.txt`
   - **Start command:** `python app.py`
4. Deploy. Auto-redeploy triggers on every push to main.

## API

`POST /check` — accepts JSON body `{ "drugs": [...], "conditions": [...] }`, returns a structured safety report.

The core logic lives in `calculators/med_checker.py` → `get_structured_results(drug_names, conditions)`.
