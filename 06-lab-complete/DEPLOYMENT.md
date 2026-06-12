# Deployment Information

## Public URL
https://reasonable-comfort-production-cd88.up.railway.app

## Platform
Railway (Containerized Deployment)

## Test Commands

### 1. Health Check
```bash
curl https://reasonable-comfort-production-cd88.up.railway.app/health
# Expected: {"status": "ok"}
```

### 2. API Test (Requires Authentication)
```bash
curl -X POST https://reasonable-comfort-production-cd88.up.railway.app/ask \
  -H "X-API-Key: secret123" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test_user", "question": "Hello, how are you?"}'
```

## Environment Variables Set
- `PORT`: 8000
- `REDIS_URL`: URL connection string từ Railway Redis
- `AGENT_API_KEY`: `secret123`
- `LOG_LEVEL`: `INFO`

## Screenshots
- [Deployment dashboard](screenshots/dashboard.png)
- [Service running](screenshots/running.png)
- [Test results](screenshots/test.png)