# NutriTrack — Nutrition Tracking & Analysis Dashboard

NutriTrack is a **data-driven web application** built to practice backend development,
database design, and nutritional data analysis.

The project focuses on **food logging, nutrition statistics, and dashboard-based insights**
rather than advanced recommendations or machine learning.

Development is ongoing and intentionally paced alongside other data science and analytics projects.

---

## 📌 Project Overview

NutriTrack allows users to log daily food intake and view nutritional summaries through
a clean dashboard interface.

The goal is to build a solid foundation for:
- nutritional data modeling
- statistical aggregation
- visual analysis
- scalable backend design

This project is **not production-ready** and is being developed incrementally.

---

## ✅ Current Features (Implemented)

- User authentication
- Daily food logging
- Nutritional calculation (calories & macros)
- Dashboard displaying:
  - daily totals
  - basic statistics
  - visual summaries
- Persistent storage using PostgreSQL
- Containerized development using Docker

---

## 🏗 Architecture & Design

- Backend: Flask (Python)
- Database: PostgreSQL
- Data processing: Pandas, NumPy
- Visualization: Matplotlib / Plotly
- Frontend: HTML, CSS
- Environment: Docker & Docker Compose

The application follows a modular backend structure with:
- route separation
- data access abstraction
- reusable data processing utilities

## Current Demo Setup

Run with Docker:

```bash
docker compose up -d --build
```

Reset Docker data when you do not need old local records:

```bash
docker compose down -v
docker compose up -d --build
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the app locally:

```bash
python run.py
```

Seed a few demo Indian food rows if the food database is empty:

```bash
python scripts/seed.py
```

Reset the local SQLite demo database if the schema is stale:

```bash
python scripts/reset_demo_db.py
```

Import the full Excel dataset:

```bash
python scripts/import_food_data.py
```

Run smoke tests:

```bash
pytest -q
```

---

## ⚠️ Current Technical Debt

- The Alembic migration history needs a clean baseline migration for fresh PostgreSQL databases.
- The demo initializer currently uses `db.create_all()` for local/Docker demo reliability; production should rely on migrations only.
- Runtime, development, testing, data science, and deployment packages are mixed in one `requirements.txt`.
- Database files and local backups should remain untracked and ignored.
- Docker should eventually use health checks instead of retry logic in the app initialization script.
- UI templates are functional but still need component reuse, consistent layout rules, and accessibility polish.

---

## 🧰 Tech Stack

| Layer | Technology |
|-----|-----------|
| Backend | Python (Flask) |
| Database | PostgreSQL |
| Data Processing | Pandas, NumPy |
| Visualization | Matplotlib, Plotly |
| Frontend | HTML, CSS |
| Containerization | Docker |

---

## 📊 Dashboard Capabilities

- Daily calorie overview
- Macronutrient breakdown
- Food consumption statistics
- Simple visual summaries for quick insights

---

## 🚧 Planned Enhancements (Not Yet Implemented)

- Micronutrient tracking
- Weekly/monthly trend analysis
- Rule-based dietary suggestions
- PDF/Excel report export
- Improved frontend dashboard UI

These features are planned but **not currently implemented**.

---

## 📚 What I’m Learning From This Project

- Designing data schemas for real-world datasets
- Aggregating and analyzing time-series nutrition data
- Building dashboards that communicate insights clearly
- Using Docker for reproducible development environments
- Structuring Flask applications for long-term extensibility

---

## ⏸ Development Status

NutriTrack is being developed gradually.
Current focus is on **data science, machine learning fundamentals**, and
a sports biomechanics analysis project.

This repository will be revisited and expanded once core priorities are completed.

---

## 👤 Author
  
<a href="https://github.com/SumeetBhosale17">
    <img src="https://github.com/SumeetBhosale17.png" width="80px;" alt="Sumeet Bhosale"/>
    <br />
    <sub><b>Sumeet Bhosale</b></sub>
