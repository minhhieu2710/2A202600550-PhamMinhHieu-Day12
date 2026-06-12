import redis
from fastapi import Depends, HTTPException, status
from .config import settings
import time
from .auth import verify_api_key

r = redis.from_url(settings.REDIS_URL)

async def check_rate_limit(user_id: str = Depends(verify_api_key)):
    current_minute = int(time.time() / 60)
    key = f"rate_limit:{user_id}:{current_minute}"
    
    count = r.incr(key)
    if count == 1:
        r.expire(key, 60)
        
    if count > settings.RATE_LIMIT_PER_MINUTE:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Please wait a minute."
        )