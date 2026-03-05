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

    status: computeStatus(node),

    wind_dir_text: windDirText(node.wind_direction),

    // safe fallbacks if backend fields missing
    temperature: node.temperature ?? null,
    humidity: node.humidity ?? null,
    pressure: node.pressure ?? null,
    wind_speed: node.wind_speed ?? null,
    rainfall: node.rainfall ?? null,

    latitude: node.latitude ?? null,
    longitude: node.longitude ?? null,
    location_name: node.location_name ?? null,
  };
}