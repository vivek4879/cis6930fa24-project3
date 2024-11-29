from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3
import pandas as pd
import plotly.express as px
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)
CORS(app) #enable cross origin resource sharing

def connect_db():
    return sqlite3.connect("../resources/normanpd.db")

def fetch_data(query):
    con = connect_db()
    df  = pd.read_sql_query(query,con)
    con.close()
    return df
def preprocess_data(df):
    df['incident_hour'] = pd.to_datetime(df['incident_time']).dt.hour
    df['incident_date'] = pd.to_datetime(df['incident_time']).dt.date
    return df

@app.route('/')
def home():
    return "Welcome to the Incident Visualizations API! Use /Visualizations to get the data."

@app.route('/favicon.ico')
def favicon():
    return '', 204

@app.route('/Visualizations', methods=['GET'])
def Visualizations():
    # Fetch data for time-series and weekly trends
    query = "SELECT incident_time, nature FROM incidents"
    df = fetch_data(query)

    if df.empty:
        return jsonify({"error": "No data available"}), 400

    # Preprocess data
    df['incident_time'] = pd.to_datetime(df['incident_time'], errors='coerce')
    df = df.dropna(subset=['incident_time'])  # Remove rows with invalid timestamps
    df['hour'] = df['incident_time'].dt.hour
    df['day_of_week'] = df['incident_time'].dt.day_name()

    # 1. Incident Frequency by Hour (Histogram)
    hourly_data = df['hour'].value_counts().sort_index()
    histogram_data = {
        "x": hourly_data.index.tolist(),
        "y": hourly_data.values.tolist(),
    }

    # 2. Day of the Week Trends (Line Chart)
    weekly_data = df['day_of_week'].value_counts().reindex(
        ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], fill_value=0
    )
    line_chart_data = {
        "x": weekly_data.index.tolist(),
        "y": weekly_data.values.tolist(),
    }

    # Fetch data for clustering and bar graph
    query = "SELECT incident_time, incident_location, nature FROM incidents"
    df = fetch_data(query)
    df = preprocess_data(df)

    if df.empty:
        return jsonify({"error": "No data available"}), 400

    # Clustering visualization
    le = LabelEncoder()
    df['nature_encoded'] = le.fit_transform(df['nature'].fillna("Unknown"))
    df = df.dropna(subset=['incident_hour', 'nature_encoded'])  # Ensure valid data for clustering
    kmeans = KMeans(n_clusters=3, random_state=0)
    df['cluster'] = kmeans.fit_predict(df[['incident_hour', 'nature_encoded']])
    cluster_fig = px.scatter(df, x="incident_hour", y="nature_encoded", color="cluster",
                             title="Incident Clusters",
                             labels={"incident_hour": "Hour of Incident", "nature_encoded": "Incident Type"})

    # Bar graph visualization
    bar_data = df['nature'].value_counts()
    bar_fig = px.bar(x=bar_data.index, y=bar_data.values, title="Incident Type Counts",
                     labels={"x": "Incident Type", "y": "Count"})

    # # Time-series visualization
    # df['incident_time'] = pd.to_datetime(df['incident_time'], errors='coerce')  # Convert to datetime
    # df = df.dropna(subset=['incident_time'])  # Remove rows with invalid or missing timestamps

    # df['incident_date'] = pd.to_datetime(df['incident_time']).dt.date  # Extract date only
    # time_series_data = df.groupby('incident_date').size().reset_index(name='count')
    # time_series_fig = px.line(
    #     time_series_data,
    #     x='incident_date',
    #     y='count',
    #     title="Incidents Over Time",
    #     labels={"incident_date": "Date", "count": "Number of Incidents"})

    # Return Visualizations as JSON
    return jsonify({
        "cluster": cluster_fig.to_json(),
        "bar": bar_fig.to_json(),
        # "time_series": time_series_fig.to_json(),
        "hourly_histogram": histogram_data,
        "weekly_trends": line_chart_data
    })


if __name__ == '__main__':
    app.run(debug=True)


