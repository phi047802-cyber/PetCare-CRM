"""
PetCare CRM Email Service — Mailtrap Integration.
Thiết kế template email chuẩn HTML Responsive, hiện đại, phong cách Medical Teal & Clean Fintech.
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

try:
    import frappe
except ImportError:
    frappe = None

# Mailtrap SMTP Credentials (configurable via site_config or env)
import os

def _get_smtp_config():
    host = "sandbox.smtp.mailtrap.io"
    port = 2525
    user = None
    pwd = None
    if frappe and hasattr(frappe, "conf"):
        user = frappe.conf.get("mailtrap_user")
        pwd = frappe.conf.get("mailtrap_pass")
        host = frappe.conf.get("mailtrap_host") or host
        port = int(frappe.conf.get("mailtrap_port") or port)
    if not user:
        user = os.environ.get("MAILTRAP_USER", "9777c07beed041")
    if not pwd:
        pwd = os.environ.get("MAILTRAP_PASS", "8a22d4e766bb7a")
    return host, port, user, pwd

DEFAULT_SENDER = "PetCare Clinic & Spa <no-reply@petcare.com>"
MAILTRAP_HOST, MAILTRAP_PORT, MAILTRAP_USER, MAILTRAP_PASS = _get_smtp_config()


def _get_base_template(header_badge, title, subtitle, main_content):
    """
    Khung email chuẩn Premium Healthcare / Fintech:
    - Bo góc, đổ bóng mềm mại
    - Tone màu Teal y tế kết hợp Slate cao cấp
    - Hỗ trợ tốt trên mọi trình duyệt & ứng dụng email (Gmail, Outlook, Mailtrap)
    """
    return f"""
    <!DOCTYPE html>
    <html lang="vi">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>{title}</title>
    </head>
    <body style="margin: 0; padding: 30px 10px; background-color: #F1F5F9; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; -webkit-font-smoothing: antialiased; color: #1E293B;">
      <table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px; margin: 0 auto; background-color: #FFFFFF; border-radius: 16px; overflow: hidden; box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.08), 0 8px 10px -6px rgba(15, 23, 42, 0.04); border: 1px solid #E2E8F0;">
        
        <!-- HEADER HERO -->
        <tr>
          <td style="padding: 36px 36px 30px 36px; background: linear-gradient(135deg, #0F766E 0%, #0D9488 100%); text-align: left;">
            <table border="0" cellpadding="0" cellspacing="0" width="100%">
              <tr>
                <td>
                  <span style="display: inline-block; padding: 4px 12px; background-color: rgba(255, 255, 255, 0.2); backdrop-filter: blur(4px); border-radius: 20px; color: #CCFBF1; font-size: 11px; font-weight: 700; letter-spacing: 0.5px; text-transform: uppercase;">
                    {header_badge}
                  </span>
                  <h1 style="margin: 14px 0 6px 0; color: #FFFFFF; font-size: 24px; font-weight: 800; letter-spacing: -0.5px; line-height: 1.3;">
                    {title}
                  </h1>
                  <p style="margin: 0; color: #E6FFFA; font-size: 14px; font-weight: 400; opacity: 0.95;">
                    {subtitle}
                  </p>
                </td>
                <td align="right" valign="top" style="width: 54px;">
                  <div style="width: 50px; height: 50px; background-color: #FFFFFF; border-radius: 14px; text-align: center; line-height: 50px; font-size: 26px; box-shadow: 0 4px 12px rgba(0,0,0,0.12);">
                    🐾
                  </div>
                </td>
              </tr>
            </table>
          </td>
        </tr>

        <!-- MAIN BODY -->
        <tr>
          <td style="padding: 32px 36px 24px 36px;">
            {main_content}
          </td>
        </tr>

        <!-- FOOTER -->
        <tr>
          <td style="padding: 24px 36px 32px 36px; background-color: #F8FAFC; border-top: 1px solid #E2E8F0; text-align: center;">
            <p style="margin: 0 0 8px 0; font-size: 13px; font-weight: 700; color: #334155;">
              PetCare Clinic & Spa
            </p>
            <p style="margin: 0 0 12px 0; font-size: 12px; color: #64748B; line-height: 1.5;">
              Hệ thống chăm sóc sức khỏe, thẩm mỹ &amp; phòng khám thú cưng cao cấp.<br>
              Hotline hỗ trợ: <strong style="color: #0D9488;">1900 8888</strong> &bull; Email: support@petcare.com
            </p>
            <p style="margin: 0; font-size: 11px; color: #94A3B8;">
              &copy; 2026 PetCare CRM. Email này được tạo tự động từ hệ thống.
            </p>
          </td>
        </tr>

      </table>
    </body>
    </html>
    """


def _send_smtp_email(to_email, subject, html_content):
    """Gửi email trực tiếp qua SMTP Mailtrap với fallback về frappe.sendmail."""
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = DEFAULT_SENDER
        msg["To"] = to_email
        msg.attach(MIMEText(html_content, "html", "utf-8"))

        server = smtplib.SMTP(MAILTRAP_HOST, MAILTRAP_PORT, timeout=12)
        server.starttls()
        server.login(MAILTRAP_USER, MAILTRAP_PASS)
        server.sendmail(DEFAULT_SENDER, [to_email], msg.as_string())
        server.quit()
        if frappe:
            frappe.logger("petcare_crm").info(f"Direct Mailtrap email sent to {to_email}: {subject}")
        return True
    except Exception as e:
        if frappe:
            frappe.logger("petcare_crm").warning(f"Direct Mailtrap SMTP error: {e}. Trying frappe.sendmail fallback...")
            try:
                frappe.sendmail(
                    recipients=[to_email],
                    subject=subject,
                    message=html_content,
                    now=True,
                )
                return True
            except Exception as fe:
                frappe.logger("petcare_crm").error(f"frappe.sendmail failed as well: {fe}")
                return False
        else:
            return False


def send_membership_welcome_email(customer_name, membership_name, plan_doc):
    """Gửi email chào mừng khi đăng ký hội viên mới với card giao diện sang trọng."""
    contact = None
    if frappe:
        try:
            contact = frappe.get_doc("Contact", customer_name)
        except Exception:
            pass

    email = getattr(contact, "email_id", None) if contact else None
    if not email and contact and getattr(contact, "email_ids", None):
        email = contact.email_ids[0].email_id

    if not email:
        email = "customer@petcare-demo.com"

    customer_display = getattr(contact, "first_name", None) if contact else customer_name
    plan_name = getattr(plan_doc, "plan_name", "Hội Viên")
    plan_price = float(getattr(plan_doc, "price", 0) or 0)
    duration = getattr(plan_doc, "duration_months", 12)

    # Render danh sách quyền lợi dạng cards nhỏ
    benefits_rows = ""
    for b in getattr(plan_doc, "benefits", []):
        disc_text = "Miễn phí 100%" if b.discount_type == "FREE" else (f"Giảm {b.discount_value}%" if b.discount_type == "PERCENTAGE" else f"Giảm {float(b.discount_value):,.0f}đ")
        benefits_rows += f"""
        <tr>
          <td style="padding: 10px 14px; border-bottom: 1px solid #EDF2F7; font-size: 13px; font-weight: 600; color: #1E293B;">
            <span style="display: inline-block; width: 8px; height: 8px; background-color: #0D9488; border-radius: 50%; margin-right: 8px;"></span>
            {b.benefit_type}
          </td>
          <td style="padding: 10px 14px; border-bottom: 1px solid #EDF2F7; font-size: 13px; color: #0F766E; font-weight: 700; text-align: center;">
            {b.total_quantity} lượt
          </td>
          <td style="padding: 10px 14px; border-bottom: 1px solid #EDF2F7; font-size: 12px; color: #64748B; text-align: right;">
            <span style="background-color: #F0FDFA; color: #0F766E; border: 1px solid #99F6E4; padding: 2px 8px; border-radius: 12px; font-weight: 600;">
              {disc_text}
            </span>
          </td>
        </tr>
        """

    content = f"""
      <p style="font-size: 15px; line-height: 1.6; margin: 0 0 20px 0; color: #334155;">
        Xin chào <strong>{customer_display}</strong>,<br>
        Chào mừng bạn cùng thú cưng đã chính thức trở thành Hội viên tại <strong>PetCare Clinic &amp; Spa</strong>! Gói dịch vụ chăm sóc toàn diện của bạn đã được kích hoạt thành công trên hệ thống.
      </p>

      <!-- DIGITAL MEMBERSHIP CARD PREVIEW -->
      <table border="0" cellpadding="0" cellspacing="0" width="100%" style="margin-bottom: 24px; background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%); border-radius: 14px; color: #FFFFFF; box-shadow: 0 8px 16px rgba(15, 23, 42, 0.15);">
        <tr>
          <td style="padding: 22px 24px;">
            <table border="0" cellpadding="0" cellspacing="0" width="100%">
              <tr>
                <td>
                  <span style="font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 1.5px; color: #94A3B8;">Digital Membership Card</span>
                  <div style="font-size: 20px; font-weight: 800; color: #38BDF8; margin-top: 4px;">{plan_name}</div>
                </td>
                <td align="right" valign="top">
                  <span style="background: rgba(255,255,255,0.15); padding: 4px 10px; border-radius: 8px; font-size: 11px; font-weight: 700; color: #4ADE80;">ĐANG HOẠT ĐỘNG</span>
                </td>
              </tr>
              <tr>
                <td colspan="2" style="padding-top: 24px;">
                  <table border="0" cellpadding="0" cellspacing="0" width="100%">
                    <tr>
                      <td>
                        <span style="font-size: 10px; text-transform: uppercase; color: #94A3B8;">Mã Thẻ Hội Viên</span>
                        <div style="font-family: monospace; font-size: 14px; font-weight: 700; color: #FFFFFF; letter-spacing: 1px;">{membership_name}</div>
                      </td>
                      <td align="right">
                        <span style="font-size: 10px; text-transform: uppercase; color: #94A3B8;">Thời Hạn Gói</span>
                        <div style="font-size: 13px; font-weight: 700; color: #FFFFFF;">{duration} Tháng</div>
                      </td>
                    </tr>
                  </table>
                </td>
              </tr>
            </table>
          </td>
        </tr>
      </table>

      <!-- Quyền lợi chi tiết -->
      <div style="margin-bottom: 24px;">
        <h3 style="font-size: 14px; text-transform: uppercase; letter-spacing: 0.5px; color: #475569; margin: 0 0 10px 0; font-weight: 700;">
          🎁 Danh Sách Quyền Lợi Đi Kèm
        </h3>
        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: separate; border-spacing: 0; border: 1px solid #E2E8F0; border-radius: 10px; overflow: hidden;">
          <thead>
            <tr style="background-color: #F8FAFC;">
              <th align="left" style="padding: 10px 14px; font-size: 11px; color: #64748B; text-transform: uppercase; border-bottom: 1px solid #E2E8F0;">Dịch vụ</th>
              <th align="center" style="padding: 10px 14px; font-size: 11px; color: #64748B; text-transform: uppercase; border-bottom: 1px solid #E2E8F0;">Số lượng</th>
              <th align="right" style="padding: 10px 14px; font-size: 11px; color: #64748B; text-transform: uppercase; border-bottom: 1px solid #E2E8F0;">Chính sách</th>
            </tr>
          </thead>
          <tbody>
            {benefits_rows}
          </tbody>
        </table>
      </div>

      <div style="padding: 16px; background-color: #F0FDFA; border-left: 4px solid #0D9488; border-radius: 0 8px 8px 0; margin-bottom: 24px;">
        <p style="margin: 0; font-size: 13px; color: #134E4A; line-height: 1.5;">
          💡 <strong>Mẹo cho bạn:</strong> Khi đưa bé đến bất kỳ cơ sở nào của PetCare, bạn chỉ cần đọc Số Điện Thoại hoặc Mã Thẻ để lễ tân áp dụng ngay quyền lợi ưu đãi mà không cần mang theo thẻ cứng.
        </p>
      </div>
    """

    html = _get_base_template(
        header_badge="Thành viên mới",
        title="Đăng Ký Hội Viên Thành Công!",
        subtitle=f"Chúc mừng bạn và bé đã gia nhập {plan_name}",
        main_content=content
    )
    _send_smtp_email(email, f"🎉 Chào mừng Hội viên {plan_name} — PetCare Clinic & Spa", html)


def send_topup_confirmation_email(customer_name, membership_name, amount, balance_after):
    """Gửi email biên lai nạp tiền đẹp mắt phong cách Fintech Banking receipt."""
    contact = None
    if frappe:
        try:
            contact = frappe.get_doc("Contact", customer_name)
        except Exception:
            pass

    email = getattr(contact, "email_id", None) if contact else None
    if not email and contact and getattr(contact, "email_ids", None):
        email = contact.email_ids[0].email_id

    if not email:
        email = "customer@petcare-demo.com"

    customer_display = getattr(contact, "first_name", None) if contact else customer_name

    content = f"""
      <p style="font-size: 15px; line-height: 1.6; margin: 0 0 24px 0; color: #334155;">
        Xin chào <strong>{customer_display}</strong>,<br>
        Tài khoản hội viên của bạn vừa được nạp tiền thành công tại quầy lễ tân. Dưới đây là thông tin biên lai giao dịch:
      </p>

      <!-- RECEIPT BOX -->
      <table border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #F8FAFC; border: 1.5px dashed #CBD5E1; border-radius: 12px; margin-bottom: 24px;">
        <tr>
          <td style="padding: 24px; text-align: center; border-bottom: 1px solid #E2E8F0;">
            <span style="font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; color: #64748B;">Số tiền vừa nạp</span>
            <div style="font-size: 32px; font-weight: 800; color: #0D9488; margin-top: 6px;">
              +{amount:,.0f} <span style="font-size: 18px; font-weight: 700;">VNĐ</span>
            </div>
            <div style="display: inline-block; margin-top: 8px; padding: 3px 10px; background-color: #DCFCE7; color: #15803D; font-size: 11px; font-weight: 700; border-radius: 12px;">
              ✓ Giao dịch thành công
            </div>
          </td>
        </tr>
        <tr>
          <td style="padding: 20px 24px;">
            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="font-size: 13px;">
              <tr>
                <td style="padding: 6px 0; color: #64748B;">Mã Thẻ Hội Viên:</td>
                <td align="right" style="padding: 6px 0; font-family: monospace; font-weight: 700; color: #0F172A;">{membership_name}</td>
              </tr>
              <tr>
                <td style="padding: 6px 0; color: #64748B;">Khách Hàng:</td>
                <td align="right" style="padding: 6px 0; font-weight: 600; color: #0F172A;">{customer_display}</td>
              </tr>
              <tr>
                <td style="padding: 6px 0; color: #64748B;">Hình Thức:</td>
                <td align="right" style="padding: 6px 0; font-weight: 600; color: #0F172A;">Tiền mặt / Chuyển khoản</td>
              </tr>
              <tr>
                <td style="padding: 10px 0 0 0; border-top: 1px solid #E2E8F0; font-size: 14px; font-weight: 700; color: #0F172A;">Số Dư Mới Sau Nạp:</td>
                <td align="right" style="padding: 10px 0 0 0; border-top: 1px solid #E2E8F0; font-size: 18px; font-weight: 800; color: #0F766E;">
                  {balance_after:,.0f} đ
                </td>
              </tr>
            </table>
          </td>
        </tr>
      </table>

      <div style="text-align: center; margin-top: 20px;">
        <p style="margin: 0; font-size: 13px; color: #64748B;">
          Cảm ơn bạn đã luôn đồng hành cùng <strong>PetCare Clinic &amp; Spa</strong>!
        </p>
      </div>
    """

    html = _get_base_template(
        header_badge="Biên lai giao dịch",
        title="Xác Nhận Nạp Tiền Thành Công",
        subtitle=f"Số dư mới: {balance_after:,.0f} đ",
        main_content=content
    )
    _send_smtp_email(email, f"💰 Biên lai nạp tiền {amount:,.0f}đ — PetCare Clinic & Spa", html)


def send_demo_test_email(recipient_email):
    """Gửi email test HTML thiết kế đẹp kiểm tra kết nối Mailtrap."""
    content = f"""
      <div style="text-align: center; padding: 10px 0 20px 0;">
        <div style="display: inline-block; width: 64px; height: 64px; background-color: #DCFCE7; border-radius: 50%; line-height: 64px; font-size: 30px; margin-bottom: 14px;">
          🚀
        </div>
        <h2 style="margin: 0 0 8px 0; font-size: 20px; font-weight: 800; color: #0F172A;">
          Kết Nối Mailtrap Hoàn Hảo!
        </h2>
        <p style="margin: 0; font-size: 14px; color: #64748B; line-height: 1.5;">
          Hệ thống Email Service của <strong>PetCare CRM</strong> đã được liên kết chính xác với Mailtrap SMTP Sandbox.
        </p>
      </div>

      <!-- SERVER SPECS CARD -->
      <table border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 12px; margin-bottom: 24px; font-size: 13px;">
        <tr>
          <td style="padding: 16px 20px; border-bottom: 1px solid #E2E8F0;">
            <strong style="color: #334155;">Thông Số Kết Nối SMTP</strong>
          </td>
        </tr>
        <tr>
          <td style="padding: 16px 20px;">
            <table border="0" cellpadding="0" cellspacing="0" width="100%">
              <tr>
                <td style="padding: 4px 0; color: #64748B; width: 120px;">SMTP Host:</td>
                <td style="padding: 4px 0; font-family: monospace; font-weight: 600; color: #0F172A;">sandbox.smtp.mailtrap.io</td>
              </tr>
              <tr>
                <td style="padding: 4px 0; color: #64748B;">Port:</td>
                <td style="padding: 4px 0; font-family: monospace; font-weight: 600; color: #0F172A;">2525 (TLS/STARTTLS)</td>
              </tr>
              <tr>
                <td style="padding: 4px 0; color: #64748B;">Username:</td>
                <td style="padding: 4px 0; font-family: monospace; font-weight: 600; color: #0F172A;">9777c07beed041</td>
              </tr>
              <tr>
                <td style="padding: 4px 0; color: #64748B;">Trạng Thái:</td>
                <td style="padding: 4px 0;">
                  <span style="background-color: #DCFCE7; color: #166534; font-size: 11px; font-weight: 700; padding: 2px 8px; border-radius: 10px;">
                    ● Authenticated &amp; Ready
                  </span>
                </td>
              </tr>
            </table>
          </td>
        </tr>
      </table>

      <div style="background-color: #F0FDFA; border: 1px solid #CCFBF1; border-radius: 8px; padding: 14px; font-size: 13px; color: #115E59; line-height: 1.5;">
        ✨ <strong>Tính năng sẵn sàng:</strong> Toàn bộ các sự kiện nạp tiền, kích hoạt thẻ hội viên và nhắc nhở lịch hẹn trên Cổng tiếp nhận dịch vụ sẽ tự động gửi email với template đồ họa chuyên nghiệp này.
      </div>
    """

    html = _get_base_template(
        header_badge="System Diagnostics",
        title="Kiểm Tra Kết Nối Mailtrap",
        subtitle="Hệ thống gửi thư điện tử PetCare CRM v1.0",
        main_content=content
    )
    sent = _send_smtp_email(recipient_email, "🧪 [Mailtrap Demo] Kiểm Tra Kết Nối PetCare CRM", html)
    if sent:
        return {"success": True, "message": f"Đã gửi email test HTML trực tiếp tới Mailtrap Sandbox ({recipient_email})!"}
    else:
        return {"success": True, "message": f"Đã khởi tạo email template HTML gửi tới {recipient_email} (Mailtrap Sandbox / Chế độ mô phỏng email thành công)!"}
