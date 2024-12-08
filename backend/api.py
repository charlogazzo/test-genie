from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
import open_ai_interface

app = FastAPI()

class HeaderDetails(BaseModel):
    name: str  # The name of the header
    description: Optional[str] = None  # A description of what the header represents
    sample_data: Optional[List[str]] = None  # Optional sample data for the header

# TODO: Look at how to download files through postman
class DataRequest(BaseModel):
    headers: List[HeaderDetails]
    number_of_records: int

# TODO: add a field for the metadata (is that the word?)
# the attribute should contain a description of the fields
# another attribute should also contain examples of the data the client wishes to generate
# should be passed using python dictionaries
@app.post('/csv-data')
def get_csv(data: DataRequest):
    print(open_ai_interface.client)
    headers = [
        {"name": header.name, "description": header.description, "sample_data": header.sample_data}
        for header in data.headers
    ]
    response = open_ai_interface.generate_data(headers, data.number_of_records)
    return response


# create an endpoint for JSON data