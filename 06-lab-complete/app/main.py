"""
Production AI Agent — Part 6 Final Project
"""
import json
import logging
import signal
import sys
import time
from contextlib import asynccontextmanager
from datetime import datetime, timezone

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from app.auth import verify_api_key
from app.config import settings
from app.cost_guard import check_budget, record_cost
from app.rate_limiter import check_rate_limit
from app.redis_client import redis_healthy
from utils.mock_llm import ask as llm_ask


class JsonFormatter(logging.Formatter):
    """Format mọi log của app thành một JSON object hợp lệ trên từng dòng."""

    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "lvl": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
        }
        extra_fields = getattr(record, "fields", None)
        if isinstance(extra_fields, dict):
            payload.update(extra_fields)
        if record.exc_info:
            payload["exc"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=False)


def _setup_logger() -> logging.Logger:
    app_logger = logging.getLogger("production_agent")
    app_logger.setLevel(logging.INFO)
    app_logger.handlers.clear()
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())
    app_logger.addHandler(handler)
    app_logger.propagate = False
    return app_logger


logger = _setup_logger()
_is_shutting_down = False


@asynccontextmanager
async def lifespan(app: FastAPI):
    global _is_shutting_down
    _is_shutting_down = False

    previous_sigterm = signal.getsignal(signal.SIGTERM)

    def _on_sigterm(signum, frame):
        global _is_shutting_down
        _is_shutting_down = True
        logger.info("sigterm", extra={"fields": {"event": "sigterm", "signal": signum}})
        if callable(previous_sigterm):
            previous_sigterm(signum, frame)

    signal.signal(signal.SIGTERM, _on_sigterm)
    logger.info(
        "startup",
        extra={"fields": {"event": "startup", "environment": settings.environment, "port": settings.port}},
    )
    yield
    _is_shutting_down = True
    logger.info("shutdown", extra={"fields": {"event": "shutdown"}})


app = FastAPI(title="Production AI Agent", lifespan=lifespan)


class AskRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=2000)
    user_id: str | None = Field(default=None, max_length=128)


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.error(
        "unhandled_error",
        extra={"fields": {"event": "error", "path": request.url.path, "error_type": type(exc).__name__}},
    )
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


@app.get("/health")
def health():
    """Liveness probe: luôn trả 200 khi process còn sống, không phụ thuộc Redis."""
    return {
        "status": "ok",
        "environment": settings.environment,
    }


@app.get("/ready")
def ready():
    """Readiness probe: 200 khi sẵn sàng, 503 khi Redis mất kết nối hoặc đang shutdown."""
    if _is_shutting_down or not redis_healthy():
        raise HTTPException(status_code=503, detail="Service not ready")
    return {"status": "ready"}


@app.post("/ask")
def ask(
    body: AskRequest,
    api_key: str = Depends(verify_api_key),
):
    started = time.perf_counter()
    check_rate_limit(api_key)
    check_budget()

    answer = llm_ask(body.question)
    input_tokens = max(1, len(body.question.split()) * 2)
    output_tokens = max(1, len(answer.split()) * 2)
    cost_usd = record_cost(input_tokens, output_tokens)

    elapsed_ms = round((time.perf_counter() - started) * 1000, 2)
    logger.info(
        "request",
        extra={
            "fields": {
                "event": "request",
                "path": "/ask",
                "status": 200,
                "ms": elapsed_ms,
                "cost_usd": cost_usd,
            }
        },
    )
    return {
        "question": body.question,
        "answer": answer,
        "usage": {
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "cost_usd": cost_usd,
        },
    }
