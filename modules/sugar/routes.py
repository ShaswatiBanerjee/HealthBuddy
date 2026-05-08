from flask import Blueprint, render_template, request, session, redirect
from models import db, Sugar
from datetime import datetime, date

sugar_bp = Blueprint("sugar", __name__)

@sugar_bp.route("/sugar", methods=["GET","POST"])
def sugar():
    if "user_id" not in session:
        return redirect("/login")

    category = None
    recommendation = None

    if request.method == "POST":
        sugar_level = float(request.form["sugar"])

        # CATEGORY LOGIC
        if sugar_level < 70:
            category = "Low"
            recommendation = "Eat something sweet immediately."

        elif 70 <= sugar_level <= 140:
            category = "Normal"
            recommendation = "Good! Maintain your lifestyle."

        else:
            category = "High"
            recommendation = "Avoid sugar and do light exercise."

        # SAVE DATA
        new_entry = Sugar(
            sugar_level=sugar_level,
            entry_date=str(date.today()),
            user_id=session["user_id"]
        )
        db.session.add(new_entry)
        db.session.commit()

    # ALWAYS OUTSIDE POST
    history = Sugar.query.filter_by(user_id=session["user_id"]).all()

    sugar_values = [entry.sugar_level for entry in history]
    dates = [entry.entry_date for entry in history]

    return render_template(
        "sugar.html",
        history=history,
        category=category,
        recommendation=recommendation,
        sugar_values=sugar_values,
        dates=dates,
    )