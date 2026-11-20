import { getApiBaseUrl } from './config';

/**
 * Enterprise Resilient API Client
 * - Prepends getApiBaseUrl() dynamically
 * - Attaches auth tokens if present
 * - Enforces timeout (default 8s) to avoid indefinite hangs
 * - Provides graceful error objects rather than unhandled promise rejections
 */
export async function apiFetch(endpoint, options = {}, timeoutMs = 12000) {
  const baseUrl = getApiBaseUrl();
  const url = endpoint.startsWith('http') ? endpoint : `${baseUrl}${endpoint.startsWith('/') ? '' : '/'}${endpoint}`;

  const headers = {
    ...(options.headers || {})
  };

  // Add auth token if available and not already set
  try {
    const token = localStorage.getItem('hiremind_token');
    if (token && !headers['Authorization'] && !(options.body instanceof FormData)) {
      headers['Authorization'] = `Bearer ${token}`;
    }
  } catch (e) {
    // ignore localStorage errors
  }

  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeoutMs);

  try {
    const response = await fetch(url, {
      ...options,
      headers,
      signal: controller.signal
    });
    clearTimeout(timeoutId);
    return response;
  } catch (err) {
    clearTimeout(timeoutId);
    if (err.name === 'AbortError') {
      throw new Error(`Request timed out after ${Math.round(timeoutMs / 1000)}s. Backend may be waking up.`);
    }
    throw err;
  }
}
