# Day 12 Lab - Mission Answers

## Part 1: Localhost vs Production

### Exercise 1.1: Anti-patterns found
1. **Hardcoded Secrets**: API Key được viết trực tiếp trong code (ví dụ: `api_key = "sk-..."`), dễ bị lộ khi commit lên Git.
2. **Fixed Port**: Sử dụng port cố định (8000) thay vì đọc từ biến môi trường, gây khó khăn khi deploy lên các nền tảng tự động gán port.
3. **No Health Checks**: Thiếu các endpoint `/health` hoặc `/ready`, khiến hệ thống giám sát không biết ứng dụng có đang chạy tốt hay không.
4. **Lack of Structured Logging**: Sử dụng `print()` thay vì logging định dạng JSON, gây khó khăn cho việc truy vết lỗi trên Production.
5. **Abrupt Shutdown**: Không xử lý tín hiệu SIGTERM, dẫn đến việc ngắt kết nối đột ngột và có thể làm mất dữ liệu đang xử lý.

### Exercise 1.3: Comparison table
| Feature | Develop | Production | Why Important? |
|---------|---------|------------|----------------|
| Config  | Hardcoded | Env Vars | Bảo mật và linh hoạt khi thay đổi môi trường. |
| Health check | None | /health, /ready | Giúp Cloud Platform tự động restart khi app lỗi. |
| Logging | print() | JSON Structured | Dễ dàng quản lý, tìm kiếm và phân tích log tập trung. |
| Shutdown | Abrupt | Graceful | Đảm bảo hoàn thành các request dở dang trước khi tắt. |

## Part 2: Docker

### Exercise 2.1: Dockerfile questions
1. **Base image**: `python:3.11-slim` (để tối ưu kích thước image).
2. **Working directory**: `/app` (thư mục gốc chứa mã nguồn trong container).
3. **Why COPY requirements.txt first?**: Để tận dụng cơ chế Layer Caching của Docker. Nếu chỉ sửa code mà không thêm thư viện, Docker sẽ bỏ qua bước cài đặt lại `pip install`.
4. **CMD vs ENTRYPOINT**: `ENTRYPOINT` xác định lệnh chính sẽ chạy, `CMD` cung cấp các tham số mặc định cho lệnh đó.

### Exercise 2.3: Image size comparison
- **Develop**: ~900 MB (dùng base image đầy đủ).
- **Production**: ~150 MB (dùng multi-stage build và slim image).
- **Difference**: Giảm khoảng 83% kích thước.

## Part 3: Cloud Deployment

### Exercise 3.1: Railway deployment
- **URL**: https://reasonable-comfort-production-cd88.up.railway.app
- **Screenshot**: Có sẵn trong thư mục `screenshots/dashboard.png`.

## Part 4: API Security

### Exercise 4.1-4.3: Test results
- **Auth**: Trả về 401 Unauthorized khi thiếu `X-API-Key`.
- **Rate Limit**: Trả về 429 Too Many Requests khi gọi quá 10 lần/phút.

### Exercise 4.4: Cost guard implementation
Tôi sử dụng Redis để lưu trữ số tiền đã chi tiêu của từng user theo tháng (`budget:{user_id}:{YYYY-MM}`). Trước mỗi request, hệ thống sẽ kiểm tra giá trị này. Nếu vượt quá `MONTHLY_BUDGET_USD` (10$), hệ thống trả về lỗi 402 Payment Required. Sau mỗi request thành công, sử dụng `incrbyfloat` để cập nhật chi phí thực tế.

## Part 5: Scaling & Reliability

### Exercise 5.1-5.5: Implementation notes
1. **Health Checks**: Triển khai `/health` (kiểm tra process) và `/ready` (kiểm tra kết nối Redis).
2. **Graceful Shutdown**: Sử dụng `contextmanager` (lifespan) trong FastAPI để xử lý các tác vụ dọn dẹp và kết hợp với `signal.signal` để bắt tín hiệu SIGTERM.
3. **Stateless Design**: Chuyển toàn bộ dữ liệu phiên làm việc (Conversation History) vào Redis thay vì lưu trong biến toàn cục. Điều này cho phép hệ thống mở rộng (scale) lên nhiều container mà không làm mất lịch sử chat của người dùng.
4. **Load Balancing**: Sử dụng Nginx làm Gateway để phân phối request đến 3 replicas của Agent theo thuật toán Round Robin.

## Part 6: Final Project

### Checklist Đã Hoàn Thành:
- [x] Dockerfile Multi-stage (< 200MB)
- [x] Authentication (API Key)
- [x] Rate Limiting (Redis)
- [x] Cost Guard (Redis)
- [x] Stateless Architecture
- [x] Structured JSON Logging
- [x] Graceful Shutdown
- [x] Health & Readiness Endpoints
- [x] Docker Compose (Agent x3 + Redis + Nginx)

---
*Người thực hiện: Phạm Minh Hiếu*
*Mã sinh viên: 2A202600550*