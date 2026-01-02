export type SearchItem = {
  id?: number | null;
  osm_type?: string | null;
  name: string;
  lat: number;
  lon: number;
  address?: string | null;
  phone?: string | null;
  website?: string | null;
  opening_hours?: string | null;
  distance_m?: number | null;
  tags?: Record<string, any>;
};

export type SearchResponse = {
  run_id: string;
  query: string;
  place_type: string;
  radius_m: number;
  count: number;
  center: { lat: number; lon: number };
  triage_hint: string;
  items: SearchItem[];
  timings_ms?: Record<string, number>;
  providers?: Record<string, string>;
};
