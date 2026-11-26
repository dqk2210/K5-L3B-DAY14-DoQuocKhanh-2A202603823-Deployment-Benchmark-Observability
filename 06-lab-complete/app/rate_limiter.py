"""
Rate limiting (tiêu chí 7) — sliding window 60s lưu trong Redis.
"""
import hashlib
import time
import uuid
from fastapi import HTTPException
from redis.exceptions import RedisError

from app.config import settings
from app.redis_client import r

WINDOW_SECONDS = 60


def check_rate_limit(key: str) -> None:
    """Giới hạn số request trong 60 giây theo API key, state lưu trong Redis."""
    if r is None:
        raise HTTPException(status_code=503, detail="Redis unavailable for rate limiting")

    key_hash = hashlib.sha256(key.encode("utf-8")).hexdigest()[:16]
    redis_key = f"rate_limit:{key_hash}"
    now = time.time()
    member = f"{now}:{uuid.uuid4().hex}"

    try:
        r.zremrangebyscore(redis_key, 0, now - WINDOW_SECONDS)
        current_count = r.zcard(redis_key)
        if current_count >= settings.rate_limit_per_minute:
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded",
                headers={"Retry-After": str(WINDOW_SECONDS)},
            )
        pipe = r.pipeline()
        pipe.zadd(redis_key, {member: now})
        pipe.expire(redis_key, WINDOW_SECONDS)
        pipe.execute()
    except HTTPException:
        raise
    except RedisError:
        raise HTTPException(status_code=503, detail="Rate limiter storage error")
