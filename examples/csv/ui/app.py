import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
import requests

load_dotenv()
api_host = os.environ.get("HOST", "0.0.0.0")
api_port = int(os.environ.get("PORT", 8080))

st.title("📝 Discounts tracker with LLM App")
uploaded_file = st.file_uploader("Upload a CSV file", type=("csv"))

question = st.text_input("Search for something",
    placeholder="What discounts are looking for?",
    disabled=not uploaded_file)

if uploaded_file:
    dataframe = pd.read_csv(uploaded_file)
    dataframe.to_csv("../data/discounts.csv", index=False)


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
