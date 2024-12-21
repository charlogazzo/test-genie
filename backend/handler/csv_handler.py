import open_ai_interface
import os
import csv
import json
import pandas as pd
from datetime import datetime
from io import StringIO

STORAGE_DIR = "generated_files"
os.makedirs(STORAGE_DIR, exist_ok=True)

def get_json_data(data):

    headers = [
        {"name": header.name, "description": header.description, "sample_data": header.sample_data}
        for header in data.headers
    ]
    # TODO: generate the data as JSON and then write each field into a csv row
    # this also helps complete the JSON endpoint
    response = open_ai_interface.generate_data(headers, data.number_of_records)

    # output = StringIO(newline=None)
    json_response = json.loads(response)

    return json_response


def get_csv_data(data):
    
    # convert the json object to a pandas dataframe
    # to allow it to be easily converted to csv
    json_object = pd.DataFrame(get_json_data(data))
    csv_data = json_object.to_csv(index=False, quoting=csv.QUOTE_STRINGS)

    # create the csv file object and store it locally
    # see if the file storage and returning the output to the endpoint
    # can occur on 2 different threads so that an error in generating the file
    # does not prevent the output from being returned
    csv_file_storage(csv_data)

    return csv_data


def csv_file_storage(csv_data):

    # using timestamps as file_name during development
    # in production uuid will be used
    # or another file_name consisting of the user's id
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = f"data_{timestamp}.csv"
    file_path = os.path.join(STORAGE_DIR, file_name)

    # file_name = f"data_{uuid.uuid4().hex}.csv" 
    print(csv_data)
    with open(file_path, 'w', newline='\n') as f:
        f.writelines(csv_data)
