import open_ai_interface
import os
from datetime import datetime
from io import StringIO

STORAGE_DIR = "generated_files"
os.makedirs(STORAGE_DIR, exist_ok=True)

def get_sql_data(data):
    headers = [
        {"name": header.name, "description": header.description, "sample_data": header.sample_data}
        for header in data.headers
    ]
    
    response = open_ai_interface.generate_sql(headers, data.number_of_records, data.table_name, data.create_table)
    
    # Store SQL file locally
    sql_file_storage(response)
    
    return response

def sql_file_storage(sql_data):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = f"data_{timestamp}.sql"
    file_path = os.path.join(STORAGE_DIR, file_name)

    with open(file_path, 'w') as f:
        f.write(sql_data)
