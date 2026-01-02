import type { SearchItem } from "../types";

type Props = {
  items: SearchItem[];
  selected: SearchItem | null;
  onSelect: (it: SearchItem) => void;
};

function fmtDistance(m?: number | null) {
  if (m == null) return "";
  if (m < 1000) return `${m} m`;
  return `${(m / 1000).toFixed(2)} km`;
}

export default function ResultsList({ items, selected, onSelect }: Props) {
  if (!items.length) {
    return <div className="empty">No results yet. Try searching a city.</div>;
  }

  return (
    <div className="list">
      {items.map((it, idx) => {
        const active = selected && (selected.id === it.id) && (selected.lat === it.lat) && (selected.lon === it.lon);
        return (
          <button
            key={`${it.id ?? idx}-${it.lat}-${it.lon}`}
            className={`item ${active ? "active" : ""}`}
            onClick={() => onSelect(it)}
          >
            <div className="itemTop">
              <div className="itemName">{it.name || "Unknown"}</div>
              <div className="itemDist">{fmtDistance(it.distance_m)}</div>
            </div>
            <div className="itemSub">
              <span>{it.address || "No address"}</span>
            </div>
          </button>
        );
      })}
    </div>
  );
}
