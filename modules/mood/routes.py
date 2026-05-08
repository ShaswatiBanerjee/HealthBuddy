from flask import Blueprint, render_template, request, session, redirect, send_file
from models import db, Mood
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from reportlab.pdfgen import canvas
from collections import defaultdict
from datetime import datetime, timedelta
import random

mood_bp = Blueprint("mood", __name__)

analyzer = SentimentIntensityAnalyzer()


# =========================
# 🧠 MOOD DETECTION (5 TYPES)
# =========================
def detect_mood(note):
    note_lower = note.lower()

    # 😡 ANGRY
    angry_words = [
        "angry", "mad", "furious", "rage",
        "annoyed", "irritated", "hate",
        "frustrated", "frustrating"
    ]

    if any(word in note_lower for word in angry_words):
        return "Angry 😡"

    # 😔 SAD
    sad_words = [
        "sad", "depressed", "lonely", "tired",
        "hopeless", "cry", "pain", "hurt",
        "disgusted", "bad", "not happy",
        "not good", "not feeling well"
    ]

    if any(word in note_lower for word in sad_words):
        return "Sad 😔"

    # 🤩 EXCITED
    excited_words = [
        "excited", "thrilled", "amazing",
        "can't wait", "so happy", "awesome",
        "super excited"
    ]

    if any(word in note_lower for word in excited_words):
        return "Excited 🤩"

    # 😊 HAPPY
    happy_words = [
        "happy", "good", "great", "love",
        "fantastic", "productive", "relaxed",
        "completed", "achievement", "win"
    ]

    if any(word in note_lower for word in happy_words):
        return "Happy 😊"

    # 🧠 VADER fallback
    scores = analyzer.polarity_scores(note)
    compound = scores['compound']

    if compound >= 0.5:
        return "Excited 🤩"
    elif compound >= 0.2:
        return "Happy 😊"
    elif compound <= -0.5:
        return "Angry 😡"
    elif compound <= -0.2:
        return "Sad 😔"
    else:
        return "Neutral 😐"


# =========================
# 🌈 MAIN ROUTE
# =========================
@mood_bp.route('/mood', methods=['GET', 'POST'])
def mood():

    if "user_id" not in session:
        return redirect("/login")

    # 🔥 POST
    if request.method == 'POST':
        note = request.form.get('note')

        if not note or not note.strip():
            return "Note is required"

        selected_mood = detect_mood(note)

        new_mood = Mood(
            mood=selected_mood,
            note=note,
            user_id=session["user_id"]
        )

        db.session.add(new_mood)
        db.session.commit()

        return render_template("ai_result.html", emotion=selected_mood)

    # 🔥 GET
    moods = Mood.query.filter_by(
        user_id=session["user_id"]
    ).order_by(Mood.date.desc()).all()

    latest_mood = moods[0].mood if moods else None

    suggestion = None
    video_link = None
    support_msg = None

    # =========================
    # 🎯 SUGGESTIONS (ALL 5 MOODS)
    # =========================
    happy_suggestions = [
        "Keep the positivity going! 🌞",
        "Celebrate your progress 🎉",
        "Share your happiness with someone 🤍",
        "Use this energy productively 🚀"
    ]

    sad_suggestions = [
        "Take deep breaths 🧘",
        "Listen to calm music 🎧",
        "Talk to someone you trust 🤍",
        "Go for a walk 🌿"
    ]

    angry_suggestions = [
        "Pause and breathe deeply 😌",
        "Step away and relax 🧘",
        "Avoid reacting immediately ⚠️",
        "Try physical activity 💪"
    ]

    excited_suggestions = [
        "Channel this energy into work 🚀",
        "Start something new 🔥",
        "Share your excitement 🤩",
        "Make a plan and act 💡"
    ]

    neutral_suggestions = [
        "Take a short walk 🌿",
        "Stay hydrated 💧",
        "Do something creative 🎨",
        "Take a mindful break 🧘"
    ]

    if latest_mood == "Happy 😊":
        suggestion = random.choice(happy_suggestions)

    elif latest_mood == "Sad 😔":
        suggestion = random.choice(sad_suggestions)
        video_link = "https://youtu.be/inpok4MKVLM"
        support_msg = "It's okay to feel this way 💙"

    elif latest_mood == "Angry 😡":
        suggestion = random.choice(angry_suggestions)
        support_msg = "Take it slow. You're in control 💛"

    elif latest_mood == "Excited 🤩":
        suggestion = random.choice(excited_suggestions)

    elif latest_mood == "Neutral 😐":
        suggestion = random.choice(neutral_suggestions)

    # =========================
    # 📊 MOOD COUNTS
    # =========================
    mood_counts = {
        "Happy 😊": Mood.query.filter_by(mood="Happy 😊", user_id=session["user_id"]).count(),
        "Sad 😔": Mood.query.filter_by(mood="Sad 😔", user_id=session["user_id"]).count(),
        "Angry 😡": Mood.query.filter_by(mood="Angry 😡", user_id=session["user_id"]).count(),
        "Excited 🤩": Mood.query.filter_by(mood="Excited 🤩", user_id=session["user_id"]).count(),
        "Neutral 😐": Mood.query.filter_by(mood="Neutral 😐", user_id=session["user_id"]).count()
    }

    # =========================
    # 📈 INSIGHT
    # =========================
    if mood_counts["Sad 😔"] >= 3:
        insight = "You've been feeling low recently 💙"
    elif mood_counts["Angry 😡"] >= 3:
        insight = "Too much stress detected ⚠️ Try relaxation"
    elif mood_counts["Happy 😊"] > mood_counts["Sad 😔"]:
        insight = "Overall you are doing well 😊"
    else:
        insight = "Your mood is balanced ⚖️"

    # =========================
    # 📅 WEEKLY TREND
    # =========================
    last_week = datetime.now() - timedelta(days=7)

    weekly_moods = Mood.query.filter(
        Mood.user_id == session["user_id"],
        Mood.date >= last_week
    ).all()

    day_data = defaultdict(list)

    for mood_obj in weekly_moods:
        day_name = mood_obj.date.strftime("%a")
        day_data[day_name].append(mood_obj.mood)

    mood_score_map = {
        "Happy 😊": 1,
        "Excited 🤩": 1,
        "Neutral 😐": 0,
        "Sad 😔": -1,
        "Angry 😡": -1
    }

    weekly_labels = [(datetime.now() - timedelta(days=i)).strftime("%a") for i in range(6, -1, -1)]
    weekly_scores = []

    for day in weekly_labels:
        moods_list = day_data.get(day, [])

        if moods_list:
            avg = sum([mood_score_map.get(m, 0) for m in moods_list]) / len(moods_list)
        else:
            avg = 0

        weekly_scores.append(round(avg, 2))

    # =========================
    # 📊 PERCENTAGE
    # =========================
    total = sum(mood_counts.values())

    if total > 0:
        mood_percent = {
            mood: round((count / total) * 100, 1)
            for mood, count in mood_counts.items()
        }
    else:
        mood_percent = {m: 0 for m in mood_counts}

    return render_template(
        "mood.html",
        moods=moods,
        mood_counts=mood_counts,
        suggestion=suggestion,
        video_link=video_link,
        insight=insight,
        weekly_labels=weekly_labels,
        weekly_scores=weekly_scores,
        mood_percent=mood_percent,
        support_msg=support_msg
    )


# =========================
# 📄 PDF DOWNLOAD
# =========================
from flask import send_file
import matplotlib.pyplot as plt
import os

@mood_bp.route('/download-report')
def download_report():

    if "user_id" not in session:
        return redirect("/login")

    moods = Mood.query.filter_by(user_id=session["user_id"]).all()

    # =========================
    # 📊 COUNT DATA
    # =========================
    mood_counts = {
        "Happy 😊": 0,
        "Sad 😔": 0,
        "Angry 😡": 0,
        "Excited 🤩": 0,
        "Neutral 😐": 0
    }

    for m in moods:
        if m.mood in mood_counts:
            mood_counts[m.mood] += 1

    # =========================
    # 🥧 PIE CHART
    # =========================
    labels = list(mood_counts.keys())
    values = list(mood_counts.values())

    plt.figure()
    plt.pie(values, labels=labels, autopct='%1.1f%%')
    pie_path = "pie.png"
    plt.savefig(pie_path)
    plt.close()

    # =========================
    # 📅 WEEKLY GRAPH
    # =========================
    from datetime import datetime, timedelta
    from collections import defaultdict

    last_week = datetime.now() - timedelta(days=7)

    weekly_moods = [
        m for m in moods if m.date >= last_week
    ]

    day_data = defaultdict(list)

    for m in weekly_moods:
        day = m.date.strftime("%a")
        day_data[day].append(m.mood)

    mood_score_map = {
        "Happy 😊": 1,
        "Excited 🤩": 1,
        "Neutral 😐": 0,
        "Sad 😔": -1,
        "Angry 😡": -1
    }

    days = [(datetime.now() - timedelta(days=i)).strftime("%a") for i in range(6, -1, -1)]
    scores = []

    for d in days:
        moods_list = day_data.get(d, [])
        if moods_list:
            avg = sum([mood_score_map.get(m, 0) for m in moods_list]) / len(moods_list)
        else:
            avg = 0
        scores.append(avg)

    plt.figure()
    plt.plot(days, scores, marker='o')
    plt.ylim(-1, 1)
    plt.title("Weekly Mood Trend")
    graph_path = "weekly.png"
    plt.savefig(graph_path)
    plt.close()

    # =========================
    # 📄 CREATE PDF (ADVANCED)
    # =========================
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
    from reportlab.lib.styles import getSampleStyleSheet

    pdf_path = "mood_report.pdf"

    doc = SimpleDocTemplate(pdf_path)
    styles = getSampleStyleSheet()

    elements = []

    elements.append(Paragraph("<b>HealthBuddy Mood Report</b>", styles['Title']))
    elements.append(Spacer(1, 20))

    elements.append(Paragraph("📊 Mood Distribution", styles['Heading2']))
    elements.append(Image(pie_path, width=400, height=250))
    elements.append(Spacer(1, 20))

    elements.append(Paragraph("📈 Weekly Mood Trend", styles['Heading2']))
    elements.append(Image(graph_path, width=400, height=250))
    elements.append(Spacer(1, 20))

    elements.append(Paragraph("📝 Mood History", styles['Heading2']))

    for m in moods[-10:]:  # last 10 entries
        text = f"{m.date.strftime('%d-%m-%Y')} - {m.mood} - {m.note}"
        elements.append(Paragraph(text, styles['Normal']))
        elements.append(Spacer(1, 10))

    doc.build(elements)

    # =========================
    # 🌐 OPEN IN BROWSER + DOWNLOAD OPTION
    # =========================
    return send_file(pdf_path)