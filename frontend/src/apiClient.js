import { getApiBaseUrl, API_BASE_URL } from './config';

export { getApiBaseUrl, API_BASE_URL };

/**
 * Enterprise Resilient API Client
 * - Prepends getApiBaseUrl() dynamically
 * - Attaches auth tokens if present
 * - Enforces timeout (default 12s) to avoid indefinite hangs
 * - Provides graceful error handling
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
    // ignore localStorage errors in private browsing / sandboxes
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
      throw new Error(`Request timed out after ${Math.round(timeoutMs / 1000)}s. Gateway may be waking up.`);
    }
    throw err;
  }
}

/**
 * Safe JSON/Text API fetcher that throws on non-2xx responses
 * so calling pages can smoothly trigger their deterministic failovers.
 */
export async function safeApiFetch(endpoint, options = {}, timeoutMs = 12000) {
  const res = await apiFetch(endpoint, options, timeoutMs);
  if (!res.ok) {
    throw new Error(`API returned HTTP ${res.status}`);
  }
  const contentType = res.headers.get('content-type') || '';
  if (contentType.includes('application/json')) {
    return await res.json();
  }
  return await res.text();
}
