
from flask import Blueprint, render_template, request, session, redirect
from models import db, BMI
import io
import matplotlib 
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from flask import send_file

bmi_bp = Blueprint("bmi", __name__)

@bmi_bp.route("/bmi", methods=["GET", "POST"])
def bmi():
    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":
        date = request.form['date']
        height = float(request.form["height"])
        weight = float(request.form["weight"])
        calories = int(request.form['calories'])

        height_m = height / 100
        bmi_value = weight / (height_m ** 2)

        new_entry = BMI(
             date=date, 
             height=height, 
             weight=weight, 
             bmi_value=bmi_value, 
             calories=calories,
             user_id=session["user_id"]
        )
        db.session.add(new_entry)
        db.session.commit()

    history = BMI.query.filter_by(user_id=session["user_id"]).all()
    return render_template("bmi.html", history=history)


@bmi_bp.route("/bmi/graph")
def graph():
    if "user_id" not in session:
        return redirect("/login")
    entries = BMI.query.filter_by(user_id=session["user_id"]).all()

    dates = [str(e.date) for e in entries]
    bmis = [e.bmi_value for e in entries]

    plt.figure()
    plt.plot(dates, bmis, marker='o')
    plt.xlabel("Date")
    plt.ylabel("BMI")
    plt.title("BMI Trend Over Time")
    plt.xticks(rotation=45)

    img = io.BytesIO()
    plt.savefig(img, format='png')
    plt.close()  

    img.seek(0)
    return send_file(img, mimetype='image/png')