import csv
import open_ai_interface
from api import DataRequest, HeaderDetails


# the aim of this test is to provide a method to iterate through
# each record add the quotes manually

# Alternatively, OpenAI can be instructed to add quotes to the data

header_details_1 = HeaderDetails()
header_details_1.name = 'country'

header_details_2 = HeaderDetails()
header_details_2.name = 'year of independence'

data = DataRequest()
data.headers = [header_details_1, header_details_2]

headers = [
        {"name": header.name, "description": header.description, "sample_data": header.sample_data}
        for header in data.headers
    ]

generated_data = open_ai_interface.generate_data(headers, 5)
print('generated data type:', type(generated_data))
print(generated_data)