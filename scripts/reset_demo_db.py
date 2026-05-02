from datetime import datetime
from pathlib import Path
import sys


BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from app import create_app, db
from scripts.seed import seed_demo_foods


DB_PATH = BASE_DIR / "nutritrack.db"


def backup_existing_db():
    if not DB_PATH.exists():
        return None

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = DB_PATH.with_name(f"{DB_PATH.stem}.backup_{timestamp}{DB_PATH.suffix}")
    DB_PATH.rename(backup_path)
    return backup_path


backup_path = backup_existing_db()

app = create_app()
with app.app_context():
    db.drop_all()
    db.create_all()
    seed_demo_foods()

if backup_path:
    print(f"Backed up old database to {backup_path}")
print(f"Created fresh demo database at {DB_PATH}")
