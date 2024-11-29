import sqlite3


def populatedb(con, cleaned_data_to_use):
    cur = con.cursor()
    try:
        insertion_query = "INSERT INTO incidents( incident_time, incident_number, incident_location, nature, incident_ori) VALUES (?, ?, ?, ?, ?)"

        for i in range(len(cleaned_data_to_use)):
            try:
                date = cleaned_data_to_use[i][0]
                incident_number = cleaned_data_to_use[i][1]
                location = cleaned_data_to_use[i][2]
                nature = cleaned_data_to_use[i][3]
                incident_ori = cleaned_data_to_use[i][4]
                cur.execute(insertion_query, (date, incident_number, location, nature, incident_ori))

            except IndexError:
                print(f"skipping incident due to error: {cleaned_data_to_use[i]}")
                continue


        con.commit()
    except sqlite3.Error as e:
        print(f"error line is:{cleaned_data_to_use[i]}")
        con.rollback()
        # print(f"error occured while inserting data: {e}")
    finally:
        cur.close()