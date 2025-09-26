from . import db
import datetime

class User(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    email = db.Column(db.String(128), unique=True, nullable=False)
    weight = db.Column(db.Float)
    height = db.Column(db.Float)
    # relations

class FoodItem(db.Model):
    __tablename__ = "food_items"
    food_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    calories = db.Column(db.Float)
    protein = db.Column(db.Float)
    carbs = db.Column(db.Float)
    fat = db.Column(db.Float)
