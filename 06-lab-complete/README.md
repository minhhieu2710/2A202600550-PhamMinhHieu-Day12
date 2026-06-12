# Production-Ready AI Agent (Day 12 Lab)

Đây là dự án hoàn chỉnh kết hợp tất cả các tiêu chuẩn triển khai chuyên nghiệp cho một AI Agent, bao gồm đóng gói Docker tối ưu, bảo mật API, khả năng mở rộng Stateless và vận hành tin cậy.

**Thông tin sinh viên:**
- Họ và tên: Phạm Minh Hiếu
- MSSV: 2A202600550

## Checklist Deliverable

- [x] Dockerfile (multi-stage, < 500 MB)
- [x] docker-compose.yml (agent + redis)
- [x] .dockerignore
- [x] Health check endpoint (`GET /health`)
- [x] Readiness endpoint (`GET /ready`)
- [x] API Key authentication
- [x] Rate limiting
- [x] Cost guard
- [x] Config từ environment variables
- [x] Structured logging
- [x] Graceful shutdown
- [x] Public URL ready (Railway / Render config)

---

## Cấu Trúc

```
06-lab-complete/
├── app/
│   ├── main.py         # Entry point — kết hợp tất cả
│   ├── config.py       # 12-factor config
│   ├── auth.py         # API Key + JWT
│   ├── rate_limiter.py # Rate limiting
│   └── cost_guard.py   # Budget protection
├── Dockerfile          # Multi-stage, production-ready
├── docker-compose.yml  # Full stack
├── railway.toml        # Deploy Railway
├── render.yaml         # Deploy Render
├── .env.example        # Template
├── .dockerignore
└── requirements.txt
```

---

## Chạy Local

```bash
# 1. Setup
copy .env.example .env

# 2. Chạy với Docker Compose
docker compose up

# 3. Test
curl http://localhost:80/health
```

## Các tính năng đã triển khai
- **Stateless Architecture**: Lưu trữ lịch sử chat và budget trong Redis, hỗ trợ scale ngang.
- **Security**: Xác thực qua API Key, giới hạn tốc độ (Rate Limiting) và kiểm soát chi phí (Cost Guard).
- **Reliability**: Health/Readiness checks và xử lý tín hiệu SIGTERM (Graceful Shutdown).
- **Optimization**: Docker image nhỏ gọn (<200MB) sử dụng multi-stage build và chạy dưới quyền non-root user.
- **Monitoring**: Hệ thống Log định dạng JSON chuẩn Production.

# 4. Lấy API key từ .env, test endpoint
API_KEY=$(grep AGENT_API_KEY .env | cut -d= -f2)
curl -H "X-API-Key: $API_KEY" \
     -X POST http://localhost/ask \
     -H "Content-Type: application/json" \
     -d '{"question": "What is deployment?"}'
```

---

## Deploy Railway (< 5 phút)

```bash
# Cài Railway CLI
npm i -g @railway/cli

# Login và deploy
railway login
railway init
railway variables set OPENAI_API_KEY=sk-...
railway variables set AGENT_API_KEY=your-secret-key
railway up

# Nhận public URL!
railway domain
```

---

## Deploy Render

1. Push repo lên GitHub
2. Render Dashboard → New → Blueprint
3. Connect repo → Render đọc `render.yaml`
4. Set secrets: `OPENAI_API_KEY`, `AGENT_API_KEY`
5. Deploy → Nhận URL!

---

## Kiểm Tra Production Readiness

```bash
python check_production_ready.py
```

Script này kiểm tra tất cả items trong checklist và báo cáo những gì còn thiếu.
