
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