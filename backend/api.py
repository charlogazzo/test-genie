# from fastapi import FastAPI, HTTPException, Query
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import FileResponse
# from pydantic import BaseModel
# from typing import List, Optional
# import open_ai_interface
# import os
# import csv
# from datetime import datetime

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=['*'],
#     allow_credentials = True,
#     allow_methods = ['*'],
#     allow_headers = ['*']
# )

# # to store the generated files
# STORAGE_DIR = "generated_files"
# os.makedirs(STORAGE_DIR, exist_ok=True)

# class HeaderDetails(BaseModel):
#     name: str  # The name of the header
#     description: Optional[str] = None  # A description of what the header represents
#     sample_data: Optional[List[str]] = None  # Optional sample data for the header

# class DataRequest(BaseModel):
#     headers: List[HeaderDetails]
#     number_of_records: int

# # TODO: check the real format of csv files
# # how the headers are written and where quotation marks are used
# # will the quotation marks be needed for numbers?
# @app.post('/csv-data')
# def get_csv(data: DataRequest):
#     if not data.headers:
#         raise HTTPException(status_code=400, detail="Headers cannot be empty")
#     if data.number_of_records <= 0:
#         raise HTTPException(status_code=400, detail="Number of requested records must be more than 0")
    
#     # Generate filename with a timestamp
#     timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
#     file_name = f"data_{timestamp}.csv"
#     file_path = os.path.join(STORAGE_DIR, file_name)

#     headers = [
#         {"name": header.name, "description": header.description, "sample_data": header.sample_data}
#         for header in data.headers
#     ]
#     response = open_ai_interface.generate_data(headers, data.number_of_records)

#     with open(file_path, mode="w", newline="", encoding="utf-8") as csvfile:
#         csvwriter = csv.writer(csvfile)
#         for row in response:
#             csvwriter.writerow(row.split(','))
#         # TODO: Figure out how to write string values with quotation marks
#         # The user will state the data types they require for each field
#         # these data types will be used to format the data as it's being written to the csv file

#     return {"file_path": file_path, "file_name": file_name}

# @app.get('/download-csv/{file_name}')
# def download_csv(file_name: str):
#     file_path = os.path.join(STORAGE_DIR, file_name)
#     if not os.path.exists(file_path):
#         raise HTTPException(status_code=404, detail='file not found')
#     return FileResponse(file_path, media_type='text/csv', filename=file_name)


# # create an endpoint for JSON data

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel
from typing import List, Optional
import open_ai_interface
import os
import csv
from datetime import datetime
from io import StringIO

app = FastAPI()

# Allow CORS from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# to store the generated files
STORAGE_DIR = "generated_files"
os.makedirs(STORAGE_DIR, exist_ok=True)

class HeaderDetails(BaseModel):
    name: str
    description: Optional[str] = None
    sample_data: Optional[List[str]] = None

class DataRequest(BaseModel):
    headers: List[HeaderDetails]
    number_of_records: int

@app.post('/csv-data')
def get_csv(data: DataRequest):
    if not data.headers:
        raise HTTPException(status_code=400, detail="Headers cannot be empty")
    if data.number_of_records <= 0:
        raise HTTPException(status_code=400, detail="Number of requested records must be more than 0")

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = f"data_{timestamp}.csv"
    file_path = os.path.join(STORAGE_DIR, file_name)

    headers = [
        {"name": header.name, "description": header.description, "sample_data": header.sample_data}
        for header in data.headers
    ]
    response = open_ai_interface.generate_data(headers, data.number_of_records)

    output = StringIO()
    csvwriter = csv.writer(output, quoting=csv.QUOTE_MINIMAL)
    # csvwriter.writerow([header['name'] for header in headers])
    for row in response:
        csvwriter.writerow(row.split(','))

    # find a way to store this output locally and also send it as a Streaming response
    output.seek(0)
    return StreamingResponse(output, media_type="text/csv", headers={"Content-Disposition": f"attachment; filename={file_name}"})

@app.get('/download-csv/{file_name}')
def download_csv(file_name: str):
    file_path = os.path.join(STORAGE_DIR, file_name)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail='file not found')
    return FileResponse(file_path, media_type='text/csv', filename=file_name)

# @app.post('/json-data')
# def get_json(data: DataRequest):
#     if not data.headers:
#         raise HTTPException(status_code=400, detail="Headers cannot be empty")
#     if data.number_of_records <= 0:
#         raise HTTPException(status_code=400, detail="Number of requested records must be more than 0")

#     headers = [
#         {"name": header.name, "description": header.description, "sample_data": header.sample_data}
#         for header in data.headers
#     ]
#     response = open_ai_interface.generate_data(headers, data.number_of_records)

#     return JSONResponse(content=response)
