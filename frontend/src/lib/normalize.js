// Convert wind direction degrees to compass text
export function windDirText(deg) {
  if (deg === null || deg === undefined) return "—";

  const dirs = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"];
  const index = Math.round((deg % 360) / 45) % 8;

  return dirs[index];
}

// Determine if a node is online/offline based on last timestamp
export function computeStatus(node) {
  if (!node.timestamp) return "offline";

  const last = new Date(node.timestamp).getTime();
  const ageSeconds = (Date.now() - last) / 1000;

  if (ageSeconds <= 60) return "online";
  if (ageSeconds <= 300) return "warning";

  return "offline";
}

// Format node data for the UI
export function decorateNode(node) {
  return {
    ...node,

    // identity
    box_id: node.box_id ?? "unknown",

    // sensor values from backend API
    temperature_f: node.temperature_f ?? null,
    temperature_c: node.temperature_c ?? null,
    humidity: node.humidity ?? null,
    pressure: node.pressure ?? null,
    wind_speed: node.wind_speed ?? null,
    wind_direction: node.wind_direction ?? null,
    rainfall: node.rainfall ?? null,

    // derived display helpers
    status: node.status ?? computeStatus(node),
    wind_dir_text: windDirText(node.wind_direction),

    // location from backend API shape
    latitude: node.location?.lat ?? null,
    longitude: node.location?.lon ?? null,
    location_name: node.location?.name ?? null,

    // keep timestamp safe
    timestamp: node.timestamp ?? null,
  };
}