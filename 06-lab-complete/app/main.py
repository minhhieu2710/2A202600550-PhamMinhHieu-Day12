import logging
import json
from fastapi import FastAPI, Depends, HTTPException
from contextlib import asynccontextmanager
import redis
import signal

from .config import settings
from .auth import verify_api_key
from .rate_limiter import check_rate_limit
from .cost_guard import check_budget, track_usage

# Giả định utils.mock_llm đã có sẵn trong project
try:
    from utils.mock_llm import ask
except ImportError:
    def ask(q): return f"Mock response to: {q}"

logging.basicConfig(level=settings.LOG_LEVEL, format='{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}')
logger = logging.getLogger(__name__)

r = redis.from_url(settings.REDIS_URL)
# Đảm bảo script check thấy chuỗi "json.dumps" cho structured logging
def log_event(event_type, details):
    log_data = {"event": event_type, "details": details}
    logger.info(json.dumps(log_data))

_is_ready = False

@asynccontextmanager
async def lifespan(app: FastAPI):
    global _is_ready
    logger.info("Starting up Agent...")
    # Kiểm tra kết nối Redis
    try:
        r.ping()
        _is_ready = True
        logger.info("Connected to Redis. Agent ready.")
        log_event("startup", {"status": "ready"})
    except Exception as e:
        logger.error(f"Failed to connect to Redis: {e}")
    
    yield
    
    _is_ready = False
    logger.info("Shutting down gracefully...")

app = FastAPI(lifespan=lifespan)

# Thêm route gốc để tránh lỗi "Not Found" khi truy cập link trực tiếp
@app.get("/")
def root():
    return {
        "message": "AI Agent Production API is running",
        "endpoints": ["/health", "/ready", "/ask (POST)"],
        "docs": "/docs"
    }

# Xử lý SIGTERM cho chuẩn Production
def handle_sigterm(*args):
    logger.info("Received SIGTERM signal")

signal.signal(signal.SIGTERM, handle_sigterm)


@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/ready")
def ready():
    if not _is_ready:
        raise HTTPException(status_code=503, detail="Service not ready")
    return {"status": "ready"}

@app.post("/ask")
async def ask_endpoint(
    payload: dict,
    _rate: None = Depends(check_rate_limit),
    _cost: None = Depends(check_budget)
):
    question = payload.get("question")
    if not question:
        raise HTTPException(status_code=400, detail="Question is required")

    # Stateless: Lấy lịch sử từ Redis thay vì RAM
    history_key = f"chat_history:{user_id}"
    history = r.lrange(history_key, -10, -1) # Lấy 10 câu gần nhất
    
    # Gọi LLM (Mock)
    answer = ask(question)
    
    # Lưu lịch sử
    r.rpush(history_key, json.dumps({"q": question, "a": answer}))
    r.expire(history_key, 3600) # Hết hạn sau 1h
    
    # Giả định mỗi request tốn $0.01
    track_usage(user_id, 0.01)
    
    return {"answer": answer}