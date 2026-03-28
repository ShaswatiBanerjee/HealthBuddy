from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash

from models import db, User

from modules.bmi.routes import bmi_bp
from modules.water.routes import water_bp
from modules.bp.routes import bp_bp
from modules.sugar.routes import sugar_bp
from modules.mood.routes import mood_bp


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///health.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "supersecretkey"

db.init_app(app)

app.register_blueprint(bmi_bp)
app.register_blueprint(water_bp)
app.register_blueprint(bp_bp)
app.register_blueprint(sugar_bp)
app.register_blueprint(mood_bp)


# Home route
@app.route("/")
def home():
    return render_template("index.html")

# Register route
@app.route("/register", methods=["GET","POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])

        existing = User.query.filter_by(email=email).first()

        if existing:
            return "Email already registered"

        new_user = User(
            name=name,
            email=email,
            password=password
        )

        db.session.add(new_user)
        db.session.commit()

        return redirect("/login")

    return render_template("register.html")

# Log-in route
@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password,password):

            session["user_id"] = user.id
            session["user_name"] = user.name

            return redirect("/dashboard")

        return "Invalid credentials"

    return render_template("login.html")

# Dashboard route
@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/login")

    return render_template(
        "dashboard.html",
        name=session["user_name"]
    )

# Log-out route 
@app.route("/logout")
def logout():

    session.clear()
    return redirect("/")



import os

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    
