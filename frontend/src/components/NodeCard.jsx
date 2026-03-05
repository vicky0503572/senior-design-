import { windDirText } from "../lib/normalize";

export default function NodeCard({ node }) {
  const status = node.status; // online / warning / offline

  return (
    <div className={`nodeCard ${status}`}>
      <div className="nodeHeader">
        <div className="nodeTitle">Box #{node.box_id}</div>

        <span className={`statusPill ${status}`}>
          {status}
        </span>
      </div>

      <div className="rows">
        <div className="row">
          <span className="label">Temp</span>
          <span className="value">{node.temperature ?? "—"}°F</span>
        </div>

        <div className="row">
          <span className="label">Humidity</span>
          <span className="value">{node.humidity ?? "—"}%</span>
        </div>

        <div className="row">
          <span className="label">Wind</span>
          <span className="value">
            {node.wind_speed ?? "—"} m/s {windDirText(node.wind_direction)}
          </span>
        </div>

        <div className="row">
          <span className="label">Rain</span>
          <span className="value">{node.rainfall ?? "—"} mm</span>
        </div>
      </div>
    </div>
  );
}