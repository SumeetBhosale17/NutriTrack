from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import pytz

ist = pytz.timezone('Asia/Kolkata')
datetime.now(ist)

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_object="config.Config"):
    app = Flask(__name__)

    app.config.from_object(config_object)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    with app.app_context():
        db.create_all()
        
    return app
