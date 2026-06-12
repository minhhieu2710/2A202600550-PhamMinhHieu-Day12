from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from .config import settings

# Định nghĩa Security Scheme cho Swagger UI
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def verify_api_key(x_api_key: str = Depends(api_key_header)):
    if not x_api_key or x_api_key != settings.AGENT_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key",
        )
    return "user_123"