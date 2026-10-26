from app.models.hybrid import HybridRecommender
import logging

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    recommender = HybridRecommender()
    logging.info("Starting batch training...")
    recommender.train()
    logging.info("Batch training completed!")
