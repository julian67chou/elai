// 伊萊診所網站 JavaScript
// 主要功能：導覽列、表單處理、動畫效果

// 等待 DOM 完全載入
document.addEventListener('DOMContentLoaded', function() {
    initClinicSite();
});

// 初始化診所網站
function initClinicSite() {
    // 設定最後更新日期
    setLastUpdated();
    
    // 初始化導覽列滾動效果
    initNavbarScroll();
    
    // 初始化平滑滾動
    initSmoothScroll();
    
    // 初始化表單處理
    initForms();
    
    // 初始化預約功能
    initAppointmentForm();
    
    // 初始化健康資訊篩選
    initHealthInfoFilter();
    
    // 初始化緊急聯絡提示
    initEmergencyNotice();
    
    // 顯示載入完成訊息
    console.log('伊萊診所網站已載入完成');
}

// 設定最後更新日期
function setLastUpdated() {
    const elements = document.querySelectorAll('#last-updated, .last-updated');
    if (elements.length > 0) {
        const now = new Date();
        const dateString = now.toLocaleDateString('zh-TW', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            weekday: 'long'
        });
        elements.forEach(el => {
            el.textContent = dateString;
        });
    }
}

// 導覽列滾動效果
function initNavbarScroll() {
    const navbar = document.querySelector('.navbar');
    if (!navbar) return;
    
    window.addEventListener('scroll', function() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        if (scrollTop > 100) {
            navbar.classList.add('shadow-medium');
            navbar.classList.remove('bg-light');
            navbar.classList.add('bg-white');
        } else {
            navbar.classList.remove('shadow-medium');
            navbar.classList.remove('bg-white');
            navbar.classList.add('bg-light');
        }
    });
}

// 平滑滾動
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            
            // 如果是空連結或 #，不處理
            if (href === '#' || href === '') return;
            
            const target = document.querySelector(href);
            if (target) {
                e.preventDefault();
                
                window.scrollTo({
                    top: target.offsetTop - 100,
                    behavior: 'smooth'
                });
                
                // 更新 URL（不重新載入頁面）
                history.pushState(null, null, href);
            }
        });
    });
}

// 表單處理（聯絡我們）
function initForms() {
    const contactForm = document.getElementById('contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // 簡單的表單驗證
            const name = document.getElementById('name')?.value.trim();
            const phone = document.getElementById('phone')?.value.trim();
            const email = document.getElementById('email')?.value.trim();
            const message = document.getElementById('message')?.value.trim();
            
            if (!name || !phone || !message) {
                showAlert('請填寫所有必填欄位（姓名、電話、訊息）', 'danger');
                return;
            }
            
            if (email && !isValidEmail(email)) {
                showAlert('請輸入有效的電子郵件地址', 'danger');
                return;
            }
            
            // 顯示成功訊息
            showAlert('感謝您的訊息！我們會盡快與您聯絡。', 'success');
            
            // 重置表單
            contactForm.reset();
            
            // 在實際應用中，這裡會發送資料到後端
            // sendFormData({ name, phone, email, message });
        });
    }
}

// 預約表單處理（使用 FormSubmit.co）
function initAppointmentForm() {
    const appointmentForm = document.getElementById('appointment-form');
    if (appointmentForm) {
        // 表單已有 action 指向 FormSubmit，submit 沖由 HTML 處理
        // 僅保留客戶端驗證（防止空表單提交）
        appointmentForm.addEventListener('submit', function(e) {
            const name = document.getElementById('name')?.value.trim();
            const phone = document.getElementById('phone')?.value.trim();
            const date = document.getElementById('date')?.value;
            const service = document.getElementById('service')?.value;
            
            if (!name || !phone || !date || !service) {
                e.preventDefault();
                showAlert('請填寫所有必填欄位（姓名、電話、預約日期、服務項目）', 'danger');
            }
            // 驗證通過 → 不 preventDefault，讓 FormSubmit 處理
        });
    }
}

// 健康資訊篩選
function initHealthInfoFilter() {
    const filterButtons = document.querySelectorAll('.health-filter-btn');
    const healthCards = document.querySelectorAll('.health-card');
    
    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            const filter = this.getAttribute('data-filter');
            
            // 更新按鈕狀態
            filterButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            
            // 篩選卡片
            healthCards.forEach(card => {
                if (filter === 'all' || card.getAttribute('data-category') === filter) {
                    card.style.display = 'block';
                    setTimeout(() => {
                        card.classList.add('fade-in-up');
                    }, 100);
                } else {
                    card.style.display = 'none';
                    card.classList.remove('fade-in-up');
                }
            });
        });
    });
}

// 緊急聯絡提示
function initEmergencyNotice() {
    const emergencyBtn = document.getElementById('emergency-call-btn');
    if (emergencyBtn) {
        emergencyBtn.addEventListener('click', function() {
            if (confirm('緊急情況請直接撥打 119 或急診專線。是否要顯示附近醫院資訊？')) {
                showAlert('附近醫院：宜蘭陽明醫院 (03) 932-5192，羅東博愛醫院 (03) 954-3131', 'info');
            }
        });
    }
}

// 電子郵件驗證
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// 顯示提示訊息
function showAlert(message, type = 'info') {
    // 移除現有的提示
    const existingAlert = document.querySelector('.custom-alert');
    if (existingAlert) existingAlert.remove();
    
    // 建立新的提示
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} custom-alert position-fixed top-0 start-50 translate-middle-x mt-3 shadow`;
    alertDiv.style.zIndex = '9999';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close float-end" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alertDiv);
    
    // 自動消失
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
}

// 電話號碼格式化
function formatPhoneNumber(phone) {
    const cleaned = ('' + phone).replace(/\D/g, '');
    const match = cleaned.match(/^(\d{2})(\d{4})(\d{4})$/);
    if (match) {
        return `(${match[1]}) ${match[2]}-${match[3]}`;
    }
    return phone;
}

// 開啟地圖
function openMap() {
    // 預設宜蘭市的位置
    const address = encodeURIComponent('宜蘭市');
    window.open(`https://www.google.com/maps/search/?api=1&query=${address}`, '_blank');
}

// 分享診所資訊
function shareClinic() {
    if (navigator.share) {
        navigator.share({
            title: '伊萊診所 - 自然醫學、整合醫學、預防醫學',
            text: '伊萊診所提供專業的自然醫學、整合醫學、預防醫學與能量醫學服務。',
            url: window.location.href
        });
    } else {
        // 複製連結到剪貼簿
        navigator.clipboard.writeText(window.location.href)
            .then(() => showAlert('診所連結已複製到剪貼簿', 'success'))
            .catch(() => showAlert('無法複製連結', 'danger'));
    }
}

// 生成頁面PDF（供下載）
function generateClinicPDF() {
    // 使用瀏覽器列印功能
    window.print();
}

// 導出函數供全域使用
window.shareClinic = shareClinic;
window.generateClinicPDF = generateClinicPDF;
window.openMap = openMap;