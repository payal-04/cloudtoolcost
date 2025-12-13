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
    <div style={{
      minHeight: "100vh",
      backgroundColor: "#000",   // black background
      color: "#fff",
      fontFamily: "Segoe UI, sans-serif",
      padding: "40px",
      display: "flex",
      justifyContent: "flex-start", // align left
      alignItems: "flex-start"      // top-left corner
    }}>
      <div style={{
        maxWidth: "600px",
        width: "100%",
        textAlign: "left",
        padding: "30px",
        background: "rgba(20,20,20,0.9)",
        borderRadius: "16px",
        boxShadow: "0 8px 30px rgba(0,0,0,0.6)"
      }}>
        <h1 style={{ fontSize: "42px", marginBottom: "20px" }}>
          🌩 Cloud Cost Dashboard
        </h1>
        <h2 style={{ fontWeight: "400", marginBottom: "20px", color: "#ccc" }}>
          Today's AWS Cost:
        </h2>
        <div style={{
          fontSize: "48px",
          fontWeight: "bold",
          background: "linear-gradient(135deg, #1f1f1f, #333)",
          color: "#00ffcc",
          padding: "25px 50px",
          borderRadius: "12px",
          display: "inline-block",
          boxShadow: "0 4px 20px rgba(0, 255, 204, 0.4)",
          transition: "transform 0.2s ease, box-shadow 0.2s ease"
        }}
        onMouseEnter={e => {
          e.currentTarget.style.transform = "scale(1.05)";
          e.currentTarget.style.boxShadow = "0 6px 30px rgba(0, 255, 204, 0.6)";
        }}
        onMouseLeave={e => {
          e.currentTarget.style.transform = "scale(1)";
          e.currentTarget.style.boxShadow = "0 4px 20px rgba(0, 255, 204, 0.4)";
        }}>
          ${todayCost}
        </div>
      </div>
    </div>
  );
}