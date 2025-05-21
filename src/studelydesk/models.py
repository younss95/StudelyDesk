import sqlite3
from collections import Counter
from dataclasses import dataclass
from datetime import datetime
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime, insert, select, update, delete
from sqlalchemy.ext.declarative import declarative_base

from studelydesk.db import get_db_connection  # Importation de la fonction get_db_connection

DATABASE = "data.db"

# Crée une instance de base
Base = declarative_base()

# Connexion à la base de données
engine = create_engine('sqlite:///data.db', echo=True)
metadata = MetaData()

# Définition de la table 'entries'
entries_table = Table(
    "entries",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("title", String, nullable=False),
    Column("description", String, nullable=False),
    Column("name", String, nullable=False),
    Column("date", DateTime, nullable=False),
    Column("status", String, nullable=False),
    Column("priority", String, nullable=False),
    Column("departement", String, nullable=True),
    Column("categorie", String, nullable=True),
    Column("assigne_a", String, nullable=True),
    Column("email", String, nullable=True),
    Column("pays", String, nullable=True),
    Column("user_id", Integer, nullable=True)  # Ajout ici
)


def init_db():
    metadata.create_all(engine)

@dataclass
class Entry:
    id: int
    title: str
    description: str
    name: str
    date: datetime
    status: str
    priority: str
    departement: str
    categorie: str
    assigne_a: str
    email: str
    pays: str
    user_id: int  # ✅ Ajout de cette ligne

    @classmethod
    def from_db(cls, _id, title, description, name, date, status, priority,
                departement, categorie, assigne_a, email, pays, user_id):  # ✅ Ajout de user_id ici aussi
        return cls(_id, title, description, name, date, status, priority,
                   departement, categorie, assigne_a, email, pays, user_id)


# Fonction pour créer une entrée
def create_entry(title, description, name, date, status, priority,
                 departement, categorie, assigne_a, email, pays, user_id=None):
    stmt = insert(entries_table).values(
        title=title,
        description=description,
        name=name,
        date=date,
        status=status,
        priority=priority,
        departement=departement,
        categorie=categorie,
        assigne_a=assigne_a,
        email=email,
        pays=pays,
        user_id=user_id  # ✅ Ajout ici
    )
    with engine.connect() as conn:
        conn.execute(stmt)
        conn.commit()


# Fonction pour obtenir une entrée par ID
def get_entry(_id: int):
    stmt = select(entries_table).where(entries_table.c.id == _id)
    with engine.connect() as conn:
        result = conn.execute(stmt).mappings().fetchone()  # .mappings() pour un dict-like
        if result:
            return dict(result)  # renvoie toutes les colonnes : id, title, description, user_id, etc.
        else:
            return None

# Fonction pour obtenir toutes les entrées
def get_all_entries():
    stmt = select(entries_table)
    with engine.connect() as conn:
        results = conn.execute(stmt).fetchall()
        return [Entry.from_db(*row) for row in results]

# Fonction pour mettre à jour une entrée
def update_entry(_id, title, description, name, status, priority,
                 departement, categorie, assigne_a, email, pays):
    stmt = update(entries_table).where(entries_table.c.id == _id).values(
        title=title,
        description=description,
        name=name,
        status=status,
        priority=priority,
        departement=departement,
        categorie=categorie,
        assigne_a=assigne_a,
        email=email,
        pays=pays
    )
    with engine.connect() as conn:
        conn.execute(stmt)
        conn.commit()

# Fonction pour supprimer une entrée
def delete_entry(_id: int):
    stmt = delete(entries_table).where(entries_table.c.id == _id)
    with engine.connect() as conn:
        conn.execute(stmt)
        conn.commit()

def get_stats_par_statut():
    entries = get_all_entries()
    statuts = [entry.status for entry in entries]
    return Counter(statuts)

def get_stats_par_priority():
    entries = get_all_entries()
    priority = [entry.priority for entry in entries]
    return Counter(priority)

# Fonction pour obtenir les entrées par user_id
def get_entries_by_user(user_id):
    conn = get_db_connection()  # Assurez-vous que `get_db_connection` est bien définie dans `studelydesk.db`
    rows = conn.execute("SELECT * FROM entries WHERE user_id = ?", (user_id,)).fetchall()
    conn.close()
    return rows


def get_tickets_by_user_id(user_id):
    stmt = select(entries_table).where(entries_table.c.user_id == user_id)
    with engine.connect() as conn:
        results = conn.execute(stmt).fetchall()
        return [dict(row._mapping) for row in results]


def ajouter_reponse(ticket_id, contenu):
    conn = get_db_connection()
    try:
        conn.execute(
            "INSERT INTO reponses (ticket_id, contenu, date) VALUES (?, ?, ?)",
            (ticket_id, contenu, datetime.now())
        )
        conn.commit()
    finally:
        conn.close()





