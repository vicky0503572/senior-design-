import { useEffect, useState } from "react";
import NodeCard from "./components/NodeCard";
import NodeDetail from "./components/NodeDetail";
import NetworkMap from "./components/NetworkMap";
import { decorateNode } from "./lib/normalize";
import { API_BASE } from "./config";
import "./App.css";

export default function App() {
  const [data, setData] = useState({});
  const [err, setErr] = useState(null);
  const [lastUpdate, setLastUpdate] = useState(null);
  const [selectedNode, setSelectedNode] = useState(null);

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

  const nodes = Object.values(data || {}).map(decorateNode);
  const activeCount = nodes.filter((n) => n.status !== "offline").length;
  const totalCount = nodes.length;
  const offlineCount = totalCount - activeCount;
  const lastUpdateText = lastUpdate ? lastUpdate.toLocaleTimeString() : "--";

  if (selectedNode) {
    return (
      <NodeDetail
        node={selectedNode}
        onBack={() => setSelectedNode(null)}
      />
    );
  }

  return (
    <div className="appShell">
      <header className="topBar">
        <div className="titleBlock">
          <h1 className="pageTitle">MicroWeather Network</h1>
          <p className="pageMeta">
            API: {API_BASE}
            {lastUpdate && <span> • Last update: {lastUpdateText}</span>}
          </p>
        </div>

        <button className="refreshBtn" onClick={load}>
          Refresh now
        </button>
      </header>

      {err && <p className="errorText">Error: {err}</p>}

      <div className="summaryGrid">
        <div className="summaryCard">
          <div className="summaryLabel">Total Nodes</div>
          <div className="summaryValue">{totalCount}</div>
        </div>

        <div className="summaryCard">
          <div className="summaryLabel">Online Nodes</div>
          <div className="summaryValue onlineText">{activeCount}</div>
        </div>

        <div className="summaryCard">
          <div className="summaryLabel">Offline Nodes</div>
          <div className="summaryValue offlineText">{offlineCount}</div>
        </div>

        <div className="summaryCard">
          <div className="summaryLabel">Last Update</div>
          <div className="summaryValue summaryTime">{lastUpdateText}</div>
        </div>
      </div>

      <NetworkMap nodes={nodes} />

      <div className="activeNodesTitle">
        Active Nodes ({activeCount}/{totalCount})
      </div>

      <div className="nodesGrid">
        {nodes.map((node) => (
          <div key={node.box_id} onClick={() => setSelectedNode(node)}>
            <NodeCard node={node} />
          </div>
        ))}
      </div>
    </div>
  );
}