from flask import Blueprint, render_template
from flask_login import login_required, current_user
import matplotlib.pyplot as plt
import io
import base64
from datetime import date
from app.models import UserMealLog

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    user = current_user
    user_name = user.first_name or 'User'

    # 1️⃣ Login streak (keep bubbles for future use)
    login_streak = user.daily_login_streak
    week_streak = [True, True, False, True, False, False, True]

    # 2️⃣ Fetch today's total nutrient intake from UserMealLog
    today = date.today()
    meal_log = UserMealLog.query.filter_by(user_id=user.id, date=today).first()

    # If no log exists yet for today, fallback to zeros
    if not meal_log:
        total_calories = total_protein = total_carbs = total_fats = total_fibre = 0
        total_iron = total_calcium = total_vitc = total_sodium = total_potassium = 0
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
    maintenance_calories = user.maintenance_calories or 2000
    protein_goal = float(user.protein)
    carbs_goal = float(user.carbs)
    fats_goal = float(user.fats)
    fibers_goal = float(user.fibers)
    iron_goal = float(user.iron)
    calcium_goal = float(user.calcium)
    potassium_goal = float(user.potassium)
    sodium_goal = float(user.sodium)
    vitamin_c_goal = float(user.vitamin_c)

    # 4️⃣ Calculate percentage for circular calories graph
    calorie_percent = round((total_calories / maintenance_calories) * 100, 1) if maintenance_calories else 0
    if calorie_percent > 100:
        calorie_percent = 100

    # 5️⃣ Prepare macro summary cards
    summary = [
        {"name": "Calories", "value": total_calories, "goal": maintenance_calories, "unit": "kcal", "percent": calorie_percent},
        {"name": "Protein", "value": total_protein, "goal": protein_goal,"unit": "g", "percent": round((total_protein / protein_goal) * 100, 1) if protein_goal else 0},
        {"name": "Carbs", "value": total_carbs, "goal": carbs_goal,"unit": "g", "percent": round((total_carbs / carbs_goal) * 100, 1) if carbs_goal else 0},
        {"name": "Fats", "value": total_fats, "goal": fats_goal,"unit": "g", "percent": round((total_fats / fats_goal) * 100, 1) if fats_goal else 0},
        {"name": "Fiber", "value": total_fibre, "goal": fibers_goal,"unit": "g", "percent": round((total_fibre / fibers_goal) * 100, 1) if fibers_goal else 0},
    ]

    # 6️⃣ Micronutrients section (no bars, just totals)
    micros = [
        {"name": "Iron (mg)", "value": total_iron, "percent": round((total_iron / iron_goal) * 100, 1) if iron_goal else 0},
        {"name": "Calcium (mg)", "value": total_calcium, "percent": round((total_calcium / calcium_goal) * 100, 1) if calcium_goal else 0},
        {"name": "Vitamin C (mg)", "value": total_vitc, "percent": round((total_vitc / vitamin_c_goal) * 100, 1) if vitamin_c_goal else 0},
        {"name": "Sodium (mg)", "value": total_sodium, "percent": round((total_sodium / sodium_goal) * 100, 1) if sodium_goal else 0},
        {"name": "Potassium (mg)", "value": total_potassium, "percent": round((total_potassium / potassium_goal) * 100, 1) if potassium_goal else 0}
    ]

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
        chart_data=chart_base64
    )