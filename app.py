from flask import Flask, render_template, request
import os
from database import get_logs, setup_db
from sender import send_bulk_messages
from config import UPLOAD_FOLDER

app = Flask(__name__)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["csv_file"]
        if file:
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)
            send_bulk_messages(file.filename)
            return "✅ File uploaded and messages sent!"

    logs = get_logs()
    return render_template("index.html", logs=logs)

if __name__ == "__main__":
    setup_db()
    app.run(host="0.0.0.0", port=8080)
