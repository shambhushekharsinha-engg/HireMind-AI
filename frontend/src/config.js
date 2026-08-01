// Centralized Dynamic API Base URL configuration
// Always resolves dynamically to ensure Vercel production deployments use live Render backend
export const getApiBaseUrl = () => {
  // 1. User manual override stored in browser localStorage
  if (typeof window !== 'undefined') {
    try {
      const custom = localStorage.getItem('hiremind_api_url');
      if (custom && custom.trim()) {
        return custom.trim().replace(/\/$/, "");
      }
    } catch (e) {
      // Ignore localStorage errors
    }
  }

  // 2. If running in browser on production Vercel deployment (non-localhost), ALWAYS default to live Render backend
  if (typeof window !== 'undefined' && window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1') {
    return "https://hiremind-ai-au7b.onrender.com";
  }

  // 3. Environment Variable VITE_API_BASE_URL (only if valid non-localhost URL)
  const envUrl = typeof import.meta !== 'undefined' && import.meta.env ? import.meta.env.VITE_API_BASE_URL : null;
  if (envUrl && envUrl.trim() && !envUrl.includes('localhost') && !envUrl.includes('127.0.0.1')) {
    return envUrl.trim().replace(/\/$/, "");
  }

  // 4. Default for local development
  return "http://127.0.0.1:8000";
};

export const API_BASE_URL = getApiBaseUrl();
