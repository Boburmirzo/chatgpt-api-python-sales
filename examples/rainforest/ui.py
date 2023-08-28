import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
import requests
import json

load_dotenv()
api_host = os.environ.get("HOST", "0.0.0.0")
api_port = int(os.environ.get("PORT", 8080))

with st.sidebar:
    rainforest_api_key = st.text_input("Rainforest API Key", key="rainforest_api_key", type="password")
    amazon_product_category_id = st.text_input("Amazong Product Category Id", key="amazon_product_category_id", type="password")
    "[Get an Rainforest API key](https://www.rainforestapi.com/)"
    "[View the source code](https://github.com/Boburmirzo/chatgpt-api-python-sales)"

st.title("📝 Discounts tracker with LLM App and Rainforest API")
uploaded_file = st.file_uploader("Upload a CSV file", type=("csv"))

question = st.text_input("Search for something",
    placeholder="What discounts are looking for?",
    disabled=not uploaded_file)

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    # Convert DataFrame to the desired format
    formatted_rows = []
    for _, row in df.iterrows():
        row_data = [f"{title}: {value}" for title, value in row.items()]
        row_data = ', '.join(row_data)
        formatted_rows.append({"doc": row_data})

    # Write to a jsonlines file
    with open('../data/discounts.jsonl', 'w') as outfile:
        for obj in formatted_rows:
            outfile.write(json.dumps(obj) + '\n')


if uploaded_file and question:
    url = f'http://{api_host}:{api_port}/'
    data = {
        "query": f"{question}"
    }

    # Send the POST request with the JSON data payload
    response = requests.post(url, json=data)

    # Check if the request was successful
    if response.status_code == 200:
        # Handle the response, e.g., print it
        st.write("### Answer")
        st.write(response.json())
    else:
        print(f"Failed to send data to API. Status code: {response.status_code}")
