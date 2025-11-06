from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import date
from app.models import db, UserMealLog, MealEntry, IndianMeal
from collections import defaultdict

meal_bp = Blueprint('meal', __name__)

@meal_bp.route('/log-food', methods=['GET', 'POST'])
@login_required
def log_meal():
    foods = IndianMeal.query.all()
    today = date.today()

    meal_log = UserMealLog.query.filter_by(user_id=current_user.id, date=today).first()

    if request.method == 'POST':
        meal_type = request.form.get('meal_type')
        food_ids = request.form.getlist('food_ids')
        quantities = request.form.getlist('quantities')

        if not meal_log:
            meal_log = UserMealLog(user_id=current_user.id, date=today)
            db.session.add(meal_log)
            db.session.flush()

        # Totals to update daily summary
        new_totals = {k: 0 for k in ["calories","protein","carbs","fat","fibre","iron","calcium","vitc","sodium","potassium"]}

        for food_id, qty in zip(food_ids, quantities):
            food = IndianMeal.query.get(int(food_id))
            qty = float(qty)
            factor = qty / 100

            entry = MealEntry(
                meal_log_id=meal_log.id,
                food_id=food.id,
                meal_type=meal_type,
                quantity=qty,
                calories=food.energy_kcal * factor,
                protein=food.protein_g * factor,
                carbs=food.carb_g * factor,
                fat=food.fat_g * factor,
                fibre=food.fibre_g * factor,
                iron=food.iron_mg * factor,
                calcium=food.calcium_mg * factor,
                vitc=food.vitc_mg * factor,
                sodium=food.sodium_mg * factor,
                potassium=food.potassium_mg * factor
            )
            db.session.add(entry)
            for k in new_totals:
                new_totals[k] += getattr(entry, k)

        for k, v in new_totals.items():
            current_val = getattr(meal_log, f"total_{k}", 0)
            setattr(meal_log, f"total_{k}", current_val + v)

        db.session.commit()
        flash(f"{meal_type.capitalize()} logged successfully!", "success")
        return redirect(url_for('meal.log_meal'))

    meal_entries = []
    if meal_log:
        meal_entries = MealEntry.query.filter_by(meal_log_id=meal_log.id).join(IndianMeal).all()

    grouped_meals = defaultdict(list)
    for entry in meal_entries:
        grouped_meals[entry.meal_type].append(entry)

    return render_template('log_food.html', foods=foods, grouped_meals=grouped_meals, meal_log=meal_log)
