from flask import Flask, redirect, url_for, render_template, request
app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template("index.html")

@app.route("/visualization")
def viz():
    return render_template("visualization.html")

@app.route("/admin")
def admin():
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run()