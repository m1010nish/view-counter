from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

VIEWS_FILE = "views.txt"
IPS_FILE = "ips.txt"

# Ensure both files exist
def ensure_files_exist():
    for file in [VIEWS_FILE, IPS_FILE]:
        if not os.path.exists(file):
            with open(file, "w") as f:
                f.write("0" if file == VIEWS_FILE else "")

def get_current_views():
    with open(VIEWS_FILE, "r") as f:
        return int(f.read())

def get_ip_list():
    with open(IPS_FILE, "r") as f:
        return set(line.strip() for line in f.readlines())

def increment_views():
    views = get_current_views() + 1
    with open(VIEWS_FILE, "w") as f:
        f.write(str(views))
    return views

def add_ip(ip):
    with open(IPS_FILE, "a") as f:
        f.write(ip + "\n")

@app.route("/increment-view", methods=["GET"])
def handle_view():
    ensure_files_exist()

    # Get visitor's IP
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)

    seen_ips = get_ip_list()

    if ip not in seen_ips:
        views = increment_views()
        add_ip(ip)
    else:
        views = get_current_views()

    return jsonify({
        "views": views,
        "your_ip": ip,
        "unique": ip not in seen_ips
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
