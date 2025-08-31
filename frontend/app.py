from flask import Flask, render_template
import os
app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route("/")
def index():
    backend_url = os.getenv("BACKEND_URL", "http://backend:5000")
    return render_template("index.html", backend_url=backend_url)
