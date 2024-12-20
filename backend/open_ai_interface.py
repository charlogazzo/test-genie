from openai import OpenAI
import csv

client = OpenAI()

# ask it to do it without the extra response text at the beginning and the end of the file
# only the csv data is required
def generate_data(headers, number_of_records):
    # separate the header attributes here into different variables
    # so they can be used in text
    header_description = '\n'.join([(header['name'] + ': ' + header['description']) for header in headers])
    header_examples = ', '.join([(header['name'] + ': ' + str(header['sample_data'])) for header in headers])

    messages = [{
        'role': 'user',
        'content': f'''
I wish to generate test data in csv format.
This test data describes the pulses taken for a number of patients.
The data is to be generated with the following headers:
{[header['name'] for header in headers]}

--- add description and sample data ---
These are further details that describe the headers:
{header_description}

These are some examples to generate the headers according to:
{header_examples}

Generate {number_of_records} rows of data

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


# print("Synthetic data generation and appending completed.")

# generate 100 rows of test data using first name, last name, age, project_number
# generate 5 rows first and use those 5 rows to generate 100 more rows
# by asking the model to output similar data types
