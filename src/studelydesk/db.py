import psycopg2
import sqlite3
import os

def get_db_connection():
    database_url = os.getenv('ARCHILOG_DATABASE_URL')

    if database_url.startswith("sqlite://"):
        path = database_url.replace("sqlite:///", "")
        conn = sqlite3.connect(path)
        return conn
    else:
        # Connexion PostgreSQL en passant l’URL complète (y compris les paramètres)
        conn = psycopg2.connect(database_url)
        return conn
