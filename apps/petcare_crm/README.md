# PetCare CRM (v2.0-release)
> **Comprehensive CRM Platform for Pet Care Services on Frappe Framework v15**  
> Quản lý khách hàng toàn diện, thẻ hội viên, cấn trừ quyền lợi và công cụ chăm sóc khách hàng chủ động.

---

## 📋 Giới Thiệu
**PetCare CRM** là ứng dụng hoàn chỉnh cho **Frappe Framework v15**, được thiết kế để số hóa toàn diện quy trình vận hành cho chuỗi dịch vụ chăm sóc thú cưng:
1. **CRM Tiếp Thị & Bán Hàng**: Ghi nhận Lead, chuẩn hóa số điện thoại Việt Nam, chuyển đổi không gộp trùng khách hàng, quản lý Sales Pipeline.
2. **Quản Lý Thú Cưng & Dịch Vụ**: Quản lý hồ sơ Pet (Multi-pet), bảng giá dịch vụ chuẩn, phiếu Service Visit và phản hồi khiếu nại (PetCare Case).
3. **Quản Lý Gói Hội Viên (Membership & Loyalty)**: Theo dõi quyền lợi linh hoạt, trừ lượt tự động, kiểm soát số dư tuyệt đối không bị âm, chống race condition và hỗ trợ rollover.
4. **Công Cụ Dự Đoán Chu Kỳ Chăm Sóc (Care Intelligence & Retention)**: Áp dụng thuật toán EWMA và lọc ngoại lai IQR để dự đoán ngày tái sử dụng dịch vụ, phát hiện khách hàng sắp đến hạn (`DUE_SOON`) và khách hàng có nguy cơ rời bỏ (`AT_RISK`).
5. **Tự Động Hóa Chăm Sóc Khách Hàng (Automated Care Schedulers)**: Tự động phân bổ nhiệm vụ ToDo idempotent, cảnh báo hết hạn thẻ hội viên, giám sát SLA và Safe Mode.
6. **Bảo Mật Phân Quyền & Báo Cáo Desk**: Ma trận RBAC 5 vai trò (System Manager, CRM Manager, Sales, Technician, Analyst), xác thực sở hữu chéo và báo cáo 8 chỉ số KPI.

---

## 🛠️ Yêu Cầu Hệ Thống & Cài Đặt

### Cài Đặt & Chạy Môi Trường (Docker Compose)
```bash
# 1. Khởi động Docker containers
docker compose -f compose.yaml -f overrides/compose.mariadb.yaml -f overrides/compose.redis.yaml --project-name petcare up -d

# 2. Cài đặt app và migrate
docker exec -it petcare-backend-1 bench --site petcare.localhost install-app petcare_crm
docker exec -it petcare-backend-1 bench --site petcare.localhost migrate

# 3. Nạp dữ liệu demo thuần Việt (Seed Data chuẩn Prompt 10)
docker exec -it petcare-backend-1 bench --site petcare.localhost execute petcare_crm.patches.v1_0.seed_demo_data.execute
```

---

## 🌐 Truy Cập Hệ Thống
* **URL**: `http://localhost:8080` (hoặc `http://petcare.localhost:8080`)
* **Tài khoản mặc định**: `Administrator` / `admin123`
* **Workspace chính**: `http://localhost:8080/app/petcare-crm`

---

## 🧪 Kiểm Thử Tự Động (Automated Testing)

Chạy toàn bộ 58 kịch bản kiểm thử (100% Pass) trực tiếp qua Master Test Runner:
```powershell
python apps/petcare_crm/petcare_crm/tests/run_all_tests.py
```

Hoặc chạy trong container bench:
```bash
docker exec -it petcare-backend-1 bench --site petcare.localhost run-tests --app petcare_crm
```

---

## 📂 Hệ Thống Tài Liệu Bàn Giao
Toàn bộ tài liệu chi tiết đã được biên soạn và cập nhật tại thư mục `docs/`:
* `docs/FINAL_IMPLEMENTATION_REPORT.md`: Báo cáo nghiệm thu tổng thể dự án.
* `docs/DEMO_SCRIPT.md`: Kịch bản trình diễn 3 câu chuyện cốt lõi (Lead, Service/Membership, Care Intelligence).
* `docs/SETUP_GUIDE.md`: Hướng dẫn cài đặt và thiết lập môi trường.
* `docs/BUSINESS_RULES.md`: Đặc tả toàn bộ quy tắc nghiệp vụ bất biến.
* `docs/API_DOCUMENTATION.md`: Tài liệu kỹ thuật các API endpoints.
* `docs/ROLE_PERMISSION_MATRIX.md`: Ma trận phân quyền vai trò và bảo vệ sở hữu chéo.
* `docs/TEST_GUIDE.md`: Hướng dẫn chạy và giải thích kết quả kiểm thử.
* `docs/KNOWN_LIMITATIONS.md`: Các giới hạn hiện tại và định hướng phát triển sau đồ án.
* `docs/SYSTEM_ARCHITECTURE.md`: Sơ đồ kiến trúc 8 tầng Clean Architecture.
* `docs/DATA_CONTRACT.md`: Đặc tả hợp đồng dữ liệu và sơ đồ ERD thực thể.
