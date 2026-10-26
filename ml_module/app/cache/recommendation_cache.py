import redis
import json
from app.config import settings

class RecommendationCache:
    def __init__(self):
        self.redis = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            decode_responses=True
        )

    def get(self, user_id: str) -> list[str] | None:
        """Hämtar cachade rekommendationer för användare"""
        cached = self.redis.get(f"recs:{user_id}")
        return json.loads(cached) if cached else None

    def set(self, user_id: str, recommendations: list[str]):
        """Cachar rekommendationer för användare"""
        self.redis.setex(
            f"recs:{user_id}",
            settings.CACHE_TTL_SECONDS,
            json.dumps(recommendations)
        )
