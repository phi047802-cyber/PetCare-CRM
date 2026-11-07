# PetCare CRM - 1-Click Clean Deployment Script
# Task T51 (Day 13 Schedule) - Updated with Full Audit Fixes

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "         PETCARE CRM -- 1-CLICK CLEAN DEPLOYMENT          " -ForegroundColor Yellow
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Kiem tra Docker
Write-Host "[1/6] Kiem tra dich vu Docker..." -ForegroundColor White
docker ps > $null 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Error "Docker Desktop chua khoi dong. Vui long mo Docker Desktop va thu lai!"
    exit 1
}
Write-Host "Docker dang hoat dong on dinh." -ForegroundColor Green

# 2. Khoi dong cac container PetCare CRM
Write-Host "[2/6] Khoi dong cac container PetCare CRM..." -ForegroundColor White
docker start petcare-db-1 petcare-redis-cache-1 petcare-redis-queue-1 petcare-backend-1 petcare-frontend-1 petcare-websocket-1 petcare-queue-short-1 petcare-queue-long-1 petcare-scheduler-1 > $null 2>&1
Start-Sleep -Seconds 4

# 3. Dong bo ma nguon giao dien va logic vao container
Write-Host "[3/6] Dong bo ma nguon giao dien va logic vao container..." -ForegroundColor White
Copy-Item -Path "apps\petcare_crm\petcare_crm\www\index.html" -Destination "apps\petcare_crm\petcare_crm\www\frontend.html" -Force
$containers = "petcare-backend-1", "petcare-frontend-1"
foreach ($c in $containers) {
    docker cp "apps\petcare_crm\petcare_crm\www\index.html" "${c}:/home/frappe/frappe-bench/apps/petcare_crm/petcare_crm/www/index.html"
    docker cp "apps\petcare_crm\petcare_crm\www\frontend.html" "${c}:/home/frappe/frappe-bench/apps/petcare_crm/petcare_crm/www/frontend.html"
    docker cp "apps\petcare_crm\petcare_crm\api.py" "${c}:/home/frappe/frappe-bench/apps/petcare_crm/petcare_crm/api.py"
    docker cp "apps\petcare_crm\petcare_crm\tasks.py" "${c}:/home/frappe/frappe-bench/apps/petcare_crm/petcare_crm/tasks.py"
    docker cp "apps\petcare_crm\petcare_crm\utils\." "${c}:/home/frappe/frappe-bench/apps/petcare_crm/petcare_crm/utils/"
    docker cp "apps\petcare_crm\petcare_crm\tests\." "${c}:/home/frappe/frappe-bench/apps/petcare_crm/petcare_crm/tests/"
    docker cp "apps\petcare_crm\petcare_crm\petcare_crm\doctype\." "${c}:/home/frappe/frappe-bench/apps/petcare_crm/petcare_crm/petcare_crm/doctype/"
    docker cp "apps\petcare_crm\petcare_crm\patches\v1_0\seed_demo_data.py" "${c}:/home/frappe/frappe-bench/apps/petcare_crm/petcare_crm/patches/v1_0/seed_demo_data.py"
}

docker exec petcare-backend-1 bench clear-cache
docker exec petcare-backend-1 bench clear-website-cache
docker restart petcare-backend-1
Start-Sleep -Seconds 4

# 4. Nap du lieu mau thuan Viet da dang va tinh toan khuyen nghi
Write-Host "[4/6] Nap du lieu mau thuan Viet va tinh toan khuyen nghi..." -ForegroundColor White
docker exec petcare-backend-1 bench --site localhost execute petcare_crm.patches.v1_0.seed_demo_data.execute
docker exec petcare-backend-1 bench --site localhost execute petcare_crm.tasks.daily_petcare_scan

# 5. Chay kiem thu tu dong 22/22 Unit Tests
Write-Host "[5/6] Chay kiem thu tu dong 22/22 Unit Tests..." -ForegroundColor White
docker exec petcare-backend-1 bench --site localhost run-tests --app petcare_crm

# 6. Thong bao hoan tat
Write-Host ""
Write-Host "==========================================================" -ForegroundColor Green
Write-Host "             HE THONG DA SAN SANG HOAT DONG               " -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Green
Write-Host "Giao dien le tan va tra cuu:  http://localhost:8080/frontend" -ForegroundColor Yellow
Write-Host "Trang chu he thong:          http://localhost:8080/" -ForegroundColor Yellow
Write-Host "Cong quan tri Frappe Desk:   http://localhost:8080/app" -ForegroundColor Yellow
Write-Host "Tai khoan: Administrator | Mat khau: admin123" -ForegroundColor Gray
Write-Host "==========================================================" -ForegroundColor Green
