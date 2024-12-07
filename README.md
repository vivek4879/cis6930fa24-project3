
# README.md

## Project Name: Incident Data Processing and Visualization System

### Author: Vivek Aher

---

### Project Description

This project provides a comprehensive solution for uploading, processing, and visualizing incident data from NormanPD-style incident PDF reports. The system allows users to:

1. Upload incident data via PDF or URL.
2. Process the data to extract, clean, and store it in a SQLite database.
3. Visualize the data through various interactive charts and graphs using a React-based web interface and a Flask-powered backend.

---

### Installation and Usage

#### Prerequisites

- Python (version 3.8 or above)
- Node.js and npm
- Pipenv (for managing Python virtual environments)
- Flask (for backend development)
- React (for frontend development)

---

#### Steps to Run

1. **Backend Setup (Flask)**:
    - Navigate to the `backend` directory.
    - Install pipenv if not already installed:
      ```bash
      pip install pipenv
      ```
    - Install backend dependencies using pipenv:
      ```bash
      pipenv install
      ```
    - Activate the virtual environment:
      ```bash
      pipenv shell
      ```
    - Start the Flask server:
      ```bash
      python app.py
      ```

2. **Frontend Setup (React)**:
    - Navigate to the `frontend` directory.
    - Install frontend dependencies using npm:
      ```bash
      npm install
      ```
    - Start the React development server:
      ```bash
      npm start
      ```

3. **Access the Application**:
    - Open your browser and navigate to `http://localhost:3000` to access the frontend interface.
    - Use the interface to upload a PDF file or provide a URL for processing incident data.
    - Visualizations, including clustering and trends, will be displayed based on the processed data.

---
#### Visualize Data:

Access the visualizations at `http://localhost:3000`.

---

### Assumptions

1. PDF reports follow a consistent format with tabular incident data.
2. All incident dates and times are in a recognizable format for parsing.
3. Only NormanPD-style PDFs are supported.
4. Data visualization is limited to the incident fields present in the database.
5. Only one pdf uploaded at a time.

---
### External Resources Used

1. **Backend Libraries**:
    - Flask, Flask-CORS
    - pandas
    - sklearn
    - Plotly
    - sqlite3
2. **Frontend Libraries**:
    - React
    - React-Plotly
3. **Documentation**:
    - [Flask Documentation](https://flask.palletsprojects.com/)
    - [React Documentation](https://reactjs.org/)
    - [Plotly Documentation](https://plotly.com/javascript/react/)
4. **Other Resources**:
    - Official Python and JavaScript documentation for specific language features.

---

# Flask API Documentation

## Function Descriptions

### **1. `allowed_file(filename)`**
- **Purpose**: Validates whether the uploaded file is a PDF.
- **Logic**:
  - Checks if the file has an extension.
  - Verifies that the extension matches the allowed type (`pdf`).
- **Returns**: `True` if the file is valid; otherwise, `False`.

---

### **2. `connect_db()`**
- **Purpose**: Establishes a connection to the SQLite database.
- **Logic**: Connects to the database file `normanpd.db` in the `resources` folder.
- **Returns**: An active SQLite connection object.

---

### **3. `fetch_data(query)`**
- **Purpose**: Executes a SQL query and retrieves data from the SQLite database.
- **Logic**:
  - Connects to the database.
  - Executes the SQL query.
  - Converts the results into a Pandas DataFrame for easier manipulation.
- **Returns**: A Pandas DataFrame containing the queried data.

---

### **4. `preprocess_data(df)`**
- **Purpose**: Prepares incident data for further analysis.
- **Logic**:
  - Extracts the hour and date from the `incident_time` column.
  - Adds two new columns: `incident_hour` and `incident_date`.
- **Returns**: A modified DataFrame with the additional columns.

---

### **5. `home()`**
- **Route**: `/`
- **Method**: GET
- **Purpose**: Displays a welcome message and basic usage instructions.
- **Returns**: A plain text message.

---

### **6. `favicon()`**
- **Route**: `/favicon.ico`
- **Method**: GET
- **Purpose**: Handles favicon requests from browsers.
- **Logic**: Returns a 204 status code (no content) to prevent errors.

---

### **7. `feedback()`**
- **Route**: `/feedback`
- **Method**: POST
- **Purpose**: Accepts user feedback about the visualizations.
- **Logic**:
  - Extracts feedback data from the request body in JSON format.
  - Stores the feedback using the `add_feedback()` function.
- **Returns**: A 200 status code to indicate success.

---

### **8. `upload_file()`**
- **Route**: `/upload`
- **Method**: POST
- **Purpose**: Handles file or URL uploads for processing incident data.
- **Logic**:
  - Checks for uploaded file or provided URL in the request.
  - If a file is uploaded:
    - Saves it to the `resources` folder.
    - Processes it with the `handle_file()` function.
  - If a URL is provided:
    - Downloads the PDF from the URL.
    - Processes it with the `handle_file()` function.
  - Returns an error if neither is provided.
- **Returns**: A JSON success or error message.

---

### **9. `handle_file(filepath)`**
- **Purpose**: Processes the uploaded file by extracting, cleaning, and saving data to the database.
- **Logic**:
  - Extracts rows from the PDF using `extracting_rows()`.
  - Cleans the extracted data using `clean_data()`.
  - Resets or creates the database using `createdb()`.
  - Populates the database with the cleaned data using `populatedb()`.
- **Returns**: A success message if processing is successful; an error message otherwise.

---

### **10. `visualizations()`**
- **Route**: `/Visualizations`
- **Method**: GET
- **Purpose**: Generates visualizations from database data.
- **Logic**:
  - Fetches incident data from the database using SQL queries.
  - Processes the data to generate:
    - **Clustering Visualization**: Groups incidents by time and nature using KMeans.
    - **Bar Chart**: Counts incidents by type.
    - **Hourly Trends**: Shows the frequency of incidents by hour.
    - **Weekly Trends**: Visualizes incidents across the days of the week.
  - Encodes the visualizations in JSON format.
- **Returns**: A JSON object containing all visualizations and their data.

---

### **11. `add_feedback(feedback)`**
- **Purpose**: Saves user feedback into the SQLite database.
- **Logic**:
  - Creates a `feedback` table if it does not already exist.
  - Inserts the provided feedback into the table.
  - Commits the transaction to the database.
- **Returns**: None (logs success to the console).

---

## How to Use the API

### **Base URL**
http://127.0.0.1:5000/


### **Endpoints**

#### **Home**
- **Route**: `/`
- **Method**: GET
- **Description**: Displays a welcome message with instructions for using the API.

#### **Upload File or URL**
- **Route**: `/upload`
- **Method**: POST
- **Description**: Processes an uploaded PDF file or a PDF URL.
- **Parameters**:
  - `file`: A PDF file (multipart form data).
  - `url`: A URL pointing to a PDF file (JSON).
- **Response**:
  - Success: `{"message": "File processed and data uploaded successfully."}`
  - Error: `{"error": "No valid file or URL provided"}`

#### **Visualizations**
- **Route**: `/Visualizations`
- **Method**: GET
- **Description**: Provides visualizations of the incident data.
- **Response**:
  - JSON object containing clustering, bar charts, and trend data.

#### **Submit Feedback**
- **Route**: `/feedback`
- **Method**: POST
- **Description**: Allows users to submit feedback.
- **Parameters**:
  - `feedback`: A string containing user feedback (JSON).
- **Response**:
  - Success: A status code of 200.

---
# React Component Documentation: `Visualizations`

## Component Overview
The `Visualizations` component handles file or URL submissions, fetches incident data from the backend, and displays visualizations such as clustering, bar charts, hourly histograms, and weekly trends using Plotly.js.

---

## Component Functions

### **1. `useState` Hooks**
- **`file`**: Stores the selected file for upload.
- **`url`**: Stores the URL input for PDF retrieval.
- **`visualizationData`**: Holds the fetched visualization data.
- **`error`**: Stores error messages for display.
- **`prevData`**: Keeps track of previously fetched visualization data for refresh purposes.

---

### **2. `handleFileChange(e)`**
- **Purpose**: Updates the state when a file is selected for upload.
- **Logic**:
  - Sets the `file` state to the selected file.
  - Clears the `url` state to ensure only one input method is used.
- **Parameters**:
  - `e`: Event object from the file input.
- **Usage**: Triggered by the file input field.

---

### **3. `refreshPage()`**
- **Purpose**: Resets the `visualizationData` to allow new uploads.
- **Logic**:
  - Saves the current visualization data to `prevData`.
  - Clears the `visualizationData` state.

---

### **4. `handleUrlChange(e)`**
- **Purpose**: Updates the state when a URL is entered.
- **Logic**:
  - Sets the `url` state to the input value.
  - Clears the `file` state to ensure only one input method is used.
- **Parameters**:
  - `e`: Event object from the text input.
- **Usage**: Triggered by the URL input field.

---

### **5. `fetchVisualizations()`**
- **Purpose**: Fetches visualization data from the backend.
- **Logic**:
  - Sends a GET request to the backend at `/Visualizations`.
  - Sets the response data in `visualizationData` state.
  - Sets an error message if the request fails.
- **Usage**: Called after successful file or URL submission.

---

### **6. `handleSubmit(e)`**
- **Purpose**: Handles form submission for uploading files or URLs.
- **Logic**:
  - Prevents the default form submission behavior.
  - Checks if `file` or `url` is provided:
    - **File**: Appends the file to a `FormData` object and uploads via POST.
    - **URL**: Sends a JSON object with the URL to the backend via POST.
  - Calls `fetchVisualizations()` to retrieve visualizations after successful upload.
  - Sets an error if neither file nor URL is provided or the upload fails.
- **Parameters**:
  - `e`: Event object from the form submission.
- **Usage**: Triggered by the "Submit" button.

---

## Rendering Logic

### **Error Display**
- If `error` is set, displays the error message in a `div`.

### **Upload Form**
- Displays a form with:
  - File input for PDF upload.
  - Text input for URL submission.
  - Submit button.
- Triggered when `visualizationData` is `null`.

### **Visualizations**
- Displays the fetched visualizations when `visualizationData` is available.
- Includes:
  - **Clustering Visualization**:
    - Scatter plot showing incident clustering based on time and type.
    - Generated using `Plot` component from Plotly.js.
  - **Bar Chart**:
    - Displays the count of incidents by type.
    - Created using `Plot` component.
  - **Hourly Histogram**:
    - Bar chart showing incident frequency by hour.
  - **Weekly Trends**:
    - Line chart showing incidents across days of the week.

---

## Component Structure

### **File Upload Section**
- Includes:
  - **File Input**: Allows users to select a PDF file.
  - **URL Input**: Allows users to enter a URL to a PDF file.
  - **Submit Button**: Sends the selected input for processing.

### **Visualization Display**
- Includes:
  - A "Refresh" button to upload a new file.
  - Visualizations based on the fetched data:
    - Clustering (Scatter plot).
    - Incident type counts (Bar chart).
    - Hourly incident trends (Histogram).
    - Weekly incident trends (Line chart).

---

## Dependencies
- **React**: Core library for building the component.
- **axios**: Handles HTTP requests to the backend.
- **Plotly.js**: Used for creating interactive visualizations.
- **Input.js**: A reusable input component used in the form.

---

## Example Workflow
1. User uploads a file or enters a URL.
2. The backend processes the input and returns visualization data.
3. The component fetches and displays the data as interactive plots.

---

## Watch the Demo
[![YouTube Demo](https://img.youtube.com/vi/bosWzV0g6j4/0.jpg)](https://youtu.be/bosWzV0g6j4)

Click the thumbnail to watch the video on YouTube.


