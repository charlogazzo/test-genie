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
I wish to generate test data in json format.
The data is to be generated with the following headers:
{[header['name'] for header in headers]}

--- add description and sample data ---
These are further details that describe the headers:
{header_description}

These are some examples to generate the headers according to:
{header_examples}

Generate {number_of_records} rows of data

Exclude any text in the response that is not the JSON data.

'''
    }]

    response = client.chat.completions.create(
        model='chatgpt-4o-latest',
        messages=messages
    )

    data = response.choices[0].message.content.replace('```json', '').replace('```', '')

    generated_data = []
    generated_data.extend(data.strip().split('\n'))


    return data


def generate_sql(headers, number_of_records, table_name, create_table):
    header_description = '\n'.join([(header['name'] + ': ' + header['description']) for header in headers])
    header_examples = ', '.join([(header['name'] + ': ' + str(header['sample_data'])) for header in headers])
    print('create table:', create_table)

    create_table = 'a' if create_table == 'CREATE TABLE' else 'no'

    messages = [{
        'role': 'user',
        'content': f'''
I wish to generate test data that will be inserted in an sql database
The data is to be generated with the following column names:
{[header['name'] for header in headers]}

--- add description and sample data ---
These are further details that describe the headers:
{header_description}

These are some examples to generate the headers according to:
{header_examples}

Generate {number_of_records} rows of data

Exclude any text in the response that is not the SQL data.

The name of the table is {table_name} and generate {create_table} create table statement.
If a create table statement is added, drop the table with the same table name first
'''
    }]

    response = client.chat.completions.create(
        model='chatgpt-4o-latest',
        messages=messages
    )

    return response.choices[0].message.content.replace('```sql', '').replace('```', '')

    

