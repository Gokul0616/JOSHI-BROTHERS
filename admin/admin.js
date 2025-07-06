const API_BASE_URL = 'http://localhost:8001/api';
let adminToken = localStorage.getItem('adminToken');
let currentSection = 'dashboard';

// Initialize the admin panel
document.addEventListener('DOMContentLoaded', function() {
    if (adminToken) {
        showAdminPanel();
        loadDashboard();
    } else {
        showLoginModal();
    }

    // Set up event listeners
    setupEventListeners();
});

function setupEventListeners() {
    // Login form
    document.getElementById('loginForm').addEventListener('submit', handleLogin);
    
    // Logout button
    document.getElementById('logoutBtn').addEventListener('click', handleLogout);
    
    // Sidebar toggle
    document.getElementById('sidebarToggle').addEventListener('click', toggleSidebar);
    
    // Sidebar overlay
    document.getElementById('sidebarOverlay').addEventListener('click', closeSidebar);
}

async function handleLogin(e) {
    e.preventDefault();
    
    const email = document.getElementById('adminEmail').value;
    const password = document.getElementById('adminPassword').value;
    const errorDiv = document.getElementById('loginError');
    
    try {
        const response = await fetch(`${API_BASE_URL}/admin/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password }),
        });
        
        if (response.ok) {
            const data = await response.json();
            adminToken = data.token;
            localStorage.setItem('adminToken', adminToken);
            localStorage.setItem('adminName', data.admin.name);
            
            showAdminPanel();
            loadDashboard();
            errorDiv.classList.add('hidden');
        } else {
            const error = await response.json();
            errorDiv.textContent = error.detail || 'Login failed';
            errorDiv.classList.remove('hidden');
        }
    } catch (error) {
        errorDiv.textContent = 'Network error. Please try again.';
        errorDiv.classList.remove('hidden');
    }
}

function handleLogout() {
    adminToken = null;
    localStorage.removeItem('adminToken');
    localStorage.removeItem('adminName');
    showLoginModal();
}

function showLoginModal() {
    document.getElementById('loginModal').classList.add('active');
    document.getElementById('adminPanel').classList.add('hidden');
}

function showAdminPanel() {
    document.getElementById('loginModal').classList.remove('active');
    document.getElementById('adminPanel').classList.remove('hidden');
    
    const adminName = localStorage.getItem('adminName');
    document.getElementById('adminName').textContent = adminName || 'Admin';
}

function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebarOverlay');
    
    sidebar.classList.toggle('closed');
    overlay.classList.toggle('hidden');
}

function closeSidebar() {
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebarOverlay');
    
    sidebar.classList.add('closed');
    overlay.classList.add('hidden');
}

function hideAllSections() {
    const sections = document.querySelectorAll('.content-section');
    sections.forEach(section => section.classList.add('hidden'));
    
    // Remove active class from nav links
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => link.classList.remove('bg-gray-700'));
}

function showSection(sectionId) {
    hideAllSections();
    document.getElementById(sectionId).classList.remove('hidden');
    currentSection = sectionId.replace('Content', '');
    
    // Close mobile sidebar
    closeSidebar();
}

async function makeAuthenticatedRequest(url, options = {}) {
    const headers = {
        'Authorization': `Bearer ${adminToken}`,
        'Content-Type': 'application/json',
        ...options.headers,
    };
    
    const response = await fetch(url, {
        ...options,
        headers,
    });
    
    if (response.status === 401) {
        handleLogout();
        throw new Error('Authentication failed');
    }
    
    return response;
}

// Dashboard functions
async function showDashboard() {
    showSection('dashboardContent');
    await loadDashboard();
}

async function loadDashboard() {
    try {
        const response = await makeAuthenticatedRequest(`${API_BASE_URL}/admin/dashboard`);
        const data = await response.json();
        
        // Update statistics
        const stats = data.statistics;
        document.getElementById('totalProducts').textContent = stats.total_products;
        document.getElementById('totalCategories').textContent = stats.total_categories;
        document.getElementById('totalBrands').textContent = stats.total_brands;
        document.getElementById('totalUsers').textContent = stats.total_users;
        document.getElementById('totalOrders').textContent = stats.total_orders;
        
        // Update recent orders table
        const ordersTable = document.getElementById('recentOrdersTable');
        ordersTable.innerHTML = '';
        
        data.recent_orders.forEach(order => {
            const row = document.createElement('tr');
            const orderDate = new Date(order.order_date).toLocaleDateString();
            
            row.innerHTML = `
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    #${order.id.substring(0, 8)}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    ${order.user_details ? order.user_details.name : 'Unknown'}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    ₹${order.total_amount.toFixed(2)}
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                    <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${getStatusBadgeClass(order.status)}">
                        ${order.status}
                    </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    ${orderDate}
                </td>
            `;
            ordersTable.appendChild(row);
        });
        
    } catch (error) {
        console.error('Error loading dashboard:', error);
    }
}

function getStatusBadgeClass(status) {
    switch (status) {
        case 'pending':
            return 'bg-yellow-100 text-yellow-800';
        case 'confirmed':
            return 'bg-blue-100 text-blue-800';
        case 'delivered':
            return 'bg-green-100 text-green-800';
        case 'cancelled':
            return 'bg-red-100 text-red-800';
        default:
            return 'bg-gray-100 text-gray-800';
    }
}

// Products functions
async function showProducts() {
    showSection('productsContent');
    await loadProducts();
}

async function loadProducts() {
    try {
        const response = await makeAuthenticatedRequest(`${API_BASE_URL}/products`);
        const data = await response.json();
        
        const productsTable = document.getElementById('productsTable');
        productsTable.innerHTML = '';
        
        data.products.forEach(product => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td class="px-6 py-4 whitespace-nowrap">
                    <div class="flex items-center">
                        <img class="h-10 w-10 rounded-lg object-cover mr-4" src="${product.image_url}" alt="${product.name}">
                        <div>
                            <div class="text-sm font-medium text-gray-900">${product.name}</div>
                            <div class="text-sm text-gray-500">${product.description.substring(0, 50)}...</div>
                        </div>
                    </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${product.category}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${product.brand}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">₹${product.price}</td>
                <td class="px-6 py-4 whitespace-nowrap">
                    <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${product.stock > 0 ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}">
                        ${product.stock}
                    </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <button onclick="editProduct('${product.id}')" class="text-indigo-600 hover:text-indigo-900 mr-4">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button onclick="deleteProduct('${product.id}')" class="text-red-600 hover:text-red-900">
                        <i class="fas fa-trash"></i>
                    </button>
                </td>
            `;
            productsTable.appendChild(row);
        });
        
    } catch (error) {
        console.error('Error loading products:', error);
    }
}

function showAddProductModal() {
    // This would open a modal for adding new products
    alert('Add Product functionality would be implemented here');
}

function editProduct(productId) {
    // This would open an edit modal for the product
    alert(`Edit Product ${productId} functionality would be implemented here`);
}

async function deleteProduct(productId) {
    if (confirm('Are you sure you want to delete this product?')) {
        try {
            const response = await makeAuthenticatedRequest(`${API_BASE_URL}/admin/products/${productId}`, {
                method: 'DELETE',
            });
            
            if (response.ok) {
                alert('Product deleted successfully');
                loadProducts();
            } else {
                const error = await response.json();
                alert(error.detail || 'Failed to delete product');
            }
        } catch (error) {
            console.error('Error deleting product:', error);
            alert('Failed to delete product');
        }
    }
}

// Categories functions
function showCategories() {
    showSection('categoriesContent');
    // Load categories logic would go here
}

// Brands functions
function showBrands() {
    showSection('brandsContent');
    // Load brands logic would go here
}

// Orders functions
function showOrders() {
    showSection('ordersContent');
    // Load orders logic would go here
}

// Users functions
function showUsers() {
    showSection('usersContent');
    // Load users logic would go here
}