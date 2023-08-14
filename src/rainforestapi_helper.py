import os
from dotenv import load_dotenv
from urllib.parse import urlencode

load_dotenv()

api_key = os.environ.get("RAINFOREST_API_KEY", "")
base_params = {
    "api_key": api_key,
    "type": "deals",
    "amazon_domain": "amazon.com"
}


def Get_URL(params):
    base_url = "https://run.mocky.io/v3/f17d8811-09ff-4ba6-8d14-31ef972ce6cd/request"

    query_parameters = {**base_params, **params}

    encoded_parameters = urlencode(query_parameters)
    return f"{base_url}?{encoded_parameters}"
