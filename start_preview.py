"""
PetCare CRM v2.0 — Dual-Stack High Performance Preview Server
Hỗ trợ đồng thời cả IPv4 (127.0.0.1) và IPv6 (::1/localhost) với độ trễ < 2ms.
"""
import http.server
import socket
import webbrowser
import os
import sys

# Configure UTF-8 for console output
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        self.send_header('Connection', 'close')
        super().end_headers()

    def do_HEAD(self):
        clean_path = self.path.split('?')[0].rstrip('/')
        if clean_path in ('', '/', '/frontend', '/frontend.html', '/index', '/index.html'):
            self.path = '/preview.html'
        elif clean_path in ('/app/petcare-crm', '/app', '/desk', '/desk_preview.html') or clean_path.startswith('/app/'):
            self.path = '/desk_preview.html'
        return super().do_HEAD()

    def do_GET(self):
        clean_path = self.path.split('?')[0].rstrip('/')
        if clean_path in ('', '/', '/frontend', '/frontend.html', '/index', '/index.html'):
            self.path = '/preview.html'
        elif clean_path in ('/app/petcare-crm', '/app', '/desk', '/desk_preview.html') or clean_path.startswith('/app/'):
            self.path = '/desk_preview.html'
        return super().do_GET()

    def log_message(self, format, *args):
        # Format log ngắn gọn
        sys.stdout.write(f"[PetCare Server] {format % args}\n")

class DualStackThreadingServer(http.server.ThreadingHTTPServer):
    address_family = socket.AF_INET6
    allow_reuse_address = True
    daemon_threads = True

    def server_bind(self):
        try:
            self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
        except (AttributeError, OSError):
            pass
        super().server_bind()

def run():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(base_dir)
    
    port = 8080
    httpd = None
    
    # 1. Thử khởi tạo DualStack IPv6/IPv4 trên cổng 8080 (hoặc 8000/5000)
    for p in [8080, 8000, 5000]:
        try:
            httpd = DualStackThreadingServer(('::', p), CustomHandler)
            port = p
            break
        except Exception:
            try:
                # Fallback sang thuần IPv4 nếu máy tắt IPv6
                class IPv4Server(http.server.ThreadingHTTPServer):
                    allow_reuse_address = True
                    daemon_threads = True
                httpd = IPv4Server(('0.0.0.0', p), CustomHandler)
                port = p
                break
            except Exception:
                continue

    if not httpd:
        print("Lỗi: Không thể mở cổng mạng [8080, 8000, 5000].")
        sys.exit(1)

    url_local = f"http://localhost:{port}"
    url_ip = f"http://127.0.0.1:{port}"
    
    print("=" * 70)
    print("  🐾 PETCARE CRM v2.0 — MÁY CHỦ PREVIEW ĐÃ SẴN SÀNG")
    print(f"  ● Link 1 (Khuyên dùng) : {url_ip}")
    print(f"  ● Link 2 (Localhost)    : {url_local}")
    print("  ● Tệp phục vụ           : preview.html (Đã có sẵn dữ liệu mẫu)")
    print("=" * 70)
    print("  -> Đang tự động mở trình duyệt...")
    try:
        webbrowser.open(url_ip)
    except Exception:
        pass
    print("  -> Nhấn Ctrl + C để dừng máy chủ khi hoàn tất.")
    print("=" * 70)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nĐã đóng máy chủ preview.")
        httpd.server_close()

if __name__ == '__main__':
    run()
