from . import db
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from datetime import datetime
from datetime import date
from sqlalchemy.sql import func
from pytz import timezone

IST = timezone('Asia/Kolkata')

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uuid = db.Column(db.String(36), unique=True, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255))
    google_id = db.Column(db.String(255), nullable=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100))
    gender = db.Column(db.String(20))
    age = db.Column(db.Integer)
    height_cm = db.Column(db.Numeric(5, 2))
    weight_kg = db.Column(db.Numeric(5, 2))
    goal = db.Column(db.String(100))
    activity_level = db.Column(db.String(50))
    bmi = db.Column(db.Numeric(5, 2))
    maintenance_calories = db.Column(db.Integer)
    email_verified = db.Column(db.Boolean, default=False)
    verification_token = db.Column(db.String(255), nullable=True)
    reset_token = db.Column(db.String(255), nullable=True)
    two_fa_enabled = db.Column(db.Boolean, default=False)
    last_login = db.Column(db.DateTime, nullable=True)
    daily_login_streak = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(IST), nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(IST), nullable=False)

    meals = db.relationship('UserMealLog', back_populates='user', cascade='all, delete')

    # ---------------------
    # Password Handling
    # ---------------------
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    # ---------------------
    # BMI Calculation
    # ---------------------
    def calculate_bmi(self):
        if self.height_cm and self.weight_kg:
            height_m = float(self.height_cm) / 100
            self.bmi = round(float(self.weight_kg) / (height_m ** 2), 2)
        else:
            self.bmi = None


    # ---------------------
    # Maintenance Calories Calculations
    # ---------------------
    def calculate_maintenance_calories(self):
        if self.gender and self.age and self.height_cm and self.weight_kg and self.activity_level:
            if self.gender.lower() == 'male':
                bmr = 10 * float(self.weight_kg) + 6.25 * float(self.height_cm) - 5 * int(self.age) + 5
            else:
                bmr = 10 * float(self.weight_kg) + 6.25 * float(self.height_cm) - 5 * int(self.age) - 16
            
            activity_factors = {
                "Sedentary (Little or no exercise)": 1.2,
                "Lightly Active (1–3 days/week)": 1.375,
                "Moderately Active (3–5 days/week)": 1.55,
                "Very Active (6–7 days/week)": 1.725,
                "Super Active (Physical job or athlete)": 1.9
            }

            factor = activity_factors.get(self.activity_level, 1.375)
            self.maintenance_calories = int(bmr * factor)
        else:
            self.maintenance_calories = None
    
    # ---------------------
    # Representation
    # ---------------------
    def __repr__(self):
        return f"<User {self.email}>"
    

class IndianMeal(db.Model):
    __tablename__ = 'indian_foods'

    id = db.Column(db.Integer, primary_key=True)
    food_code = db.Column(db.String(10))
    food_name = db.Column(db.String(150))
    energy_kcal = db.Column(db.Float)
    protein_g = db.Column(db.Float)
    carb_g = db.Column(db.Float)
    fat_g = db.Column(db.Float)
    fibre_g = db.Column(db.Float)
    iron_mg = db.Column(db.Float)
    calcium_mg = db.Column(db.Float)
    vitc_mg = db.Column(db.Float)
    sodium_mg = db.Column(db.Float)
    potassium_mg = db.Column(db.Float)

class UserMealLog(db.Model):
    __tablename__ = 'user_meal_log'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.Date, default=date.today, nullable=False)

    user = db.relationship('User', back_populates='meals')
    meal_entries = db.relationship('MealEntry', back_populates='meal_log', cascade='all, delete')


class MealEntry(db.Model):
    __tablename__ = 'meal_entry'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    meal_log_id = db.Column(db.Integer, db.ForeignKey('user_meal_log.id'), nullable=False)
    food_id = db.Column(db.Integer, db.ForeignKey('indian_foods.id'), nullable=False)

    meal_type = db.Column(db.Enum('breakfast', 'lunch', 'dinner', 'misc', name='meal_type_enum'), nullable=False)
    quantity = db.Column(db.Float, nullable=False, default=1.0)
    tota_calories = db.Column(db.Float)

    meal_log = db.relationship('UserMealLog', back_populates='meal_entries')
    food = db.relationship('IndianMeal')