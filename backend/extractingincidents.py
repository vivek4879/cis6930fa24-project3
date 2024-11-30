
from pypdf import PdfReader
import re

def extracting_rows(pdf_path):
    try:
        with open(pdf_path, "rb") as pdf_file:
            reader = PdfReader(pdf_file)
            all_rows = []

            for page in reader.pages:
                text = page.extract_text(extraction_mode = "layout", layout_mode_space_vertically = False, layout_mode_scale_weight = 2.0)
                if text:
                    rows = text.split("\n")
                    all_rows.extend(rows)
            return all_rows[1:]
    except FileNotFoundError:
        # print(f"file {pdf_path} not found.")
        return []
    
def clean_data(cleaning_list):
    cleaned_data_to_use = []
    for row in cleaning_list:
        if(row.startswith("    ")): 
            continue
        row = row.strip()  # Remove leading and trailing spaces from the row
        split_row = re.split(r"\s{4,}", row)  # Split the row into parts wherever there are 4 or more spaces
        cleaned_row = [part.strip() for part in split_row]  # Strip leading and trailing spaces from each part      
        # print(cleaned_row)
        cleaned_row_new = []
        if(len(cleaned_row) == 5):
            for i in range(5):
                cleaned_row_new.append (cleaned_row[i])
            cleaned_data_to_use.append(cleaned_row_new)
        elif(len(cleaned_row) == 3):
            for i in range(3):
                if i == 2:
                    cleaned_row_new.append('')              
                if i == 3:
                    cleaned_row_new.append('') 
                else:
                    cleaned_row_new.append (cleaned_row[i])
            cleaned_data_to_use.append(cleaned_row_new)

    return cleaned_data_to_use