from flask import Flask, render_template, request, session
import re
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Replace with a secure key
app.permanent_session_lifetime = timedelta(days=1)

def extract_video_id(url):
    match = re.search(r"(?:v=|be/)([a-zA-Z0-9_-]{11})", url)
    return match.group(1) if match else None

@app.route("/", methods=["GET", "POST"])
def index():
    if "video_id" not in session:
        session["video_id"] = None
        session["autorefresh"] = True
        session["play_count"] = 0

    if request.method == "POST":
        if "new_url" in request.form:
            video_id = extract_video_id(request.form.get("new_url"))
            if video_id:
                session["video_id"] = video_id
                session["play_count"] = 0
                session["autorefresh"] = True
        elif "stop" in request.form:
            session["autorefresh"] = False
        elif "start" in request.form:
            session["autorefresh"] = True

    if session.get("video_id") and session.get("autorefresh"):
        session["play_count"] += 1

    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)

    return render_template("index.html",
                           video_id=session.get("video_id"),
                           autorefresh=session.get("autorefresh"),
                           play_count=session.get("play_count"),
                           ip_address=user_ip)
