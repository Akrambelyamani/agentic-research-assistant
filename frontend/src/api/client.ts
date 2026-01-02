import type { SearchResponse } from "../types";

const BASE = import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000";

export async function searchPlaces(params: {
  q: string;
  type: string;
  radius: number;
  limit: number;
}): Promise<SearchResponse> {
  const url = new URL(`${BASE}/api/search`);
  url.searchParams.set("q", params.q);
  url.searchParams.set("type", params.type);
  url.searchParams.set("radius", String(params.radius));
  url.searchParams.set("limit", String(params.limit));

  const res = await fetch(url.toString());
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    const detail = data?.detail ? String(data.detail) : `HTTP ${res.status}`;
    throw new Error(detail);
  }
  return data as SearchResponse;
}
