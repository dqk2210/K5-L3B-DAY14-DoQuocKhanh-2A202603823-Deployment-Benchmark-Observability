"""
Cost guard (tiêu chí 8) — theo dõi chi phí LLM trong Redis.
"""
from datetime import datetime, timezone
from fastapi import HTTPException
from redis.exceptions import RedisError

from app.config import settings
from app.redis_client import r

# Giá USD / 1K tokens (tham khảo gpt-4o-mini)
PRICE_INPUT_PER_1K = 0.00015
PRICE_OUTPUT_PER_1K = 0.0006


def _budget_key() -> str:
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    return f"cost_guard:daily:{today}"


def check_budget() -> None:
    """Gọi TRƯỚC khi gọi LLM. Hết budget → raise HTTPException(status_code=402)."""
    if r is None:
        raise HTTPException(status_code=503, detail="Redis unavailable for budget check")

    try:
        current = float(r.get(_budget_key()) or 0.0)
    except (RedisError, ValueError):
        raise HTTPException(status_code=503, detail="Cost guard storage error")

    if current >= settings.daily_budget_usd:
        raise HTTPException(
            status_code=402,
            detail="Daily budget exceeded",
        )


def record_cost(input_tokens: int, output_tokens: int) -> float:
    """Gọi SAU khi gọi LLM. Cộng chi phí của request vào tổng trong Redis."""
    cost = (
        (input_tokens / 1000.0) * PRICE_INPUT_PER_1K
        + (output_tokens / 1000.0) * PRICE_OUTPUT_PER_1K
    )
    if r is None:
        return round(cost, 8)

    key = _budget_key()
    try:
        pipe = r.pipeline()
        pipe.incrbyfloat(key, cost)
        pipe.expire(key, 2 * 24 * 3600)
        pipe.execute()
    except RedisError:
        pass
    return round(cost, 8)
