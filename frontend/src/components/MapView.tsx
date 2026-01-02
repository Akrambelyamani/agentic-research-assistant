import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import type { SearchItem } from "../types";
import "leaflet/dist/leaflet.css";
import L from "leaflet";
import markerIcon2x from "leaflet/dist/images/marker-icon-2x.png";
import markerIcon from "leaflet/dist/images/marker-icon.png";
import markerShadow from "leaflet/dist/images/marker-shadow.png";

delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: markerIcon2x,
  iconUrl: markerIcon,
  shadowUrl: markerShadow,
});

type Props = {
  center: { lat: number; lon: number };
  items: SearchItem[];
  selected: SearchItem | null;
  onSelect: (it: SearchItem) => void;
};

export default function MapView({ center, items, selected, onSelect }: Props) {
  const c: [number, number] = [center.lat, center.lon];
  const zoom = 12;

  return (
    <div className="mapWrap">
      <MapContainer center={c} zoom={zoom} scrollWheelZoom className="map">
        <TileLayer
          attribution='&copy; OpenStreetMap contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {items.map((it, idx) => (
          <Marker
            key={`${it.id ?? idx}-${it.lat}-${it.lon}`}
            position={[it.lat, it.lon]}
            eventHandlers={{ click: () => onSelect(it) }}
          >
            <Popup>
              <div className="popup">
                <div className="popupTitle">{it.name || "Unknown"}</div>
                <div className="popupSub">{it.address || "No address"}</div>
                {it.opening_hours && <div className="popupSub">Hours: {it.opening_hours}</div>}
              </div>
            </Popup>
          </Marker>
        ))}
      </MapContainer>

      {selected && (
        <div className="floating">
          <div className="floatingTitle">{selected.name}</div>
          <div className="floatingSub">{selected.address || "No address"}</div>
        </div>
      )}
    </div>
  );
}
