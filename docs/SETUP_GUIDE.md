# HƯỚNG DẪN CÀI ĐẶT & THIẾT LẬP HỆ THỐNG (SETUP & INSTALLATION GUIDE)

> **Dự án**: PetCare CRM (Hệ Thống CRM Dịch Vụ Chăm Sóc Thú Cưng)  
> **Nền tảng**: Frappe Framework v15 (Desk Native)  
> **Đối tượng**: Giảng viên, Hội đồng chấm đồ án, Developer, SysAdmin  

---

## 1. Yêu Cầu Môi Trường (Prerequisites)

| Thành phần | Phiên bản khuyến nghị | Ghi chú |
|---|---|---|
| **Hệ điều hành** | Ubuntu 22.04 LTS / macOS / Windows 11 (WSL2 hoặc Docker) | Khuyến nghị môi trường Docker hoặc Linux native |
| **Docker Engine & Compose** | Docker Desktop >= 4.25 (Compose v2) | Cho phương án triển khai containerized |
| **Python** | 3.10, 3.11, 3.12, 3.14 | Môi trường runtime backend |
| **Node.js** | >= 18.x (kèm Yarn hoặc npm) | Cho build tài nguyên Desk UI |
| **MariaDB** | 10.6+ hoặc 11.x (InnoDB, utf8mb4) | Cơ sở dữ liệu quan hệ |
| **Redis** | 6.x hoặc 7.x | Cache & Background worker queues |

---

## 2. Phương Án 1: Triển Khai Qua Docker Compose (Khuyến Nghị Nhanh Nhất)

Phương án này đóng gói toàn bộ Frappe Framework, MariaDB và Redis, không làm ảnh hưởng tới môi trường máy chủ host.

```bash
# Bước 1: Khởi động các container cơ sở dữ liệu và redis
docker compose -f compose.yaml -f overrides/compose.mariadb.yaml -f overrides/compose.redis.yaml --project-name petcare up -d

# Bước 2: Kiểm tra trạng thái các container đang hoạt động
docker ps

# Bước 3: Cài đặt ứng dụng petcare_crm vào site
docker exec -it petcare-backend-1 bench --site petcare.localhost install-app petcare_crm

# Bước 4: Chạy migration schema
docker exec -it petcare-backend-1 bench --site petcare.localhost migrate

# Bước 5: Nạp dữ liệu demo thuần Việt (Seed Data chuẩn Prompt 10)
docker exec -it petcare-backend-1 bench --site petcare.localhost execute petcare_crm.patches.v1_0.seed_demo_data.execute
```

---

## 3. Phương Án 2: Triển Khai Native Qua Frappe Bench (Dành Cho Nhà Phát Triển)

```bash
# Bước 1: Chuyển tới thư mục bench
cd /path/to/frappe-bench

# Bước 2: Kéo hoặc liên kết ứng dụng petcare_crm
bench get-app /path/to/Doan_CRM/apps/petcare_crm

# Bước 3: Cài đặt app vào site hiện có
bench --site [ten_site] install-app petcare_crm

# Bước 4: Thực thi migration
bench --site [ten_site] migrate

# Bước 5: Khởi tạo dữ liệu demo mẫu
bench --site [ten_site] execute petcare_crm.patches.v1_0.seed_demo_data.execute

# Bước 6: Khởi chạy môi trường Desk
bench start
```

---

## 4. Truy Cập Hệ Thống & Tài Khoản Mặc Định

* **Địa chỉ truy cập**: `http://localhost:8080` (hoặc `http://petcare.localhost:8080`)
* **Tài khoản quản trị viên (System Administrator)**:
  * **Tên đăng nhập**: `Administrator`
  * **Mật khẩu**: `admin123`
* **Workspace chính**: Chọn **PetCare CRM** trên thanh Desk Navigation hoặc truy cập:
  `http://localhost:8080/app/petcare-crm`

---

## 5. Hướng Dẫn Chạy Bộ Kiểm Thử Tự Động (Test Suite)

Hệ thống cung cấp Master Test Runner độc lập, có thể chạy trực tiếp bằng Python mà không bắt buộc khởi động container daemon:

```powershell
# Chạy toàn bộ 58 kịch bản kiểm thử (7 Test Suites)
python apps/petcare_crm/petcare_crm/tests/run_all_tests.py
```

Kết quả mong đợi:
```text
================================================================================
TỔNG HỢP KẾT QUẢ KIỂM THỬ (AUDIT SUMMARY)
================================================================================
Tổng số kịch bản kiểm thử (Total Tests) : 58
Thành công (PASS)                      : 58
Thất bại (FAIL)                        : 0
Lỗi cú pháp / runtime (ERRORS)         : 0
Bỏ qua (SKIPPED)                       : 0
Bị chặn (BLOCKED)                      : 0
Tổng thời gian thực thi (Total Time)   : ~1.5s
Tỷ lệ thành công (Pass Rate)           : 100.0%
================================================================================
```

---

## 6. Xử Lý Sự Cố Thường Gặp (Troubleshooting)

1. **Lỗi cổng 8080 đã bị chiếm dụng**:
   * Kiểm tra tiến trình đang chạy cổng 8080: `netstat -ano | findstr 8080` (Windows) hoặc `lsof -i :8080` (Linux/macOS).
   * Thay đổi cổng mapping trong file `compose.yaml` (ví dụ: `8085:8080`).
2. **Lỗi Permission Denied khi chạy bench**:
   * Chạy quyền quản trị hoặc kiểm tra user container: `docker exec -u 0 -it petcare-backend-1 ...`
3. **Lỗi UnicodeEncodeError trên PowerShell Windows cũ**:
   * Đặt biến môi trường UTF-8: `$env:PYTHONIOENCODING="utf-8"`.
   * Hoặc sử dụng Windows Terminal với font Cascadia Code.
