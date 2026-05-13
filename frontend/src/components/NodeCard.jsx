export default function NodeCard({ node }) {
  return (
    <div className={`nodeCard ${node.status}`}>
      <div className="nodeHeader">
        <div className="nodeTitle">{node.box_id}</div>
        <div className={`statusPill ${node.status}`}>{node.status}</div>
      </div>

      <div className="rows">
        <div className="row">
          <span className="label">Temperature</span>
          <span className="value">{node.temperature_f ?? "--"} °F</span>
        </div>

        <div className="row">
          <span className="label">Humidity</span>
          <span className="value">{node.humidity ?? "--"} %</span>
        </div>

        <div className="row">
          <span className="label">Wind</span>
          <span className="value">{node.wind_speed ?? "--"} m/s · {node.wind_dir_text ?? "—"}</span>
        </div>

        <div className="row">
          <span className="label">Rainfall</span>
          <span className="value">{node.rainfall ?? "--"} mm</span>
        </div>

        <div className="row">
          <span className="label">Pressure</span>
          <span className="value">{node.pressure ?? "--"} hPa</span>
        </div>
      </div>
    </div>
  );
}