import pytest

from app import create_app, db
from app.models import IndianMeal, MealEntry, User, UserMealLog


@pytest.fixture
def app():
    app = create_app("config.TestingConfig")
    app.config.update(WTF_CSRF_ENABLED=False)

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def create_user(email="test@example.com"):
    user = User(email=email, first_name="Test", last_name="User")
    user.set_password("password123")
    db.session.add(user)
    db.session.commit()
    return user


def complete_profile(user):
    user.gender = "Male"
    user.age = 25
    user.height_cm = 175
    user.weight_kg = 70
    user.goal = "Maintain Weight"
    user.activity_level = "Moderately Active (3–5 days/week)"
    user.calculate_bmi()
    user.calculate_maintenance_calories()
    user.calculate_nutrition()
    db.session.commit()


def seed_food():
    food = IndianMeal(
        food_code="T001",
        food_name="Dal Tadka",
        energy_kcal=120,
        protein_g=6,
        carb_g=16,
        fat_g=3.5,
        fibre_g=4,
        iron_mg=1.8,
        calcium_mg=35,
        vitc_mg=2,
        sodium_mg=250,
        potassium_mg=260,
    )
    db.session.add(food)
    db.session.commit()
    return food


def login(client, email="test@example.com"):
    return client.post(
        "/auth/login",
        data={"email": email, "password": "password123"},
        follow_redirects=True,
    )


def test_app_creation_and_home_redirect(client):
    response = client.get("/")
    assert response.status_code == 302
    assert "/auth/login" in response.location


def test_register_login_logout_flow(client, app):
    response = client.post(
        "/auth/register",
        data={
            "first_name": "Test",
            "last_name": "User",
            "email": "test@example.com",
            "password": "password123",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert User.query.filter_by(email="test@example.com").first() is not None

    response = login(client)
    assert response.status_code == 200
    assert b"Complete Your Profile" in response.data

    response = client.get("/auth/logout", follow_redirects=True)
    assert response.status_code == 200
    assert b"LOGIN" in response.data


def test_profile_setup_computes_targets(client, app):
    create_user()
    login(client)

    response = client.post(
        "/auth/setup-profile",
        data={
            "gender": "Male",
            "age": "25",
            "height_cm": "175",
            "weight_kg": "70",
            "goal": "Maintain Weight",
            "activity_level": "Moderately Active (3–5 days/week)",
        },
        follow_redirects=True,
    )

    user = User.query.filter_by(email="test@example.com").first()
    assert response.status_code == 200
    assert user.is_profile_complete()
    assert user.bmi is not None
    assert user.maintenance_calories is not None
    assert user.protein is not None


def test_dashboard_requires_login(client):
    response = client.get("/dashboard")
    assert response.status_code == 302
    assert "/auth/login" in response.location


def test_dashboard_loads_with_no_meals(client, app):
    user = create_user()
    complete_profile(user)
    response = login(client)

    assert response.status_code == 200
    assert b"Today's Suggestions" in response.data
    assert b"No meals logged today yet" in response.data


def test_food_logging_creates_daily_log_and_entry(client, app):
    user = create_user()
    complete_profile(user)
    food = seed_food()
    login(client)

    response = client.post(
        "/log-food",
        data={
            "meal_type": "lunch",
            "food_ids": [str(food.id)],
            "quantities": ["150"],
        },
        follow_redirects=True,
    )

    meal_log = UserMealLog.query.filter_by(user_id=user.id).first()
    entry = MealEntry.query.first()
    assert response.status_code == 200
    assert meal_log is not None
    assert entry is not None
    assert entry.quantity == 150
    assert meal_log.total_calories == pytest.approx(180)


def test_invalid_food_quantity_does_not_create_entry(client, app):
    user = create_user()
    complete_profile(user)
    food = seed_food()
    login(client)

    response = client.post(
        "/log-food",
        data={
            "meal_type": "lunch",
            "food_ids": [str(food.id)],
            "quantities": ["0"],
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Food quantity must be greater than zero" in response.data
    assert MealEntry.query.count() == 0
