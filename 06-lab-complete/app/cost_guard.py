import redis
from datetime import datetime
from fastapi import HTTPException, status
from .config import settings

r = redis.from_url(settings.REDIS_URL)

async def check_budget(user_id: str):
    month_key = datetime.now().strftime("%Y-%m")
    key = f"budget:{user_id}:{month_key}"
    
    current_spent = float(r.get(key) or 0)
    if current_spent >= settings.MONTHLY_BUDGET_USD:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail="Monthly budget exceeded"
        )

def track_usage(user_id: str, cost: float):
    month_key = datetime.now().strftime("%Y-%m")
    r.incrbyfloat(f"budget:{user_id}:{month_key}", cost)