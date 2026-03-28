from flask import Blueprint, render_template, request, session, redirect
from models import db, BP
from datetime import datetime

bp_bp = Blueprint("bp", __name__)

@bp_bp.route("/bp", methods=["GET","POST"])
def bp():

    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":

        systolic = int(request.form["systolic"])
        diastolic = int(request.form["diastolic"])

        entry = BP(
            systolic=systolic,
            diastolic=diastolic,
            entry_date=str(datetime.today()),
            user_id=session["user_id"]
        )

        db.session.add(entry)
        db.session.commit()

    history = BP.query.filter_by(user_id=session["user_id"]).all()

    return render_template("bp.html", history=history)