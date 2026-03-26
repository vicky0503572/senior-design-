export default function NodeDetail({ node, onBack }) {
  return (
    <div className="detailPage">
      <div className="detailTopBar">
        <button className="backBtn" onClick={onBack}>
          ← Back to Dashboard
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
            <div className="sensorValue">
              {node.wind_speed ?? "--"} m/s {node.wind_dir_text ?? "—"}
            </div>
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
            <strong>
              {node.wind_direction ?? "--"}° {node.wind_dir_text ?? "—"}
            </strong>
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
        <div className="historyPlaceholder">
          Charts go here next
        </div>
      </section>
    </div>
  );
}