from flask import Flask, render_template
from database import get_logs

app = Flask(__name__)

@app.route("/")
def index():
    logs = get_logs()
    return render_template("index.html", logs=logs)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
