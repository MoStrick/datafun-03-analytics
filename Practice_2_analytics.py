#Introduction
    ##Week 3 Module 3


# Standard library imports
import csv
from pathlib import Path
import json
import urllib.request
from collections import Counter




# External library imports (requires virtual environment)
import requests  
import pandas as pd
from bs4 import BeautifulSoup


# Local module imports
from fetch_data import fetch_web_data
from process_data import process_web_data
from write_data import write_to_csv, write_to_json, write_to_excel

# Fetch data
url = 'http://example.com/data'
raw_data = fetch_web_data(url)
def fetch_web_data(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text
def fetch_json_data(url):
    try: 
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching JSON data: {e}")
        return None

def fetch_csv_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching CSV data: {e}")
        return None


    
# Process data
    processed_data = process_web_data(raw_data)
def process_web_data(raw_data):
     # Example: assuming raw_data is HTML and we need to parse it
    soup = BeautifulSoup(raw_data, 'html.parser')
    data = soup.find_all('p')  # Example: extracting all paragraph elements
    processed_data = Counter([p.text for p in data])

     # Example processing: parsing JSON
    data = json.loads(raw_data)
    processed_data = Counter(data)
    return processed_data

def process_json_data(json_data):
    # Example: processing JSON data
    return Counter(json_data)
    # Example processing: count the occurrences of each course
    courses = [course for user in json_data for course in user.get('courses', [])]
    course_counts = Counter(courses)
    return course_counts

   

# Write data
    write_to_csv(processed_data, 'data.csv')
    write_to_json(processed_data, 'data.json')
    write_to_excel(processed_data, 'data.xlsx')
def write_to_csv(data, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for key, value in data.items():
            writer.writerow([key, value])

def write_to_json(data, filename):
    with open(filename, 'w') as jsonfile:
        json.dump(data, jsonfile)

def write_to_excel(data, filename):
    df = pd.DataFrame(list(data.items()), columns=['Key', 'Value'])
    df.to_excel(filename, index=False)


def main():
    # Fetch data
    url = 'http://example.com/data'
    raw_data = fetch_web_data(url)
    json_data = fetch_json_data(url)
    
    # Process data
    processed_data = process_web_data(raw_data)
    processed_data = process_json_data(json_data)
    # Write data
    write_to_csv(processed_data, 'data.csv')
    write_to_json(processed_data, 'data.json')
    write_to_excel(processed_data, 'data.xlsx')

    write_to_csv(processed_data, 'courses.csv')
    write_to_json(processed_data, 'courses.json')

if __name__ == '__main__':
    main()

