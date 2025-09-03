import { useState } from "react";
import axios from "axios";
import {
  PieChart, Pie, Cell, Tooltip,
  BarChart, Bar, XAxis, YAxis, CartesianGrid
} from "recharts";

function App() {
  const [product, setProduct] = useState("");
  const [review, setReview] = useState("");
  const [summary, setSummary] = useState(null);
  const [reviewsList, setReviewsList] = useState([]);
  const COLORS = ["#0088FE", "#FF8042", "#00C49F"];

  const API_BASE = "http://127.0.0.1:5000";

  const fetchReviews = async () => {
    if (!product) return;
    try {
      const res = await axios.get(`${API_BASE}/reviews/${product}`);
      setReviewsList(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  const analyzeReview = async () => {
    if (!product || !review) {
      alert("Please enter product name and review");
      return;
    }
    try {
      await axios.post(`${API_BASE}/analyze`, { product, review });
      const sumRes = await axios.get(`${API_BASE}/summary/${product}`);
      setSummary(sumRes.data);
      setReview("");
      await fetchReviews();
    } catch (err) {
      console.error(err);
      alert("Error connecting to backend");
    }
  };

  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
      <h1>📊 Product Sentiment Analyzer</h1>

      <input
        type="text"
        placeholder="Enter product name"
        value={product}
        onChange={(e) => setProduct(e.target.value)}
        style={{ padding: "10px", marginRight: "10px", width: "300px" }}
      />
      <br /><br />

      <textarea
        placeholder="Enter review"
        value={review}
        onChange={(e) => setReview(e.target.value)}
        style={{ padding: "10px", width: "400px", height: "80px" }}
      />
      <br />
      <button
        onClick={analyzeReview}
        style={{
          padding: "10px 20px",
          marginTop: "10px",
          backgroundColor: "#0088FE",
          color: "white",
          border: "none",
          borderRadius: "5px",
          cursor: "pointer",
        }}
      >
        Analyze Review
      </button>

      {reviewsList.length > 0 && (
        <div style={{ marginTop: "30px" }}>
          <h2>📝 Reviews for {product}</h2>
          <ul>
            {reviewsList.map((r, index) => (
              <li key={index} style={{ marginBottom: "15px" }}>
                <strong>📱 Product:</strong> {r.product} <br />
                <strong>📝 Review:</strong> {r.review} <br />
                <strong>📊 TextBlob Score:</strong> {r.textblob_score.toFixed(3)} <br />
                <strong>📊 Vader Score:</strong> {r.vader_score.toFixed(3)} <br />
                <strong>😀 Sentiment:</strong>{" "}
                <span style={{ color: r.sentiment === "positive" ? "green" : r.sentiment === "negative" ? "red" : "orange" }}>
                  {r.sentiment.toUpperCase()}
                </span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {summary && (
        <div style={{ marginTop: "40px" }}>
          <h2>📈 Sentiment Summary</h2>

          <PieChart width={400} height={300}>
            <Pie
              data={Object.entries(summary).map(([key, value]) => ({ name: key, value }))}
              cx="50%"
              cy="50%"
              outerRadius={100}
              dataKey="value"
              label
            >
              {Object.entries(summary).map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip />
          </PieChart>

          <BarChart
            width={400}
            height={300}
            data={Object.entries(summary).map(([key, value]) => ({ name: key, value }))}
          >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="value" fill="#82ca9d" />
          </BarChart>
        </div>
      )}
    </div>
  );
}

export default App;
