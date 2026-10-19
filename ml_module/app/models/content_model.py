from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from app.data.db_client import fetch_books

class ContentModel:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.book_features = None
        self.books = None

    def train(self):
        self.books = fetch_books()
        # Kombinera metadata till en text-sträng per bok
        self.books["content"] = (
            self.books["genre"] + " " + self.books["author"] + " " + self.books["description"]
        )
        self.book_features = self.vectorizer.fit_transform(self.books["content"])

    def get_similar_books(self, book_id: str, top_n: int = 5) -> list[str]:
        """Returnerar top-N liknande böcker baserat på innehåll"""
        try:
            idx = self.books[self.books["book_id"] == book_id].index[0]
            book_vector = self.book_features[idx]
            similarities = cosine_similarity(book_vector, self.book_features).flatten()
            similar_indices = similarities.argsort()[-top_n - 1 : -1][::-1]
            return self.books.iloc[similar_indices]["book_id"].tolist()
        except IndexError:
            return []
