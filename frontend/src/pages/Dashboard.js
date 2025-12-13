import React, { useEffect, useState } from "react";
import axios from "axios";

export default function Dashboard() {
  const [todayCost, setTodayCost] = useState(null);

  useEffect(() => {
    axios.get("http://localhost:8000/cost/today")
      .then(res => {
        try {
          const value = res.data.ResultsByTime[0].Total.UnblendedCost.Amount;
          setTodayCost(parseFloat(value).toFixed(4));
        } catch {
          setTodayCost("0.00");
        }
      });
  }, []);

  return (
    <div style={{ padding: 20 }}>
      <h1>Cloud Cost Dashboard</h1>
      <h2>Today's AWS Cost:</h2>
      <div style={{
        fontSize: "34px",
        fontWeight: "bold",
        background: "#f2f2f2",
        padding: "10px 20px",
        borderRadius: "8px",
        display: "inline-block"
      }}>
        ${todayCost}
      </div>
    </div>
  );
}