import { useMemo, useState } from "react";

type Props = {
  onSearch: (v: { q: string; type: string; radius: number; limit: number }) => void;
  loading: boolean;
};

export default function SearchForm({ onSearch, loading }: Props) {
  const presets = useMemo(
    () => [
      { label: "Casablanca", value: "Casablanca" },
      { label: "Casablanca Maarif", value: "Casablanca Maarif" },
      { label: "Rabat", value: "Rabat" },
      { label: "Marrakech", value: "Marrakech" },
      { label: "Agadir", value: "Agadir" },
    ],
    []
  );

  const [q, setQ] = useState("Casablanca");
  const [type, setType] = useState("pharmacy");
  const [radius, setRadius] = useState(2000);
  const [limit, setLimit] = useState(20);

  function submit(e: React.FormEvent) {
    e.preventDefault();
    onSearch({ q: q.trim(), type, radius: Number(radius), limit: Number(limit) });
  }

  return (
    <form className="form" onSubmit={submit}>
      <div className="row">
        <label>
          Query (city / district)
          <input value={q} onChange={(e) => setQ(e.target.value)} placeholder="Casablanca Maarif" />
        </label>

        <label>
          Presets
          <select onChange={(e) => setQ(e.target.value)} value="">
            <option value="">Select…</option>
            {presets.map((p) => (
              <option key={p.value} value={p.value}>
                {p.label}
              </option>
            ))}
          </select>
        </label>
      </div>

      <div className="row">
        <label>
          Type
          <select value={type} onChange={(e) => setType(e.target.value)}>
            <option value="pharmacy">Pharmacy</option>
            <option value="hospital">Hospital</option>
            <option value="clinic">Clinic</option>
            <option value="doctors">Doctors</option>
            <option value="dentist">Dentist</option>
          </select>
        </label>

        <label>
          Radius (meters)
          <input type="number" value={radius} onChange={(e) => setRadius(Number(e.target.value))} min={50} max={50000} />
        </label>

        <label>
          Limit
          <input type="number" value={limit} onChange={(e) => setLimit(Number(e.target.value))} min={1} max={100} />
        </label>

        <button className="btn" type="submit" disabled={loading || !q.trim()}>
          {loading ? "Searching…" : "Search"}
        </button>
      </div>
    </form>
  );
}
