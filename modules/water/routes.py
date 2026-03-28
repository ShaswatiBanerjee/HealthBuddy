from flask import Blueprint, render_template, request, session, redirect
from models import db, Water
from datetime import datetime

water_bp = Blueprint("water", __name__)

@water_bp.route("/water", methods=["GET", "POST"])
def water():

    if "user_id" not in session:
        return redirect("/login")

    today = str(datetime.today())
    daily_goal = 2.5

    if request.method == "POST":

        amount = float(request.form["amount"])

        entry = Water(
            amount=amount,
            entry_date=today,
            user_id=session["user_id"]
        )

        db.session.add(entry)
        db.session.commit()

    entries = Water.query.filter_by(
        user_id=session["user_id"],
        entry_date=today
    ).all()

    total = sum(e.amount for e in entries)
    percentage = min((total / daily_goal) * 100, 100)

    return render_template(
        "water.html",
        total=round(total,2),
        goal=daily_goal,
        percentage=round(percentage,1),
        history=entries
    )