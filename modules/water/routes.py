from flask import Blueprint, render_template, request, session, redirect
from models import db, Water
from datetime import date,timedelta

water_bp = Blueprint("water", __name__)

@water_bp.route("/water", methods=["GET", "POST"])
def water():
    if "user_id" not in session:
        return redirect("/login")

    today = str(date.today())
    daily_goal = session.get("goal", 2.5)

    if request.method == "POST":
        # Set goal
        if "goal" in request.form:
            try:
                goal_value = float(request.form["goal"])

                if goal_value <= 0:
                    return "Goal must be greater than 0"

                session["goal"] = goal_value
            except:
                return "Invalid goal input"

        # Add water
        if "amount" in request.form:
            try:
                amount = float(request.form["amount"])
                new_entry = Water(
                    amount=amount,
                    entry_date=today,
                    user_id=session["user_id"]
                )
                db.session.add(new_entry)
                db.session.commit()
            except:
                return "Invalid water input"

    # Fetch today's entries
    today_entries = Water.query.filter_by(
        user_id=session["user_id"],
        entry_date=today
    ).all()

    today_total = sum(entry.amount for entry in today_entries)

    if daily_goal > 0:
        percentage = min((today_total / daily_goal) * 100, 100)
    else:
        percentage = 0

    # 📊 Weekly Data
    last_7_days = date.today() - timedelta(days=7)

    weekly_entries = Water.query.filter(
        Water.user_id == session["user_id"],
        Water.entry_date >= str(last_7_days)
    ).all()

    # Total weekly intake
    weekly_total = sum(entry.amount for entry in weekly_entries)

    # Weekly goal = daily_goal × 7
    weekly_goal = daily_goal * 7

    # Weekly percentage
    if weekly_goal > 0:
        weekly_percentage = (weekly_total / weekly_goal) * 100
    else:
        weekly_percentage = 0

    # 🚨 Smart Alert System
    if today_total == 0:
        alert = "⚠️ You haven't logged any water today! Start drinking 💧"
    elif percentage < 30:
        alert = "🚨 Dehydration risk! Drink water immediately!"
    elif percentage < 70:
        alert = "💧 You need more water. Keep going!"
    elif percentage < 100:
        alert = "👍 Almost there! Complete your daily goal!"
    else:
        alert = "🎉 Great job! You achieved your hydration goal!"

    # 🏆 Badge Logic
    if weekly_percentage < 40:
        badge = "🥉 Beginner"
    elif weekly_percentage < 70:
        badge = "🥈 Consistent"
    elif weekly_percentage < 100:
        badge = "🥇 Hydration Hero"
    else:
        badge = "👑 Water Master"

    # Decide progress bar color
    if percentage < 30:
        color = "bg-danger"     # Red
    elif percentage < 70:
        color = "bg-warning"    # Yellow
    else:
        color = "bg-success"    # Green

    # Punchline Message Logic
    if percentage < 25:
        message = "You need more water 💧 Stay hydrated!"
    elif percentage < 50:
        message = "Good start 👍 Keep drinking!"
    elif percentage < 75:
        message = "Nice progress 💪 You're doing well!"
    elif percentage < 100:
        message = "Almost there 🚀 Finish strong!"
    else:
        message = "Excellent 🎉 You achieved your goal!"

    # 📊 Weekly Summary Calculation
    last_7_days = date.today() - timedelta(days=7)

    weekly_entries = Water.query.filter(
        Water.user_id == session["user_id"],
        Water.entry_date >= str(last_7_days)
    ).all()

    # Total intake in last 7 days
    weekly_total = sum(entry.amount for entry in weekly_entries)

    # Average per day
    weekly_avg = weekly_total / 7

    # Weekly goal
    weekly_goal = daily_goal * 7

    # Weekly percentage
    if weekly_goal > 0:
        weekly_percentage = (weekly_total / weekly_goal) * 100
    else:
        weekly_percentage = 0

    # Graph_1: Daily average (7 days)
    daily_labels = []
    daily_data = []

    for i in range(6, -1, -1):
        day = date.today() - timedelta(days=i)
        day_str = str(day)

        day_entries = Water.query.filter_by(
            user_id=session["user_id"],
            entry_date=day_str
        ).all()

        day_total = sum(e.amount for e in day_entries)

        daily_labels.append(day.strftime("%a"))  # Mon, Tue
        daily_data.append(round(day_total, 2))

    # Graph_2: Weekly average
    weekly_labels = []
    weekly_data = []

    for i in range(3, -1, -1):   # last 4 weeks
        start_day = date.today() - timedelta(days=(i+1)*7)
        end_day = date.today() - timedelta(days=i*7)

        week_entries = Water.query.filter(
            Water.user_id == session["user_id"],
            Water.entry_date >= str(start_day),
            Water.entry_date < str(end_day)
        ).all()

        week_total = sum(e.amount for e in week_entries)

        avg = week_total / 7  # average per day in that week

        weekly_labels.append(f"Week {4-i}")
        weekly_data.append(round(avg, 2))

    return render_template(
        "water.html",
        total=round(today_total, 2),
        goal=daily_goal,
        percentage=round(percentage, 1),
        history=today_entries,
        message=message,
        color=color,
        badge=badge,  
        alert=alert,                    
        weekly_percentage=round(weekly_percentage, 1),   
        weekly_total=round(weekly_total, 2),
        weekly_avg=round(weekly_avg, 2),
        
        # graph 1
        daily_labels=daily_labels,
        daily_data=daily_data,

        # graph 2
        weekly_labels=weekly_labels,
        weekly_data=weekly_data  
    )

@water_bp.route("/undo_water")
def undo_water():
    if "user_id" not in session:
        return redirect("/login")

    # Get last entry of today
    today = str(date.today())

    last_entry = Water.query.filter_by(
        user_id=session["user_id"],
        entry_date=today
    ).order_by(Water.id.desc()).first()

    if last_entry:
        db.session.delete(last_entry)
        db.session.commit()
    else:
        print("No entry to undo")

    return redirect("/water")
