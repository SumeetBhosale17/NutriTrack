# NutriTrack: Personal Digital Diet & Nutrition Auditor
---

## Problem Statement

Modern lifestyles, busy schedules, and lack of nutritional awareness lead people to consume imbalanced diets—too many empty calories, sugar-rich foods, or insufficient vitamins and minerals.
Existing diet tracking solutions are either overly complex, focused on Western foods, or require paid subscriptions.
There is a lack of a user-friendly, Indian-food–inclusive, digital nutrition auditor that provides personalized and contextual recommendations without depending on Machine Learning.

---

## Objective / Goal
The primary goal of this project is to develop a **web-based diet and nutrition auditing system** that allows multiple users to log their daily food intake, track both **macronutrients and micronutrients**, analyze diet patterns over time, and receive **context-aware dietary recommendations** for improved health and lifestyle management.

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
        - Time of day (e.g., dinner advice if carb intake is already high).
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


## Implementation Roadmap

### Phase 1: Core Setup
- [ ] Setup Flask project structure
- [ ] Configure SQLite database
- [ ] User login/registration system
- [ ] Profile management

### Phase 2: Food Database & Logging
- [ ] Curate Indian food dataset (CSV/SQLite)
- [ ] Food logging form (manual input + portion size)
- [ ] Nutrition calculation (macros + micros)

### Phase 3: Dashboard & Analysis
- [ ] Daily dashboard (calories, macros pie, micros bar)
- [ ] Weekly/monthly trends (line charts, heatmaps)

### Phase 4: Recommendations & Planner
- [ ] Implement basic rule-based recommendations
- [ ] Extend to context-aware recommendations
- [ ] Add Meal Planner (auto suggestions)

### Phase 5: Reports & Gamification
- [ ] Export to PDF/Excel
- [ ] Implement gamification (badges, streaks, leaderboards)

### Phase 6: UI Polish
- [ ] Dashboard-style layout with Bootstrap/Tailwind
- [ ] Responsive and polished frontend
