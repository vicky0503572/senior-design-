import { useState, useEffect } from "react";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";
import { API_BASE } from "../config";

const TABS = [
  { key: "temp", label: "Temperature", unit: "°F", color: "#00d4ff", dataKey: "temp" },
  { key: "humidity", label: "Humidity", unit: "%", color: "#a78bfa", dataKey: "humidity" },
  { key: "wind", label: "Wind Speed", unit: "m/s", color: "#34d399", dataKey: "wind" },
  { key: "pressure", label: "Pressure", unit: "hPa", color: "#fb923c", dataKey: "pressure" },
];

function mockHistory(node) {
  return Array.from({ length: 24 }, (_, i) => ({
    time: `${i}:00`,
    temp: +((node.temperature_f ?? 72) + (Math.random() * 6 - 3)).toFixed(1),
    humidity: +((node.humidity ?? 45) + (Math.random() * 10 - 5)).toFixed(1),
    wind: +((node.wind_speed ?? 3) + (Math.random() * 2 - 1)).toFixed(1),
    pressure: +((node.pressure ?? 1013) + (Math.random() * 4 - 2)).toFixed(1),
  }));
}

async function fetchHistory(box_id) {
  const res = await fetch(`${API_BASE}/api/history/${box_id}`);
  if (!res.ok) throw new Error("History fetch failed");
  const json = await res.json();
  return json.history.map((point) => ({
    time: new Date(point.timestamp).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
    temp: point.temperature_f,
    humidity: point.humidity,
    wind: point.wind_speed,
    pressure: point.pressure,
  }));
}

export default function NodeDetail({ node, onBack }) {
  const [activeTab, setActiveTab] = useState("temp");
  const [history, setHistory] = useState(() => mockHistory(node));
  const tab = TABS.find((t) => t.key === activeTab);

  useEffect(() => {
    fetchHistory(node.box_id)
      .then(setHistory)
      .catch(() => setHistory(mockHistory(node)));
  }, [node.box_id]);

  return (
    <div className="detailPage">
      <div className="detailTopBar">
        <button className="backBtn" onClick={onBack}>
          ← Dashboard
        </button>
        <div className="detailLastSeen">
          Last seen: {node.timestamp ? new Date(node.timestamp).toLocaleTimeString() : "--"}
        </div>
      </div>
      <div className="detailHeader">
        <div className="detailTitleRow">
          <h1 className="detailTitle">Node: {node.box_id}</h1>
          <div className={`statusPill ${node.status}`}>{node.status}</div>
        </div>
      </div>
      <section className="detailSection">
        <h2 className="detailSectionTitle">Real-Time Sensors</h2>
        <div className="sensorGrid">
          <div className="sensorCard">
            <div className="sensorLabel">Temperature</div>
            <div className="sensorValue">{node.temperature_f ?? "--"} °F</div>
          </div>
          <div className="sensorCard">
            <div className="sensorLabel">Humidity</div>
            <div className="sensorValue">{node.humidity ?? "--"} %</div>
          </div>
          <div className="sensorCard">
            <div className="sensorLabel">Wind Speed</div>
            <div className="sensorValue">{node.wind_speed ?? "--"} m/s</div>
          </div>
          <div className="sensorCard">
            <div className="sensorLabel">Wind Direction</div>
            <div className="sensorValue">{node.wind_dir_text ?? "—"}</div>
          </div>
          <div className="sensorCard">
            <div className="sensorLabel">Pressure</div>
            <div className="sensorValue">{node.pressure ?? "--"} hPa</div>
          </div>
        </div>
      </section>
      <section className="detailSection">
        <h2 className="detailSectionTitle">Additional Info</h2>
        <div className="detailInfoCard">
          <div className="detailInfoRow">
            <span>Rainfall</span>
            <strong>{node.rainfall ?? "--"} mm</strong>
          </div>
          <div className="detailInfoRow">
            <span>Wind Direction</span>
            <strong>{node.wind_direction ?? "--"}° {node.wind_dir_text ?? "—"}</strong>
          </div>
          <div className="detailInfoRow">
            <span>Location</span>
            <strong>{node.location_name ?? "--"}</strong>
          </div>
          <div className="detailInfoRow">
            <span>Latitude</span>
            <strong>{node.latitude ?? "--"}</strong>
          </div>
          <div className="detailInfoRow">
            <span>Longitude</span>
            <strong>{node.longitude ?? "--"}</strong>
          </div>
        </div>
      </section>
      <section className="detailSection">
        <h2 className="detailSectionTitle">Historical Data</h2>
        <div className="detailInfoCard">
          <div className="chartTabs">
            {TABS.map((t) => (
              <button
                key={t.key}
                className={`chartTab ${activeTab === t.key ? "active" : ""}`}
                style={{ "--tab-color": t.color }}
                onClick={() => setActiveTab(t.key)}
              >
                {t.label}
              </button>
            ))}
          </div>
          <ResponsiveContainer width="100%" height={220}>
            <LineChart data={history}>
              <XAxis
                dataKey="time"
                tick={{ fontSize: 11, fill: "rgba(180,220,255,0.5)" }}
                axisLine={{ stroke: "rgba(0,212,255,0.1)" }}
                tickLine={false}
              />
              <YAxis
                domain={["auto", "auto"]}
                tick={{ fontSize: 11, fill: "rgba(180,220,255,0.5)" }}
                axisLine={{ stroke: "rgba(0,212,255,0.1)" }}
                tickLine={false}
                unit={` ${tab.unit}`}
              />
              <Tooltip
                contentStyle={{
                  background: "#0a1628",
                  border: "1px solid rgba(0,212,255,0.2)",
                  borderRadius: "8px",
                  color: "#e8f4ff",
                }}
                labelStyle={{ color: "rgba(180,220,255,0.6)" }}
                formatter={(val) => [`${val} ${tab.unit}`, tab.label]}
              />
              <Line
                type="monotone"
                dataKey={tab.dataKey}
                stroke={tab.color}
                dot={false}
                strokeWidth={2}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </section>
    </div>
  );
}