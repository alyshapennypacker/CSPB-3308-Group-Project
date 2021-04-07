from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    # Render HTML with count variable
    return render_template("index.html")


@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/landing")
def landing():
    return render_template("landing.html")

@app.route("/register")
def register():
    return render_template("register.html")

if __name__ == "__main__":
    app.run()