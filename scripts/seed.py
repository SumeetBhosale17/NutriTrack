from app import create_app, db
from app.models import FoodItem, User

app = create_app()
with app.app_context():
    db.session.add_all([
        FoodItem(name="Apple", calories=52, protein=0.3, carbs=14, fat=0.2),
        FoodItem(name="Boiled Egg", calories=155, protein=13, carbs=1.1, fat=11)
    ])
    db.session.commit()
    print("Seeded food items")
