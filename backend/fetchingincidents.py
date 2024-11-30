from pypdf import PdfReader
import urllib.request


def fetchincidents(url):
    headers = {}
    headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"

    req = urllib.request.Request(url, headers=headers)
    try:
        response = urllib.request.urlopen(req)
        pdf_data = response.read()
        # print("PDF downloaded")
        #to write the data to another file and download the file.
        if pdf_data:
            with open("incident_report.pdf", "wb") as f:
                f.write(pdf_data)
        return pdf_data
    except urllib.error.URLError as given_error:
        # print(f"PDF download failed: {given_error}")
        return None