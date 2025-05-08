from sqlalchemy import create_engine
from studelydesk.models import init_db

engine = create_engine("sqlite:///studelydesk-0.1/data.db")
init_db()
print("Base de données initialisée.")