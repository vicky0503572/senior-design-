import { MapContainer, TileLayer, CircleMarker, Popup, useMap } from "react-leaflet";

function RecenterButton({ center }) {
  const map = useMap();
  return (
    <button
      className="recenterBtn"
      onClick={() => map.setView(center, 11)}
      title="Re-center map"
    >
      ◎ Re-center
    </button>
  );
}

function getMarkerColor(status) {
  if (status === "online") return "#00d4ff";
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
      : [32.7767, -96.797];

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
            attribution='&copy; <a href="https://stadiamaps.com/">Stadia Maps</a> &copy; <a href="https://openmaptiles.org/">OpenMapTiles</a> &copy; OpenStreetMap contributors'
            url="https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png"
          />
          <RecenterButton center={center} />
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
                  <strong>{node.box_id}</strong>
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