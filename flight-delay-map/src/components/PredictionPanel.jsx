import { useEffect, useState } from "react";
import './PredictionPanel.css'
function PredictionPanel({ flight }) {
    const [pred, setPred] = useState(null);
    const [loading, setLoading] = useState(false);
    const [err, setErr] = useState("");


// use effect function that gathers the prediction data
  useEffect(() => {
    if (!flight) return;
    //run function: gathers the prediction and updates the state variables
    const run = async () => {
      setLoading(true);
      setErr("");
      setPred(null);
      //api (server) call to python server
      // This is where the machine learning model will actually do an inference
      try {
        const res = await fetch("http://127.0.0.1:5000/api/predict", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ flight }),
        });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        setPred(data);
      } catch (e) {
        setErr(e.message || "Failed to fetch prediction");
      } finally {
        setLoading(false);
      }
    };
    //executes run function right after defining it
    run();
  }, [flight]);



  if (!flight) return null;

  return (
    <div className="prediction-panel">
      <h2>Prediction</h2>

      <div className="meta">
        <div>{flight.flight_number || "—"}</div>
        <div>
          {flight.origin} → {flight.destination}
        </div>
        <div>{flight.date}</div>
        </div> 
    
      {loading && <div className="skeleton">Computing…</div>}


      {err && <div className="error">Error: {err}</div>}


      {pred && (
        <div className="result">
          <div className="value">
            ⏱ Predicted Delay: <strong>{Math.round(pred.prediction)} min</strong>
          </div>
          {/* <div className="confidence">Model: {pred.model || "xgb-regressor"} | v{pred.version}</div> */}
          {/* placeholder spot for SHAP later */}
          {pred.top_factors?.length ? (
            <ul className="factors">
              {pred.top_factors.map((f, i) => (
                <li key={i}>
                  <span>{f.feature}</span>
                  <span>{f.impact > 0 ? "+" : ""}{f.impact.toFixed(1)} min</span>
                </li>
              ))}
            </ul>
          ) : null}
        </div>
      )}
    </div>
  );
}
export default PredictionPanel