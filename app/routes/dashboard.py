import os

os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib")

import matplotlib
matplotlib.use('Agg')

from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
import matplotlib.pyplot as plt
import io
import base64
from datetime import date
from app.models import UserMealLog

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.dashboard'))
    return redirect(url_for('auth.login'))

def safe_float(value, default=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default

def percent(value, goal):
    goal = safe_float(goal)
    if goal <= 0:
        return 0
    return round((safe_float(value) / goal) * 100, 1)

def display_percent(value, goal):
    return min(percent(value, goal), 100)

def build_recommendations(totals, goals):
    recommendations = []

    if totals["calories"] == 0:
        recommendations.append("Log your first meal today to unlock personalized nutrition feedback.")
        return recommendations

    if percent(totals["protein"], goals["protein"]) < 50:
        recommendations.append("Protein is running low today. Add dal, curd, paneer, eggs, sprouts, or lean meat.")
    if percent(totals["fibre"], goals["fibers"]) < 50:
        recommendations.append("Fiber is behind target. Add vegetables, fruit, oats, millets, or legumes.")
    if percent(totals["sodium"], goals["sodium"]) > 90:
        recommendations.append("Sodium is close to the daily limit. Keep dinner lighter on salt and packaged foods.")
    if goals["carbs"] and percent(totals["carbs"], goals["carbs"]) > 90 and percent(totals["protein"], goals["protein"]) < 75:
        recommendations.append("Carbs are high compared with protein. Balance the next meal with a protein-rich option.")

    if not recommendations:
        recommendations.append("Nice balance so far. Keep portions steady and include a protein and vegetable source in the next meal.")

    return recommendations

@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    user = current_user
    if not user.is_profile_complete():
        flash("Please complete your profile before viewing the dashboard.", "info")
        return redirect(url_for('auth.setup_profile'))

    user_name = user.first_name or 'User'

    # 1️⃣ Login streak (keep bubbles for future use)
    login_streak = user.daily_login_streak
    week_streak = [True, True, False, True, False, False, True]

    # 2️⃣ Fetch today's total nutrient intake from UserMealLog
    today = date.today()
    meal_log = UserMealLog.query.filter_by(user_id=user.id, date=today).first()

    # If no log exists yet for today, fallback to zeros
    if not meal_log:
        total_calories = total_protein = total_carbs = total_fats = total_fibre = 0.0
        total_iron = total_calcium = total_vitc = total_sodium = total_potassium = 0.0
    else:
        total_calories = round(meal_log.total_calories, 2)
        total_protein = round(meal_log.total_protein, 2)
        total_carbs = round(meal_log.total_carbs, 2)
        total_fats = round(meal_log.total_fat, 2)
        total_fibre = round(meal_log.total_fibre, 2)
        total_iron = round(meal_log.total_iron, 2)
        total_calcium = round(meal_log.total_calcium, 2)
        total_vitc = round(meal_log.total_vitc, 2)
        total_sodium = round(meal_log.total_sodium, 2)
        total_potassium = round(meal_log.total_potassium, 2)

    # 3️⃣ Maintenance calories (from profile setup)
    maintenance_calories = safe_float(user.maintenance_calories, 2000)
    protein_goal = safe_float(user.protein)
    carbs_goal = safe_float(user.carbs)
    fats_goal = safe_float(user.fats)
    fibers_goal = safe_float(user.fibers)
    iron_goal = safe_float(user.iron)
    calcium_goal = safe_float(user.calcium)
    potassium_goal = safe_float(user.potassium)
    sodium_goal = safe_float(user.sodium)
    vitamin_c_goal = safe_float(user.vitamin_c)

    # 4️⃣ Calculate percentage for circular calories graph
    calorie_percent = display_percent(total_calories, maintenance_calories)

    # 5️⃣ Prepare macro summary cards
    summary = [
        {"name": "Calories", "value": total_calories, "goal": maintenance_calories, "unit": "kcal", "percent": calorie_percent},
        {"name": "Protein", "value": total_protein, "goal": protein_goal,"unit": "g", "percent": display_percent(total_protein, protein_goal)},
        {"name": "Carbs", "value": total_carbs, "goal": carbs_goal,"unit": "g", "percent": display_percent(total_carbs, carbs_goal)},
        {"name": "Fats", "value": total_fats, "goal": fats_goal,"unit": "g", "percent": display_percent(total_fats, fats_goal)},
        {"name": "Fiber", "value": total_fibre, "goal": fibers_goal,"unit": "g", "percent": display_percent(total_fibre, fibers_goal)},
    ]

    # 6️⃣ Micronutrients section (no bars, just totals)
    micros = [
        {"name": "Iron (mg)", "value": total_iron, "percent": display_percent(total_iron, iron_goal)},
        {"name": "Calcium (mg)", "value": total_calcium, "percent": display_percent(total_calcium, calcium_goal)},
        {"name": "Vitamin C (mg)", "value": total_vitc, "percent": display_percent(total_vitc, vitamin_c_goal)},
        {"name": "Sodium (mg)", "value": total_sodium, "percent": display_percent(total_sodium, sodium_goal)},
        {"name": "Potassium (mg)", "value": total_potassium, "percent": display_percent(total_potassium, potassium_goal)}
    ]

    totals = {
        "calories": total_calories,
        "protein": total_protein,
        "carbs": total_carbs,
        "fats": total_fats,
        "fibre": total_fibre,
        "sodium": total_sodium,
    }
    goals = {
        "protein": protein_goal,
        "carbs": carbs_goal,
        "fibers": fibers_goal,
        "sodium": sodium_goal,
    }
    recommendations = build_recommendations(totals, goals)

    # 7️⃣ Generate pie chart for macros
    macros = {"Protein": total_protein, "Carbs": total_carbs, "Fats": total_fats}
    fig, ax = plt.subplots(figsize=(4, 4))
    if sum(macros.values()) > 0:
        ax.pie(macros.values(), labels=macros.keys(), autopct='%1.1f%%', startangle=90)
    else:
        ax.text(0.5, 0.5, 'No data', ha='center', va='center', fontsize=12)
    ax.set_title("Macronutrient Breakdown")

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', transparent=True)
    buffer.seek(0)
    chart_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close(fig)

    # 8️⃣ Render template
    return render_template(
        'dashboard.html',
        user_name=user_name,
        login_streak=login_streak,
        week_streak=week_streak,
        summary=summary,
        micros=micros,
        chart_data=chart_base64,
        recommendations=recommendations,
        bmi=user.bmi,
        maintenance_calories=maintenance_calories,
        has_meals=bool(meal_log)
    )
