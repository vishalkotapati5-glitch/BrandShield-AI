export const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000/api/v1";

export interface ApiError {
  code: string;
  message: string;
  details?: unknown;
}

export async function api<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_URL}${path}`, init);
  const data = await res.json().catch(() => null);
  if (!res.ok) {
    const err: ApiError = data?.error ?? { code: "network_error", message: res.statusText };
    throw err;
  }
  return data as T;
}
