from flask import Flask, render_template, request
import re

app = Flask(__name__)

def extract_video_id(url):
    # Works for both short and full YouTube links
    match = re.search(r"(?:v=|be/)([a-zA-Z0-9_-]{11})", url)
    return match.group(1) if match else None

@app.route("/", methods=["GET", "POST"])
def index():
    video_url = None
    if request.method == "POST":
        input_url = request.form.get("youtube_url")
        video_id = extract_video_id(input_url)
        if video_id:
            video_url = f"https://www.youtube.com/embed/{video_id}?autoplay=1&mute=1"  # mute=1 for autoplay to work without click
    return render_template("index.html", video_url=video_url)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
