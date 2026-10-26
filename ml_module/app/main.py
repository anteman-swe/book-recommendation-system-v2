from fastapi import FastAPI, HTTPException
from app.models.hybrid import HybridRecommender
from app.cache.recommendation_cache import RecommendationCache
from app.config import settings
import logging

app = FastAPI(title="Book Recommender ML Service")
recommender = HybridRecommender()
cache = RecommendationCache()

# Ladda modeller vid startup (eller träna om ingen modell finns)
@app.on_event("startup")
async def startup_event():
    logging.info("Training hybrid model...")
    recommender.train()
    logging.info("Model trained successfully!")

@app.get("/recommendations/{user_id}")
async def get_recommendations(user_id: str):
    """Returnerar cachade eller nyligen beräknade rekommendationer"""
    # 1. Kolla cache först
    cached_recs = cache.get(user_id)
    if cached_recs:
        return {"user_id": user_id, "recommendations": cached_recs}

    # 2. Beräkna om ingen cache
    try:
        recommendations = recommender.recommend(user_id, settings.TOP_N_RECOMMENDATIONS)
        cache.set(user_id, recommendations)
        return {"user_id": user_id, "recommendations": recommendations}
    except Exception as e:
        logging.error(f"Error generating recommendations: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/retrain")
async def retrain_model():
    """Trigger batch-omträning av modellen"""
    try:
        recommender.train()
        return {"status": "success", "message": "Model retrained"}
    except Exception as e:
        logging.error(f"Error retraining model: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
