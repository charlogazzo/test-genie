import open_ai_interface
import os
import csv
from datetime import datetime
from io import StringIO

STORAGE_DIR = "generated_files"
os.makedirs(STORAGE_DIR, exist_ok=True)

def get_csv_data(data):

    headers = [
        {"name": header.name, "description": header.description, "sample_data": header.sample_data}
        for header in data.headers
    ]
    response = open_ai_interface.generate_data(headers, data.number_of_records)

    output = StringIO(newline=None)
    print(response)
    csvwriter = csv.writer(output, quoting=csv.QUOTE_MINIMAL)
    
    for row in response:
        csvwriter.writerow(row.split(','))
    
    # see if the file storage and returning the output to the endpoint
    # can occur on 2 different threads so that an error in generating the file
    # does not prevent the output from being returned
    csv_file_storage(output)

    return output

def csv_file_storage(output):

    # using timestamps as file_name during development
    # in production uuid will be used
    # or another file_name consisting of the user's id
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = f"data_{timestamp}.csv"
    file_path = os.path.join(STORAGE_DIR, file_name)

    # file_name = f"data_{uuid.uuid4().hex}.csv" 

    with open(file_path, 'w') as f:
        f.write(output.getvalue())