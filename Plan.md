# 📋 Kế Hoạch & Checklist Làm Bài — Day 14: Deployment, Benchmark & Observability

> **Học viên:** Đỗ Quốc Khánh · **Lớp:** K5-L3B · **MSSV:** 2A202603823  
> **Repository:** `K5-L3B-DAY14-DoQuocKhanh-2A202603823-Deployment-Benchmark-Observability`  
> **Hình thức:** Cá nhân · **Thời lượng tại lớp:** 4 giờ · **Deadline:** 23h59 (GMT+7) ngày lab (ưu tiên thông báo của Lab Coach)  
> **Thang điểm:** Tổng thô **120 điểm** → quy về thang 100 (`Tổng thô × 100 / 120`, làm tròn 0.5). **Đạt:** ≥ 70/100 (≥ 84/120). Không có điểm bonus.
>
> ⚠️ **Lưu ý bảo mật:** Tuyệt đối không dán API key thật, token cloud, email hay số điện thoại vào file này hoặc bất kỳ file nào trong repo.

---

## 🧭 1. Tổng Quan Tiến Độ (Dashboard)

Đánh dấu `[x]` khi hoàn thành từng mốc để theo dõi nhanh tiến độ và điểm số:

| Trạng thái | Checkpoint | Nội dung (theo lộ trình K5) | Thời gian | Điểm tối đa | Sản phẩm chính |
| :---: | :--- | :--- | :---: | :---: | :--- |
| [ ] | **CP0** | Setup môi trường (WSL2, Python 3.11+, Docker, Repo) | 10' | — | Repo đúng tên, Public, chạy được WSL2 + Docker |
| [x] | **CP1** | Part 1 — Localhost vs Production (Ex 1.1–1.3) | 20' | **8 đ** | `MISSION_ANSWERS.md` (mục Part 1) |
| [ ] | **CP2** | Part 2 — Docker Containerization (Ex 2.1–2.4) | 30' | **8 đ** | `MISSION_ANSWERS.md` (mục Part 2, số MB đo thật) |
| [x] | **CP3** | Part 4 — API Security (Ex 4.1–4.4) | 25' | **8 đ** | `MISSION_ANSWERS.md` (mục Part 4, output 401/200/429) |
| [x] | **CP4** | Part 5 — Scaling & Reliability (Ex 5.1–5.5) | 20' | **8 đ** | `MISSION_ANSWERS.md` (mục Part 5, test stateless) |
| [x] | **CP5** | **Part 6 — Final Project (`06-lab-complete/`)** | 60' | **50 đ** *(+10đ ở CP6)* | `python check_production_ready.py` → **`PASS 12/12`** |
| [ ] | **CP6** | Part 3 + Deploy Part 6 lên Cloud (Ex 3.1–3.3) | 25' | **8 đ** *(+10đ Part 6)* | `DEPLOYMENT.md`, 3 ảnh deploy, `MISSION_ANSWERS.md` (Part 3) |
| [ ] | **CP7** | Part 7 Bước 1 — Benchmark local (Ex 7.1–7.3) | 45' | **9 đ** | `reports/*.json`, sửa KB đạt 23/23, điền `BENCHMARK_REPORT.md` |
| [ ] | **CP8** | Part 7 Bước 2 — Observability stack & Đóng gói (Ex 7.4–7.7) | Sau lab | **11 đ** | `benchmark-results/*.csv`, 4 ảnh Part 7, nộp link LMS |
| | | **TỔNG CỘNG** | | **120 đ** | **Quy thang 100 · Đạt ≥ 84/120 (70/100)** |

> 💡 **Chiến lược quản lý giờ:** CP5 (Part 6) chiếm tới **60/120 điểm** (50% tổng điểm). Không để CP1–CP4 lấn giờ của CP5. Kẹt quá 10 phút ở một mốc → hỏi Lab Coach, ghi chú lại rồi chuyển tiếp.

---

## 🚨 2. Các Quy Định Bắt Buộc & Điều Cấm (Đọc Kỹ Tránh Mất Điểm Oan)

### Quy định từ `RULES.md` & `RUBRIC.md`
- [ ] **KHÔNG sửa** `06-lab-complete/check_production_ready.py` *(vi phạm = **0 điểm Part 6**)*.
- [ ] **KHÔNG sửa** `06-lab-complete/benchmark-observability/develop/eval/golden_dataset.jsonl` *(Ex 7.3 chỉ sửa `KNOWLEDGE_BASE` trong `develop/utils/mock_llm.py`)*.
- [ ] **KHÔNG commit secret** (`.env`, `AGENT_API_KEY` thật, token Railway/Render) kể cả trong lịch sử git *(vi phạm = **−10 điểm** và phải revoke key ngay; xóa file thôi chưa đủ)*.
- [ ] **KHÔNG ghi email, số điện thoại** vào bất kỳ file nào trong bài. Họ tên và MSSV chỉ ghi ở tên repo và ô Họ tên của `BENCHMARK_REPORT.md`.
- [ ] **KHÔNG bịa số đo:** mọi số liệu (MB image, latency, RPS, accuracy, thời gian alert firing) phải đo thật và **khớp 100%** với file JSON/CSV nộp kèm *(lệch số = **0 điểm mục Part 7 tương ứng**)*.
- [ ] **Khai báo AI Log:** mỗi lần dùng AI cho code Part 6 hoặc câu trả lời, ghi rõ vào cuối `MISSION_ANSWERS.md` mục **AI log** *(hỏi gì, nhận gì, tự sửa & tự kiểm tra thế nào)*. Phải hiểu và giải thích được code + số liệu khi Lab Coach hỏi.
- [ ] **Không sao chép:** code, câu trả lời, URL deploy, ảnh chụp, file report phải là của riêng mình *(vi phạm = 0 điểm phần liên quan và báo chương trình)*.
- [ ] **Repo Public & đúng cấu trúc:** repo Private không mở được → **không chấm**; sai tên repo/sai vị trí file → **−5 điểm** (hoặc không chấm nếu không tìm được).
- [ ] **Commit trước deadline:** bản chấm là commit cuối cùng trước deadline. Không force-push, không sửa ngày commit.

### ⚠️ 11 Lưu Ý Riêng Cho Lớp K5 (Khác Với `CODE_LAB.md` & `DAY14_DELIVERY_CHECKLIST.md`)
1. **Windows bắt buộc chạy Python trong WSL2** (Docker Desktop bật WSL2 integration). Kiểm tra `python -c "import os; print(os.name)"` phải in `posix`. Chạy Python Windows (kể cả Git Bash) sẽ không gửi được SIGTERM → Graceful shutdown luôn `⚠️` → không bao giờ `PASS 12/12`.
2. **Làm Part 6 ngay trong `06-lab-complete/`**, KHÔNG chuyển code ra `app/` ở gốc repo.
3. **Thứ tự K5:** Part 1 → Part 2 → **Part 4 → Part 5 → Part 6 → Part 3** (deploy luôn agent Part 6) → Part 7. Rút ngắn Part 1, 2, 4, 5 bằng cách chạy ví dụ có sẵn & trả lời vào `MISSION_ANSWERS.md`, không cần viết lại code mẫu.
4. **Part 1 & Part 2 (`develop/`):** `POST /ask` nhận `question` qua **query param** (`curl -X POST "http://localhost:8000/ask?question=Hello"`), gửi JSON sẽ bị `422`. Tắt server cũ (cổng 8000) trước khi bật bản mới.
5. **Part 2:** build image **từ gốc repo** (`docker build -f 02-docker/develop/Dockerfile -t my-agent:develop .` và `docker build -f 02-docker/production/Dockerfile -t my-agent:advanced .`), không `cd` vào thư mục con.
6. **Part 2 & Part 5 (`production/`):** tạo file rỗng `touch .env.local` trong `02-docker/production/` và `05-scaling-reliability/production/` trước khi chạy `docker compose up`.
7. **Part 4:**
   - `develop/`: chạy `AGENT_API_KEY=secret-key-123 python app.py`.
   - `production/`: tắt bản develop trước, cài `requirements.txt`. Lấy token ở `POST /auth/token` với `student` / `demo123` (không phải `/token` và `admin`/`secret`), giới hạn 10 req/phút. Thêm `-i` vào `curl` để thấy HTTP code `401 / 200 / 429` và **che token** trước khi dán.
8. **Part 5 (`production/`):** mở cổng **8080**, endpoint **`POST /chat`** (không phải cổng 80 và `/ask`). Chạy `docker compose -p k5-day14-scaling up -d --build --scale agent=3` rồi `python test_stateless.py` (script gửi 5 câu trong cùng một session rồi đọc history, không tự tắt instance nào). Luôn gắn `-p k5-day14-scaling` cho mọi lệnh `docker compose` (kể cả `logs`, `down`) để không đụng tên project `production` với Part 2 và Part 7.
9. **Part 3 (CP6):** chạy trong `06-lab-complete/` (không `cd 03-cloud-deployment/`). Railway CLI cài bằng `npm` (cần **Node.js**). Nếu dùng **Render**, `render.yaml` nằm trong thư mục con (`06-lab-complete/`) và phải tự khai báo Redis (kẹt thì hỏi Lab Coach). Phải tạo dịch vụ **Redis trên cloud**, đặt `REDIS_URL` cho service agent và kiểm `/ready` trả `200` **trước khi chụp ảnh**. Tự kiểm bằng 4 lệnh ở CP6 (không dùng Self-Test của `DAY14_DELIVERY_CHECKLIST.md` vì lệnh đó gọi `GET /ask` ra 405 thay vì 401).
10. **Part 7 (Ex 7.3):** sửa `KNOWLEDGE_BASE` trong `06-lab-complete/benchmark-observability/develop/utils/mock_llm.py`, tắt rồi bật lại agent v2. Muốn stack `production/` cũng đạt 100% thì copy phần sửa sang `production/utils/mock_llm.py`.
11. **Part 7:** `load_test.py` và `run_eval.py` chỉ ghi JSON khi có `--out`. Agent v2 chạy cổng `8002` thì phải thêm `--url http://localhost:8002`. Stack Bước 2 dùng `-p k5-day14-observability`.

---

## 🛠️ 3. Checklist Chi Tiết Từng Checkpoint

---

### CP0 — Setup Môi Trường (0:00 → 0:10 · 10 phút)

- [x] Fork repo, đổi tên đúng mẫu `K5-L3B-DAY14-DoQuocKhanh-2A202603823-Deployment-Benchmark-Observability` và clone về máy.
- [x] Kiểm tra trên GitHub: repo đang ở chế độ **Public** (mở link ở cửa sổ ẩn danh không bị 404).
- [x] Mở terminal **WSL2** (Ubuntu/Linux, Docker Desktop bật tích hợp WSL2) và kiểm tra môi trường *(bắt buộc trước CP5 để chạy `check_production_ready.py` gửi được `SIGTERM`)*:
  ```bash
  python3 --version                        # Cần 3.11+
  python3 -c "import os; print(os.name)"   # BẮT BUỘC in: posix
  docker --version && docker compose version
  docker run --rm hello-world
  ```
- [x] Tạo file khung `MISSION_ANSWERS.md` ở gốc repo (có các mục Part 1 → Part 5, Part 6 output, và cuối file có mục `## AI log`).
- [x] Tạo thư mục `screenshots/` ở gốc repo để lưu sẵn 7 ảnh chụp sau này.

---

### CP1 — Part 1: Localhost vs Production (0:10 → 0:30 · 20 phút · 8 điểm)

**Thư mục:** `01-localhost-vs-production/`

- [x] **Exercise 1.1 (2 đ):** Đọc `01-localhost-vs-production/develop/app.py`, tìm và liệt kê **ít nhất 5 anti-patterns** (vd: hardcode API key, port cố định, debug mode cứng, không có health check, không xử lý graceful shutdown, log bằng `print()`, config không qua env...).
- [x] **Exercise 1.2 (2 đ):** Chạy bản `develop`:
  ```bash
  cd 01-localhost-vs-production/develop
  pip install -r requirements.txt
  python app.py
  # Terminal khác (LƯU Ý K5: truyền qua query param, không gửi JSON!)
  curl -X POST "http://localhost:8000/ask?question=Hello"
  ```
  - [x] Dán kết quả gọi thành công vào `MISSION_ANSWERS.md`.
  - [x] Tắt server (`Ctrl+C`) để giải phóng cổng 8000.
- [x] **Exercise 1.3 (4 đ):** Chạy bản `production`:
  ```bash
  cd ../production
  cp .env.example .env
  pip install -r requirements.txt
  python app.py
  ```
  - [x] So sánh `develop/app.py` và `production/app.py`.
  - [x] Điền bảng so sánh đầy đủ vào `MISSION_ANSWERS.md` (Config, Secrets, Port, Health check, Logging, Shutdown...) — **bắt buộc có cột giải thích TẠI SAO quan trọng** (kèm chỉ ra ít nhất 1 anti-pattern kèm dòng code đã sửa).
  - [x] Tắt server (`Ctrl+C`). **Không commit file `.env` vừa copy!**

---

### CP2 — Part 2: Docker Containerization (0:30 → 1:00 · 30 phút · 8 điểm)

**Thư mục:** `02-docker/` (Lưu ý K5: build Docker từ **gốc repo**!)

- [ ] **Exercise 2.1 (2 đ):** Đọc `02-docker/develop/Dockerfile` và trả lời 4 câu hỏi vào `MISSION_ANSWERS.md`:
  1. Base image là gì?
  2. Working directory là gì?
  3. Tại sao `COPY requirements.txt` đứng trước `COPY . .`? *(Docker layer cache)*
  4. `CMD` vs `ENTRYPOINT` khác nhau thế nào?
- [ ] **Exercise 2.2 (2 đ):** Build và chạy bản `develop` từ **gốc repo**:
  ```bash
  docker build -f 02-docker/develop/Dockerfile -t my-agent:develop .
  docker run --rm -d --name part2-dev -p 8000:8000 my-agent:develop
  curl -X POST "http://localhost:8000/ask?question=What%20is%20Docker"
  docker images my-agent:develop
  docker stop part2-dev
  ```
  - [ ] Dán kết quả test container + dung lượng image `my-agent:develop` (MB đo thật) vào `MISSION_ANSWERS.md`.
- [ ] **Exercise 2.3 (2 đ):** Đọc `02-docker/production/Dockerfile`, build bản multi-stage từ **gốc repo** và so sánh:
  ```bash
  docker build -f 02-docker/production/Dockerfile -t my-agent:advanced .
  docker images | grep my-agent
  ```
  - [ ] Trả lời Stage 1 làm gì, Stage 2 làm gì, vì sao image nhỏ hơn.
  - [ ] Ghi số MB đo thật của `develop` vs `production` và tính **% chênh lệch** vào `MISSION_ANSWERS.md`.
- [ ] **Exercise 2.4 (2 đ):** Đọc `02-docker/production/docker-compose.yml` và chạy stack:
  ```bash
  cd 02-docker/production
  touch .env.local
  docker compose -p k5-day14-docker up -d --build
  curl http://localhost/health
  curl -X POST http://localhost/ask -H "Content-Type: application/json" -d '{"question": "Explain microservices"}'
  docker compose -p k5-day14-docker down
  ```
  - [ ] Vẽ sơ đồ kiến trúc các service (`Client → Nginx → Agent → Redis/...`) và dán kết quả test qua Nginx vào `MISSION_ANSWERS.md`.

---

### CP3 — Part 4: API Security (1:00 → 1:25 · 25 phút · 8 điểm)

**Thư mục:** `04-api-gateway/` *(Lưu ý: CP3 làm Part 4 trước, Part 3 làm ở CP6!)*

- [x] **Exercise 4.1 (2 đ) — API Key (`develop/`):**
  - [x] Đọc `04-api-gateway/develop/app.py` và trả lời: API key được check ở đâu? Sai key trả gì? Làm sao rotate key?
  - [x] Chạy server và test (dùng `-i` để lấy HTTP status code):
    ```bash
    cd 04-api-gateway/develop
    pip install -r requirements.txt
    AGENT_API_KEY=secret-key-123 python app.py
    # Terminal khác:
    curl -i -X POST http://localhost:8000/ask -H "Content-Type: application/json" -d '{"question": "Hello"}'
    curl -i -X POST http://localhost:8000/ask -H "X-API-Key: secret-key-123" -H "Content-Type: application/json" -d '{"question": "Hello"}'
    ```
  - [x] Dán output `401` và `200` vào `MISSION_ANSWERS.md`, rồi tắt server (`Ctrl+C`).
- [x] **Exercise 4.2 (2 đ) — JWT Auth (`production/`):**
  - [x] Đọc `auth.py` (hiểu JWT flow).
  - [x] Chạy bản `production` và lấy token (**LƯU Ý K5: `/auth/token`, `student` / `demo123`**):
    ```bash
    cd ../production
    pip install -r requirements.txt
    python app.py
    # Terminal khác:
    TOKEN=$(curl -s -X POST http://localhost:8000/auth/token \
      -H "Content-Type: application/json" \
      -d '{"username": "student", "password": "demo123"}' \
      | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")
    curl -i -X POST http://localhost:8000/ask \
      -H "Authorization: Bearer $TOKEN" \
      -H "Content-Type: application/json" \
      -d '{"question": "Explain JWT"}'
    ```
  - [x] Dán output `200` vào `MISSION_ANSWERS.md` (**nhớ che token**).
- [x] **Exercise 4.3 (2 đ) — Rate Limiting (`production/`):**
  - [x] Đọc `rate_limiter.py` và trả lời: thuật toán nào được dùng? Limit bao nhiêu req/phút (10 req/phút cho `student`)? Làm sao bypass limit cho admin?
  - [x] Chạy vòng lặp 15–20 request bằng `$TOKEN` (có `-i`) để tự thấy mã **`429 Too Many Requests`**:
    ```bash
    for i in {1..15}; do
      echo "=== Request $i ==="
      curl -i -s -X POST http://localhost:8000/ask \
        -H "Authorization: Bearer $TOKEN" \
        -H "Content-Type: application/json" \
        -d "{\"question\": \"Test $i\"}" | head -n 5
    done
    ```
  - [x] Dán output thấy rõ chuyển từ `200` sang `429` vào `MISSION_ANSWERS.md` (che token), rồi tắt server (`Ctrl+C`).
- [x] **Exercise 4.4 (2 đ) — Cost Guard:**
  - [x] Đọc `cost_guard.py`, giải thích cách hoạt động của cost guard (dùng Redis theo user/tháng hoặc ngày, `INCRBYFLOAT`, TTL, trả `402` khi vượt) và vì sao cần cả Rate Limiting (bảo vệ tốc độ) lẫn Cost Guard (bảo vệ tiền) vào `MISSION_ANSWERS.md`.

---

### CP4 — Part 5: Scaling & Reliability (1:25 → 1:45 · 20 phút · 8 điểm)

**Thư mục:** `05-scaling-reliability/`

- [x] **Exercise 5.1 & 5.2 (4 đ) — Health/Readiness & Graceful Shutdown (`develop/`):**
  - [x] Đọc `05-scaling-reliability/develop/app.py`, giải thích sự khác biệt giữa Liveness (`/health`) và Readiness (`/ready`), và flow Graceful Shutdown (`SIGTERM` → `_is_ready=False` → chờ `_in_flight_requests == 0` → thoát).
  - [x] Chạy thử và test `GET /health`, `GET /ready` và gửi `POST /ask?question=hello` song song rồi `kill -SIGTERM <PID>` để xác nhận request vẫn trả `200 OK`:
    ```bash
    cd 05-scaling-reliability/develop
    pip install -r requirements.txt
    python app.py
    ```
  - [x] Ghi kết quả test và giải thích vào `MISSION_ANSWERS.md`, tắt server.
- [x] **Exercise 5.3, 5.4 & 5.5 (4 đ) — Stateless Design + Nginx LB (`production/`):**
  - [x] Giải thích vì sao lưu state trong RAM bị hỏng khi scale nhiều instance và cách Redis giải quyết.
  - [x] Chạy stack 3 instance với `-p k5-day14-scaling` (cổng **8080**, endpoint **`POST /chat`**):
    ```bash
    cd ../production
    touch .env.local
    docker compose -p k5-day14-scaling up -d --build --scale agent=3
    python test_stateless.py
    docker compose -p k5-day14-scaling logs agent | tail -n 30
    docker compose -p k5-day14-scaling down
    ```
  - [x] Dán output `test_stateless.py` (thấy request được phục vụ bởi các instance khác nhau nhưng session history vẫn còn nguyên trong Redis) + giải thích vào `MISSION_ANSWERS.md`.

---

### ☕ Nghỉ 5 phút (1:45 → 1:50)

---

### CP5 — Part 6: Final Project — Production-Ready AI Agent (1:50 → 2:50 · 60 phút · 60 điểm*)

> *50 điểm code/docker/security/reliability chấm tại đây + 10 điểm Deployment chấm ở CP6.  
> **Làm trực tiếp trong `06-lab-complete/`!** Chạy `python check_production_ready.py --static-only` và `--skip-docker` liên tục sau mỗi bước.

#### Bước chuẩn bị
- [x] Cài dependencies và chạy kiểm tra tĩnh lần đầu để thấy danh sách `❌`:
  ```bash
  cd 06-lab-complete
  pip install -r requirements.txt
  python check_production_ready.py --static-only
  ```

#### Hoàn thành 12 tiêu chí theo thứ tự gợi ý (khớp Hợp đồng trong `06-lab-complete/README.md` & `check_production_ready.py`)
- [x] **1. `app/config.py` + `.env.example` (Tiêu chí 9 — Config từ env):**
  - [x] Đọc từ biến môi trường (`os.getenv` / `Settings`): `AGENT_API_KEY`, `REDIS_URL`, `PORT`, `ENVIRONMENT`, `RATE_LIMIT_PER_MINUTE` (int), `DAILY_BUDGET_USD` (float) *(hỗ trợ thêm `MONTHLY_BUDGET_USD` nếu script truyền)*.
  - [x] `.env.example` liệt kê đủ: `AGENT_API_KEY`, `REDIS_URL`, `RATE_LIMIT_PER_MINUTE`, `DAILY_BUDGET_USD`, `PORT`, `ENVIRONMENT` (không ghi secret thật).
  - [x] Kiểm tra `.env` đã có trong `.gitignore` và không hardcode secret nào trong `app/`.
- [x] **2. Structured JSON Logging trong `app/main.py` (Tiêu chí 10):**
  - [x] Viết `JsonFormatter(logging.Formatter)` dùng `json.dumps({...})` (timestamp, level, message, extra...).
  - [x] Mọi dòng log của app phát ra phải là 1 JSON object hợp lệ (không in log lỗi format bắt đầu bằng `{`).
- [x] **3. `GET /health` trong `app/main.py` (Tiêu chí 4 — Liveness):**
  - [x] Luôn trả HTTP `200` khi process còn chạy, **kể cả khi không kết nối được Redis**.
- [x] **4. `app/redis_client.py` + `GET /ready` trong `app/main.py` (Tiêu chí 5 — Readiness):**
  - [x] Kết nối Redis theo `REDIS_URL`, có hàm `redis_healthy()` (ping Redis có timeout ngắn).
  - [x] `GET /ready` trả `200` khi Redis sống; trả **`503`** khi Redis không kết nối được.
- [x] **5. `app/auth.py` (Tiêu chí 6 — API Key Authentication):**
  - [x] Dùng `APIKeyHeader(name="X-API-Key", auto_error=False)`.
  - [x] Nếu thiếu hoặc khác `settings.agent_api_key` → `raise HTTPException(status_code=401, ...)`. *(Tránh trả 422 khi thiếu header!)*
- [x] **6. `app/rate_limiter.py` (Tiêu chí 7 — Rate Limiting & Stateless):**
  - [x] Sliding window 60 giây bằng Redis Sorted Set (`ZREMRANGEBYSCORE`, `ZCARD`, `ZADD`, `EXPIRE`).
  - [x] Vượt `RATE_LIMIT_PER_MINUTE` → `raise HTTPException(status_code=429, headers={"Retry-After": "60"}, ...)`.
  - [x] **Bắt buộc lưu trong Redis** (không lưu RAM) để khi `check_production_ready.py` restart agent, request tiếp theo vẫn trả `429`.
- [x] **7. `app/cost_guard.py` (Tiêu chí 8 — Cost Guard):**
  - [x] `check_budget()`: đọc tổng chi phí trong Redis, nếu `>=` ngân sách (`DAILY_BUDGET_USD` / `MONTHLY_BUDGET_USD`) → `raise HTTPException(status_code=402, ...)`.
  - [x] `record_cost(input_tokens, output_tokens)`: tính tiền theo giá per 1K tokens và cộng vào Redis bằng `INCRBYFLOAT` + set `EXPIRE`.
- [x] **8. Nối pipeline vào `POST /ask` trong `app/main.py` (Functional 15 đ):**
  - [x] Chấp nhận JSON `{"question": "..."}` (tùy chọn `user_id`), input sai trả mã lỗi rõ ràng (422), không lộ stack trace.
  - [x] Thứ tự thực thi: `Depends(verify_api_key)` → `check_rate_limit(api_key)` → `check_budget()` → gọi `mock_llm` → `record_cost(...)` → trả `200` + log JSON.
- [x] **9. Graceful Shutdown trong `app/main.py` (Tiêu chí 11):**
  - [x] Xử lý `lifespan` / `SIGTERM`: nếu tự đăng ký `signal.signal(signal.SIGTERM, ...)` thì **phải gọi lại handler cũ của uvicorn**, nếu không uvicorn sẽ không bao giờ tắt!
  - [x] Khi nhận `SIGTERM` lúc đang có request → request vẫn trả `200`, process thoát với exit code `0` (< 10 giây khi `docker stop`).
- [x] **10. `Dockerfile` + `.dockerignore` (Tiêu chí 1 & 3):**
  - [x] `Dockerfile`: multi-stage (≥ 2 lệnh `FROM`), stage cuối dùng base gọn (`python:3.11-slim`), chạy bằng user **non-root** (`USER appuser`), có `HEALTHCHECK`, kích thước image **< 500 MB**.
  - [x] `CMD`: chạy `exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000} --workers 2` (uvicorn là PID 1, lắng nghe theo biến `PORT`).
  - [x] Lưu ý: nếu `pip install --user` ở stage builder và copy sang `/home/<user>/.local`, nhớ đặt `ENV PYTHONUSERBASE=/home/<user>/.local` và `PATH`.
  - [x] Container phải khởi động và trả `/health` 200 được cả khi **chưa có Redis**.
  - [x] `.dockerignore`: loại trừ `.env`, `.env.*`, `__pycache__`, `venv`, `.venv`, `.git`...
- [x] **11. `docker-compose.yml` (Tiêu chí 2):**
  - [x] Service `agent` build từ `.` (`Dockerfile`), có `REDIS_URL=redis://redis:6379/0`, `depends_on: redis`, `env_file` (tùy chọn `required: false`).
  - [x] Service `redis` dùng `redis:7-alpine`, có `healthcheck`.
  - [x] Test chạy thử local: `docker compose -p k5-day14-final up --build -d`, kiểm tra `/health`, `/ready`, `/ask`, rồi `docker compose -p k5-day14-final down`.
- [x] **12. `railway.toml` và/hoặc `render.yaml` (Tiêu chí 12 — Public URL ready):**
  - [x] `railway.toml`: `builder = "DOCKERFILE"`, `healthcheckPath = "/health"`.
  - [x] `render.yaml`: `type: web`, `healthCheckPath: /health`, các secret (`AGENT_API_KEY`...) dùng `generateValue: true` hoặc `sync: false` (KHÔNG ghi `value:` thẳng).

#### Nghiệm thu CP5 (chạy trong WSL2, Docker Desktop đang bật)
- [x] Chạy bản đầy đủ (KHÔNG dùng `--skip-docker` hay `--static-only`):
  ```bash
  cd 06-lab-complete
  python check_production_ready.py
  ```
- [x] Đạt đúng **`PASS 12/12`** (không có bất kỳ dấu `❌` hay `⚠️` nào!).
- [x] Dán phần **"📋 Checklist Deliverable"** trong output của `check_production_ready.py` vào `MISSION_ANSWERS.md`.

---

### CP6 — Part 3 & Deploy Agent Part 6 Lên Cloud (2:50 → 3:15 · 25 phút · 8đ Part 3 + 10đ Part 6)

> Deploy trực tiếp thư mục `06-lab-complete/` lên **Railway** (Ex 3.1) **hoặc** **Render** (Ex 3.2).

- [ ] **Deploy Agent + Redis lên nền tảng chính (Railway hoặc Render):**
  - [ ] Nếu dùng **Railway**: cài CLI bằng `npm i -g @railway/cli` (cần Node.js), chạy trong `06-lab-complete/` (`railway login` → `railway init` → tạo thêm Redis service trong project Railway → set env vars `AGENT_API_KEY`, `REDIS_URL`, `RATE_LIMIT_PER_MINUTE`, `DAILY_BUDGET_USD`, `ENVIRONMENT=production` → `railway up` → `railway domain`).
  - [ ] Nếu dùng **Render**: lưu ý `render.yaml` nằm trong thư mục con `06-lab-complete/` và phải tự khai báo Redis (hoặc tạo Web Service với Root Directory = `06-lab-complete`, Runtime = Docker + tạo Render Redis, gắn `REDIS_URL`, `AGENT_API_KEY`, `RATE_LIMIT_PER_MINUTE`, `DAILY_BUDGET_USD`, `ENVIRONMENT=production`; kẹt thì hỏi Lab Coach).
  - [ ] **Bắt buộc kiểm `/ready` trả `200`** trước khi chụp ảnh (không dùng mục Self-Test của `DAY14_DELIVERY_CHECKLIST.md` vì mục đó gọi `GET /ask` ra 405).
- [ ] **Chạy 4 lệnh tự kiểm chuẩn CP6** (không lộ key):
  ```bash
  BASE="https://<your-public-domain>"
  AGENT_API_KEY="<your-cloud-api-key>"

  curl -sS -o /dev/null -w '%{http_code}\n' "$BASE/health"                                                                                 # 200
  curl -sS -o /dev/null -w '%{http_code}\n' "$BASE/ready"                                                                                  # 200
  curl -sS -o /dev/null -w '%{http_code}\n' -X POST "$BASE/ask" -H 'Content-Type: application/json' -d '{"question":"Hello"}'              # 401
  curl -sS -o /dev/null -w '%{http_code}\n' -X POST "$BASE/ask" -H 'Content-Type: application/json' -H "X-API-Key: $AGENT_API_KEY" -d '{"question":"Hello"}'   # 200
  ```
- [ ] Chạy kiểm tra thêm với script chấm (tùy chọn xác nhận):
  ```bash
  python check_production_ready.py --public-url "$BASE" --static-only
  ```
- [ ] **Chụp đủ 3 ảnh deploy** lưu vào `screenshots/`:
  - [ ] `screenshots/dashboard.png` (dashboard Railway/Render thấy service + Redis + env vars đã che giá trị)
  - [ ] `screenshots/running.png` (trạng thái service đang Active/Running + logs khỏe mạnh)
  - [ ] `screenshots/test.png` (kết quả chạy 4 lệnh test trên: `200`, `200`, `401`, `200` không lộ key)
- [ ] **Tạo file `DEPLOYMENT.md`** ở gốc repo theo mẫu mục 3 của `DAY14_DELIVERY_CHECKLIST.md`:
  - [ ] Public URL đang hoạt động
  - [ ] Nền tảng sử dụng (Railway / Render)
  - [ ] Các lệnh test (`/health`, `/ready`, `/ask` không key & có key — dùng placeholder `YOUR_KEY`, không ghi key thật!)
  - [ ] Danh sách tên biến môi trường đã đặt trên cloud (không ghi giá trị bí mật)
  - [ ] Link tới 3 ảnh trong `screenshots/`
- [ ] **Hoàn thiện mục Part 3 trong `MISSION_ANSWERS.md` để lấy trọn 8/8 điểm:**
  - [ ] Điền URL public và link ảnh deploy (4 đ).
  - [ ] **So sánh `railway.toml` vs `render.yaml`** (khác nhau chỗ nào, vì sao — hoặc deploy thêm nền tảng kia) (3 đ).
  - [ ] **Exercise 3.3 — Cloud Run (1 đ):** Đọc `03-cloud-deployment/production-cloud-run/cloudbuild.yaml` và `service.yaml`, viết **3–5 dòng** mô tả pipeline CI/CD đi qua những bước nào *(không cần tài khoản GCP / không cần deploy)*.

---

### CP7 — Part 7 Bước 1: Benchmark Local (3:15 → 4:00 · 45 phút · 9 điểm)

**Thư mục:** `06-lab-complete/benchmark-observability/develop/`

- [ ] **Bước 0 — Khởi tạo `BENCHMARK_REPORT.md` ở gốc repo (chỉ chạy 1 lần):**
  ```bash
  cp -n 06-lab-complete/benchmark-observability/BENCHMARK_REPORT_TEMPLATE.md BENCHMARK_REPORT.md
  ```
  - [ ] Điền thông tin đầu trang (Họ tên, Ngày chạy, Môi trường — KHÔNG ghi email/SĐT) và Mục 1 (SLO của agent + lý do chọn ngưỡng).
- [ ] **Exercise 7.1 — Đọc metrics & Thêm metric:**
  - [ ] Cài dependencies và bật 2 terminal:
    ```bash
    cd 06-lab-complete/benchmark-observability/develop
    pip install -r requirements.txt
    # Terminal 1: AGENT_VERSION=v1 PORT=8001 MOCK_ERROR_RATE=0 python app.py
    # Terminal 2: AGENT_VERSION=v2 PORT=8002 python app.py
    ```
  - [ ] Gọi `POST http://localhost:8002/ask` và đọc `/metrics`.
  - [ ] Tìm 1 ví dụ cho mỗi loại: Counter, Gauge, Histogram; giải thích vì sao dùng `route.path` thay vì `request.url.path` (tránh bùng nổ cardinality).
  - [ ] Thêm Histogram `agent_question_length_chars` vào `develop/app.py` (đo độ dài `len(body.question)` trước khi gọi LLM) và kiểm tra xuất hiện ở `/metrics`.
- [ ] **Exercise 7.2 (4 đ) — Load test & Tail latency (lưu đủ 7 file JSON vào `develop/reports/`):**
  - [ ] Chạy 4 mức concurrency trên agent v2 (cổng 8002):
    ```bash
    for c in 1 10 50 100; do
      python load_test.py --url http://localhost:8002 --requests 300 --concurrency "$c" --out "reports/load_v2_c${c}.json"
    done
    ```
  - [ ] Khởi động lại agent v2 lần lượt với `MOCK_SLOW_RATE=0`, `0.03` (mặc định), `0.1` rồi chạy cùng `--requests 300 --concurrency 20`:
    ```bash
    # Lần 1: MOCK_SLOW_RATE=0 AGENT_VERSION=v2 PORT=8002 python app.py
    python load_test.py --url http://localhost:8002 --requests 300 --concurrency 20 --out reports/load_v2_slow_0.json
    # Lần 2: MOCK_SLOW_RATE=0.03 AGENT_VERSION=v2 PORT=8002 python app.py
    python load_test.py --url http://localhost:8002 --requests 300 --concurrency 20 --out reports/load_v2_slow_0.03.json
    # Lần 3: MOCK_SLOW_RATE=0.1 AGENT_VERSION=v2 PORT=8002 python app.py
    python load_test.py --url http://localhost:8002 --requests 300 --concurrency 20 --out reports/load_v2_slow_0.1.json
    ```
  - [ ] Điền Mục 2.1 và 2.2 của `BENCHMARK_REPORT.md` khớp 100% với 7 file JSON; giải thích vì sao RPS không tăng tuyến tính và vì sao SLO đặt theo p95/p99 thay vì average.
- [ ] **Exercise 7.3 (5 đ) — Eval & Quality Gate (lưu đủ 3 file JSON vào `develop/reports/`):**
  - [ ] Bật lại v1 (cổng 8001) và v2 (cổng 8002) với `MOCK_ERROR_RATE=0` để eval ổn định.
  - [ ] Chạy eval ban đầu cho v1 và v2:
    ```bash
    python eval/run_eval.py --url http://localhost:8001 --out reports/eval_v1.json
    python eval/run_eval.py --url http://localhost:8002 --out reports/eval_v2.json --baseline reports/eval_v1.json
    ```
  - [ ] Đọc `missing_keywords` của 2 câu sai (`scaling-03`, `security-02`) trong `reports/eval_v2.json`.
  - [ ] Thêm kiến thức còn thiếu vào `KNOWLEDGE_BASE` trong `06-lab-complete/benchmark-observability/develop/utils/mock_llm.py` *(KHÔNG sửa `golden_dataset.jsonl`!)*.
  - [ ] Tắt và bật lại agent v2 (`AGENT_VERSION=v2 PORT=8002 MOCK_ERROR_RATE=0 python app.py`), chạy lại eval chất lượng:
    ```bash
    python eval/run_eval.py --url http://localhost:8002 --min-accuracy 1.0 --baseline reports/eval_v2.json --out reports/eval_v2_fixed.json
    ```
  - [ ] Xác nhận output in **`23/23` (100%)**, **0 regression**, **`Quality gate ... ✅ PASS`**.
  - [ ] *(Tùy chọn nên làm)* Chép phần đã sửa sang `06-lab-complete/benchmark-observability/production/utils/mock_llm.py`.
  - [ ] Viết job CI GitHub Actions (`.github/workflows/eval.yml` hoặc dán + giải thích trong báo cáo) dùng exit code của `run_eval.py` để chặn merge PR khi accuracy < 85% hoặc có regression.
  - [ ] Điền Mục 3 của `BENCHMARK_REPORT.md` khớp 100% với `eval_v1.json`, `eval_v2.json`, `eval_v2_fixed.json` (có `cost / câu đúng` và phân tích trade-off).
  - [ ] Tắt 2 server local (8001, 8002) khi xong CP7.

---

### CP8 — Part 7 Bước 2: Observability Stack, Tracing, Alerts & Scaling (Sau giờ lab, trước deadline · 11 điểm)

**Thư mục:** `06-lab-complete/benchmark-observability/production/`  
*(Luôn dùng `-p k5-day14-observability` cho mọi lệnh `docker compose`!)*

- [ ] **Chuẩn bị & Bật stack:**
  ```bash
  cd 06-lab-complete/benchmark-observability/production
  cp -n .env.example .env
  chmod 777 benchmark-results 2>/dev/null || true   # tránh lỗi Permission denied của Locust
  docker compose -p k5-day14-observability up -d --build
  docker compose -p k5-day14-observability ps
  ```
  - [ ] Truy cập kiểm tra các UI:
    - Grafana: `http://localhost:3000` (`admin`/`admin` → Dashboard **Day 14 — AI Agent Overview**)
    - Prometheus: `http://localhost:9090` (*Target health* có target `agent` trạng thái `UP`, xem tab *Alerts*)
    - Jaeger: `http://localhost:16686` (Service `observable-agent`)
    - Locust: `http://localhost:8089`
- [ ] **Exercise 7.4 (4 đ) — Observability Stack & Grafana:**
  - [ ] Mở Locust (`http://localhost:8089`), chạy tải **30 users / ramp up 5** (đợi ~1–2 phút để Grafana vẽ đầy đủ).
  - [ ] Chụp màn hình dashboard Grafana đang có traffic → lưu thành `screenshots/grafana-dashboard.png`.
  - [ ] Kiểm tra `curl -i http://localhost:8080/metrics` (xác nhận trả `404` vì Nginx chặn không public `/metrics`).
  - [ ] Trả lời 4 câu hỏi của Exercise 7.4 (p95 vs avg, phân bố traffic giữa các instance, vì sao input tokens/s > output tokens/s, vì sao `/metrics` bị chặn ở Nginx) vào `BENCHMARK_REPORT.md` (hoặc `MISSION_ANSWERS.md`).
- [ ] **Exercise 7.5 (3 đ) — Distributed Tracing (Jaeger + JSON log):**
  - [ ] Mở Jaeger → Service `observable-agent` → **Find Traces** → sắp xếp **Longest First** → mở trace chậm nhất.
  - [ ] Chụp màn hình trace chậm (thấy rõ span chậm nhất, thường là `chat mock-llm-*`, kèm số ms) → lưu thành `screenshots/jaeger-slow-trace.png`.
  - [ ] Tìm trace lỗi (Tags `error=true`), mở xem event `exception` → chụp màn hình lưu thành `screenshots/jaeger-error-trace.png`.
  - [ ] Lấy dòng log JSON tương ứng cùng `trace_id`:
    ```bash
    docker compose -p k5-day14-observability logs agent | grep <trace_id_hoặc_llm_error> | head -n 5
    ```
  - [ ] Điền Mục 4.3 của `BENCHMARK_REPORT.md` (`trace_id`, tổng thời gian ms, span chậm nhất + ms + %, và dán đúng dòng log JSON khớp `trace_id`).
- [ ] **Exercise 7.6 (4 đ) — Unit test Alerts & Thí nghiệm "Phá hệ thống":**
  - [ ] Chạy unit test cho alert rules:
    ```bash
    docker run --rm -v "$PWD/prometheus:/p" --entrypoint promtool \
      prom/prometheus:v3.16.0 test rules /p/alert_rules_test.yml
    ```
  - [ ] Làm **ít nhất 2 thí nghiệm** (khuyến nghị làm để **cả 2 alert cùng firing** cùng lúc, ví dụ đặt đồng thời `MOCK_ERROR_RATE=0.2` và `LLM_MODEL=mock-llm-large` hoặc `MOCK_SLOW_RATE=0.3` trong `.env` → `docker compose -p k5-day14-observability up -d`, giữ Locust chạy 30 users, chờ 1–3 phút).
  - [ ] Ghi lại thời gian chính xác từ lúc đổi cấu hình tới lúc từng alert chuyển từ `pending` → `firing`.
  - [ ] Chụp **1 ảnh trang Alerts của Prometheus thấy ≥ 2 alert cùng đang FIRING** → lưu thành `screenshots/prometheus-alert-firing.png`.
  - [ ] Trả `.env` về mặc định (và `docker unpause` nếu làm thí nghiệm D) rồi `docker compose -p k5-day14-observability up -d`.
  - [ ] Điền Mục 4.2 của `BENCHMARK_REPORT.md`, **bắt buộc trả lời câu hỏi thí nghiệm E** (`AGENT_VERSION=v1` không làm alert hạ tầng nào firing → phát hiện trong production bằng cách nào: eval trong CI, online eval / LLM-as-judge, user feedback, theo dõi retrieval hit ratio...).
- [ ] **Benchmark Scaling (Locust headless — lưu CSV):**
  - [ ] Chạy đủ 2 mức `agent=1` và `agent=3` (dừng tải Locust Web UI trước khi chạy headless):
    ```bash
    docker compose -p k5-day14-observability up -d --build --scale agent=1
    sleep 15
    docker compose -p k5-day14-observability run --rm locust -f /mnt/locust/locustfile.py --host http://nginx \
      --headless -u 100 -r 10 -t 2m --csv /mnt/results/scale_1

    docker compose -p k5-day14-observability up -d --scale agent=3
    sleep 15
    docker compose -p k5-day14-observability run --rm locust -f /mnt/locust/locustfile.py --host http://nginx \
      --headless -u 100 -r 10 -t 2m --csv /mnt/results/scale_3
    ```
  - [ ] Điền Mục 5 (`scale_1_stats.csv` vs `scale_3_stats.csv`) và Mục 6 (Kết luận) trong `BENCHMARK_REPORT.md`. Giải thích nút thắt nếu scale lên 3 mà p95 ít đổi (do latency của LLM upstream).
- [ ] **Dọn dẹp Docker stack sau khi đã chụp đủ ảnh và chép đủ log:**
  ```bash
  docker compose -p k5-day14-observability down -v
  ```
- [ ] **Copy file bằng chứng JSON & CSV ra thư mục gốc repo (từ gốc repo):**
  ```bash
  mkdir -p reports benchmark-results
  cp -r 06-lab-complete/benchmark-observability/develop/reports/. reports/
  cp -r 06-lab-complete/benchmark-observability/production/benchmark-results/. benchmark-results/
  ```

---

## 📦 4. Checklist Đóng Gói & Tự Kiểm Tra Trước Khi Nộp Bài (`SUBMISSION.md`)

### Kiểm tra đủ cây thư mục bắt buộc ở gốc repo
```text
K5-L3B-DAY14-DoQuocKhanh-2A202603823-Deployment-Benchmark-Observability/
├── MISSION_ANSWERS.md          # Part 1–5 + output check_production_ready.py + AI log
├── DEPLOYMENT.md               # URL public, lệnh test, tên env vars, 3 ảnh deploy
├── BENCHMARK_REPORT.md         # Điền đủ 6 mục, số liệu khớp 100% JSON/CSV
├── reports/
│   ├── load_v2_c1.json
│   ├── load_v2_c10.json
│   ├── load_v2_c50.json
│   ├── load_v2_c100.json
│   ├── load_v2_slow_0.json
│   ├── load_v2_slow_0.03.json
│   ├── load_v2_slow_0.1.json
│   ├── eval_v1.json
│   ├── eval_v2.json
│   └── eval_v2_fixed.json
├── benchmark-results/
│   ├── scale_1_stats.csv
│   └── scale_3_stats.csv
├── screenshots/
│   ├── dashboard.png
│   ├── running.png
│   ├── test.png
│   ├── grafana-dashboard.png
│   ├── jaeger-slow-trace.png
│   ├── jaeger-error-trace.png
│   └── prometheus-alert-firing.png
└── 06-lab-complete/            # Code hoàn chỉnh, PASS 12/12
```

### Checklist rà soát cuối cùng (100% phải tick trước khi push & nộp LMS)
- [ ] **Tên repo & Quyền truy cập:** Đúng `K5-L3B-DAY14-DoQuocKhanh-2A202603823-Deployment-Benchmark-Observability`, để **Public**, mở thử bằng cửa sổ ẩn danh không bị 404.
- [ ] **Part 6 Pass 12/12:** Trong WSL2, chạy `cd 06-lab-complete && python check_production_ready.py` báo **`PASS 12/12`** (không có `❌` hay `⚠️`).
- [ ] **Không sửa file cấm:** `git diff -- 06-lab-complete/check_production_ready.py 06-lab-complete/benchmark-observability/develop/eval/golden_dataset.jsonl` không in gì.
- [ ] **MISSION_ANSWERS.md:** Đủ Part 1, 2, 3 (có so sánh `railway.toml`/`render.yaml` + 3–5 dòng Cloud Run), 4 (output `401/200/429` đã che token), 5 (test stateless), dán output `check_production_ready.py`, và có mục **AI log** ở cuối file.
- [ ] **DEPLOYMENT.md & Public URL sống:** Chạy lại 4 lệnh CP6 trên URL public trước khi nộp → ra đúng `200`, `200`, `401`, `200`.
- [ ] **BENCHMARK_REPORT.md & Bằng chứng:** Đủ 10 file JSON trong `reports/`, đủ 2 file CSV trong `benchmark-results/`, đủ 7 ảnh trong `screenshots/`; đối chiếu lại từng con số trong bảng với file JSON/CSV khớp tuyệt đối.
- [ ] **Kiểm tra rò rỉ Secret & Thông tin cá nhân:**
  ```bash
  git status                                               # Đảm bảo không có .env / .env.local được track
  git log --all --oneline -- '*.env' '.env' '*.env.local'  # PHẢI TRỐNG (không in gì)
  ```
  - [ ] Đã xóa/không ghi email, số điện thoại, API key thật, JWT token thật trong toàn bộ bài làm.
- [ ] **Dọn dẹp Docker:** Đã chạy `down -v` cho các stack (`k5-day14-docker`, `k5-day14-scaling`, `k5-day14-final`, `k5-day14-observability`).
- [ ] **Commit, Push & Nộp bài:** Commit rõ ràng, `git push origin main` trước **23h59 (GMT+7)**, và nộp **link GitHub repo** trên LMS (không nộp file zip).
