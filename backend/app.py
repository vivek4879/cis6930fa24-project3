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
    # Fetch data
    query = "SELECT incident_time, incident_location, nature FROM incidents"
    df = fetch_data(query)
    df = preprocess_data(df)

    # Clustering visualization
    le = LabelEncoder()
    df['nature_encoded'] = le.fit_transform(df['nature'])
    kmeans = KMeans(n_clusters=3, random_state=0)
    df['cluster'] = kmeans.fit_predict(df[['incident_hour', 'nature_encoded']])
    cluster_fig = px.scatter(df, x="incident_hour", y="nature_encoded", color="cluster",
                             title="Incident Clusters",
                             labels={"incident_hour": "Hour of Incident", "nature_encoded": "Incident Type"})

    # Bar graph visualization
    bar_data = df['nature'].value_counts()
    bar_fig = px.bar( x=bar_data.index,y=bar_data.values, title="Incident Type Counts",labels={"x": "Incident Type", "y": "Count"})

    # Time-series visualization
    time_series_fig = px.line(df.groupby('incident_date').size().reset_index(name='count'),
                              x='incident_date', y='count', title="Incidents Over Time",
                              labels={"incident_date": "Date", "count": "Number of Incidents"})

    # Return Visualizations as JSON
    return jsonify({
        "cluster": cluster_fig.to_json(),
        "bar": bar_fig.to_json(),
        "time_series": time_series_fig.to_json()
    })

if __name__ == '__main__':
    app.run(debug=True)


