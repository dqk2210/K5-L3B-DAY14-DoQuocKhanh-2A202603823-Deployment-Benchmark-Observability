# Benchmark & Observability Report — Day 14

> Copy file này thành `BENCHMARK_REPORT.md` trong repo của bạn và điền đầy đủ.
> Mọi con số phải lấy từ report JSON / CSV / screenshot thật, không ước lượng.

**Họ tên:** Đỗ Quốc Khánh (MSSV: 2A202603823)
**Ngày chạy:** 2026-11-27
**Môi trường:** Windows 11 + WSL2 Ubuntu 26.04.1 LTS + Docker Desktop 29.9.3

---

## 1. SLO của agent

| SLI | SLO | Lý do chọn ngưỡng này |
|---|---|---|
| p95 latency `/ask` | < 500 ms | 95% người dùng nhận phản hồi dưới 0.5 giây (khớp `--slo-p95-ms 500`), đủ nhanh cho trải nghiệm chat realtime |
| Error rate `/ask` | < 2 % | Cho phép error budget 2% để dung sai lỗi upstream ngẫu nhiên (~1%), tránh cảnh báo giả khi có spike nhỏ |
| Accuracy trên golden dataset | ≥ 85 % | Ngưỡng quality gate tối thiểu trong CI (`.github/workflows/eval.yml`) để chặn deploy khi chất lượng giảm |

---

## 2. Benchmark hiệu năng (develop, `load_test.py`)

### 2.1 Concurrency vs latency (agent v2)

| Concurrency | RPS | p50 (ms) | p95 (ms) | p99 (ms) | Error rate | SLO |
|---|---|---|---|---|---|---|
| 1 | 4.4 | 187.2 | 218.3 | 1681.6 | 1.00% | PASS |
| 10 | 41.44 | 190.6 | 220.2 | 1701.7 | 0.67% | PASS |
| 50 | 106.99 | 193.2 | 238.9 | 1698.8 | 1.00% | PASS |
| 100 | 70.36 | 311.9 | 2555.7 | 3450.6 | 0.33% | FAIL |

**Nhận xét:** RPS **không** tăng tuyến tính theo concurrency. Từ concurrency 1 → 10 → 50, throughput tăng mạnh (4.4 → 41.44 → 106.99 req/s) vì I/O bất đồng bộ xử lý song song tốt. Nhưng khi tăng lên 100 kết nối đồng thời trên 1 process uvicorn, event loop và CPU bắt đầu bão hòa nên RPS tụt xuống còn `70.36 req/s`, đồng thời p95 nhảy vọt từ `238.9 ms` lên `2555.7 ms` (vi phạm SLO ≤ 500 ms).

### 2.2 Tail latency

| `MOCK_SLOW_RATE` | avg (ms) | p95 (ms) | p99 (ms) |
|---|---|---|---|
| 0 | 189.7 | 218.5 | 226.2 |
| 0.03 (mặc định) | 254.8 | 224.7 | 1708.9 |
| 0.1 | 396.1 | 1698.5 | 1714.0 |

**Nhận xét:** **p99** (và **p95** khi tỉ lệ chậm vượt 5%, như ở mức `0.1`) nhạy nhất với request chậm bất thường. Ở `MOCK_SLOW_RATE=0.03`, `avg` chỉ tăng từ `189.7 ms` lên `254.8 ms` (+65 ms) nhưng `p99` nhảy vọt hơn 7 lần lên `1708.9 ms`; ở `0.1`, `avg` mới là `396.1 ms` (vẫn dưới 500 ms!) trong khi cả `p95` đã vọt lên `1698.5 ms`. Vì trung bình bị che giấu bởi đa số request nhanh, SLO phải đặt theo **p95/p99** để bảo vệ trải nghiệm thật của nhóm người dùng bị chậm.

---

## 3. Benchmark chất lượng (develop, `eval/run_eval.py`)

| Chỉ số | Agent v1 | Agent v2 | Agent v2 (sau khi sửa KB) |
|---|---|---|---|
| Accuracy | 4.3% (1/23) | 91.3% (21/23) | 100.0% (23/23) |
| Avg tokens / câu | 57.3 | 109.0 | 113.7 |
| Tổng cost (USD) | $0.000407 | $0.000760 | $0.000790 |
| Cost / câu đúng (USD) | $0.00040695 | $0.00003619 | $0.00003436 |
| Quality gate | FAIL | PASS (≥ 80%) | PASS (`100.0% ≥ 80%`, 0 regression) |

**Những câu v2 trả lời sai ban đầu và cách bạn sửa:**

| ID | Keyword bị thiếu | Bạn đã sửa gì |
|---|---|---|
| `security-02` | `token`, `hết hạn`, `chữ ký` | Thêm entry `(["jwt"], ...)` giải thích JWT là token có chữ ký số, chứa thời điểm hết hạn vào `KNOWLEDGE_BASE` trong `develop/utils/mock_llm.py` (và đồng bộ sang `production/utils/mock_llm.py`) |
| `scaling-03` | `cpu`, `memory`, `custom metrics` | Thêm entry `(["hpa", "kubernetes", "autoscal"], ...)` mô tả Kubernetes HPA scale pod theo CPU, memory hoặc custom metrics vào `KNOWLEDGE_BASE` |

**Nhận xét về trade-off chất lượng / chi phí / latency giữa v1 và v2:**
- Agent v2 (có RAG/retrieval) tốn gần gấp đôi token trung bình mỗi câu (`109.0`–`113.7` so với `57.3` của v1) và tổng cost tăng gần gấp đôi (`$0.000760`–`$0.000790` so với `$0.000407`), đồng thời latency p50 tăng nhẹ (`191.7`–`203.2 ms` so với `183.5 ms`) do thêm bước tìm kiếm tài liệu.
- Đổi lại, độ chính xác nhảy từ `4.3%` lên `91.3%` → `100.0%`, khiến **cost / câu trả lời đúng** giảm hơn **11 lần** (`$0.00003436` so với `$0.00040695`).
- **Quality gate trong CI (`.github/workflows/eval.yml`):** Tự động chạy `python eval/run_eval.py --url http://localhost:8000 --baseline ../../../reports/eval_v2.json --min-accuracy 0.85`; vì `run_eval.py` trả exit code `1` khi accuracy < ngưỡng hoặc có regression so với baseline, GitHub Actions sẽ làm fail job và chặn merge PR.

---

## 4. Observability stack (production)

### 4.1 Screenshot

- [x] Dashboard Grafana khi đang có tải (thấy rõ Golden Signals) → `screenshots/grafana-dashboard.png`
- [x] Một trace chậm trong Jaeger (thấy span nào chiếm thời gian) → `screenshots/jaeger-slow-trace.png`
- [x] Một trace lỗi trong Jaeger (có event `exception`) → `screenshots/jaeger-error-trace.png`
- [x] Trang Alerts của Prometheus với ít nhất 1 alert đang **firing** (mục tiêu ≥ 2 alert cùng firing: `LLMCostBurnRateHigh`, `AgentHighErrorRate`, `AgentHighLatencyP95`) → `screenshots/prometheus-alert-firing.png`

> Unit test alert rules (`promtool test rules /p/alert_rules_test.yml`): **`SUCCESS`** (tất cả test case đạt).

### 4.2 Thí nghiệm "phá hệ thống"

*(Chạy với tải Locust 30 users, ramp up 5 trong ~4.5 phút; `scrape_interval: 5s`, `evaluation_interval: 5s`.)*

| # | Thay đổi | Alert nào firing | Thời gian từ lúc đổi → firing | Panel nào phản ánh rõ nhất |
|---|---|---|---|---|
| A | `MOCK_ERROR_RATE=0.2` | `AgentHighErrorRate` (`for: 1m`) | **`82.2 s`** (~22.2s sang `pending` với rate 15–20%, cộng `for: 1m`) | **Error rate**, **Requests/s theo status code**, **LLM calls theo kết quả** |
| B | `MOCK_SLOW_RATE=0.3` | `AgentHighLatencyP95` (`for: 2m`) | **`152.3 s`** (~32.2s sang `pending` với p95 ~`1.93 s`, cộng `for: 2m`) | **Latency p95**, **Latency /ask — p50 / p95 / p99**, **LLM latency p95 theo model** |
| C | `LLM_MODEL=mock-llm-large` | `LLMCostBurnRateHigh` (`for: 2m`) | Đã firing sẵn ở mức `$3.12/h` từ test `scale_3` (`t=2.1s`), tăng vọt từ `$2.87/h` lên **`$17.27/h`** khi traffic chạy `mock-llm-large` (từ sạch sẽ cần ~2 phút theo ngưỡng `for: 2m`) | **Cost burn rate (USD/giờ)**, **LLM cost (1h)**, **LLM latency p95 theo model** |
| D | `docker pause` 1 instance (`k5-day14-observability-agent-1`) | `AgentInstanceDown` (`for: 30s`) | **`50.2 s`** kể từ lúc pause (`20.1s` sang `pending` khi `up == 0`, cộng `for: 30s`) | **Instances up** (giảm từ 2 → 1), **Requests/s theo instance** |
| E | `AGENT_VERSION=v1` | **Không có alert nào firing** từ `v1` (`error_rate = 0.75%`, `p95 = 198 ms`) | — | **Retrieval hit ratio (agent v2)** (về `0`), **Tokens/s** (`input=285.0`, `output=158.1`, giảm mạnh), **Phiên bản đang chạy** |

**Thí nghiệm E không làm alert nào firing. Bạn sẽ phát hiện loại sự cố này trong production bằng cách nào?**

- Các metric hạ tầng (RPS, 5xx error rate, p95 latency, instance up) hoàn toàn "xanh" vì `agent v1` vẫn trả HTTP `200 OK` rất nhanh (`198 ms`), nhưng chất lượng câu trả lời đã sụt từ `100%` (`v2`) xuống `4.3%` (`v1`) do không dùng RAG.
- Để phát hiện regression chất lượng trong production cần kết hợp:
  1. **Eval quality gate trong CI/CD** (`.github/workflows/eval.yml` chạy `eval/run_eval.py --baseline` trước khi deploy để chặn bản `v1` hoặc bản giảm accuracy).
  2. **Theo dõi metric chất lượng/nghiệp vụ trên Grafana**: bổ sung alert cho **`Retrieval hit ratio`** tụt bất thường về 0, **`Phiên bản đang chạy`** đổi ngoài ý muốn, hoặc `Tokens/s` tụt đột ngột.
  3. **Online evaluation & feedback người dùng**: chấm mẫu ngẫu nhiên câu trả lời production bằng LLM-as-a-judge theo golden/rubric và thu thập nút 👍/👎 từ người dùng.

### 4.3 Debug bằng trace

Chọn 1 trace chậm nhất bạn tìm được (mẫu trace lỗi tham khảo thêm trong Jaeger: `e8848e4cb5e4693e0039ee435e56c75f` với event `exception` và `event: "llm_error"`):

- `trace_id`: `a2ea87fa8828bfca9596eaa4ce9442ae`
- Tổng thời gian: `1702.78` ms (span gốc `POST /ask`)
- Span chiếm nhiều thời gian nhất: `chat mock-llm-small` (`1677.93` ms, `98.5%` tổng thời gian; nằm trong `agent.run` `1698.98` ms / `99.8%`, trong khi `agent.retrieve_context` chỉ mất `20.58` ms / `1.2%`)
- Dòng log tương ứng (grep theo `trace_id`):

```json
{"ts": "2026-11-26T17:48:04.091676+00:00", "level": "INFO", "service": "observable-agent", "instance": "4825ef76af42", "event": "llm_call", "trace_id": "a2ea87fa8828bfca9596eaa4ce9442ae", "span_id": "90109e9eb553ef8b", "request_id": "e987710d50d1", "model": "mock-llm-small", "agent_version": "v2", "input_tokens": 74, "output_tokens": 37, "cost_usd": 3.3e-05, "llm_ms": 1678.4}
```

### 4.4 Quan sát Grafana & câu hỏi Exercise 7.4

1. **p95 vs avg khác nhau thế nào?** Trên cửa sổ 5 phút sau benchmark, `avg = 234.2 ms` còn `p95 = 294.7 ms` (cao hơn ~26%), và ở p99 lên tới `1700 ms`. `avg` bị làm mượt bởi phần lớn request bình thường, nên chỉ nhìn `avg` sẽ che khuất tail latency mà 1–5% người dùng phải chịu.
2. **Traffic có chia đều giữa các instance không?** Có — khi gọi `POST /ask` nhiều lần qua Nginx, header `X-Served-By` luân phiên giữa `172.19.0.6:8000` và `172.19.0.7:8000`, và Prometheus đo được RPS hai instance gần như bằng nhau (`24.08 req/s` vs `23.88 req/s`).
3. **Vì sao Input tokens/giây lớn hơn Output tokens/giây?** Vì ở `v2`, mỗi lần gọi LLM đều gửi kèm system prompt + ngữ cảnh RAG tìm được ở bước `agent.retrieve_context`, làm lượng input token lớn hơn đáng kể so với câu trả lời đầu ra (`3676.0` input tokens/s vs `1920.5` output tokens/s khi có tải).
4. **Vì sao `curl -i http://localhost:8080/metrics` trả `404`?** Trong `production/nginx/nginx.conf`, rule `location = /metrics { return 404; }` chặn `/metrics` không cho truy cập từ bên ngoài để tránh rò rỉ dữ liệu vận hành (route, RPS, chi phí, version); chỉ Prometheus nội bộ mới scrape trực tiếp `agent:8000/metrics`.

---

## 5. Benchmark scaling (production, Locust headless, 100 users, 2 phút)

Số liệu dưới đây trích nguyên văn từ `benchmark-results/scale_1_stats.csv` và `benchmark-results/scale_3_stats.csv` cho endpoint nghiệp vụ `POST /ask` (kèm dòng `Aggregated` gồm cả `GET /health` để đối chiếu):

| Số instance | RPS (`POST /ask`) | p50 (ms) | p95 (ms) | p99 (ms) | Failures |
|---|---|---|---|---|---|
| 1 | `59.41` (`65.21` Aggregated) | `200` (`190` Agg) | `260` | `1700` | `83 / 7050` (`1.18%`; `83 / 7738` = `1.07%` Agg) |
| 3 | `60.04` (`65.85` Aggregated) | `190` (`190` Agg) | `250` (`240` Agg) | `1700` | `73 / 7129` (`1.02%`; `73 / 7820` = `0.93%` Agg) |

**Giải thích kết quả:** Scale có cải thiện p95 không? Nút thắt nằm ở đâu?

- Scale từ 1 lên 3 instance gần như **không cải thiện p95 (`260 ms` → `250 ms`), p99 (`1700 ms` giữ nguyên) hay RPS (`59.41` → `60.04 req/s`)**.
- **Nút thắt không nằm ở CPU của agent container** mà nằm ở:
  1. **Latency của LLM upstream** (`chat mock-llm-small` chiếm ~98.5% thời gian request bình thường và ~1.7s ở slow request); dù tăng thêm bản sao agent, mỗi request vẫn phải chờ LLM xử lý từng đó thời gian nên p95/p99 gần như cố định.
  2. **FastAPI xử lý I/O bất đồng bộ (`async/await`)** nên 1 instance đã phục vụ dư 100 Locust user (`wait_time` `between(0.5, 2)` giây tạo tối đa ~65 req/s), chưa bị bão hòa CPU hay event loop.
- Scale ngang nhiều replica vẫn có giá trị quan trọng về **High Availability (chịu lỗi khi 1 instance chết/pause)** và khi số user thực tế đủ lớn làm CPU/connection của 1 instance bão hòa.

---

## 6. Kết luận

- 3 điều bạn học được về benchmark & observability:
  1. **Golden Signals + Tail Latency (p95/p99) quan trọng hơn average:** Một hệ thống có `avg ~234 ms` vẫn có thể khiến 1–5% người dùng chờ `1700 ms` hoặc nhận lỗi ngầm (`504` từ Nginx hoặc tụt chất lượng ở `v1` dù `/health` vẫn `200`).
  2. **Logs + Metrics + Traces bổ trợ nhau qua `trace_id`:** Metric cho biết *hệ thống đang bất thường lúc nào* (Grafana/Prometheus), Trace cho biết *chậm hoặc lỗi ở span nào* (Jaeger thấy `98.5%` nằm ở LLM call), và Log JSON gắn `trace_id` cho biết *chi tiết ngữ cảnh của đúng request đó*.
  3. **Observability hạ tầng không thay thế được Eval chất lượng AI:** Metric hạ tầng không bắt được lỗi suy giảm accuracy (`v1` đạt `4.3%` nhưng mọi panel kỹ thuật đều xanh), nên bắt buộc phải có `eval/run_eval.py` làm quality gate trong CI và chỉ số `cost / câu trả lời đúng`.
- Nếu đưa agent này lên production thật, bạn sẽ thêm metric / alert nào nữa?
  1. **Metric & Alert cho chất lượng + nghiệp vụ AI:** `agent_retrieval_hit_ratio` (alert nếu < 0.7), tỷ lệ guardrail/refusal, điểm online eval định kỳ, và `agent_rate_limit_429_total` / `agent_budget_402_total` (phát hiện abuse hoặc khách hàng chạm trần ngân sách).
  2. **Metric từ tầng biên (Nginx / Load Balancer) & Dependencies:** giám sát tỷ lệ `499`/`502`/`504` từ Nginx access log/metrics (vì agent không tự đếm được lỗi timeout ở Nginx), kèm latency/lỗi của Redis (`redis_command_duration_seconds`) và synthetic health probe từ bên ngoài.
