import config from '../config/config.js';

class ApiService {
    static async makeRequest(endpoint, options = {}) {
        try {
            const response = await fetch(`${config.API_URL}${endpoint}`, {
                ...options,
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('token')}`,
                    ...options.headers
                },
            });

            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.message || 'Something went wrong');
            }

            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    // User related APIs
    static async registerUser(userData) {
        return this.makeRequest('/auth/register', {
            method: 'POST',
            body: JSON.stringify(userData)
        });
    }

    static async loginUser(credentials) {
        return this.makeRequest('/auth/login', {
            method: 'POST',
            body: JSON.stringify(credentials)
        });
    }

    // Chat related APIs
    static async getChatHistory() {
        return this.makeRequest('/chat/history');
    }

    static async sendMessage(message) {
        return this.makeRequest('/chat/send', {
            method: 'POST',
            body: JSON.stringify({ message })
        });
    }
}

export default ApiService; 