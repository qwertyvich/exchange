// Keep the same session on request creation, the request page and its actions.
export function apiFetch(path, options = {}) {
  const headers = new Headers(options.headers);
  const token = localStorage.getItem('token');
  if (token) headers.set('Authorization', `Bearer ${token}`);
  // Do not set Content-Type here: the browser supplies the boundary for receipt uploads.
  return fetch(path, { ...options, headers, credentials: 'same-origin' });
}
