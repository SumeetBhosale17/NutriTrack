from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from config import Config
from app.models import User
from app import db
import jwt
from datetime import datetime, timedelta, date

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = (request.form.get('email') or '').strip().lower()
        password = request.form.get('password') or ''
        first_name = (request.form.get('first_name') or '').strip()
        last_name = (request.form.get('last_name') or '').strip()

        if not email or not password or not first_name:
            flash("First name, email, and password are required.", "error")
            return render_template('sign.html', active_form="register")

        if User.query.filter_by(email=email).first():
            flash("Email already exists", "error")
            return render_template('sign.html', active_form="register")

        user = User(email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash("User Registered Successfully", "success")
        return redirect(url_for('auth.login'))
    
    return render_template('sign.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""

        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            flash("Invalid Credentials", "error")
            return redirect(url_for('auth.login'))

        login_user(user)
        
        today = date.today()

        if user.last_login:
            last_login_date = user.last_login.date()
            if last_login_date == today - timedelta(days=1):
                user.daily_login_streak += 1
            elif last_login_date == today:
                pass
            else:
                user.daily_login_streak = 1
        else:
            user.daily_login_streak = 1

        user.last_login = datetime.now()
        db.session.commit()

        flash("Login Successful", "success")
        if not user.is_profile_complete():
            return redirect(url_for('auth.setup_profile'))
        return redirect(url_for('dashboard.dashboard'))  # redirect to dashboard or home page
    
    return render_template('sign.html')

@auth_bp.route('/setup-profile', methods=['GET', 'POST'])
@login_required
def setup_profile():
    user = current_user

    if request.method == 'POST':
        try:
            gender = request.form.get('gender', '').strip()
            age = int(request.form.get('age', ''))
            height_cm = float(request.form.get('height_cm', ''))
            weight_kg = float(request.form.get('weight_kg', ''))
            goal = request.form.get('goal', '').strip()
            activity_level = request.form.get('activity_level', '').strip()
        except ValueError:
            flash("Please enter valid numeric values for age, height, and weight.", "error")
            return render_template('profile-setup.html', user=user)

        if not gender or not goal or not activity_level:
            flash("Please complete all profile fields.", "error")
            return render_template('profile-setup.html', user=user)
        if age <= 0 or height_cm <= 0 or weight_kg <= 0:
            flash("Age, height, and weight must be greater than zero.", "error")
            return render_template('profile-setup.html', user=user)

        user.gender = gender
        user.age = age
        user.height_cm = height_cm
        user.weight_kg = weight_kg
        user.goal = goal
        user.activity_level = activity_level
        user.updated_at = datetime.now()

        user.calculate_bmi()
        user.calculate_maintenance_calories()
        user.calculate_nutrition()

        db.session.commit()
        flash("Profile setup complete!", "success")
        return redirect(url_for('dashboard.dashboard'))
    
    return render_template('profile-setup.html', user=user)

def generate_verification_token(email):
    payload = {
        'email': email,
        'exp': datetime.now() + timedelta(minutes=30)
    }
    token = jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')
    return token

@auth_bp.route('/send-verification', methods=['POST'])
@login_required
def send_verification():
    user = current_user
    if user.email_verified:
        flash("Email already verified!", "info")
        return redirect(url_for('auth.setup_profile'))
    
    token = generate_verification_token(user.email)
    verification_link = url_for('auth.verify_email', token=token, _external=True)
    user.verification_token = token
    db.session.commit()

    # TODO: Replace this with actual email sending logic
    print(f"Verification Link: {verification_link}") # temporary for dev

    flash("Verification email sent! Check your inbox", "success")
    return redirect(url_for('auth.setup_profile'))

@auth_bp.route('/verify-email/<token>')
def verify_email(token):
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        email = payload.get('email')

        user = User.query.filter_by(email=email).first()
        if not user:
            flash("Invalid Verification Link", "error")
            return redirect(url_for('auth.login'))
        
        user.email_verified = True
        db.session.commit()

        flash("Email Verified Successfully!", "success")
        return redirect(url_for('auth.setup_profile'))
    
    except jwt.ExpiredSignatureError:
        flash("Verification Link expired. Please request new one", "error")
        return redirect(url_for('auth.setup_profile'))
    except jwt.InvalidTokenError:
        flash("Invalid Token", "error")
        return redirect(url_for('auth.setup_profile'))
    
@auth_bp.route('/profile-complete')
@login_required
def profile_complete():
    if current_user.is_profile_complete():
        return redirect(url_for('dashboard.dashboard'))
    return redirect(url_for('auth.setup_profile'))

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for('auth.login'))
