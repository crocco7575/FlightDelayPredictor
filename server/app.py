from flask import Flask, request, jsonify
from flask_cors import CORS
from flightawareScraper import get_flightaware_info


import pandas as pd
app = Flask(__name__)
CORS(app)
# Load airport data once
df = pd.read_csv("airports_info.csv")
df_filtered = df[df["iata_code"].notna() & df["lat_decimal"].notna() & df["lon_decimal"].notna()]
airport_coords = {
    row["iata_code"].strip().upper(): {
        "lat": row["lat_decimal"],
        "lng": row["lon_decimal"]
    }
    for _, row in df_filtered.iterrows()
}


  # Allows React (localhost:3000) to talk to Flask (localhost:5000)

@app.route("/api/flights")
def get_flights():
    flight_num = request.args.get("flightNumber", "").strip().upper()
    flight_db = get_flightaware_info(flight_num)
    matches = [f for f in  flight_db if flight_num in f["flight_number"]]

    return jsonify(matches)


@app.route("/api/coords")
def get_airport_coords():
    origin = request.args.get("origin", "").upper()
    destination = request.args.get("destination", "").upper()

    if origin not in airport_coords or destination not in airport_coords:
        return jsonify({"error": "Invalid IATA code(s)"}), 400

    return jsonify({
        "origin": airport_coords[origin],
        "destination": airport_coords[destination]
    })


@app.route("/api/predict", methods=["POST"])
def predict():
    payload = request.get_json(force=True) or {}
    flight = payload.get("flight", {})

    # TODO: replace with real model inference
    base_prediction = 8.0  # minutes, stubbed
    resp = {
        "prediction": base_prediction,
        "version": "0.1.0",
        "model": "xgb-regressor",
        # Optional placeholder for per-flight explanation you’ll add later
        "top_factors": [
            {"feature": "PrevTailDelay", "impact": 3.1},
            {"feature": "Carrier_Route_Avg_Delay", "impact": 2.4},
            {"feature": "SchDep_Hour", "impact": 1.2},
            {"feature": "DayOfWeek", "impact": 0.6},
        ]
    }
    return jsonify(resp)

if __name__ == "__main__":
    app.run(debug=True)
    