// Centralized API Base URL configuration
// Dynamically reads from localStorage if saved by user, otherwise VITE_API_BASE_URL,
// otherwise defaults to live production backend on Vercel deployments, or http://127.0.0.1:8000 on localhost.
export const getApiBaseUrl = () => {
  const custom = localStorage.getItem('hiremind_api_url');
  if (custom && custom.trim()) {
    return custom.trim().replace(/\/$/, "");
  }
  const envUrl = import.meta.env.VITE_API_BASE_URL;
  if (envUrl && envUrl.trim()) {
    return envUrl.trim().replace(/\/$/, "");
  }
  
  // If running in browser on production Vercel deployment, default to live Render backend
  if (typeof window !== 'undefined' && window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1') {
    return "https://hiremind-ai-au7b.onrender.com";
  }

  return "http://127.0.0.1:8000";
};

export const API_BASE_URL = getApiBaseUrl();
