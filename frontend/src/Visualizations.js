import React, { useState } from "react";
import axios from "axios";
import Plot from "react-plotly.js";

const Visualizations = () => {
  const [file, setFile] = useState(null); // Holds the selected file
  const [url, setUrl] = useState(""); // Holds the URL input
  const [visualizationData, setVisualizationData] = useState(null); // Visualization data
  const [error, setError] = useState(null); // Error messages

  // Handle file selection
  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setUrl(""); // Clear URL if file is selected
  };

  // Handle URL input
  const handleUrlChange = (e) => {
    setUrl(e.target.value);
    setFile(null); // Clear file if URL is entered
  };

  const fetchVisualizations = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:5000/Visualizations");
      console.log("Visualization response:", response.data);
      setVisualizationData(response.data);
    } catch (error) {
      console.error("Error fetching visualizations:", error);
      setError("Failed to fetch visualizations.");
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    try {
      if (file) {
        const formData = new FormData();
        formData.append("file", file);
        const response = await axios.post("http://127.0.0.1:5000/upload", formData, {
          headers: { "Content-Type": "multipart/form-data" },
        });
        console.log("Upload response:", response.data);
        await fetchVisualizations(); // Fetch visualizations after upload
      } else if (url) {
        const response = await axios.post("http://127.0.0.1:5000/upload", { url });
        console.log("Upload response (URL):", response.data);
        await fetchVisualizations(); // Fetch visualizations after URL submission
      } else {
        setError("Please upload a file or enter a URL.");
      }
    } catch (error) {
      console.error("Error uploading data:", error);
      setError("Failed to upload data. Please try again.");
    }
  };

  if (error) {
    return <div>{error}</div>;
  }

  if (!visualizationData) {
    return (
      <div style={{ padding: "20px" }}>
        <h1>Upload Incident Data</h1>
        <form onSubmit={handleSubmit}>
          <div>
            <label htmlFor="file">Upload PDF:</label>
            <input type="file" id="file" accept="application/pdf" onChange={handleFileChange} />
          </div>
          <div>
            <label htmlFor="url">Enter URL:</label>
            <input type="text" id="url" value={url} onChange={handleUrlChange} />
          </div>
          <button type="submit">Submit</button>
        </form>
      </div>
    );
  }

  return (
    <div style={{ padding: "20px" }}>
      <h1>Incident visualizations</h1>

      {/* Clustering Visualization */}
      {visualizationData.cluster && (
        <div>
          <h2>Clustering of Incidents</h2>
          <Plot
            data={JSON.parse(visualizationData.cluster).data}
            layout={JSON.parse(visualizationData.cluster).layout}
          />
        </div>
      )}

      {/* Bar Graph Visualization */}
      {visualizationData.bar && (
        <div>
          <h2>Incident Type Counts</h2>
          <Plot
            data={JSON.parse(visualizationData.bar).data}
            layout={JSON.parse(visualizationData.bar).layout}
          />
        </div>
      )}
      {/* Hourly Histogram */}
      {visualizationData.hourly_histogram && (
        <div>
          <h2>Incident Frequency by Hour</h2>
          <Plot
            data={[
              {
                x: visualizationData.hourly_histogram.x,
                y: visualizationData.hourly_histogram.y,
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
      )}
      {/* Weekly Trends */}
      {visualizationData.weekly_trends && (
        <div>
          <h2>Weekly Incident Trends</h2>
          <Plot
            data={[
              {
                x: visualizationData.weekly_trends.x,
                y: visualizationData.weekly_trends.y,
                type: "line",
              },
            ]}
            layout={{
              title: "Weekly Trends",
              xaxis: { title: "Day of the Week" },
              yaxis: { title: "Number of Incidents" },
            }}
          />
        </div>
      )}
    </div>
  );
};

export default Visualizations;