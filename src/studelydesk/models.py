from dataclasses import dataclass
from datetime import datetime
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime, insert, select, update, delete
from sqlalchemy.ext.declarative import declarative_base

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
    Column("priority", String, nullable=False)
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

    @classmethod
    def from_db(cls, _id: int, title: str, description: str, name: str, date: datetime, status: str, priority: str):
        return cls(
            id=_id,
            title=title,
            description=description,
            name=name,
            date=date,
            status=status,
            priority=priority,
        )

# Fonction pour créer une entrée
def create_entry(title: str, description: str, name: str, date: datetime, status: str, priority: str):
    stmt = insert(entries_table).values(
        title=title,
        description=description,
        name=name,
        date=date,
        status=status,
        priority=priority
    )
    with engine.connect() as conn:
        conn.execute(stmt)
        conn.commit()

# Fonction pour obtenir une entrée par ID
def get_entry(_id: int):
    stmt = select(entries_table).where(entries_table.c.id == _id)
    with engine.connect() as conn:
        result = conn.execute(stmt).fetchone()
        if result:
            return Entry.from_db(*result)
        else:
            return None

# Fonction pour obtenir toutes les entrées
def get_all_entries():
    stmt = select(entries_table)
    with engine.connect() as conn:
        results = conn.execute(stmt).fetchall()
        return [Entry.from_db(*row) for row in results]

# Fonction pour mettre à jour une entrée
def update_entry(_id: int, title: str, description: str, name: str, status: str, priority: str):
    stmt = update(entries_table).where(entries_table.c.id == _id).values(
        title=title,
        description=description,
        name=name,
        status=status,
        priority=priority
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
