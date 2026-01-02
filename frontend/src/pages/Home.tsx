import { useMemo, useState } from "react";
import type { SearchResponse, SearchItem } from "../types";
import { searchPlaces } from "../api/client";
import SearchForm from "../components/SearchForm";
import ResultsList from "../components/ResultsList";
import MapView from "../components/MapView";

export default function Home() {
  const [data, setData] = useState<SearchResponse | null>(null);
  const [selected, setSelected] = useState<SearchItem | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string>("");

  const stats = useMemo(() => {
    if (!data) return null;
    return {
      run_id: data.run_id,
      count: data.count,
      radius: data.radius_m,
      type: data.place_type,
      query: data.query,
    };
  }, [data]);

  async function onSearch(values: { q: string; type: string; radius: number; limit: number }) {
    setLoading(true);
    setError("");
    setSelected(null);
    try {
      const res = await searchPlaces(values);
      const sorted = [...(res.items || [])].sort((a, b) => (a.distance_m ?? 1e12) - (b.distance_m ?? 1e12));
      const next = { ...res, items: sorted };
      setData(next);
      setSelected(sorted[0] ?? null);
    } catch (e: any) {
      setData(null);
      setSelected(null);
      setError(e?.message ? String(e.message) : "Request failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="page">
      <header className="topbar">
        <div className="brand">
          <div className="logo">OSM</div>
          <div>
            <h1>OSM Health Locator</h1>
            <p>Find nearby pharmacies, clinics, hospitals using OpenStreetMap data</p>
          </div>
        </div>
        <div className="meta">
          <a className="link" href="http://127.0.0.1:8000/docs" target="_blank" rel="noreferrer">
            API Docs
          </a>
        </div>
      </header>

      <main className="container">
        <section className="card">
          <SearchForm onSearch={onSearch} loading={loading} />
          {stats && (
            <div className="stats">
              <span className="pill">run_id: {stats.run_id}</span>
              <span className="pill">count: {stats.count}</span>
              <span className="pill">radius: {stats.radius} m</span>
              <span className="pill">type: {stats.type}</span>
            </div>
          )}
          {error && <div className="alert error">Error: {error}</div>}
          {loading && <div className="alert info">Searching…</div>}
          {data && !loading && (
            <div className="alert warn">
              {data.triage_hint}
              {data.providers?.places && <span className="dim"> · provider: {data.providers.places}</span>}
              {data.providers?.overpass && <span className="dim"> · overpass: {data.providers.overpass}</span>}
            </div>
          )}
        </section>

        <section className="grid">
          <div className="left">
            <div className="card fill">
              <div className="cardTitle">
                <h2>Results</h2>
                <span className="dim">{data ? `${data.count} places` : "No results yet"}</span>
              </div>
              <ResultsList
                items={data?.items ?? []}
                selected={selected}
                onSelect={(it) => setSelected(it)}
              />
            </div>
          </div>
          <div className="right">
            <div className="card fill">
              <div className="cardTitle">
                <h2>Map</h2>
                <span className="dim">{selected ? selected.name : "Select a place"}</span>
              </div>
              <MapView
                center={data?.center ?? { lat: 33.57311, lon: -7.589843 }}
                items={data?.items ?? []}
                selected={selected}
                onSelect={(it) => setSelected(it)}
              />
            </div>
          </div>
        </section>

        <footer className="footer">
          <span className="dim">Data: OpenStreetMap · Built for real-world reliability (fallback geocoding + resilient querying)</span>
        </footer>
      </main>
    </div>
  );
}
