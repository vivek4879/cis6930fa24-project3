import React, { useEffect, useState } from "react";
import axios from "axios";
import Plot from "react-plotly.js";

const Visualizations = () => {
  const [data, setData] = useState(null); // Holds the visualization data
  const [error, setError] = useState(null); // Tracks errors

  // Fetch data from Flask backend
  useEffect(() => {
    axios
      .get("http://127.0.0.1:5000/Visualizations") // Change URL if backend is hosted elsewhere
      .then((response) => {
        setData(response.data);
      })
      .catch((error) => {
        console.error("Error fetching Visualizations:", error);
        setError("Failed to load Visualizations. Please try again later.");
      });
  }, []);

  if (error) {
    return <div>{error}</div>;
  }

  if (!data) {
    return <div>Loading Visualizations...</div>;
  }

  return (
    <div style={{ padding: "20px" }}>
      <h1>Incident Visualizations</h1>

      {/* Clustering Visualization */}
      {data.cluster && (
        <div>
          <h2>Clustering of Incidents</h2>
          <Plot
            data={JSON.parse(data.cluster).data}
            layout={JSON.parse(data.cluster).layout}
          />
        </div>
      )}

      {/* Bar Graph Visualization */}
      {data.bar && (
        <div>
          <h2>Incident Type Counts</h2>
          <Plot
            data={JSON.parse(data.bar).data}
            layout={JSON.parse(data.bar).layout}
          />
        </div>
      )}

      {/* Time-Series Visualization */}
      {data.time_series && (
        <div>
          <h2>Incident Trends Over Time</h2>
          <Plot
            data={JSON.parse(data.time_series).data}
            layout={JSON.parse(data.time_series).layout}
          />
        </div>
      )}
      {/* Hourly Histogram */}
      <div>
        <h2>Incident Frequency by Hour</h2>
        <Plot
          data={[
            {
              x: data.hourly_histogram.x,
              y: data.hourly_histogram.y,
              type: "bar",
              marker: { color: "blue" },
            },
          ]}
          layout={{
            title: "Incident Frequency by Hour",
            xaxis: { title: "Hour of the Day" },
            yaxis: { title: "Number of Incidents" },
          }}
        />
      </div>
      {/* Weekly Trends Line Chart */}
      <div>
        <h2>Incident Trends by Day of the Week</h2>
        <Plot
          data={[
            {
              x: data.weekly_trends.x,
              y: data.weekly_trends.y,
              type: "scatter",
              mode: "lines+markers",
              marker: { color: "green" },
            },
          ]}
          layout={{
            title: "Incident Trends by Day of the Week",
            xaxis: { title: "Day of the Week" },
            yaxis: { title: "Number of Incidents" },
          }}
        />
      </div>           
      
    </div>
  );
};

export default Visualizations;
