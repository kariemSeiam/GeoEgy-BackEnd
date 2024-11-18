// script.js

// Check if the user is authenticated
function isAuthenticated() {
    return localStorage.getItem('access_token') !== null;
}

// Handle user login
function handleLogin(event) {
    event.preventDefault();
    const phoneNumber = document.getElementById('phone-number').value.trim();

    if (!phoneNumber) {
        alert('يرجى إدخال رقم الهاتف');
        return;
    }

    fetch('/api/user/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ phone_number: phoneNumber })
    })
    .then(response => response.json())
    .then(data => {
        if (data.code === 200) {
            localStorage.setItem('access_token', data.data.access_token);
            initializeApp();
        } else {
            alert(data.message || 'خطأ في تسجيل الدخول');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('حدث خطأ أثناء تسجيل الدخول');
    });
}

// Initialize the application
function initializeApp() {
    document.getElementById('login-container').style.display = 'none';
    document.getElementById('main-container').style.display = 'block';
    fetchUserProfile();
    setupEventListeners();
}

// Fetch user profile
function fetchUserProfile() {
    fetch('/api/user/profile', {
        headers: { 'Authorization': 'Bearer ' + localStorage.getItem('access_token') }
    })
    .then(response => response.json())
    .then(data => {
        if (data.code === 200) {
            const user = data.data;
            if (user.is_blocked) {
                alert('حسابك محظور. يرجى الاتصال بالإدارة.');
                logout();
            }
        } else {
            alert(data.message || 'خطأ في جلب بيانات المستخدم');
            logout();
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('حدث خطأ أثناء جلب بيانات المستخدم');
        logout();
    });
}

// Logout function
function logout() {
    localStorage.removeItem('access_token');
    location.reload();
}

// Setup event listeners
function setupEventListeners() {
    // Logout button
    document.getElementById('logout-btn').addEventListener('click', logout);

    // Buy data button
    document.getElementById('buy-data-btn').addEventListener('click', openBuyModal);

    // Search input
    document.getElementById('search-input').addEventListener('input', debounce(applySearch, 500));

    // Theme toggle button
    document.getElementById('toggle-theme-btn').addEventListener('click', toggleTheme);

    // Back to top button
    window.addEventListener('scroll', handleScroll);
    document.getElementById('back-to-top').addEventListener('click', scrollToTop);

    // Buy form submission
    document.getElementById('buy-form').addEventListener('submit', handleBuyFormSubmit);

    // WhatsApp option change
    document.querySelectorAll('input[name="whatsappOption"]').forEach(input => {
        input.addEventListener('change', toggleWhatsAppInput);
    });

    // Select all governorates
    document.getElementById('select-all').addEventListener('change', toggleSelectAllGovernorates);

    // Load governorates list
    loadGovernorates();
}

// Apply search
function applySearch() {
    const query = document.getElementById('search-input').value.trim();
    if (!query) {
        renderData([]);
        return;
    }

    fetch(`/api/search/places?query=${encodeURIComponent(query)}`, {
        headers: { 'Authorization': 'Bearer ' + localStorage.getItem('access_token') }
    })
    .then(response => response.json())
    .then(data => {
        if (data.code === 200) {
            renderData(data.data);
        } else {
            alert(data.message || 'خطأ في البحث');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('حدث خطأ أثناء البحث');
    });
}

// Render data
function renderData(places) {
    const dataGrid = document.getElementById('data-grid');
    dataGrid.innerHTML = '';

    if (places.length === 0) {
        dataGrid.innerHTML = '<p class="no-results">لم يتم العثور على نتائج.</p>';
        return;
    }

    places.forEach(place => {
        const card = document.createElement('div');
        card.className = 'data-card';

        const title = document.createElement('h2');
        title.textContent = place.name || 'اسم غير متوفر';
        card.appendChild(title);

        // Add more place details as needed

        dataGrid.appendChild(card);
    });
}

// Open buy modal
function openBuyModal() {
    document.getElementById('buy-modal').style.display = 'flex';
}

// Close buy modal
function closeBuyModal() {
    document.getElementById('buy-modal').style.display = 'none';
}

// Handle buy form submission
function handleBuyFormSubmit(event) {
    event.preventDefault();

    const placeName = document.getElementById('place-name-input').value.trim();
    const businessDetails = document.getElementById('business-info').value.trim();
    const selectedGovernorates = getSelectedGovernorates();
    const whatsappOption = document.querySelector('input[name="whatsappOption"]:checked').value;
    let whatsappNumber = null;

    if (whatsappOption === 'no') {
        whatsappNumber = document.getElementById('whatsapp-number').value.trim();
        if (!whatsappNumber) {
            alert('يرجى إدخال رقم واتساب الخاص بك');
            return;
        }
    }

    if (!placeName || selectedGovernorates.length === 0) {
        alert('يرجى إدخال الأماكن التي تريد البحث عنها واختيار محافظة واحدة على الأقل.');
        return;
    }

    const orderData = {
        place_name: placeName,
        business_details: businessDetails,
        selected_govs: selectedGovernorates,
        whatsapp_number: whatsappNumber
    };

    fetch('/api/order/place', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + localStorage.getItem('access_token')
        },
        body: JSON.stringify(orderData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.code === 201) {
            alert('تم إرسال طلبك بنجاح. سيتم التواصل معك قريبًا.');
            closeBuyModal();
        } else {
            alert(data.message || 'خطأ في إرسال الطلب');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('حدث خطأ أثناء إرسال الطلب');
    });
}

// Get selected governorates
function getSelectedGovernorates() {
    const selected = [];
    if (document.getElementById('select-all').checked) {
        selected.push('كل محافظات مصر');
    } else {
        document.querySelectorAll('.governorate-checkbox:checked').forEach(checkbox => {
            selected.push(checkbox.value);
        });
    }
    return selected;
}

// Toggle WhatsApp input field
function toggleWhatsAppInput() {
    const whatsappOption = document.querySelector('input[name="whatsappOption"]:checked').value;
    if (whatsappOption === 'no') {
        document.getElementById('whatsapp-number-section').style.display = 'block';
    } else {
        document.getElementById('whatsapp-number-section').style.display = 'none';
    }
}

// Toggle select all governorates
function toggleSelectAllGovernorates() {
    const checked = this.checked;
    document.querySelectorAll('.governorate-checkbox').forEach(checkbox => {
        checkbox.checked = checked;
    });
    updateTotalPrice();
}

// Load governorates list
function loadGovernorates() {
    fetch('/api/admin/governorates', {
        headers: { 'Authorization': 'Bearer ' + localStorage.getItem('access_token') }
    })
    .then(response => response.json())
    .then(data => {
        if (data.code === 200) {
            const govList = document.getElementById('governorates-list');
            data.data.forEach(gov => {
                const label = document.createElement('label');
                label.className = 'modal__option';

                const input = document.createElement('input');
                input.type = 'checkbox';
                input.value = gov.name;
                input.className = 'governorate-checkbox';
                input.addEventListener('change', updateTotalPrice);

                const span = document.createElement('span');
                span.textContent = `${gov.name} - ${gov.price} جنيه`;

                label.appendChild(input);
                label.appendChild(span);
                govList.appendChild(label);
            });
        } else {
            alert(data.message || 'خطأ في جلب المحافظات');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('حدث خطأ أثناء جلب المحافظات');
    });
}

// Update total price
function updateTotalPrice() {
    let totalPrice = 0;
    const selectedGovernorates = getSelectedGovernorates();

    if (selectedGovernorates.includes('كل محافظات مصر')) {
        totalPrice = 4000; // Assuming fixed price for all
    } else {
        document.querySelectorAll('.governorate-checkbox:checked').forEach(checkbox => {
            const priceText = checkbox.nextSibling.textContent;
            const price = parseFloat(priceText.match(/\d+/)[0]);
            totalPrice += price;
        });
    }

    document.getElementById('total-price').textContent = `${totalPrice} جنيه مصري`;
}

// Debounce function
function debounce(func, wait) {
    let timeout;
    return function () {
        clearTimeout(timeout);
        timeout = setTimeout(func, wait);
    };
}

// Handle scroll for back to top button
function handleScroll() {
    const backToTopBtn = document.getElementById('back-to-top');
    if (window.scrollY > 300) {
        backToTopBtn.style.display = 'flex';
    } else {
        backToTopBtn.style.display = 'none';
    }
}

// Scroll to top
function scrollToTop() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Toggle theme
function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
    const targetTheme = currentTheme === 'light' ? 'dark' : 'light';
    document.documentElement.setAttribute('data-theme', targetTheme);
    const icon = document.getElementById('toggle-theme-btn').querySelector('i');
    icon.className = targetTheme === 'light' ? 'fas fa-moon' : 'fas fa-sun';
}

// Initialize application on DOMContentLoaded
document.addEventListener('DOMContentLoaded', () => {
    if (isAuthenticated()) {
        initializeApp();
    } else {
        document.getElementById('login-container').style.display = 'flex';
        document.getElementById('main-container').style.display = 'none';
        document.getElementById('login-form').addEventListener('submit', handleLogin);
    }

    // Close modals when clicking outside
    window.addEventListener('click', (e) => {
        if (e.target.classList.contains('modal')) {
            e.target.style.display = 'none';
        }
    });

    // Close modal when clicking close button
    document.querySelectorAll('.modal__close-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            btn.closest('.modal').style.display = 'none';
        });
    });
});
