from . import db
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from datetime import datetime
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
    email_verified = db.Column(db.Boolean, default=False)
    verification_token = db.Column(db.String(255), nullable=True)
    reset_token = db.Column(db.String(255), nullable=True)
    two_fa_enabled = db.Column(db.Boolean, default=False)
    last_login = db.Column(db.DateTime, nullable=True)
    daily_login_streak = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(IST), nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(IST), nullable=False)

    # ---------------------
    # Password Handling
    # ---------------------
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    # ---------------------
    # Representation
    # ---------------------
    def __repr__(self):
        return f"<User {self.email}>"