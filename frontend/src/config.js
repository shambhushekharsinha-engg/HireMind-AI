// Centralized API Base URL configuration
// In production (Vercel), set VITE_API_BASE_URL environment variable to your deployed backend API URL (e.g. https://hiremind-backend.onrender.com)
export const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000").replace(/\/$/, "");
