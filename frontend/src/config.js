// Centralized API Base URL configuration
// Dynamically reads from localStorage if saved by user, otherwise VITE_API_BASE_URL, otherwise http://127.0.0.1:8000
export const getApiBaseUrl = () => {
  const custom = localStorage.getItem('hiremind_api_url');
  if (custom && custom.trim()) {
    return custom.trim().replace(/\/$/, "");
  }
  const envUrl = import.meta.env.VITE_API_BASE_URL;
  if (envUrl && envUrl.trim()) {
    return envUrl.trim().replace(/\/$/, "");
  }
  return "http://127.0.0.1:8000";
};

export const API_BASE_URL = getApiBaseUrl();
