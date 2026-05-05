import axios from 'axios';

const API_BASE = 'http://localhost:8000';

const api = axios.create({
    baseURL: API_BASE,
    headers: {
        'Content-Type': 'application/json',
    }
});

export const apiService = {
    // Core endpoints
    getHome: () => api.get('/'),
    
    getHealth: () => api.get('/health'),
    
    getStats: () => api.get('/stats'),
    
    // Analysis endpoints
    analyze: () => api.get('/analyze'),
    
    analyzeWithEmail: (email) => api.get(`/analyze-email/${email}`),
    
    // Reports endpoints
    getReports: () => api.get('/reports'),
    
    getSupabaseReports: () => api.get('/reports-supabase'),
    
    clearReports: () => api.delete('/reports'),
    
    // Email endpoint
    sendEmail: (email) => api.post('/send-email', { email }),
    
    // Export endpoints
    exportPDF: () => api.get('/export', { responseType: 'blob' }),
    
    // Google endpoint
    googleUsers: (accessToken) => api.post('/google-users', { access_token: accessToken }),
};

export default api;
