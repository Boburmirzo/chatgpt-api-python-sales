import os
import requests
import json
from dotenv import load_dotenv
from urllib.parse import urlencode


load_dotenv()

api_key = os.environ.get("RAINFOREST_API_KEY", "")
base_url = os.environ.get("RAINFOREST_BASE_URL", "https://run.mocky.io/v3/f17d8811-09ff-4ba6-8d14-31ef972ce6cd/request")

base_params = {
    "api_key": api_key,
    "type": "deals",
    "amazon_domain": "amazon.com"
}


def get_url(params):
    query_parameters = {**base_params, **params}

    encoded_parameters = urlencode(query_parameters)
    return f"{base_url}?{encoded_parameters}"


def send_request(data_dir, params):
    response = requests.get(get_url(params))

    if response.status_code == 200:
        data = response.json()

        deals_results = data.get('deals_results', [])

        with open(data_dir + "/rainforest/rainforest_discounts.jsonl", 'w') as file:
            for deal in deals_results:
                deal['deal_price'] = deal.get('deal_price', {}).get('value', '')
                deal['old_price'] = deal.get('list_price', {}).get('value', '')
                deal['currency'] = deal.get('list_price', {}).get('currency', '')

                file.write(json.dumps(deal) + '\n')
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
