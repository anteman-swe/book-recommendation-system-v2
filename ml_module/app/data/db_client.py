from sqlalchemy import create_engine, text
import pandas as pd
from app.config import settings

engine = create_engine(
    f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
)

def fetch_ratings() -> pd.DataFrame:
    """Hämtar alla betyg (user_id, book_id, rating)"""
    query = text("SELECT user_id, book_id, rating FROM ratings")
    return pd.read_sql(query, engine)

def fetch_books() -> pd.DataFrame:
    """Hämtar bokmetadata (book_id, title, author, genre, description)"""
    query = text("SELECT book_id, title, author, genre, description FROM books")
    return pd.read_sql(query, engine)

def fetch_user_read_books(user_id: str) -> list[str]:
    """Hämtar bok_id:n för böcker användaren läst"""
    query = text("SELECT book_id FROM read_books WHERE user_id = :user_id")
    return pd.read_sql(query, engine, params={"user_id": user_id})["book_id"].tolist()
