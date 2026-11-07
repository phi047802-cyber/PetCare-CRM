/**
 * PetCare CRM Lead Capture Frontend Script
 * Vanilla JavaScript (No jQuery dependency), Accessible, Double-submit prevention
 */

document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('petcare-lead-form');
    if (!form) return;

    const submitBtn = document.getElementById('petcare-submit-btn');
    const btnText = submitBtn.querySelector('.petcare-btn-text');
    const btnSpinner = submitBtn.querySelector('.petcare-spinner');
    const alertBox = document.getElementById('petcare-form-alert');

    const nameInput = document.getElementById('petcare_lead_name');
    const phoneInput = document.getElementById('petcare_phone');
    const emailInput = document.getElementById('petcare_email');
    const serviceSelect = document.getElementById('petcare_service_type');
    const petInfoInput = document.getElementById('petcare_pet_info');
    const hpInput = document.getElementById('petcare_hp_website');

    const errorName = document.getElementById('error_lead_name');
    const errorPhone = document.getElementById('error_phone');
    const errorEmail = document.getElementById('error_email');

    // Cấu hình endpoint từ WordPress wp_localize_script (hoặc fallback)
    const restEndpoint = (window.PetCareConfig && window.PetCareConfig.rest_url) 
                         ? window.PetCareConfig.rest_url 
                         : '/wp-json/petcare/v1/lead';
    const restNonce = (window.PetCareConfig && window.PetCareConfig.nonce) 
                      ? window.PetCareConfig.nonce 
                      : '';

    // Hàm hiển thị thông báo
    function showAlert(type, message) {
        alertBox.className = 'petcare-alert petcare-alert-' + type;
        alertBox.textContent = message;
        alertBox.classList.remove('petcare-hidden');
        alertBox.focus(); // Hỗ trợ Accessibility ARIA Live
    }

    function hideAlert() {
        alertBox.className = 'petcare-alert petcare-hidden';
        alertBox.textContent = '';
    }

    // Xóa lỗi trường
    function clearFieldError(input, errorEl) {
        input.classList.remove('petcare-has-error');
        errorEl.classList.remove('petcare-visible');
        errorEl.textContent = '';
    }

    function setFieldError(input, errorEl, message) {
        input.classList.add('petcare-has-error');
        errorEl.textContent = message;
        errorEl.classList.add('petcare-visible');
    }

    // Xóa lỗi khi người dùng gõ
    nameInput.addEventListener('input', function () {
        clearFieldError(nameInput, errorName);
    });
    phoneInput.addEventListener('input', function () {
        clearFieldError(phoneInput, errorPhone);
    });
    if (emailInput) {
        emailInput.addEventListener('input', function () {
            clearFieldError(emailInput, errorEmail);
        });
    }

    // Bắt sự kiện Submit
    form.addEventListener('submit', async function (e) {
        e.preventDefault();
        hideAlert();

        let hasError = false;

        // 1. Client-side Validation: Họ tên
        const nameVal = nameInput.value.trim();
        if (!nameVal) {
            setFieldError(nameInput, errorName, 'Vui lòng nhập họ và tên của bạn.');
            hasError = true;
        }

        // 2. Client-side Validation: Số điện thoại Việt Nam
        let phoneVal = phoneInput.value.trim().replace(/[\s\-\.]/g, '');
        if (phoneVal.startsWith('+84')) {
            phoneVal = '0' + phoneVal.substring(3);
        }

        const phoneRegex = /^0[0-9]{8,10}$/;
        if (!phoneVal) {
            setFieldError(phoneInput, errorPhone, 'Vui lòng nhập số điện thoại liên hệ.');
            hasError = true;
        } else if (!phoneRegex.test(phoneVal)) {
            setFieldError(phoneInput, errorPhone, 'Số điện thoại không hợp lệ (cần là SĐT Việt Nam 10 chữ số, ví dụ 0912345678).');
            hasError = true;
        }

        // 3. Client-side Validation: Email (nếu có)
        const emailVal = emailInput ? emailInput.value.trim() : '';
        if (emailVal) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(emailVal)) {
                setFieldError(emailInput, errorEmail, 'Địa chỉ email không đúng định dạng.');
                hasError = true;
            }
        }

        if (hasError) {
            return;
        }

        // 4. Chuyển sang Trạng thái 2: Đang gửi (Submitting State)
        const originalBtnText = btnText.textContent;
        submitBtn.disabled = true;
        btnText.textContent = 'Đang gửi thông tin...';
        btnSpinner.classList.remove('petcare-hidden');

        // Chuẩn bị Payload
        const payload = {
            lead_name: nameVal,
            phone: phoneVal,
            email: emailVal,
            service_type: serviceSelect ? serviceSelect.value : '',
            pet_info: petInfoInput ? petInfoInput.value.trim() : '',
            petcare_hp_website: hpInput ? hpInput.value.trim() : '', // Honeypot trap
        };

        try {
            const response = await fetch(restEndpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-WP-Nonce': restNonce,
                },
                body: JSON.stringify(payload),
            });

            const data = await response.json();

            if (response.ok && data.success) {
                // Trạng thái 3A: Thành công (Success State)
                form.reset();
                showAlert('success', data.message || 'Gửi thông tin thành công! Tư vấn viên PetCare sẽ liên hệ sớm nhất.');
                submitBtn.disabled = false;
                btnText.textContent = 'Đã Gửi Thành Công ✓';
                btnSpinner.classList.add('petcare-hidden');

                // Khôi phục nút sau 4 giây
                setTimeout(function () {
                    btnText.textContent = originalBtnText;
                }, 4000);
            } else {
                // Trạng thái 3B: Thất bại (Error State)
                const errorMsg = data.message || 'Đã có lỗi xảy ra. Vui lòng kiểm tra lại thông tin hoặc thử lại sau.';
                showAlert('error', '⚠️ ' + errorMsg);
                submitBtn.disabled = false;
                btnText.textContent = originalBtnText;
                btnSpinner.classList.add('petcare-hidden');
            }
        } catch (err) {
            // Lỗi mạng hoặc hạ tầng
            showAlert('error', '⚠️ Không thể kết nối đến máy chủ. Vui lòng kiểm tra kết nối mạng hoặc gọi hotline để được hỗ trợ.');
            submitBtn.disabled = false;
            btnText.textContent = originalBtnText;
            btnSpinner.classList.add('petcare-hidden');
        }
    });
});
