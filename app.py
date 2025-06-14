from flask import Flask, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

VIEWS_FILE = "views.txt"

def get_current_views():
    if not os.path.exists(VIEWS_FILE):
        with open(VIEWS_FILE, "w") as f:
            f.write("0")
        return 0
    with open(VIEWS_FILE, "r") as f:
        return int(f.read())

def increment_views():
    views = get_current_views() + 1
    with open(VIEWS_FILE, "w") as f:
        f.write(str(views))
    return views

@app.route("/increment-view", methods=["GET"])
def handle_view():
    updated_views = increment_views()
    return jsonify({"views": updated_views})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
