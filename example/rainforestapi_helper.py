import os
import json
import pathway as pw
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("RAINFOREST_API_KEY", "")


def FindAmazonDeals(category_id):
    def mapper(msg: bytes) -> bytes:
        parsed_data = json.loads(msg.decode())
        # Extract deals_results
        deals_results = parsed_data["deals_results"]
        # Map the desired fields for each deal
        mapped_results = [
            {
                "position": deal["position"],
                "link": deal["link"],
                "asin": deal["asin"],
                "deal_type": deal["deal_type"],
                "title": deal["title"],
                "image": deal["image"],
                "deal_price": deal["deal_price"]["raw"],
                "list_price": deal["list_price"]["raw"],
                "current_price": deal["current_price"]["raw"],
                "merchant_name": deal["merchant_name"],
                "description": deal["description"],
                "rating": deal["rating"]
             } for deal in deals_results
        ]

        return json.dumps(mapped_results).encode()

    url = f"https://api.rainforestapi.com/request?api_key={api_key}&type=deals&amazon_domain=amazon.com&category_id={category_id}"

    value_columns = [
        "position",
        "link",
        "asin",
        "deal_type",
        "title",
        "image",
        "deal_price",
        "list_price",
        "current_price",
        "merchant_name",
        "description",
        "rating"
    ]

    table = pw.io.http.read(
        url,
        method="GET",
        value_columns=value_columns,
        response_mapper=mapper,
        autocommit_duration_ms=1000,
    )

    pw.debug.compute_and_print(table)

    return table
