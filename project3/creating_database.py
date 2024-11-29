
import os
import sqlite3
def createdb():
    #specifying the directory where I want my database, in this case the resourcs folder
    if os.path.exists("./resources/normanpd.db"):
        os.remove("./resources/normanpd.db")
    #creating path to the database file  
    
    db_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'resources'))

    if not os.path.exists(db_directory):
        os.makedirs(db_directory)  # Create the directory if it doesn't exist

    # Specify the database path
    db_path = os.path.join(db_directory, 'normanpd.db')



    #connection to the db
    con = sqlite3.connect(db_path)

    #to execute sql statements and fetch results from sql queries, we need a database cursor, we create it using co.cursor
    cur = con.cursor()
    #executing the sql command using cur.execute()
    cur.execute("DROP TABLE IF EXISTS incidents;")
    cur.execute("CREATE TABLE IF NOT EXISTS incidents(incident_time TEXT, incident_number TEXT, incident_location TEXT,nature TEXT,incident_ori TEXT);")
    # print(f"table inserted")
    return con
    # cur.execute("select * from incidents")