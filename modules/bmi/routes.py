
from flask import Blueprint, render_template, request, session, redirect
from models import db, BMI

bmi_bp = Blueprint("bmi", __name__)

@bmi_bp.route("/bmi", methods=["GET", "POST"])
def bmi():

    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":

        height = float(request.form["height"])
        weight = float(request.form["weight"])

        height_m = height / 100
        bmi_value = weight / (height_m ** 2)

        entry = BMI(
            height=height,
            weight=weight,
            bmi_value=bmi_value,
            user_id=session["user_id"]
        )

        db.session.add(entry)
        db.session.commit()

    history = BMI.query.filter_by(user_id=session["user_id"]).all()

    return render_template("bmi.html", history=history)