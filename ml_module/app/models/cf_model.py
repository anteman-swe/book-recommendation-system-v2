from sklearn.decomposition import NMF
from sklearn.metrics import mean_squared_error
import numpy as np
import pandas as pd
from app.data.db_client import fetch_ratings

class CFModel:
    def __init__(self, n_components: int = 50):
        self.model = NMF(n_components=n_components, random_state=42)
        self.user_index = None
        self.book_index = None
        self.user_book_matrix = None

    def train(self):
        ratings = fetch_ratings()
        # Skapa user-book matris (pivot)
        self.user_book_matrix = ratings.pivot_table(
            index="user_id", columns="book_id", values="rating", fill_value=0
        )
        self.user_index = self.user_book_matrix.index
        self.book_index = self.user_book_matrix.columns
        self.model.fit(self.user_book_matrix)

    def predict_rating(self, user_id: str, book_id: str) -> float:
        """Förutsäger betyg för en användare och bok"""
        try:
            user_idx = self.user_index.get_loc(user_id)
            book_idx = self.book_index.get_loc(book_id)
            return self.model.transform(self.user_book_matrix)[user_idx, book_idx]
        except KeyError:
            return 0.0  # Användare/bok finns inte i träningsdata
