from flask import Blueprint, request, render_template, redirect, url_for, flash, session
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
        email = request.form.get('email')
        password = request.form.get('password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')

        if User.query.filter_by(email=email).first():
            flash("Email already exists", "error")
            return redirect(url_for('auth.register'))

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
        email = request.form.get("email")
        password = request.form.get("password")

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
        if abs((user.updated_at - user.created_at).total_seconds()) < 1:
            return redirect(url_for('auth.setup_profile'))
        return redirect(url_for('dashboard.dashboard'))  # redirect to dashboard or home page
    
    return render_template('sign.html')

@auth_bp.route('/setup-profile', methods=['GET', 'POST'])
@login_required
def setup_profile():
    user_id = current_user.id
    if not user_id:
        return redirect(url_for('auth.login'))
    
    user = User.query.get(user_id)

    if request.method == 'POST':
        user.gender = request.form['gender']
        user.age = int(request.form['age'])
        user.height_cm = float(request.form['height_cm'])
        user.weight_kg = float(request.form['weight_kg'])
        user.goal = request.form['goal']
        user.activity_level = request.form['activity_level']
        user.updated_at = datetime.now()

        user.calculate_bmi()
        user.calculate_maintenance_calories()
        user.calculate_nutrition()

        db.session.commit()
        flash("Profile setup complete!", "Success")
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
def send_verification():
    user_id = session.get('user_id')
    if not user_id:
        flash("Please login first", 'error')
        return redirect(url_for('auth.login'))
    
    user = User.query.get(user_id)
    if user.email_verified:
        flash("Email already verified!", "info")
        return redirect(url_for('auth.dashboard'))
    
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
def profile_complete():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))
    
    user = User.query.get(user_id)
    return 'profile complete'

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for('auth.login'))