import { useEffect, useState } from "react";
import NodeCard from "./components/NodeCard";
import { decorateNode } from "./lib/normalize";
import { API_BASE } from "./config";

export default function App() {
  const [data, setData] = useState({});
  const [err, setErr] = useState(null);
  const [lastUpdate, setLastUpdate] = useState(null);

  async function load() {
    try {
      setErr(null);
      const res = await fetch(`${API_BASE}/api/latest`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const json = await res.json();
      setData(json || {});
      setLastUpdate(new Date());
    } catch (e) {
      setErr(e.message || String(e));
    }
  }

  useEffect(() => {
    load();
    const t = setInterval(load, 5000);
    return () => clearInterval(t);
  }, []);

  // Convert backend object -> array of nodes -> UI-ready nodes
  const nodes = Object.values(data || {}).map(decorateNode);
  const activeCount = nodes.filter((n) => n.status !== "offline").length;

  return (
    <div style={{ padding: 24, fontFamily: "system-ui" }}>
      <h1 style={{ margin: 0 }}>MicroWeather Network</h1>

      <div style={{ opacity: 0.7, marginTop: 6 }}>
        API: {API_BASE}
        {lastUpdate && (
          <span style={{ marginLeft: 12 }}>
            • Last update: {lastUpdate.toLocaleTimeString()}
          </span>
        )}
      </div>

      <button onClick={load} style={{ marginTop: 12 }}>
        Refresh now
      </button>

      {err && (
        <p style={{ color: "crimson", marginTop: 12 }}>
          Error: {err}
        </p>
      )}

      <div className="activeNodesTitle" style={{ marginTop: 22 }}>
        Active Nodes ({activeCount}/{nodes.length})
      </div>

      <div className="nodesGrid">
        {nodes.map((node) => (
          <NodeCard key={node.box_id} node={node} />
        ))}
      </div>
    </div>
  );
}