from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import date
from app.models import db, UserMealLog, MealEntry, IndianMeal
from collections import defaultdict

meal_bp = Blueprint('meal', __name__)

VALID_MEAL_TYPES = {'breakfast', 'lunch', 'dinner', 'misc'}
NUTRIENT_KEYS = ["calories", "protein", "carbs", "fat", "fibre", "iron", "calcium", "vitc", "sodium", "potassium"]

def nutrient_value(food, attr):
    return float(getattr(food, attr) or 0)

@meal_bp.route('/log-food', methods=['GET', 'POST'])
@login_required
def log_meal():
    if not current_user.is_profile_complete():
        flash("Please complete your profile before logging food.", "info")
        return redirect(url_for('auth.setup_profile'))

    foods = IndianMeal.query.all()
    today = date.today()

    meal_log = UserMealLog.query.filter_by(user_id=current_user.id, date=today).first()

    if request.method == 'POST':
        meal_type = request.form.get('meal_type')
        food_ids = request.form.getlist('food_ids')
        quantities = request.form.getlist('quantities')

        if meal_type not in VALID_MEAL_TYPES:
            flash("Please choose a valid meal type.", "error")
            return redirect(url_for('meal.log_meal'))
        if not foods:
            flash("No food database rows are available yet. Import or seed foods first.", "error")
            return redirect(url_for('meal.log_meal'))
        if not food_ids:
            flash("Please select at least one food item.", "error")
            return redirect(url_for('meal.log_meal'))
        if len(food_ids) != len(quantities):
            flash("Please enter a quantity for every selected food.", "error")
            return redirect(url_for('meal.log_meal'))

        parsed_items = []
        for food_id, qty in zip(food_ids, quantities):
            try:
                food_id_int = int(food_id)
                qty_float = float(qty)
            except (TypeError, ValueError):
                flash("Food selections and quantities must be valid numbers.", "error")
                return redirect(url_for('meal.log_meal'))

            if qty_float <= 0:
                flash("Food quantity must be greater than zero.", "error")
                return redirect(url_for('meal.log_meal'))

            food = db.session.get(IndianMeal, food_id_int)
            if not food:
                flash("One selected food item could not be found.", "error")
                return redirect(url_for('meal.log_meal'))

            parsed_items.append((food, qty_float))

        if not meal_log:
            meal_log = UserMealLog(user_id=current_user.id, date=today)
            db.session.add(meal_log)
            db.session.flush()

        # Totals to update daily summary
        new_totals = {k: 0 for k in NUTRIENT_KEYS}

        for food, qty in parsed_items:
            factor = qty / 100

            entry = MealEntry(
                meal_log_id=meal_log.id,
                food_id=food.id,
                meal_type=meal_type,
                quantity=qty,
                calories=nutrient_value(food, 'energy_kcal') * factor,
                protein=nutrient_value(food, 'protein_g') * factor,
                carbs=nutrient_value(food, 'carb_g') * factor,
                fat=nutrient_value(food, 'fat_g') * factor,
                fibre=nutrient_value(food, 'fibre_g') * factor,
                iron=nutrient_value(food, 'iron_mg') * factor,
                calcium=nutrient_value(food, 'calcium_mg') * factor,
                vitc=nutrient_value(food, 'vitc_mg') * factor,
                sodium=nutrient_value(food, 'sodium_mg') * factor,
                potassium=nutrient_value(food, 'potassium_mg') * factor
            )
            db.session.add(entry)
            for k in new_totals:
                new_totals[k] += getattr(entry, k)

        for k, v in new_totals.items():
            current_val = getattr(meal_log, f"total_{k}", 0) or 0
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
