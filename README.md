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

---

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

---

## 🗂️ Modular Development Roadmap – NutriTrack
### Phase 1: Core Setup & User Management

Goal: Build the project foundation and authentication system.

- Sumeet

    - Setup Flask project structure (routes, templates, static, DB config).

    - Configure SQLite database.

    - Create database schema (Users, Profiles, Food, Logs, Reports).

- Vivek

    - Implement User Registration + Login with password hashing.

    - Create Profile Management module (age, gender, weight, activity, diet preferences, allergies).

    - Basic frontend forms for login/registration/profile.

✅ Deliverable: Working multi-user login + profile system with DB.

### Phase 2: Food Database & Logging

Goal: Create Indian food database and logging system.

- Sumeet

    - Curate CSV/SQLite database of Indian foods with macros + micronutrients.

    - Write data handling functions (using Pandas) to fetch nutrition values from DB.

- Vivek

    - Build Food Logging UI (form for manual entry + portion sizes).

    - Connect form to backend → save logs in DB.

    - Daily nutrition calculation (totals for macros + micros).

✅ Deliverable: Food logging system with database connection.

### Phase 3: Dashboard & Analysis

Goal: Build user dashboard + analysis features.

- Sumeet

    - Backend data processing: daily/weekly summaries with Pandas.

    - Generate plots (Matplotlib/Seaborn) → calories, macros pie, micros bar.

- Vivek

    - Design Dashboard UI (Bootstrap/Tailwind).

    - Display charts, daily summary cards, and streak counter.

✅ Deliverable: Interactive dashboard with charts + daily/weekly tracking.

### Phase 4: Recommendations & Meal Planner

Goal: Add intelligence with context-aware advice.

- Sumeet

    - Implement Rule-based → extend to Context-Aware Recommendations.

    - Example: If carbs > 70% by dinner → suggest protein-rich dinner options.

- Vivek

    - Develop Meal Planner (generate balanced meals from DB).

    - UI integration for recommendations + meal planner.

✅ Deliverable: Smart recommendations + meal planner visible on dashboard.

### Phase 5: Reports & Gamification

Goal: Enhance usability and engagement.

- Sumeet

    - PDF report generation (ReportLab) with daily/weekly summaries.

    - Excel export (OpenPyXL).

- Vivek

    -Implement Gamification: badges, streaks, leaderboards.

    - UI integration of gamification elements.

✅ Deliverable: Exportable reports + gamified user experience.

### Phase 6: UI Polish & Final Integration

Goal: Deliver a polished, production-ready dashboard.

- Sumeet

    - Backend optimization (clean routes, modularize functions).

    - API endpoints for food/nutrition (if needed for future expansion).

- Vivek

    - Polished frontend dashboard (navigation, responsive design).

    - Final UI/UX improvements.

✅ Deliverable: Fully working NutriTrack web app with polished dashboard.

### ⚖️ Task Balance

- Sumeet → More backend/data handling heavy (DB, Pandas, reports, recommendations).

- Vivek → More frontend/UI heavy (forms, dashboard, gamification, styling).

Both share integration tasks and testing.

### 📆 Suggested Timeline (6 Weeks)

- Week 1 → Phase 1 (User Management)

- Week 2 → Phase 2 (Food Database + Logging)

- Week 3 → Phase 3 (Dashboard + Analysis)

- Week 4 → Phase 4 (Recommendations + Planner)

- Week 5 → Phase 5 (Reports + Gamification)

- Week 6 → Phase 6 (Polish, testing, documentation)

## Contributors
<table>
  <tr>
    <td align="center">
      <a href="https://github.com/SumeetBhosale17">
        <img src="https://github.com/SumeetBhosale17.png" width="80px;" alt="Sumeet Bhosale"/><br />
        <sub><b>Sumeet Bhosale</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/viveksisal">
        <img src="https://github.com/viveksisal.png" width="80px;" alt="Siddhant Kore"/><br />
        <sub><b>Siddhant Kore</b></sub>
      </a>
    </td>
  </tr>
</table>