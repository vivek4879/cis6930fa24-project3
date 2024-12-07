import pytest
import os
import sqlite3
from app import allowed_file, connect_db, handle_file, app
from creating_database import createdb
from extractingincidents import extracting_rows, clean_data
from fetchingincidents import fetchincidents
from populatedb import populatedb

# Test for app.py
def test_allowed_file():
    assert allowed_file("test.pdf") is True
    assert allowed_file("test.txt") is False
    assert allowed_file("test") is False

def test_connect_db():
    con = connect_db()
    assert isinstance(con, sqlite3.Connection)
    con.close()


# Test for extractingincidents.py
def test_extracting_rows():
    test_file = "../backend/test_incident_report.pdf"

    # Ensure the test file exists
    assert os.path.exists(test_file), "The test_incident_report.pdf file does not exist in the backend folder."

    rows = extracting_rows(test_file)
    assert isinstance(rows, list)
    assert len(rows) > 0

def test_clean_data():
    raw_data = [
        "2024-01-01    1234    Some Location    Some Nature    ORI123",
        "2024-01-02    5678    Another Location    Another Nature    ORI567"
    ]
    cleaned_data = clean_data(raw_data)
    assert isinstance(cleaned_data, list)
    assert len(cleaned_data) == 2

# Test for fetchingincidents.py
@pytest.mark.parametrize("url, expected", [
    ("https://www.example.com/test.pdf", None),  # Replace with a valid test URL if needed
    ("https://invalid-url.com", None),
])
def test_fetchincidents(url, expected):
    response = fetchincidents(url)
    assert response == expected

# Test for populatedb.py
def test_populatedb():
    con = createdb()
    test_data = [
        ["2024-01-01", "1234", "Some Location", "Some Nature", "ORI123"],
        ["2024-01-02", "5678", "Another Location", "Another Nature", "ORI567"]
    ]
    populatedb(con, test_data)

    cur = con.cursor()
    cur.execute("SELECT * FROM incidents")
    rows = cur.fetchall()
    assert len(rows) == 2
    con.close()
