# import argparse
# from pypdf import PdfReader
# import os
# import sqlite3
# from creating_database import createdb
# from extractingincidents import extracting_rows 
# from extractingincidents import clean_data 
# from fetchingincidents import fetchincidents
# from populatedb import populatedb
# from urllib.parse import urlparse

# def main(url):
#     if is_url(url):
#         print("input is url.Fetching pdf")
#         #Download data
#         fetchincidents(url)
#     else:
#         if url.endswith('.pdf') and os.path.isfile(url):
#             print("input is a valid pdf file. using directly")
#             os.rename(url, "incident_report.pdf")
#         else:
#             raise ValueError("Input neither URL nor valid PDF")
#     print("File saved as incident_report.pdf")
    
#     # Extract data
#     pdf_path = os.getcwd()
#     required_path = os.path.join(pdf_path,"incident_report.pdf")
#     extracted_rows_list = extracting_rows(required_path)
#     # print(extracted_rows_list)
#     cleaned_data_to_use = clean_data(extracted_rows_list)
#     # print(cleaned_data_to_use)


#     con = createdb()
    
#     # # Insert data
#     populatedb(con, cleaned_data_to_use)

#     # # #Print incident counts
#     status(con)
# def status(con):
#     cur = con.cursor()
#     cur.execute("select nature, count(*) as count from incidents group by nature order by nature asc;")
#     # cur.execute("select * from incidents where Nature = 'MVA Non Injury';")
#     rows = cur.fetchall()
#     # print(rows)

#     for row in rows:
#         nature = row[0]
#         count = row[1]
#         print(f"{nature}|{count}")
#     cur.close
# def is_url(path):
#     try:
#         result = urlparse(path)
#         return all([result.scheme,result.netloc])
#     except ValueError:
#         return False

# if __name__ == '__main__':
#     parser = argparse.ArgumentParser()
#     parser.add_argument("--incidents", type = str, required = True, help = "Incident summary url.")

#     args = parser.parse_args()
#     if args.incidents:
#         main(args.incidents)