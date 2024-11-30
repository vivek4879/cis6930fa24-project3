from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import urllib.request
from werkzeug.utils import secure_filename
import sqlite3
import pandas as pd
import plotly.express as px
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder
from extractingincidents import extracting_rows, clean_data
from creating_database import createdb
from populatedb import populatedb

UPLOAD_FOLDER = "../resources"
ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__)
CORS(app)  # Enable cross-origin resource sharing
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def connect_db():
    return sqlite3.connect("../resources/normanpd.db")


def fetch_data(query):
    con = connect_db()
    df = pd.read_sql_query(query, con)
    con.close()
    return df


def preprocess_data(df):
    df['incident_hour'] = pd.to_datetime(df['incident_time']).dt.hour
    df['incident_date'] = pd.to_datetime(df['incident_time']).dt.date
    return df


@app.route('/')
def home():
    return "Welcome to the Incident Visualizations API! Use /upload to upload a file or URL and /visualizations to get the data."


@app.route('/favicon.ico')
def favicon():
    return '', 204


@app.route('/upload', methods=['POST'])
def upload_file():
    RESOURCES_FOLDER = "../resources"  # Define the resources folder path

    # Ensure the resources folder exists
    os.makedirs(RESOURCES_FOLDER, exist_ok=True)

    if 'file' in request.files:
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(RESOURCES_FOLDER, filename)  # Save in the resources folder

            # Check if the file exists and remove it
            if os.path.exists(filepath):
                os.remove(filepath)

            file.save(filepath)  # Save the file
            return handle_file(filepath)  # Process the saved file

    elif 'url' in request.json:
        url = request.json['url']
        if url:
            filename = "incident_report.pdf"  # Define a consistent filename for URL downloads
            filepath = os.path.join(RESOURCES_FOLDER, filename)  # Save in the resources folder

            # Check if the file exists and remove it
            if os.path.exists(filepath):
                os.remove(filepath)

            urllib.request.urlretrieve(url, filepath)  # Download and save the file
            return handle_file(filepath)  # Process the saved file

    return jsonify({"error": "No valid file or URL provided"}), 400


def handle_file(filepath):
    """
    Handles file processing: extraction, cleaning, and database population.
    """
    try:
        # Extract rows from PDF
        extracted_rows = extracting_rows(filepath)

        # Clean data
        cleaned_data = clean_data(extracted_rows)

        # Create and populate database
        con = createdb()
        populatedb(con, cleaned_data)
        con.close()

        return jsonify({"message": "File processed and data uploaded successfully."}), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred while processing the file: {str(e)}"}), 500


@app.route('/Visualizations', methods=['GET'])
def visualizations():
    query1 = "SELECT incident_time, nature FROM incidents"
    df1 = fetch_data(query1)

    if df1.empty:
        print("DataFrame df1 is empty.")
        return jsonify({"error": "No data available"}), 400

    df1['incident_time'] = pd.to_datetime(df1['incident_time'], errors='coerce')
    df1 = df1.dropna(subset=['incident_time'])
    df1['hour'] = df1['incident_time'].dt.hour
    df1['day_of_week'] = df1['incident_time'].dt.day_name()

    hourly_data = df1['hour'].value_counts().sort_index()
    histogram_data = {
        "x": hourly_data.index.tolist(),
        "y": hourly_data.values.tolist(),
    }

    weekly_data = df1['day_of_week'].value_counts().reindex(
        ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], fill_value=0
    )
    line_chart_data = {
        "x": weekly_data.index.tolist(),
        "y": weekly_data.values.tolist(),
    }

    query2 = "SELECT incident_time, incident_location, nature FROM incidents"
    df2 = fetch_data(query2)

    if df2.empty:
        print("DataFrame df2 is empty.")
        return jsonify({"error": "No data available"}), 400

    df2 = preprocess_data(df2)

    if df2.empty:
        print("DataFrame df2 is empty after preprocessing.")
        return jsonify({"error": "No data available"}), 400

    le = LabelEncoder()
    df2['nature_encoded'] = le.fit_transform(df2['nature'].fillna("Unknown"))
    df2 = df2.dropna(subset=['incident_hour', 'nature_encoded'])

    if df2[['incident_hour', 'nature_encoded']].isna().any().any():
        print("NaN values found in clustering data.")
        return jsonify({"error": "Clustering data is invalid."}), 400

    kmeans = KMeans(n_clusters=3, random_state=0)
    df2['cluster'] = kmeans.fit_predict(df2[['incident_hour', 'nature_encoded']])
    cluster_fig = px.scatter(
        df2,
        x="incident_hour",
        y="nature_encoded",
        color="cluster",
        title="Incident Clusters",
        labels={"incident_hour": "Hour of Incident", "nature_encoded": "Incident Type"}
    )

    bar_data = df2['nature'].value_counts()
    bar_fig = px.bar(
        x=bar_data.index,
        y=bar_data.values,
        title="Incident Type Counts",
        labels={"x": "Incident Type", "y": "Count"}
    )

    response = {
        "cluster": cluster_fig.to_json(),
        "bar": bar_fig.to_json(),
        "hourly_histogram": histogram_data,
        "weekly_trends": line_chart_data
    }
    # print("Response JSON:", response)
    return jsonify(response)



if __name__ == '__main__':
    app.run(debug=True)