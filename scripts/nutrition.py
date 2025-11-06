
from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    users = User.query.all()

    for user in users:
        user.calculate_nutrition()  # Assuming this updates nutrition fields
        print(f"Updated nutrition for user: {user.first_name}")

    db.session.commit()

    print("✅ All users' nutrition updated successfully.")

    