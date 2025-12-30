from flask import Flask, redirect, request, session, url_for
import requests
import os
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = "dev-secret-key"  # intentionally weak for lab

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
USERINFO_URL = "https://www.googleapis.com/oauth2/v1/userinfo"

LOG_FILE = "logs/auth.log"

def log_event(event_type, data):
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "event": event_type,
        "ip": request.remote_addr,
        "user_agent": request.headers.get("User-Agent"),
        "data": data
    }
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

@app.route("/")
def index():
    return '<a href="/login">Login with Google</a>'

@app.route("/login")
def login():
    auth_params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "consent"
    }
    url = requests.Request("GET", AUTH_URL, params=auth_params).prepare().url
    return redirect(url)

@app.route("/callback")
def callback():
    code = request.args.get("code")

    # ⚠️ INTENTIONAL LOGGING FLAW
    log_event("oauth_code_received", {"code": code})

    token_data = {
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code"
    }

    token_response = requests.post(TOKEN_URL, data=token_data).json()

    # ⚠️ TOKEN LOGGED IN PLAINTEXT (BAD PRACTICE)
    log_event("token_issued", token_response)

    access_token = token_response.get("access_token")

    headers = {"Authorization": f"Bearer {access_token}"}
    userinfo = requests.get(USERINFO_URL, headers=headers).json()

    log_event("userinfo_accessed", userinfo)

    session["user"] = userinfo
    return redirect(url_for("dashboard"))

@app.route("/dashboard")
def dashboard():
    user = session.get("user")
    if not user:
        return redirect("/")
    return f"""
    <h2>Welcome {user.get('email')}</h2>
    <p>You are logged in.</p>
    """

if __name__ == "__main__":
    app.run(debug=True)
