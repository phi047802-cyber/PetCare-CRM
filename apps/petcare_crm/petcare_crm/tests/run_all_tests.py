"""
Master Test Runner and Comprehensive Validator for PetCare CRM (Prompt 9).
Executes all test suites across Unit, Integration, and End-to-End layers.
Produces a rigorous, auditable report differentiating PASS, FAIL, SKIPPED, and BLOCKED.
"""

import os
import sys
import time
import subprocess
from datetime import datetime

# Configure stdout and stderr for UTF-8 on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Test suite configuration
TEST_SUITES = [
    {
        "file": "apps/petcare_crm/petcare_crm/tests/test_crm_core_mock.py",
        "name": "Suite 1: CRM Core & Lead/Opportunity Lifecycle",
        "layer": "Unit & Integration",
        "description": "Validation số điện thoại, chu kỳ Lead, phân giai đoạn Opportunity, phòng chống gộp trùng Customer."
    },
    {
        "file": "apps/petcare_crm/petcare_crm/tests/test_service_operations_mock.py",
        "name": "Suite 2: PetCare Service Operations & Visit Catalog",
        "layer": "Unit & Integration",
        "description": "Danh mục dịch vụ chuẩn, tính giá dịch vụ, cấn trừ quyền lợi 100% FREE, kiểm tra hồ sơ Pet."
    },
    {
        "file": "apps/petcare_crm/petcare_crm/tests/test_membership_lifecycle_mock.py",
        "name": "Suite 3: Membership Lifecycle, Benefits & Redemption Engine",
        "layer": "Domain & Transaction Safety",
        "description": "Gói hội viên Active/Expired, cấn trừ quyền lợi, bảo vệ Idempotency chống double-redeem, rollover gia hạn."
    },
    {
        "file": "apps/petcare_crm/petcare_crm/tests/test_care_intelligence_mock.py",
        "name": "Suite 4: Care Intelligence, Pattern Analytics & Deduplication",
        "layer": "Intelligence & Retention",
        "description": "Thuật toán lọc IQR outlier, tính EWMA, dự đoán ngày tiếp theo, phân loại Due Soon/At Risk, khử trùng lặp."
    },
    {
        "file": "apps/petcare_crm/petcare_crm/tests/test_workflow_automation_mock.py",
        "name": "Suite 5: Workflow Automation & Scheduled Jobs",
        "layer": "Automation & Integration",
        "description": "Tác vụ nền idempotent: nhắc Lead chưa liên hệ, cảnh báo hết hạn thẻ, quét SLA khiếu nại, Safe Mode."
    },
    {
        "file": "apps/petcare_crm/petcare_crm/tests/test_security_and_reporting_mock.py",
        "name": "Suite 6: Security, RBAC Matrix & Analytics KPIs",
        "layer": "Security & Analytics",
        "description": "Thực thi phân quyền RBAC đa vai trò, kiểm tra sở hữu chéo, khử nhiễm đầu vào, 8 chỉ số KPI chuẩn."
    },
    {
        "file": "apps/petcare_crm/petcare_crm/tests/test_e2e_scenarios_mock.py",
        "name": "Suite 7: End-to-End (E2E) Scenarios A-F",
        "layer": "End-to-End Systems Validation",
        "description": "6 kịch bản E2E toàn diện: Lead->Khách hàng, Dịch vụ->360, Hội viên->Redemption, Care Engine, RBAC, Automation."
    },
    {
        "file": "apps/petcare_crm/petcare_crm/tests/test_extended_capabilities_mock.py",
        "name": "Suite 8: Advanced Extensions & Resolved Limitations",
        "layer": "Extensions & Integrations",
        "description": "Hệ số mùa vụ & độ tuổi, Dynamic VietQR, Payment Webhook đối soát tự động, Omnichannel ZNS/SMS, Owner Portal."
    },
    {
        "file": "apps/petcare_crm/petcare_crm/tests/test_wordpress_lead_integration.py",
        "name": "Suite 9: WordPress Lead Capture & Server-Side Proxy Integration (A4.8)",
        "layer": "External Web Integration & Security",
        "description": "Validation số điện thoại VN, bẫy bot Honeypot, khử trùng lặp, bảo mật Zero Secret và Proxy Server."
    },
    {
        "file": "apps/petcare_crm/petcare_crm/tests/test_audit_remediation.py",
        "name": "Suite 10: Audit Remediation & System Hardening (All 20 Findings)",
        "layer": "Security, Data Integrity & Analytics Hardening",
        "description": "Kiểm tra toàn diện 14 kịch bản xác minh vá lỗi cho các phát hiện P0-P4 từ hội đồng kiểm toán."
    },
    {
        "file": "apps/petcare_crm/petcare_crm/tests/test_woocommerce_integration.py",
        "name": "Suite 11: WooCommerce Order Webhook Integration (A4.8)",
        "layer": "Commerce Integration & Security",
        "description": "HMAC-SHA256, ánh xạ đơn hàng, chống webhook trùng, cập nhật Opportunity và retry WordPress."
    }
]


def run_suite(suite_info):
    file_path = suite_info["file"]
    start_time = time.perf_counter()
    
    cmd = [sys.executable, "-m", "unittest", "-v", file_path]
    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    duration = time.perf_counter() - start_time
    
    output = result.stderr if result.stderr else result.stdout
    lines = output.splitlines()
    
    tests_detail = []
    total_ran = 0
    passed = 0
    failed = 0
    errors = 0
    skipped = 0
    
    for line in lines:
        if " ... " in line:
            parts = line.split(" ... ")
            test_name = parts[0].strip()
            status_str = parts[1].strip()
            
            if "ok" in status_str.lower():
                status = "PASS"
                passed += 1
            elif "fail" in status_str.lower():
                status = "FAIL"
                failed += 1
            elif "error" in status_str.lower():
                status = "ERROR"
                errors += 1
            elif "skip" in status_str.lower():
                status = "SKIPPED"
                skipped += 1
            else:
                status = "BLOCKED"
            
            total_ran += 1
            tests_detail.append({"test": test_name, "status": status})
        elif line.startswith("Ran ") and "tests in" in line:
            try:
                total_ran = int(line.split()[1])
            except Exception:
                pass
    
    is_success = (result.returncode == 0) and (failed == 0) and (errors == 0)
    
    return {
        "suite_info": suite_info,
        "is_success": is_success,
        "duration": duration,
        "total_ran": total_ran or (passed + failed + errors + skipped),
        "passed": passed or (total_ran if is_success else 0),
        "failed": failed,
        "errors": errors,
        "skipped": skipped,
        "blocked": 0,
        "tests_detail": tests_detail,
        "raw_output": output
    }


def main():
    print("=" * 80)
    print("PETCARE CRM — AUTOMATED TEST SUITE & END-TO-END VALIDATOR")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Python: {sys.version.split()[0]} | Platform: {sys.platform}")
    print("=" * 80)
    print()

    suite_results = []
    grand_total = 0
    grand_passed = 0
    grand_failed = 0
    grand_errors = 0
    grand_skipped = 0
    grand_blocked = 0

    total_start_time = time.perf_counter()

    for suite in TEST_SUITES:
        print(f"Executing {suite['name']} ... ", end="", flush=True)
        res = run_suite(suite)
        suite_results.append(res)
        
        status_tag = "PASS" if res["is_success"] else "FAIL"
        print(f"[{status_tag}] ({res['passed']} passed, {res['duration']:.3f}s)")
        
        grand_total += res["total_ran"]
        grand_passed += res["passed"]
        grand_failed += res["failed"]
        grand_errors += res["errors"]
        grand_skipped += res["skipped"]
        grand_blocked += res["blocked"]

    total_duration = time.perf_counter() - total_start_time

    print()
    print("=" * 80)
    print("TỔNG HỢP KẾT QUẢ KIỂM THỬ (AUDIT SUMMARY)")
    print("=" * 80)
    print(f"Tổng số kịch bản kiểm thử (Total Tests) : {grand_total}")
    print(f"Thành công (PASS)                      : {grand_passed}")
    print(f"Thất bại (FAIL)                        : {grand_failed}")
    print(f"Lỗi cú pháp / runtime (ERRORS)         : {grand_errors}")
    print(f"Bỏ qua (SKIPPED)                       : {grand_skipped}")
    print(f"Bị chặn (BLOCKED)                      : {grand_blocked}")
    print(f"Tổng thời gian thực thi (Total Time)   : {total_duration:.3f}s")
    print(f"Tỷ lệ thành công (Pass Rate)           : {(grand_passed / grand_total * 100):.1f}%" if grand_total > 0 else "N/A")
    print("=" * 80)

    # Exit code
    if grand_failed > 0 or grand_errors > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
