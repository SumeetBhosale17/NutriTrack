import pytest
from app import create_app, db
from app.models import User  # Example model

@pytest.fixture
def app():
    # Create a test Flask app
    app = create_app("config.TestingConfig")  # Make sure you have a testing config
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_homepage(client):
    """Test the homepage route"""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Hello, NutriTrack" in response.data # Adjust based on your homepage content


def test_user_creation(app):
    """Test creating a user in the database"""
    user = User(name="testuser", email="test@example.com")
    db.session.add(user)
    db.session.commit()
    
    retrieved = User.query.filter_by(name="testuser").first()
    assert retrieved is not None
    assert retrieved.email == "test@example.com"
