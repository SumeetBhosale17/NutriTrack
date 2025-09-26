# NutriTrack: Personal Digital Diet & Nutrtion Auditor
---

## Problem Statement

Modern lifestyles, busy schedules, and lack of nutritional awareness lead people to consume imbalanced diets—too many empty calories, sugar-rich foods, or insufficient vitamins and minerals.
Existing diet tracking solutions are either overly complex, focused on Western foods, or require paid subscriptions.
There is a lack of a user-friendly, Indian-food–inclusive, digital nutrition auditor that provides personalized and contextual recommendations without depending on Machine Learning.

---

## Objective / Goal
The primary goal of this project is to develop a **web-based diet and nutrition auditing system** that allows multiple user to log their daily food intake, track both **macronutrients and micronutrients**, analyze diet patterns over time, and receive **context-aware dietary recommendations** for improved health and lifestyle management.

---

## Features
- ### User Management
    - Multi-user support (login, registration, secure password hashing).
    - Profile setup (age, gender, weight, height, activity level, dietary preferences, allergies).

- ### Food Logging & Database
    - Food entry system (manual portion logging)
    - Nutritional database curated for Indian foods with macro + micronutrients.
    - Option to expand with additional datasets.

- ### Analysis & Tracking
    - Daily calorie and macronutrient tracking (Protein, Carbs, Fats).
    - Micronutrient tracking (Iron, Calcium, Vitamin C, Vitamin D, Fiber, Sodium, etc.).
    - Weekly/monthly reports with line charts, pie charts, heatmaps.
- ### Recommendations (Context-Aware)
    - Smart suggestions based on:
        - Time of day (e.g., dinner advice if card intake is already high).
        - Daily Patterns (e.g., "You've had high sugar 3 days in a row, reduce intake tomorrow").
        - Weekly/Monthly trends (e.g., "Consistently low in Vitamin D this month → add fortified foods").
- ### Additional Features
    - Meal Planner (auto generated suggestions)
    - Report export (PDF/Excel for weekly/monthly summaries).
    - Gamification (badges, streaks, leaderboards).
    - Dashboard-style polished UI with charts and navigation.

---

## Technology Stack
- Backend: Python (Flask framework).
- Frontend: HTML, CSS, Bootstrap/Tailwind (dashboard UI)
- Data Handling: Pandas, NumPy.
- Visualization: Matplotlib, Seaborn, Plotly.
- Database: SQLite
- Report Generation: ReportLab (PDF), OpenPyXL (Excel)


## Implementation
- [ ] Multi-user support with login
- [ ] User profiles (age, gender, weight, goals, diet preference)
- [ ] Food database (Indian foods curated CSV/SQLite)
- [ ] Daily logging (manual entry + portion size)
- [ ] Macros + Micronutrients tracking
- [ ] Dashboard (daily calories, macros pie, micros bar, streak counter)
- [ ] Weekly/monthly trend analysis (line charts, heatmaps)
- [ ] Rule-based recommendations → extended to context-aware
- [ ] Meal planner (auto-suggestions)
- [ ] Export reports (PDF/Excel)
- [ ] Gamification (badges, streaks)