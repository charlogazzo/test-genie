from openai import OpenAI
import csv

client = OpenAI()

# ask it to do it without the extra response text at the beginning and the end of the file
# only the csv data is required
def generate_data(columns, number_of_records):
    messages = [{
        'role': 'user',
        'content': f'''
I wish to generate test data in csv format.
This test data describes the pulses taken for a number of patients.
The data is to be generated with the following columns:
{columns}


Generate {number_of_records} rows of data using these guidelines:
Duration: describes how long the pulse was measured for. It should be specified in seconds.
Possible values are 45 seconds, 60 seconds and 120 seconds
Date: indicates the date the measurement was taken. This shoud be in dd.mm.yyyy format
Pulse: indicate the average pulse recored for the duration of the measuremnt
Max_Pulse: indicates the maximum pulse recored during the measurement
Age: indicates the patients age

I would like some omitted values in the age column

The csv file should be comma-separated

Exclude any text in the response that is not the CSV data.

'''
    }]

    response = client.chat.completions.create(
        model='chatgpt-4o-latest',
        messages=messages
    )

    data = response.choices[0].message.content.replace('```csv', '').replace('```', '')

    generated_data = []
    generated_data.extend(data.strip().split('\n'))

    return generated_data

# generated_data = []
# data = generate_data()
# generated_data.extend(data.strip().split('\n'))

# with open('./medicalData.csv', 'a+', newline='') as csvfile:
#     csvwriter = csv.writer(csvfile)
#     for row in generated_data:
#         csvwriter.writerow(row.split(','))

# print("Synthetic data generation and appending completed.")

# generate 100 rows of test data using first name, last name, age, project_number
# generate 5 rows first and use those 5 rows to generate 100 more rows
# by asking the model to output similar data types