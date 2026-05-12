# 🩺 HealthBuddy – Smart-Enhanced Health Monitoring System

HealthBuddy is a comprehensive full-stack web application designed to help users monitor and improve their physical and mental well-being through a centralized, intelligent, and user-friendly platform.

## 🚀 Key Features

* **🔐 Secure User Authentication:** Registration and login system using cryptographic password hashing (Werkzeug).
* **📊 Diverse Health Tracking Modules:**
  * **BMI Calculator:** Tracks daily caloric intake and logs long-term BMI progress.
  * **Water Tracker:** Monitors daily hydration against customized goals with a gamified achievement system.
  * **Blood Pressure Monitor:** Securely logs systolic and diastolic readings.
  * **Blood Sugar Tracker:** Records glucose levels and provides contextual health status feedback.
* **🧠 Smart Mood Tracker (Core Module):**
  * **Automated Sentiment Analysis:** Uses Natural Language Processing (NLP) via VADER to detect emotional polarity from user journal entries.
  * **Smart Wellness Suggestions:** Triggers personalized actionable advice and multimedia support (e.g., meditation videos) based on detected emotions.
  * **Dual-Chart Visualization:** Dynamic Pie Charts (Mood Distribution) and Bar Charts (Weekly Mood Trends) rendered via Chart.js.
  * **Automated PDF Reporting:** Generates downloadable, multi-page health reports compiling historical data and visual trends.

## 🛠️ Technology Stack

**Frontend:**
* HTML5, CSS3, Bootstrap 5
* Chart.js (Dynamic Client-Side Visualization)
* Jinja2 (Templating Engine)

**Backend:**
* Python 3
* Flask (Web Framework)
* Flask Blueprints (Modular Routing)

**Database & Security:**
* SQLite
* Flask-SQLAlchemy (ORM)
* Werkzeug Security

**Advanced Analysis & Reporting Libraries:**
* `vaderSentiment` (Rule-based NLP Sentiment Analysis)
* `ReportLab` (Dynamic PDF Document Generation)
* `Matplotlib` (Server-Side Graphing for PDFs)
* `pytz` (Timezone Management)

## 🧠 System Architecture

The application follows an advanced Client-Server architecture pattern:
1. **Frontend:** Users interact through a responsive browser interface.
2. **Backend Routing:** The Flask server handles incoming requests and delegates them via modular **Blueprints**.
3. **Analysis Layer:** The Mood module intercepts journal notes and processes them through the VADER NLP Engine before saving.
4. **Database:** Each module processes core business logic and securely interacts with the SQLite database using SQLAlchemy to maintain strict user data isolation.
5. **Reporting Engine:** Aggregates historical data and utilizes Matplotlib and ReportLab to stream downloadable PDF reports back to the user.

## 💡 My Core Contribution 

I designed and developed the **Mood Tracker** module end-to-end. For the final capstone phase, I upgraded this module from a simple logging tool into an intelligent wellness companion. Key contributions include:
* Designing the responsive frontend UI (`mood.html`).
* Implementing the backend logic and database integration.
* Engineering the hybrid NLP emotion detection algorithm using `vaderSentiment`.
* Integrating real-time data visualizations via `Chart.js`.
* Developing the fully automated PDF reporting system utilizing `ReportLab` and `Matplotlib`.

## 📂 Project Structure

```text
HealthBuddy/
│── app.py
│── models.py
│── requirements.txt
│
├── templates/
│   ├── layout.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── mood.html
│   ├── bmi.html
│   ├── water.html
│   ├── sugar.html
│   ├── bp.html
│   └── smart_result.html
│
├── static/
│   ├── css/
│   └── js/
│       └── mood_chart.js
│
└── modules/
    ├── mood/
    │   └── routes.py
    ├── bmi/
    ├── water/
    ├── sugar/
    └── bp/
```

## ⚙️ How to Run the Project

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/ShaswatiBanerjee/HealthBuddy.git](https://github.com/ShaswatiBanerjee/HealthBuddy.git)
   cd HealthBuddy
   ```
2. **Install dependencies:**

```bash
pip install -r requirements.txt
```
3. **Run the application:**

```bash
python app.py
```
4. **Access the platform:**
Open your browser and navigate to:
```bash
http://127.0.0.1:5000/
```
## 🔮 Future Scope

* **📱 Mobile Integration:** Development of a native Android/iOS application for better accessibility.
* **⌚ Wearable Synchronization:** API integration with fitness trackers (e.g., Apple Watch, Fitbit) for automated physical data syncing.
* **📈 Advanced Predictive Analytics:** Cross-module correlation (e.g., analyzing how hydration levels impact daily mood).
* **🔒 Enhanced Data Security:** Implementation of end-to-end encryption for private journal entries.


## 👩‍💻 Authors & Team Contributions

* **🧠 Shaswati Banerjee** – *NLP-Integrated Mood Tracker (Core Contribution)*
* **⚖️ Riddhiman Banerjee** – *BMI Calculator Module*
* **💧 Ronit Banerjee** – *Water Intake Tracker Module*
* **🩸 Tanmoy Bapari** – *Blood Sugar Monitoring Module*
* **🩺 Aryaman Barua** – *Blood Pressure Tracking Module*


