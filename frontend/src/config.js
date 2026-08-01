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

  // 2. Vite Environment Variable VITE_API_BASE_URL
  const envUrl = typeof import.meta !== 'undefined' && import.meta.env ? import.meta.env.VITE_API_BASE_URL : null;
  if (envUrl && envUrl.trim()) {
    return envUrl.trim().replace(/\/$/, "");
  }

  // 3. Localhost check (only if explicitly running on localhost or 127.0.0.1)
  if (typeof window !== 'undefined' && (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1')) {
    return "http://127.0.0.1:8000";
  }

  // 4. Default for production Vercel deployment or build-time evaluation
  return "https://hiremind-ai-au7b.onrender.com";
};

// Export API_BASE_URL object with dynamic toString() to guarantee runtime evaluation
export const API_BASE_URL = {
  toString() {
    return getApiBaseUrl();
  },
  valueOf() {
    return getApiBaseUrl();
  },
  replace(pattern, replacement) {
    return getApiBaseUrl().replace(pattern, replacement);
  }
};
