# Count the frequency of the most used words in presidential
#speeches and create a visual graphic of the most used words

# Standard library imports
import csv
from pathlib import Path
import json
import urllib.request
from collections import Counter
import re
import os
import sys



# External library imports (requires virtual environment)
import requests  
import pandas as pd
from bs4 import BeautifulSoup
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Local module imports
from fetch_data import fetch_speech,fetch_json_data, fetch_csv_data, fetch_plain_text, fetch_html_data
from process_data import clean_text, count_word_frequencies, process_csv_data, process_excel_data
from visualize_data import plot_word_frequencies, create_word_cloud
from write_data import write_to_csv, write_to_json, write_to_plain_text, write_insights_to_text
#from my_module import my_function

# fetch data
import requests
from bs4 import BeautifulSoup

def fetch_speech(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    # Modify this line according to the structure of the webpage
    speech = soup.find('div', class_='transcript').get_text()
    return speech

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
def fetch_plain_text(url):
    try: 
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching plain text data: {e}")
        return None
def fetch_html_data(url):
    try: 
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.get_text()
    except requests.RequestException as e:
        print(f"Error fetching html data: {e}")
        return None

# process data
import re
from collections import Counter
from nltk.corpus import stopwords


def clean_text(text):
    # Remove punctuation and make lowercase
    text = re.sub(r'[^\w\s]', '', text).lower()
    # Tokenize the text
    words = text.split()
    # Remove stop words
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]
    return words

def count_word_frequencies(words):
    return Counter(words)

import csv
import pandas as pd

def process_csv_data(csv_file):
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        data = list(reader)  # Convert CSV rows to a list of lists
    return data

def process_excel_data(excel_file):
    data = pd.read_excel(excel_file)  # Read Excel file into a DataFrame
    return data

#visualize data
import matplotlib.pyplot as plt
from wordcloud import WordCloud

def plot_word_frequencies(word_counts, top_n=20):
    # Get the most common words
    common_words = word_counts.most_common(top_n)
    words, counts = zip(*common_words)
    
    plt.figure(figsize=(10, 8))
    plt.barh(words, counts, color='skyblue')
    plt.xlabel('Frequency')
    plt.title('Top {} Most Common Words'.format(top_n))
    plt.gca().invert_yaxis()
    plt.show()

def create_word_cloud(word_counts):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_counts)
    
    plt.figure(figsize=(10, 8))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('Word Cloud of Most Common Words')
    plt.show()


#write data
import json
import csv
import pandas as pd

def write_to_csv(data, filename):
    if isinstance(data, str):
        with open(filename, 'w') as file:
            file.write(data)
    else:
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for row in data:
                writer.writerow(row)

def write_to_json(data, filename):
    with open(filename, 'w') as jsonfile:
        json.dump(data, jsonfile, indent=4)

def write_to_plain_text(data, filename):
    with open(filename, 'w') as file:
        file.write(data)

def write_insights_to_text(insights, filename):
    with open(filename, 'w') as file:
        for line in insights:
            file.write(line + '\n')



#main
from fetch_data import fetch_speech,fetch_json_data, fetch_csv_data, fetch_plain_text, fetch_html_data
from process_data import clean_text, count_word_frequencies, process_csv_data, process_excel_data
from visualize_data import plot_word_frequencies, create_word_cloud
from write_data import write_to_csv, write_to_json, write_to_plain_text, write_insights_to_text

def main():
    url = 'https://example.com/speech-transcript'  # Replace with actual URL
    speech_text = fetch_speech(url)

    # Example URLs (replace with actual URLs)
    json_url = 'https://api.example.com/data.json'
    csv_url = 'https://api.example.com/data.csv'
    text_url = 'https://example.com/speech.txt'
    html_url = 'https://example.com/speech.html'
    excel_file = 'data.xlsx'
    
    # Fetch data
    json_data = fetch_json_data(json_url)
    if json_data is None:
        return  # Exit if JSON data fetching fails
    csv_data = fetch_csv_data(csv_url)
    if csv_data is None:
        return  # Exit if CSV data fetching fails
    plain_text_data = fetch_plain_text(text_url)
    if plain_text_data is None:
        return  # Exit if  data fetching fails
    html_data = fetch_html_data(html_url)
    if html_data is None:
        return  # Exit if  data fetching fails
    # Write raw data to files
    write_to_json(json_data, 'data.json')
    write_to_csv(csv_data, 'data.csv')
    write_to_plain_text(plain_text_data, 'speech.txt')
    write_to_plain_text(html_data, 'speech_from_html.txt')
    
    # Process text data (example with plain text data)
    cleaned_words = clean_text(plain_text_data)
    word_counts = count_word_frequencies(cleaned_words)
    
    # Visualize data
    plot_word_frequencies(word_counts)
    create_word_cloud(word_counts)

    # Process CSV data
    csv_insights = process_csv_data('data.csv')
    write_insights_to_text(csv_insights, 'csv_insights.txt')
    
    # Process Excel data
    excel_insights = process_excel_data(excel_file)
    write_insights_to_text(str(excel_insights), 'excel_insights.txt')


if __name__ == '__main__':
    main()
    