function FarePredictor() {
  const [pickupId, setPickupId] = useState("");
  const [dropoffId, setDropoffId] = useState("");
  const [fareDetails, setFareDetails] = useState(null);
  const [status, setStatus] = useState("");

  const predictFare = async () => {
    try {
      const res = await axios.get(`http://localhost:8000/predict-fare`, {
        params: {
          pickup: pickupId,
          dropoff: dropoffId,
          hour: new Date().getHours(),
          day_of_week: new Date().getDay(),
          is_jfk: false,
          tolls: 0.0,
        },
      });
      setFareDetails(res.data.fare_details);
      setStatus("Prediction successful.");
    } catch (error) {
      setStatus("Error predicting fare.");
    }
  };

  return (
    <div>
      <h2>Fare Price Predictor</h2>
      <input
        type="number"
        placeholder="Pickup Zone ID"
        value={pickupId}
        onChange={(e) => setPickupId(e.target.value)}
      />
      <input
        type="number"
        placeholder="Dropoff Zone ID"
        value={dropoffId}
        onChange={(e) => setDropoffId(e.target.value)}
      />
      <button onClick={predictFare}>Predict Fare</button>

      {fareDetails && (
        <div>
          <h3>Fare Breakdown:</h3>
          <ul>
            <li>Base Fare: ${fareDetails.base_fare.toFixed(2)}</li>
            <li>Distance Fare: ${fareDetails.distance_fare.toFixed(2)}</li>
            <li>Time Fare: ${fareDetails.time_fare.toFixed(2)}</li>
            <li>MTA Surcharge: ${fareDetails.mta_surcharge.toFixed(2)}</li>
            <li>Improvement Surcharge: ${fareDetails.improvement_surcharge.toFixed(2)}</li>
            {fareDetails.congestion_surcharge > 0 && (
              <li>Congestion Surcharge: ${fareDetails.congestion_surcharge.toFixed(2)}</li>
            )}
            {fareDetails.night_surcharge > 0 && (
              <li>Night Surcharge: ${fareDetails.night_surcharge.toFixed(2)}</li>
            )}
            {fareDetails.rush_hour_surcharge > 0 && (
              <li>Rush Hour Surcharge: ${fareDetails.rush_hour_surcharge.toFixed(2)}</li>
            )}
            {fareDetails.airport_fee > 0 && <li>Airport Fee: ${fareDetails.airport_fee.toFixed(2)}</li>}
            <li>Total Fare: ${fareDetails.total_fare.toFixed(2)}</li>
          </ul>
        </div>
      )}
      {status && <p>{status}</p>}
    </div>
  );
}
