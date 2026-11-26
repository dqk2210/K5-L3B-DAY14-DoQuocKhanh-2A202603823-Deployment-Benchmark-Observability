# Deployment Information

## Public URL
https://day14-agent-khanh.onrender.com

## Platform
Render (Web Service Docker + Render Key Value / Redis, region Virginia)

## Test Commands

### Health Check & Readiness
```bash
curl https://day14-agent-khanh.onrender.com/health
# Expected: {"status":"ok","environment":"production"}

curl https://day14-agent-khanh.onrender.com/ready
# Expected: {"status":"ready"}
```

### API Test (without key → 401)
```bash
curl -i -X POST https://day14-agent-khanh.onrender.com/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Hello"}'
# Expected: HTTP 401 Unauthorized
```

### API Test (with authentication → 200)
```bash
curl -X POST https://day14-agent-khanh.onrender.com/ask \
  -H "X-API-Key: YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test", "question": "Hello"}'
# Expected: HTTP 200 OK
```

## Environment Variables Set
- `PORT` (cấp tự động bởi Render)
- `REDIS_URL` (Internal Key Value / Redis URL trên Render)
- `AGENT_API_KEY`
- `ENVIRONMENT` (`production`)
- `RATE_LIMIT_PER_MINUTE` (`10`)
- `DAILY_BUDGET_USD` (`1.0`)

## Screenshots
- [Deployment dashboard](screenshots/dashboard.png)
- [Service running](screenshots/running.png)
- [Test results](screenshots/test.png)
