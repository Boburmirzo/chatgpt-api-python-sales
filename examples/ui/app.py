import os
import json
import shutil
import pandas as pd
import streamlit as st
import requests
from dotenv import load_dotenv
from enum import Enum

# Load environment variables
load_dotenv()
api_host = os.environ.get("HOST", "0.0.0.0")
api_port = int(os.environ.get("PORT", 8080))

# Paths for data files
rainforest_path = "../data/rainforest_discounts.jsonl"
csv_path = "../data/csv_discounts.jsonl"


# Enum for data sources
class DataSource(Enum):
    RAINFOREST_API = 'RainforestAPI'
    CSV = 'CSV'


# Streamlit UI elements
st.title("🏷️ Discounts tracker with LLM App")
data_sources = st.multiselect(
    'Choose data sources',
    [source.value for source in DataSource]
)

uploaded_file = st.file_uploader(
    "Upload a CSV file",
    type=("csv"),
    disabled=(DataSource.CSV.value not in data_sources)
)

question = st.text_input(
    "Search for something",
    placeholder="What discounts are looking for?",
    disabled=not data_sources
)

# Handle CSV upload
if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Format the DataFrame rows and write to a jsonlines file
    formatted_rows = [
        {"doc": ', '.join([f"{title}: {value}" for title, value in row.items()])}
        for _, row in df.iterrows()
    ]

    with open(csv_path, 'w') as outfile:
        for obj in formatted_rows:
            outfile.write(json.dumps(obj) + '\n')

# Handle data sources
if DataSource.RAINFOREST_API.value in data_sources:
    shutil.copy("../rainforest/rainforest_discounts.jsonl", rainforest_path)
elif os.path.exists(rainforest_path):
    os.remove(rainforest_path)

if DataSource.CSV.value not in data_sources and os.path.exists(csv_path):
    os.remove(csv_path)

# Handle API request if data source is selected and a question is provided
if data_sources and question:
    url = f'http://{api_host}:{api_port}/'
    data = {"query": question}

    response = requests.post(url, json=data)

    if response.status_code == 200:
        st.write("### Answer")
        st.write(response.json())
    else:
        st.error(f"Failed to send data to API. Status code: {response.status_code}")
