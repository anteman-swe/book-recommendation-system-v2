from typing import Dict
import numpy as np
from app.models.cf_model import CFModel
from app.models.content_model import ContentModel
from app.data.db_client import fetch_user_read_books

class HybridRecommender:
    def __init__(self, cf_weight: float = 0.7, content_weight: float = 0.3):
        self.cf_model = CFModel()
        self.content_model = ContentModel()
        self.cf_weight = cf_weight
        self.content_weight = content_weight

    def train(self):
        """Träna båda modellerna"""
        self.cf_model.train()
        self.content_model.train()

    def recommend(self, user_id: str, top_n: int = 10) -> list[str]:
        """
        Genererar hybrid-rekommendationer:
        1. CF: Förutsäger betyg för alla oblästrade böcker
        2. Content-Based: Hittar böcker liknande de användaren gillat
        3. Kombinerar poängen
        """
        # 1. Hämta böcker användaren redan läst
        read_books = fetch_user_read_books(user_id)
        all_books = self.content_model.books["book_id"].tolist()
        unread_books = [b for b in all_books if b not in read_books]

        if not unread_books:
            return []

        # 2. CF-poäng (förutsagda betyg)
        cf_scores = {
            book: self.cf_model.predict_rating(user_id, book)
            for book in unread_books
        }

        # 3. Content-Based-poäng (genomsnittlig similarity till lästa böcker)
        content_scores = {}
        for book in unread_books:
            similarities = []
            for read_book in read_books:
                similar_books = self.content_model.get_similar_books(read_book, top_n=5)
                if book in similar_books:
                    # Hämta similarity score (förenklat: 1 om lik, 0 annars)
                    similarities.append(1.0)
            content_scores[book] = np.mean(similarities) if similarities else 0.0

        # 4. Kombinera poäng
        hybrid_scores = {
            book: self.cf_weight * cf_scores[book] + self.content_weight * content_scores[book]
            for book in unread_books
        }

        # 5. Sortera och returnera top-N
        sorted_books = sorted(hybrid_scores.items(), key=lambda x: x[1], reverse=True)
        return [book for book, _ in sorted_books[:top_n]]
