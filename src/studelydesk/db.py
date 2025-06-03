import os
from urllib.parse import urlparse
import psycopg2
import sqlite3

def get_db_connection():
    database_url = os.getenv('ARCHILOG_DATABASE_URL')
    if database_url.startswith("sqlite://"):
        # Extraire chemin fichier SQLite
        path = database_url.replace("sqlite:///", "")
        conn = sqlite3.connect(path)
        return conn
    else:
        # PostgreSQL
        result = urlparse(database_url)
        username = result.username
        password = result.password
        database = result.path[1:]
        hostname = result.hostname
        port = result.port

        conn = psycopg2.connect(
            dbname=database,
            user=username,
            password=password,
            host=hostname,
            port=port,
            sslmode='require'
        )
        return conn
