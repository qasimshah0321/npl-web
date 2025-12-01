// Main JavaScript - Shared utilities and functions

const API_BASE = '';

// Check authentication status
async function checkAuth() {
    try {
        const response = await fetch(`${API_BASE}/api/auth/check`, {
            credentials: 'include'
        });
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Auth check failed:', error);
        return { authenticated: false };
    }
}

// Update navigation based on auth status
async function updateNavigation() {
    const auth = await checkAuth();
    const loginBtn = document.getElementById('loginBtn');
    const logoutBtn = document.getElementById('logoutBtn');
    const adminLink = document.getElementById('adminLink');

    if (auth.authenticated) {
        if (loginBtn) loginBtn.style.display = 'none';
        if (logoutBtn) logoutBtn.style.display = 'inline-block';
        if (adminLink && auth.user.role === 'admin') {
            adminLink.style.display = 'inline-block';
        }
    } else {
        if (loginBtn) loginBtn.style.display = 'inline-block';
        if (logoutBtn) logoutBtn.style.display = 'none';
        if (adminLink) adminLink.style.display = 'none';
    }
}

// Logout function
async function logout() {
    try {
        await fetch(`${API_BASE}/api/auth/logout`, {
            method: 'POST',
            credentials: 'include'
        });
        window.location.href = '/index.html';
    } catch (error) {
        console.error('Logout failed:', error);
    }
}

// Format date
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

// Show loading state
function showLoading(containerId) {
    const container = document.getElementById(containerId);
    if (container) {
        container.innerHTML = '<div class="loading">Loading...</div>';
    }
}

// Show empty state
function showEmptyState(containerId, message) {
    const container = document.getElementById(containerId);
    if (container) {
        container.innerHTML = `<div class="empty-state">${message}</div>`;
    }
}

// Show error message
function showError(message) {
    alert(`Error: ${message}`);
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    updateNavigation();
});
