import ApiService from '../services/apiService.js';

async function testDatabaseConnection() {
    try {
        const response = await ApiService.makeRequest('/health-check');
        console.log('Database connection:', response.status);
        return true;
    } catch (error) {
        console.error('Database connection failed:', error);
        return false;
    }
}

// Test on page load
document.addEventListener('DOMContentLoaded', testDatabaseConnection); 