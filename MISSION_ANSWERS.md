# Day 14 Lab - Mission Answers

> Ghi chú theo [RULES.md](RULES.md):
> - Không ghi email, số điện thoại, API key thật hay token vào file này.
> - Mọi số liệu (dung lượng MB, kết quả test...) phải lấy từ kết quả chạy thật trên máy.
> - Khai báo việc sử dụng AI vào mục **AI log** ở cuối file.

---

## Part 1: Localhost vs Production

### Exercise 1.1: Anti-patterns found in `01-localhost-vs-production/develop/app.py`
1. **Hardcode secrets trong source code (dòng 17–18):** `OPENAI_API_KEY = "sk-hardcoded-fake-key-never-do-this"` và `DATABASE_URL = "postgresql://admin:password123@localhost:5432/mydb"` được ghi trực tiếp vào file Python. Nếu push lên GitHub public thì secret bị lộ ngay lập tức.
2. **Không có config management tập trung (dòng 21–22):** `DEBUG = True` và `MAX_TOKENS = 500` viết cứng trong code, không đọc từ biến môi trường nên mỗi lần đổi môi trường (dev/staging/prod) phải sửa code.
3. **Dùng `print()` thay cho structured logging và log lộ secret (dòng 33–34, 38, 48):** Dùng `print(f"[DEBUG] ...")` không có cấu trúc JSON/timestamp/level để thu thập trên hệ thống log tập trung; nghiêm trọng hơn ở dòng 34 còn in thẳng `OPENAI_API_KEY` ra màn hình console.
4. **Không có health check / readiness endpoint (dòng 42–43):** Không có `GET /health` hay `GET /ready`, khiến cloud platform hoặc load balancer không biết process còn sống hay sẵn sàng nhận traffic để tự động restart hoặc định tuyến.
5. **Bind `host="localhost"`, hardcode `port=8000` và bật `reload=True` (dòng 49–53):**
   - `host="localhost"` chỉ lắng nghe loopback nội bộ, chạy trong Docker container sẽ không nhận được request từ bên ngoài.
   - `port=8000` cố định, không đọc biến môi trường `PORT` do cloud platform (Railway/Render) cấp phát.
   - `reload=True` bật chế độ tự reload file trong production gây tốn tài nguyên và không ổn định.
6. **Không xử lý graceful shutdown:** Thiếu `lifespan` hoặc signal handler (`SIGTERM`), khi platform dừng container thì server tắt ngang, có thể làm đứt request đang xử lý dở.

### Exercise 1.2: Chạy thử bản `develop`
Lệnh chạy server trong `01-localhost-vs-production/develop/`:
```bash
python app.py
```
Lệnh gọi endpoint (truyền `question` qua query parameter):
```bash
curl -X POST "http://localhost:8000/ask?question=Hello"
```
Output thực tế:
```json
{"answer":"Agent đang hoạt động tốt! (mock response) Hỏi thêm câu hỏi đi nhé."}
```
Kiểm tra endpoint gốc `GET /`:
```json
{"message":"Hello! Agent is running on my machine :)"}
```

### Exercise 1.3: So sánh `develop/app.py` vs `production/app.py`
| Feature | Develop (`develop/app.py`) | Production (`production/app.py` & `config.py`) | Tại sao quan trọng? |
|---------|----------------------------|-----------------------------------------------|---------------------|
| Config & Secrets | Hardcode trực tiếp (`OPENAI_API_KEY`, `DATABASE_URL`, `MAX_TOKENS`, `DEBUG = True`) | Tách ra `config.py` dùng `os.getenv(...)` có giá trị mặc định và hàm `validate()` fail-fast | Đổi cấu hình giữa dev/staging/prod mà không cần sửa code; không bao giờ lộ mật khẩu/API key lên Git |
| Host & Port | Cố định `host="localhost"`, `port=8000`, `reload=True` | `host=settings.host` (`0.0.0.0`), `port=settings.port` (đọc từ `PORT`), `reload=settings.debug` | `0.0.0.0` giúp container nhận traffic từ ngoài; đọc `PORT` động để chạy được trên Railway/Render; tắt `reload` ở prod |
| Health & Readiness check | Không có (chỉ có `GET /`) | Có `GET /health` (liveness: uptime, version, timestamp) và `GET /ready` (readiness: trả `503` nếu `is_ready=False`) | Giúp cloud orchestrator biết khi nào container treo để restart (`/health`) và khi nào sẵn sàng nhận traffic (`/ready`) |
| Logging | Dùng `print("[DEBUG] ...")`, dòng 34 còn in cả `OPENAI_API_KEY` | Dùng `logging` format JSON (`{"time":...,"level":...,"msg":...}`) và `json.dumps(...)`, chỉ log độ dài câu hỏi & `client_ip`, không log secret | Log JSON dễ parse/lọc/cảnh báo trên Datadog, Grafana Loki... và đảm bảo không rò rỉ dữ liệu nhạy cảm |
| Shutdown | Không có handler, tắt đột ngột | Dùng `lifespan` context manager (set `is_ready = False`, chờ request hoàn thành) + đăng ký `signal.signal(signal.SIGTERM, handle_sigterm)` | Khi deploy bản mới hoặc scale-in, server không làm rớt request của người dùng đang xử lý |
| Input & CORS | `POST /ask` nhận query param, không cấu hình CORS | `POST /ask` nhận JSON body + validate trả `422` nếu thiếu `question`; cấu hình `CORSMiddleware` theo `ALLOWED_ORIGINS` | Chuẩn hóa REST API, trả mã lỗi rõ ràng khi input sai và kiểm soát domain được phép gọi API từ trình duyệt |

**Ví dụ cụ thể đoạn code đã sửa từ `develop/app.py` sang `production/`:**
- **Chống hardcode secret & port:**
  - Trong `develop/app.py` (dòng 17, 51–52):
    ```python
    OPENAI_API_KEY = "sk-hardcoded-fake-key-never-do-this"
    uvicorn.run("app:app", host="localhost", port=8000, reload=True)
    ```
  - Đã sửa trong `production/config.py` (dòng 17–19, 27) và `production/app.py` (dòng 194–199):
    ```python
    host: str = field(default_factory=lambda: os.getenv("HOST", "0.0.0.0"))
    port: int = field(default_factory=lambda: int(os.getenv("PORT", "8000")))
    openai_api_key: str = field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))
    ```
- **Bổ sung health check & graceful shutdown:**
  - `develop/app.py` không có endpoint `/health` và không xử lý `SIGTERM`.
  - `production/app.py` thêm `@app.get("/health")` (dòng 135–149), `@app.get("/ready")` (dòng 152–161), `lifespan` (dòng 39–67) và `signal.signal(signal.SIGTERM, handle_sigterm)` (dòng 189).

**Output test thực tế bản `production/app.py` (chạy kiểm tra ở cổng 8011):**
- `GET /health`: `{"status":"ok","uptime_seconds":1.5,"version":"1.0.0","environment":"development","timestamp":"2026-11-26T08:23:44.722448+00:00"}`
- `GET /ready`: `{"ready":true}`
- `POST /ask` với JSON `{"question":"Hello"}`: `{"question":"Hello","answer":"Agent đang hoạt động tốt! (mock response) Hỏi thêm câu hỏi đi nhé.","model":"gpt-4o-mini"}`

---

## Part 2: Docker

### Exercise 2.1: Câu hỏi về `02-docker/develop/Dockerfile`
1. **Base image:** `python:3.11` (full Python image ~1 GB, chứa sẵn nhiều công cụ hệ thống).
2. **Working directory:** `/app` (`WORKDIR /app`).
3. **Tại sao `COPY requirements.txt` đứng trước `COPY . .`:** Tận dụng **Docker layer cache**. File `requirements.txt` ít thay đổi hơn source code (`app.py`). Khi chỉ sửa code mà không sửa thư viện, Docker dùng lại cache của bước `RUN pip install --no-cache-dir -r requirements.txt`, giúp build lại rất nhanh.
4. **Sự khác nhau giữa `CMD` và `ENTRYPOINT`:**
   - `CMD` chỉ định lệnh mặc định khi container chạy và **dễ dàng bị ghi đè** bởi lệnh truyền vào cuối `docker run <image> <cmd_mới>`.
   - `ENTRYPOINT` định nghĩa file thực thi chính (cố định hơn); các tham số truyền thêm ở `docker run` sẽ được nối làm argument cho `ENTRYPOINT` (muốn ghi đè phải dùng cờ `--entrypoint`).

### Exercise 2.2: Build và chạy container `develop`
Lệnh build từ gốc repo & chạy test container:
```bash
docker build -f 02-docker/develop/Dockerfile -t my-agent:develop .
docker run --rm -d --name part2-dev -p 8000:8000 my-agent:develop
curl -X POST "http://localhost:8000/ask?question=What%20is%20Docker"
docker images my-agent:develop
docker stop part2-dev
```
Output thực tế:
```text
{"answer":"Container là cách đóng gói app để chạy ở mọi nơi. Build once, run anywhere!"}
```
Kích thước image `my-agent:develop`: **`1.67GB`** (`1,667,784,070` bytes ≈ `1,668 MB`).

### Exercise 2.3: Multi-stage build (`02-docker/production/Dockerfile`)
- **Stage 1 (`builder`, từ `python:3.11-slim AS builder`):** Cài đặt các công cụ biên dịch (`gcc`, `libpq-dev`), copy `02-docker/production/requirements.txt` và cài Python packages bằng `pip install --no-cache-dir --user` vào `/root/.local`.
- **Stage 2 (`runtime`, từ `python:3.11-slim AS runtime`):** Tạo user non-root `appuser`, chỉ `COPY --from=builder /root/.local /home/appuser/.local` (packages đã cài) và copy source code (`main.py`, `utils/mock_llm.py`), đặt `USER appuser`, cấu hình `PATH`, `PYTHONPATH`, `HEALTHCHECK` và `CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]`.
- **Tại sao image nhỏ hơn:** Dùng base image gọn (`python:3.11-slim`) và bỏ lại toàn bộ compiler (`gcc`, `libpq-dev`), cache build ở Stage 1 không đưa vào image cuối; đồng thời chạy dưới user `appuser` (non-root) giúp bảo mật hơn.

**So sánh kích thước image (đo bằng `docker images` / `docker image inspect`):**
- Develop (`my-agent:develop`): `1.67 GB` (`1,667.8 MB`)
- Production (`my-agent:advanced`): `240 MB` (`239.8 MB`)
- Chênh lệch (giảm): **`85.6%`** (nhẹ hơn ~`1,428 MB`)

### Exercise 2.4: Docker Compose stack (`02-docker/production/docker-compose.yml`)
**Sơ đồ kiến trúc các service (network `internal` — `driver: bridge`):**
```text
Client
  │  HTTP (:80 trong compose; test local qua :18080 do Windows HTTPAPI chiếm :80)
  ▼
Nginx (nginx:alpine — Reverse Proxy, rate limit 10r/s, security headers)
  │  proxy_pass http://agent_backend (port 8000)
  ▼
Agent (FastAPI + uvicorn --workers 2, phụ thuộc redis & qdrant healthy)
  ├──► Redis (redis:7-alpine, port 6379 — session cache & rate limiting)
  └──► Qdrant (qdrant/qdrant:v1.9.0, port 6333 — vector DB cho RAG)
```
*(Các service `agent`, `redis`, `qdrant` giao tiếp qua tên service DNS nội bộ trong bridge network `internal`, không expose port trực tiếp ra host; chỉ `nginx` nhận traffic từ ngoài.)*

**Kết quả test qua Nginx (`/health` và `POST /ask`):**
*(Trên máy Windows có `Microsoft-HTTPAPI/2.0` đang giữ cổng 80 nên khi test thực tế đã map port tạm `18080:80` cho Nginx để kiểm tra đầy đủ luồng qua Nginx → Agent, sau đó `down` dọn dẹp stack)*
```text
GET /health:
HTTP/1.1 200 OK
Server: nginx
Content-Type: application/json
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
X-XSS-Protection: 1; mode=block

{"status":"ok","uptime_seconds":9.4,"version":"2.0.0","timestamp":"2026-11-26T09:03:33.556866"}

POST /ask (body: {"question":"Explain microservices"}):
HTTP/1.1 200 OK
Server: nginx
Content-Type: application/json

{"answer":"Agent đang hoạt động tốt! (mock response) Hỏi thêm câu hỏi đi nhé."}
```

---

## Part 3: Cloud Deployment (Deploy Agent Part 6)

### Exercise 3.1 / 3.2: Deploy lên nền tảng chính (Railway hoặc Render)
- **Nền tảng chọn:** [Railway / Render]
- **Public URL:** `https://...`
- **Screenshots:**
  - `screenshots/dashboard.png`
  - `screenshots/running.png`
  - `screenshots/test.png`

### So sánh `railway.toml` và `render.yaml`
- [TODO: Khác nhau chỗ nào, vì sao? (Hoặc ghi URL nếu đã deploy cả 2 nền tảng)]

### Exercise 3.3: GCP Cloud Run (`03-cloud-deployment/production-cloud-run/`)
- [TODO: Đọc `cloudbuild.yaml` và `service.yaml`, viết 3–5 dòng mô tả pipeline CI/CD đi qua những bước nào]

---

## Part 4: API Security

### Exercise 4.1: API Key Authentication (`04-api-gateway/develop/`)
- **API key được kiểm tra ở đâu:** Tại dependency `verify_api_key` trong `04-api-gateway/develop/app.py` (dòng 39–54), đọc header `X-API-Key` bằng `APIKeyHeader(name="X-API-Key", auto_error=False)` và inject vào route `POST /ask` thông qua `Depends(verify_api_key)` (dòng 70).
- **Điều gì xảy ra nếu sai/thiếu key:**
  - Thiếu header `X-API-Key` → trả **`401 Unauthorized`** (`Missing API key. Include header: X-API-Key: <your-key>`).
  - Sai giá trị key → trả **`403 Forbidden`** (`Invalid API key.`).
- **Làm sao rotate key:** Vì key được đọc từ biến môi trường `AGENT_API_KEY` (dòng 35), chỉ cần cập nhật biến môi trường mới và restart/redeploy service; để rotate không downtime (zero-downtime), cho phép cấu hình danh sách nhiều key hợp lệ (chấp nhận cả key cũ lẫn key mới trong thời gian chuyển giao rồi mới gỡ key cũ).

**Output test (`curl -i` cho trường hợp 401, 403 và 200):**
```text
--- Không có X-API-Key ---
HTTP/1.1 401 Unauthorized
date: Thu, 26 Nov 2026 09:51:49 GMT
server: uvicorn
content-length: 67
content-type: application/json

{"detail":"Missing API key. Include header: X-API-Key: <your-key>"}

--- Sai X-API-Key ---
HTTP/1.1 403 Forbidden
date: Thu, 26 Nov 2026 09:51:49 GMT
server: uvicorn
content-length: 29
content-type: application/json

{"detail":"Invalid API key."}

--- Đúng X-API-Key ---
HTTP/1.1 200 OK
date: Thu, 26 Nov 2026 09:51:49 GMT
server: uvicorn
content-length: 145
content-type: application/json

{"question":"Hello","answer":"Đây là câu trả lời từ AI agent (mock). Trong production, đây sẽ là response từ OpenAI/Anthropic."}
```

### Exercise 4.2 & 4.3: JWT Authentication & Rate Limiting (`04-api-gateway/production/`)
- **JWT flow (`auth.py`):** Client gửi username/password tới `POST /auth/token` → `authenticate_user` xác thực tài khoản (`student` / `demo123`) → `create_token` tạo JWT ký bằng `HS256` (chứa `sub`, `role`, `exp` 60 phút) → Client gắn `Authorization: Bearer <TOKEN_DA_CHE>` khi gọi `/ask` → `verify_token` xác minh chữ ký và hạn dùng stateless.
- **Thuật toán rate limiting sử dụng (`rate_limiter.py`):** **Sliding Window Counter** — dùng `collections.deque` lưu danh sách timestamp các request trong 60 giây gần nhất, tự loại bỏ các timestamp cũ hơn `now - window_seconds` rồi kiểm tra `len(window) >= max_requests`.
- **Giới hạn requests/phút:** Tài khoản thường (`student`, role `user`) là **10 requests / 60 giây** (`rate_limiter_user`); tài khoản admin (`teacher`, role `admin`) là **100 requests / 60 giây** (`rate_limiter_admin`).
- **Cách bypass / nới limit cho admin:** Trong `app.py` dòng 141 (`limiter = rate_limiter_admin if role == "admin" else rate_limiter_user`), dựa vào `role` giải mã từ JWT để cấp hạn mức cao hơn cho admin (hoặc bỏ qua `limiter.check(username)` nếu `role == "admin"`).

**Output test (`curl -i` với tài khoản `student` ở `POST /auth/token` — đã che token):**
```text
--- Không có token ---
HTTP/1.1 401 Unauthorized
server: uvicorn
www-authenticate: Bearer
content-type: application/json

{"detail":"Authentication required. Include: Authorization: Bearer <token>"}

--- Có Bearer token (Request 1/10, header: Authorization: Bearer <TOKEN_DA_CHE>) ---
HTTP/1.1 200 OK
server: uvicorn
content-type: application/json
x-content-type-options: nosniff
x-frame-options: DENY
x-xss-protection: 1; mode=block
referrer-policy: strict-origin-when-cross-origin

{"question":"Explain JWT","answer":"Agent đang hoạt động tốt! (mock response) Hỏi thêm câu hỏi đi nhé.","usage":{"requests_remaining":9,"budget_remaining_usd":1.6e-05}}

--- Request 10/10 ---
HTTP/1.1 200 OK
content-type: application/json

{"question":"Test 10","answer":"Agent đang hoạt động tốt! (mock response) Hỏi thêm câu hỏi đi nhé.","usage":{"requests_remaining":0,"budget_remaining_usd":0.000184}}

--- Request 11 (Vượt giới hạn 10 req/phút) ---
HTTP/1.1 429 Too Many Requests
server: uvicorn
x-ratelimit-limit: 10
x-ratelimit-remaining: 0
x-ratelimit-reset: 1795686791
retry-after: 59
content-length: 98
content-type: application/json

{"detail":{"error":"Rate limit exceeded","limit":10,"window_seconds":60,"retry_after_seconds":59}}
```

### Exercise 4.4: Cost Guard (`04-api-gateway/production/cost_guard.py`)
- **Cách triển khai Cost Guard:**
  - Trước khi gọi LLM, `check_budget(user_id)` kiểm tra ngân sách tổng toàn hệ thống (vượt `$10/ngày` trả `503`) và ngân sách từng user (vượt `$1/ngày` ở bản demo — hoặc `$10/tháng` / `DAILY_BUDGET_USD` khi làm với Redis — trả **`402 Payment Required`**); nếu chi phí đạt ≥ 80% thì log cảnh báo.
  - Sau khi LLM trả lời, `record_usage(user_id, input_tokens, output_tokens)` tính chi phí dựa trên đơn giá từng 1K input/output token và cộng dồn vào bộ đếm. Trong môi trường production nhiều instance (như Part 6), bộ đếm này phải lưu trong **Redis** (dùng `INCRBYFLOAT` + `EXPIRE` theo key ngày/tháng) để chia sẻ trạng thái giữa các instance và không mất khi restart.
- **Vì sao cần cả Rate Limiting và Cost Guard:**
  - **Rate Limiting** bảo vệ **tốc độ/lưu lượng** (ngăn spam hoặc DDoS làm quá tải server trong từng phút).
  - **Cost Guard** bảo vệ **ngân sách/tiền** (vì ngay cả khi người dùng gọi dưới ngưỡng rate limit, các prompt rất dài hoặc việc gọi đều đặn cả ngày vẫn có thể tiêu tốn vượt quá budget LLM cho phép).

---

## Part 5: Scaling & Reliability

### Exercise 5.1 & 5.2: Health Check (`/health`, `/ready`) & Graceful Shutdown (`develop/`)
- **Sự khác nhau giữa `/health` (liveness) và `/ready` (readiness):**
  - `GET /health` (**Liveness probe**): kiểm tra process của agent còn sống hay không (uptime, memory). Nếu fail → platform sẽ **restart container**.
  - `GET /ready` (**Readiness probe**): kiểm tra agent đã sẵn sàng nhận traffic chưa (đã khởi tạo xong model/kết nối dependencies và chưa bước vào quá trình shutdown). Nếu trả về `503` → load balancer **tạm ngừng đẩy request mới** vào instance đó (nhưng không restart).
- **Cơ chế Graceful Shutdown khi nhận `SIGTERM`:**
  1. Platform gửi signal `SIGTERM` → hàm `handle_sigterm` ghi log đã nhận tín hiệu, sau đó `uvicorn` kích hoạt block shutdown của `lifespan`.
  2. Trong `lifespan` (`05-scaling-reliability/develop/app.py` dòng 55–66), cờ `_is_ready` được chuyển thành `False` (nên `/ready` trả `503`, load balancer không gửi thêm request mới).
  3. Server chờ cho `_in_flight_requests == 0` (tối đa `30` giây) để các request đang xử lý dở kịp trả `200 OK`, rồi mới kết thúc sạch sẽ.

**Kết quả test thực tế (`05-scaling-reliability/develop/`):**
```text
GET /health:
{"status":"ok","uptime_seconds":0.9,"version":"1.0.0","environment":"development","timestamp":"2026-11-26T10:09:45.408470+00:00","checks":{"memory":{"status":"ok","used_percent":11.4}}}

GET /ready:
{"ready":true,"in_flight_requests":1}

Test Graceful Shutdown (gửi 2 request song song rồi gửi SIGTERM ngay sau 0.05s):
Response 1: {"answer":"Agent đang hoạt động tốt! (mock response) Hỏi thêm câu hỏi đi nhé."} [HTTP 200]
Response 2: {"answer":"Agent đang hoạt động tốt! (mock response) Hỏi thêm câu hỏi đi nhé."} [HTTP 200]

Server logs:
INFO:     Shutting down
INFO:     127.0.0.1:44070 - "POST /ask?question=hello1 HTTP/1.1" 200 OK
INFO:     127.0.0.1:44068 - "POST /ask?question=hello2 HTTP/1.1" 200 OK
INFO:     Waiting for application shutdown.
2026-11-26 17:09:51,589 INFO 🔄 Graceful shutdown initiated...
2026-11-26 17:09:51,589 INFO ✅ Shutdown complete
INFO:     Application shutdown complete.
INFO:     Finished server process [5034]
2026-11-26 17:09:51,590 INFO Received signal 15 — uvicorn will handle graceful shutdown
```

### Exercise 5.3, 5.4 & 5.5: Stateless Design, Load Balancing & `test_stateless.py` (`production/`)
- **Vì sao state trong RAM bị hỏng khi scale nhiều instance & cách Redis giải quyết:**
  - Khi chạy nhiều instance (ví dụ `--scale agent=3`), mỗi container có vùng nhớ RAM riêng. Nếu lưu lịch sử hội thoại trong biến dict ở RAM của `instance-1`, khi Nginx chia request tiếp theo sang `instance-2` thì `instance-2` không có session đó → mất ngữ cảnh hoặc lỗi 404.
  - Khi chuyển toàn bộ session sang **Redis** dùng chung (`session:{session_id}` với TTL 3600s), bất kỳ instance nào nhận request cũng đọc và ghi nối tiếp được cùng một lịch sử hội thoại, đồng thời session không bị mất nếu một instance bị restart.

**Kết quả chạy `python test_stateless.py` với `--scale agent=3` (`k5-day14-scaling` qua Nginx cổng 8080):**
```text
============================================================
Stateless Scaling Demo
============================================================

Session ID: e56e5c7e-a842-471a-be30-903629d35fdf

Request 1: [instance-7af121]
  Q: What is Docker?
  A: Container là cách đóng gói app để chạy ở mọi nơi. Build once, run anywhere!...

Request 2: [instance-f090ca]
  Q: Why do we need containers?
  A: Agent đang hoạt động tốt! (mock response) Hỏi thêm câu hỏi đi nhé....

Request 3: [instance-38359a]
  Q: What is Kubernetes?
  A: Tôi là AI agent được deploy lên cloud. Câu hỏi của bạn đã được nhận....

Request 4: [instance-7af121]
  Q: How does load balancing work?
  A: Đây là câu trả lời từ AI agent (mock). Trong production, đây sẽ là response từ O...

Request 5: [instance-f090ca]
  Q: What is Redis used for?
  A: Agent đang hoạt động tốt! (mock response) Hỏi thêm câu hỏi đi nhé....

------------------------------------------------------------
Total requests: 5
Instances used: {'instance-7af121', 'instance-38359a', 'instance-f090ca'}
✅ All requests served despite different instances!

--- Conversation History ---
Total messages: 10
  [user]: What is Docker?...
  [assistant]: Container là cách đóng gói app để chạy ở mọi nơi. Build once...
  [user]: Why do we need containers?...
  [assistant]: Agent đang hoạt động tốt! (mock response) Hỏi thêm câu hỏi đ...
  [user]: What is Kubernetes?...
  [assistant]: Tôi là AI agent được deploy lên cloud. Câu hỏi của bạn đã đư...
  [user]: How does load balancing work?...
  [assistant]: Đây là câu trả lời từ AI agent (mock). Trong production, đây...
  [user]: What is Redis used for?...
  [assistant]: Agent đang hoạt động tốt! (mock response) Hỏi thêm câu hỏi đ...

✅ Session history preserved across all instances via Redis!
```
**Giải thích kết quả:** Nginx thực hiện round-robin chia 5 request lần lượt tới 3 container khác nhau (`instance-7af121`, `instance-f090ca`, `instance-38359a`), nhưng khi truy vấn `GET /chat/{session_id}/history`, toàn bộ `10` messages của cả 5 lượt hỏi đáp vẫn được giữ nguyên vẹn nhờ lưu tập trung trong Redis.

---

## Part 6: Final Project (`06-lab-complete/`)

### Kết quả `python check_production_ready.py` (mục `📋 Checklist Deliverable`)
```text
================================================================
  📋 Checklist Deliverable
     ✅ Dockerfile (multi-stage, < 500 MB)
     ✅ docker-compose.yml (agent + redis)
     ✅ .dockerignore
     ✅ Health check endpoint (GET /health)
     ✅ Readiness endpoint (GET /ready)
     ✅ API Key authentication
     ✅ Rate limiting
     ✅ Cost guard
     ✅ Config từ environment variables
     ✅ Structured logging
     ✅ Graceful shutdown
     ✅ Public URL ready (Railway / Render config)
----------------------------------------------------------------
  Result: 12/12 tiêu chí đạt · 43/43 checks passed
  🎉 PASS 12/12 — PRODUCTION READY! Deploy nào!
================================================================
```

---

## AI log

> Ghi lại mỗi lần sử dụng công cụ AI cho code Part 6 hoặc câu trả lời trong bài:

| Thời điểm / Mục | Hỏi AI nội dung gì | AI gợi ý / trả về gì | Tự chỉnh sửa & tự kiểm tra lại như thế nào |
|---|---|---|---|
| Setup (CP0) | Tạo `Plan.md` tổng hợp yêu cầu từ các file `.md` và khởi tạo file khung CP0 (`MISSION_ANSWERS.md`, `screenshots/`) | Sinh checklist `Plan.md` và khung `MISSION_ANSWERS.md` theo cấu trúc nộp bài lớp K5 | Tự đối chiếu với `CHECKPOINTS.md`, `SUBMISSION.md`, `RUBRIC.md` và `RULES.md` |
| CP1 (Part 1) | Phân tích `develop/app.py` vs `production/app.py`, kiểm tra chạy bản `develop` & `production`, viết phần trả lời CP1 và giải thích | Hoàn thiện mục Part 1 trong `MISSION_ANSWERS.md` với 6 anti-patterns, bảng so sánh 12-Factor, và output test | Tự kiểm tra đối chiếu từng dòng code trong `01-localhost-vs-production/` và test curl thực tế trên port 8000 / 8011 |
| CP2 (Part 2) | Phân tích Dockerfile single vs multi-stage, đo size, chạy test container & Docker Compose stack | Hoàn thiện mục Part 2 trong `MISSION_ANSWERS.md` kèm sơ đồ kiến trúc | Tự chạy `docker build`, `docker run`, `docker image inspect` (`1.67GB` vs `240MB`) và test qua Nginx (`200 OK`) |
| CP3 (Part 4) | Phân tích `develop` & `production` trong `04-api-gateway/`, chạy test `curl -i` để kiểm chứng 401/403/200/429 | Hoàn thiện mục Part 4 trong `MISSION_ANSWERS.md` (che token JWT, giải thích rate limit & cost guard) | Tự chạy test cả 2 bản trên WSL2 (`.venv`), xác nhận request 1–10 trả 200 và request 11 trả 429 |
| CP4 (Part 5) | Kiểm tra health/readiness, test SIGTERM graceful shutdown và scale 3 agent instances qua Nginx + Redis | Hoàn thiện mục Part 5 trong `MISSION_ANSWERS.md` với output thật từ `app.py` và `test_stateless.py` | Tự chạy trên WSL2 + Docker Compose (`-p k5-day14-scaling`), xác nhận 3 instance phục vụ cùng session và thu dọn stack |
| CP5 (Part 6) | Triển khai toàn bộ 12 tiêu chí trong `06-lab-complete/` (`app/`, `Dockerfile`, `docker-compose.yml`, `.dockerignore`, `.env.example`, `railway.toml`, `render.yaml`) | Hoàn thiện các module theo Hợp đồng trong `06-lab-complete/README.md` | Tự chạy `python check_production_ready.py` đầy đủ trong Ubuntu WSL2 đạt `PASS 12/12` (`43/43 checks passed`, image `297 MB`, `docker stop` `0.8s`) và kiểm tra stack `docker compose` |
