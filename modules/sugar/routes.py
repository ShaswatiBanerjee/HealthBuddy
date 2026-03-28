from flask import Blueprint, render_template, request, session, redirect
from models import db, Sugar
from datetime import datetime

sugar_bp = Blueprint("sugar", __name__)

@sugar_bp.route("/sugar", methods=["GET","POST"])
def sugar():

    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":

        sugar_level = float(request.form["sugar"])

        entry = Sugar(
            sugar_level=sugar_level,
            entry_date=str(datetime.today()),
            user_id=session["user_id"]
        )

        db.session.add(entry)
        db.session.commit()

    history = Sugar.query.filter_by(user_id=session["user_id"]).all()

    return render_template("sugar.html", history=history)