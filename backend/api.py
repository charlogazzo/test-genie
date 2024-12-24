from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse, JSONResponse
from pydantic import BaseModel
from typing import List, Optional
from io import StringIO
import handler.csv_handler
import os
import uuid

import handler.sql_handler


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
    table_name: Optional[str]
    create_table: Optional[str]

# csv
@app.post('/csv-data')
def get_csv(data: DataRequest):
    if not data.headers:
        raise HTTPException(status_code=400, detail="Headers cannot be empty")
    if data.number_of_records <= 0:
        raise HTTPException(status_code=400, detail="Number of requested records must be more than 0")
    
    csv_output = handler.csv_handler.get_csv_data(data)
    
    # csv_output.seek(0)
    return StreamingResponse(csv_output, media_type="text/csv", headers={"Content-Disposition": f"attachment; filename='csv_data.csv'"})

@app.get('/download-csv/{file_name}')
def download_csv(file_name: str):
    file_path = os.path.join(STORAGE_DIR, file_name)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail='file not found')
    return FileResponse(file_path, media_type='text/csv', filename=file_name)

# json
@app.post('/json-data')
def get_json(data: DataRequest):
    if not data.headers:
        raise HTTPException(status_code=400, detail="Headers cannot be empty")
    if data.number_of_records <= 0:
        raise HTTPException(status_code=400, detail="Number of requested records must be more than 0")
    
    json_output = handler.csv_handler.get_json_data(data)
    return JSONResponse(content=json_output)

def download_json(file_name: str):
    file_path = os.path.join(STORAGE_DIR, file_name)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail='File not found')
    return FileResponse(file_path, 200, media_type='application/json', filename=file_name)

@app.post('/sql-data')
def get_sql(data: DataRequest):
    if not data.headers:
        raise HTTPException(status_code=400, detail="Headers cannot be empty")
    if data.number_of_records <= 0:
        raise HTTPException(status_code=400, detail="Number of requested records must be more than 0")
    
    if not data.table_name:
        raise HTTPException(status_code=400, detail='Table name is required for sql data')
    
    sql_output = handler.sql_handler.get_sql_data(data)

    return StreamingResponse(
        StringIO(sql_output),
        media_type="text/sql",
        headers={"Content-Disposition": f"attachment; filename='sql_data.sql'"}
    )

@app.get('/download-sql/{file_name}')
def download_sql(file_name: str):
    file_path = os.path.join(STORAGE_DIR, file_name) 
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail='File not found')
    return FileResponse(file_path, media_type='text/sql', filename=file_name)
