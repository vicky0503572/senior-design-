import { MapContainer, TileLayer, CircleMarker, Popup } from "react-leaflet";

function getMarkerColor(status) {
  if (status === "online") return "#33d17a";
  if (status === "warning") return "#f5c211";
  return "#ff4d4f";
}

export default function NetworkMap({ nodes }) {
  const validNodes = nodes.filter(
    (node) =>
      typeof node.latitude === "number" &&
      typeof node.longitude === "number"
  );

  const center =
    validNodes.length > 0
      ? [validNodes[0].latitude, validNodes[0].longitude]
      : [32.7767, -96.797]; // fallback center

  return (
    <div className="overviewPanel">
      <div className="overviewHeader">Network Overview</div>

      <div className="mapWrap">
        <MapContainer
          center={center}
          zoom={11}
          scrollWheelZoom={true}
          className="leafletMap"
        >
          <TileLayer
            attribution='&copy; OpenStreetMap contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />

          {validNodes.map((node) => (
            <CircleMarker
              key={node.box_id}
              center={[node.latitude, node.longitude]}
              radius={10}
              pathOptions={{
                color: getMarkerColor(node.status),
                fillColor: getMarkerColor(node.status),
                fillOpacity: 0.85,
              }}
            >
              <Popup>
                <div>
                  <strong>Box #{node.box_id}</strong>
                  <br />
                  Status: {node.status}
                  <br />
                  Location: {node.location_name ?? "Unnamed location"}
                </div>
              </Popup>
            </CircleMarker>
          ))}
        </MapContainer>
      </div>
    </div>
  );
}