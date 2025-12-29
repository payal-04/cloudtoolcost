import React, { useEffect, useState, useMemo } from "react";
import axios from "axios";
import { Line } from "react-chartjs-2";

// ✅ Register Chart.js components once
import {
  Chart as ChartJS,
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale,
  Title,
  Tooltip,
  Legend
} from "chart.js";

ChartJS.register(
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale,
  Title,
  Tooltip,
  Legend
);

export default function Dashboard() {
  const [todayCost, setTodayCost] = useState(null);
  const [recommendations, setRecommendations] = useState([]);
  const [predictionData, setPredictionData] = useState([]);

  // Fetch today's cost
  useEffect(() => {
    axios.get("http://localhost:8000/cost/today")
      .then(res => {
        try {
          const value = res.data.ResultsByTime[0].Total.UnblendedCost.Amount;
          setTodayCost(parseFloat(value).toFixed(4));
        } catch {
          setTodayCost("0.00");
        }
      })
      .catch(() => setTodayCost("0.00"));
  }, []);

  // Fetch recommendations
  useEffect(() => {
    axios.get("http://localhost:8000/recommendations")
      .then(res => setRecommendations(res.data || []))
      .catch(() => setRecommendations([]));
  }, []);

  // Fetch prediction data (fixed endpoint)
  useEffect(() => {
    axios.get("http://localhost:8000/cost/predictions")
      .then(res => setPredictionData(res.data || []))
      .catch(() => setPredictionData([]));
  }, []);

  // ✅ Memoize chart data to avoid re‑init errors
  const chartData = useMemo(() => ({
    labels: predictionData.map(p => p.date),
    datasets: [
      {
        label: "Predicted Cost ($)",
        data: predictionData.map(p => p.amount),
        borderColor: "#00ffcc",
        backgroundColor: "rgba(0,255,204,0.2)",
      }
    ]
  }), [predictionData]);

  return (
    <div style={{
      minHeight: "100vh",
      backgroundColor: "#000",
      color: "#fff",
      fontFamily: "Segoe UI, sans-serif",
      padding: "40px",
      display: "flex",
      flexDirection: "column",
      gap: "40px"
    }}>
      {/* Header */}
      <h1 style={{ fontSize: "42px", marginBottom: "20px" }}>
        🌩 Cloud Cost Dashboard
      </h1>

      {/* Today’s Cost */}
      <div style={{
        maxWidth: "600px",
        padding: "30px",
        background: "rgba(20,20,20,0.9)",
        borderRadius: "16px",
        boxShadow: "0 8px 30px rgba(0,0,0,0.6)"
      }}>
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

      {/* Recommendations */}
      <div style={{
        maxWidth: "600px",
        padding: "30px",
        background: "rgba(20,20,20,0.9)",
        borderRadius: "16px",
        boxShadow: "0 8px 30px rgba(0,0,0,0.6)"
      }}>
        <h2 style={{ fontWeight: "400", marginBottom: "20px", color: "#ccc" }}>
          Recommendations:
        </h2>
        <ul>
          {recommendations.map((rec, idx) => (
            <li key={idx} style={{ marginBottom: "10px" }}>{rec}</li>
          ))}
        </ul>
      </div>

      {/* Prediction Chart */}
      <div style={{
        maxWidth: "800px",
        padding: "30px",
        background: "rgba(20,20,20,0.9)",
        borderRadius: "16px",
        boxShadow: "0 8px 30px rgba(0,0,0,0.6)"
      }}>
        <h2 style={{ fontWeight: "400", marginBottom: "20px", color: "#ccc" }}>
          Cost Prediction Chart:
        </h2>
        <Line id="predictionChart" data={chartData} />
      </div>
    </div>
  );
}