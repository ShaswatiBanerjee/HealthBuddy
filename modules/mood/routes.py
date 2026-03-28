from flask import Blueprint, render_template, request, session, redirect, url_for
from models import db, Mood
from datetime import datetime

mood_bp = Blueprint("mood", __name__)

@mood_bp.route('/mood', methods=['GET', 'POST'])
def mood():

    
    if "user_id" not in session:
        return redirect("/login")

    
    if request.method == 'POST':
        selected_mood = request.form.get('mood')
        note = request.form.get('note')
        if not note:
            return "Note is required"

        if selected_mood:
            new_mood = Mood(
                mood=selected_mood,
                note=note,
                user_id=session["user_id"]
            )
            db.session.add(new_mood)
            db.session.commit()

            return redirect(url_for('mood.mood'))

    
    moods = Mood.query.filter_by(
        user_id=session["user_id"]
    ).order_by(Mood.date.desc()).all()
    
    suggestion = None
    video_link = None
    latest_mood = None

    if moods:
     latest_mood = moods[0].mood

    if latest_mood == "Happy 😊":
        suggestion = "Keep the positivity going! Spread your smile today 🌞"
        video_link = None

    elif latest_mood == "Sad 😔":
        suggestion = "You seem stressed. Try this 5 minute breathing meditation 🧘"
        video_link = "https://youtu.be/inpok4MKVLM"

    elif latest_mood == "Angry 😡":
        suggestion = "Take a pause. Deep breathing can calm your mind."
        video_link = "https://youtu.be/inpok4MKVLM"

    elif latest_mood == "Excited 🤩":
        suggestion = "Great energy! Use it for something creative or productive."
        video_link = None

    elif latest_mood == "Neutral 😐":
        suggestion = "A short walk or calm music can refresh your mind."
        video_link = None

    mood_counts = {
        "Happy 😊": Mood.query.filter_by(
            mood="Happy 😊",
            user_id=session["user_id"]
        ).count(),

        "Sad 😔": Mood.query.filter_by(
            mood="Sad 😔",
            user_id=session["user_id"]
        ).count(),

        "Angry 😡": Mood.query.filter_by(
            mood="Angry 😡",
            user_id=session["user_id"]
        ).count(),

        "Excited 🤩": Mood.query.filter_by(
            mood="Excited 🤩",
            user_id=session["user_id"]
        ).count(),

        "Neutral 😐": Mood.query.filter_by(
            mood="Neutral 😐",
            user_id=session["user_id"]
        ).count()
    }

    return render_template(
        'mood.html',
        moods=moods,
        mood_counts=mood_counts,
        suggestion=suggestion,
        video_link=video_link
    )