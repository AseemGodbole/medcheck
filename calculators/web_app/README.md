# MedCheck Web App

A web application for medication safety screening (ACB, Beers, STOPP/START). Deploy to Render for free.

## Local Setup

```bash
cd calculators/web_app
pip install -r requirements.txt
python app.py
```

Open http://localhost:5000

## Deploy to Render (Free)

1. Push this folder to GitHub.
2. Go to https://render.com and sign up.
3. Create a new **Web Service**.
4. Connect your GitHub repo.
5. Set:
   - **Build command:** `pip install -r requirements.txt`
   - **Start command:** `python app.py`
6. Click Deploy.

Render's free tier includes:
- Up to 750 hours/month (always-on).
- Auto-sleep after 15 minutes of inactivity (can restart).
- Great for demos.

Your live URL will be something like: `https://medcheck-xxxxx.onrender.com`

Share that link with your founder!
