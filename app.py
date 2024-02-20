from flask import Flask, render_template, jsonify
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask("__name__", template_folder='templates', static_folder='static')

@app.route("/")
def index():
    GMAP_KEY = os.getenv("GMAP_KEY")
    return render_template("index.html", GMAP_KEY=GMAP_KEY)


if __name__ == "__main__":
    app.run(debug=True)
    
