import type { PlaceItem } from "../types";

export default function PlaceDetails({ item }: { item: PlaceItem | null }) {
  if (!item) {
    return (
      <div className="card">
        <strong>Details</strong>
        <div style={{ marginTop: 8, color: "#777" }}>Click on a result to see details.</div>
      </div>
    );
  }

  return (
    <div className="card">
      <strong>Details</strong>
      <div style={{ marginTop: 8 }}>
        <div><b>Name:</b> {item.name}</div>
        <div><b>Distance:</b> {item.distance_m} m</div>
        <div><b>Coords:</b> {item.lat}, {item.lon}</div>
        {item.address ? <div><b>Address:</b> {item.address}</div> : null}
      </div>

      <div style={{ marginTop: 10 }}>
        <b>OSM tags:</b>
        <pre style={{ whiteSpace: "pre-wrap", background: "#f7f7f7", padding: 10, borderRadius: 8 }}>
{JSON.stringify(item.tags, null, 2)}
        </pre>
      </div>
    </div>
  );
}
