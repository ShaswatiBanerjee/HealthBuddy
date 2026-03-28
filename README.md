# 🩺 HealthBuddy – A Tool for a Healthier You

HealthBuddy is a full-stack web application designed to help users monitor and improve their physical and mental well-being through a centralized and user-friendly platform.

---

## 🚀 Features

* 🔐 **User Authentication**

  * Secure registration and login using password hashing (Werkzeug)

* 📊 **Health Tracking Modules**

  * BMI Calculator
  * Water Intake Tracker
  * Blood Pressure Monitor
  * Blood Sugar Tracker
  * Mood Tracker (Core Module)

* 😊 **Mood Tracker (Core Contribution)**

  * Log daily mood with notes
  * Real-time mood summary
  * Interactive pie chart visualization (Chart.js)
  * Smart wellness suggestions
  * Mood history tracking

* 📈 **Data Visualization**

  * Dynamic charts using Chart.js for better insights

* 🧩 **Modular Architecture**

  * Implemented using Flask Blueprints for scalability

---

## 🛠️ Tech Stack

**Frontend:**

* HTML5
* CSS3
* Bootstrap 5

**Backend:**

* Python
* Flask

**Database:**

* SQLite
* Flask-SQLAlchemy

**Other Tools:**

* Chart.js
* Jinja2
* Werkzeug Security

---

## 🧠 Project Architecture

The application follows a **client-server architecture**:

* User interacts through a web browser
* Flask backend handles requests via modular Blueprints
* Each module processes logic and interacts with the database
* Dynamic HTML is rendered using Jinja2 templates

---

## 💡 My Contribution

I developed the **Mood Tracker module end-to-end**, including:

* Frontend interface (mood.html)
* Backend logic using Flask
* Database integration using SQLAlchemy
* Data visualization using Chart.js
* Smart suggestion system
* Mood history tracking

---

## 📂 Project Structure

```bash
HealthBuddy/
│── app.py
│── models.py
│── requirements.txt
│
├── templates/
│   ├── layout.html
│   ├── mood.html
│   ├── bmi.html
│   ├── water.html
│   ├── sugar.html
│   └── bp.html
│
├── static/
│   ├── css/
│   └── js/
│
├── modules/
│   ├── mood/
│   ├── bmi/
│   ├── water/
│   ├── sugar/
│   └── bp/
```

---

## ⚙️ How to Run the Project

1. Clone the repository:

```bash
git clone https://github.com/your-username/HealthBuddy.git
cd HealthBuddy
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the application:

```bash
python app.py
```

4. Open in browser:

```
http://127.0.0.1:5000/
```

---

## 🔮 Future Scope

* Sentiment analysis for mood notes
* Automated PDF mood reports
* Improved UI/UX and mobile responsiveness
* Advanced analytics for health insights

---

## 👩‍💻 Author

**Shaswati Banerjee**
Student, IIT Patna

---

## 📌 Note

This project was developed as part of the Capstone-I course and demonstrates a complete full-stack web development approach.
