"""
# ⚖️ AI-Powered Legal Case Scheduler

A Flask web app that automatically schedules tasks by calculating an **Urgency Score** based on priority and deadline.

## 📋 Requirements
* **Python 3.x**
* **Libraries:** `flask`, `pandas`, `numpy`, `scikit-learn`

## ⚙️ Setup & Run

1. **Install Dependencies:**
   ```bash
   pip install flask pandas numpy scikit-learn
   ```

2. **Run the App:**
   ```bash
   python app.py
   ```
   *(Note: No template folder needed for this version; everything is in this file)*

3. **Open Browser:**
   Go to `http://127.0.0.1:5000/`

## 🧠 How It Works
The app calculates urgency using this logic:
* **Priority:** User input is scaled to 1–100.
* **Deadline:** Randomly assigned (0–180 days).
* **Score:** `Urgency = Priority / (Days_Until_Deadline + 1)`

## 📂 Data Storage
* **Input:** `Example_Cases.csv` (Raw data)
* **Output:** `scheduled_cases.csv` (Sorted by urgency)
