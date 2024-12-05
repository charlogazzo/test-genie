from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List
import open_ai_interface

app = FastAPI()

class DataRequest(BaseModel):
    headers: List[str]
    number_of_records: int

# start with an endpoint to generate csv files with no added description
@app.post('/csv-data')
def get_csv(data: DataRequest):
    print(open_ai_interface.client)
    response = open_ai_interface.generate_data(data.headers, data.number_of_records)
    return response


# create an endpoint for JSON data