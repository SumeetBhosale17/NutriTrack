from app import create_app, db
from app.models import IndianMeal


DEMO_FOODS = [
    {
        "food_code": "DEMO001",
        "food_name": "Dal Tadka",
        "energy_kcal": 120,
        "protein_g": 6.0,
        "carb_g": 16.0,
        "fat_g": 3.5,
        "fibre_g": 4.0,
        "iron_mg": 1.8,
        "calcium_mg": 35,
        "vitc_mg": 2,
        "sodium_mg": 250,
        "potassium_mg": 260,
    },
    {
        "food_code": "DEMO002",
        "food_name": "Cooked Rice",
        "energy_kcal": 130,
        "protein_g": 2.7,
        "carb_g": 28.0,
        "fat_g": 0.3,
        "fibre_g": 0.4,
        "iron_mg": 0.2,
        "calcium_mg": 10,
        "vitc_mg": 0,
        "sodium_mg": 1,
        "potassium_mg": 35,
    },
    {
        "food_code": "DEMO003",
        "food_name": "Paneer Bhurji",
        "energy_kcal": 210,
        "protein_g": 12.0,
        "carb_g": 6.0,
        "fat_g": 15.0,
        "fibre_g": 1.5,
        "iron_mg": 0.8,
        "calcium_mg": 320,
        "vitc_mg": 8,
        "sodium_mg": 300,
        "potassium_mg": 180,
    },
]


def seed_demo_foods():
    for data in DEMO_FOODS:
        food = IndianMeal.query.filter_by(food_code=data["food_code"]).first()
        if food:
            for key, value in data.items():
                setattr(food, key, value)
        else:
            db.session.add(IndianMeal(**data))

    db.session.commit()
    print(f"Seeded {len(DEMO_FOODS)} demo food items.")


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        seed_demo_foods()
