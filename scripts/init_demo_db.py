import time
import sys
from pathlib import Path

from sqlalchemy.exc import OperationalError


BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from app import create_app, db
from scripts.seed import seed_demo_foods


MAX_ATTEMPTS = 30
SLEEP_SECONDS = 1


app = create_app()

with app.app_context():
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            db.create_all()
            seed_demo_foods()
            print("Demo database is ready.")
            break
        except OperationalError as exc:
            if attempt == MAX_ATTEMPTS:
                raise
            print(f"Database is not ready yet ({attempt}/{MAX_ATTEMPTS}): {exc}")
            time.sleep(SLEEP_SECONDS)
