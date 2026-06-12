from fastapi import Header, HTTPException, status
from .config import settings

async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != settings.AGENT_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key",
        )
    # Trong thực tế, bạn có thể map API Key này với một User ID cụ thể
    return "user_123"