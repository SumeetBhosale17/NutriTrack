from flask import Blueprint, render_template
import matplotlib.pyplot as plt
import io
import base64

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
def dashboard():
    user_name = "Sumeet"  # Later replace with current_user.name from Flask-Login
    week_streak = [True, False, True, True, False, True, False]

    summary = [
        {"name": "Calories", "value": 1800, "goal": 2200, "unit": "", "percent": 82},
        {"name": "Protein", "value": 90, "goal": 120, "unit": "g", "percent": 82},
        {"name": "Carbs", "value": 250, "goal": 300, "unit": "g", "percent": 82},
        {"name": "Fats", "value": 50, "goal": 66, "unit": "g", "percent": 82},
        {"name": "Fiber", "value": 16, "goal": 30, "unit": "g", "percent": 82},
    ]

    micros = {"Iron": 86, "Calcium": 72, "Vitamin C": 54}

    # Generate macronutrient chart dynamically in memory
    macros = {"Protein": 90, "Carbs": 250, "Fats": 50}
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.pie(macros.values(), labels=macros.keys(), autopct='%1.1f%%', startangle=90)
    ax.set_title("Macronutrient Breakdown")

    # Save chart to in-memory BytesIO object instead of file
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', transparent=True)
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close(fig)

    return render_template(
        'dashboard.html',
        user_name=user_name,
        week_streak=week_streak,
        summary=summary,
        micros=micros,
        chart_data=image_base64
    )
