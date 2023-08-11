import pathway as pw
import os
import json
from enum import Enum
from dotenv import load_dotenv
from rainforestapi_helper import Get_URL

load_dotenv()

data_dir = os.environ.get("DATA_DIR", "./data/")


class DataSourceType(Enum):
    CSV = "CSV"
    RAINFOREST_API = "RAINFOREST_API"


def Connect(source_type, schema, params=None):
    if source_type == DataSourceType.CSV:
        return read_from_csv(data_dir, schema)
    elif source_type == DataSourceType.RAINFOREST_API:
        return read_from_rainforest_api(schema, params)
    else:
        raise ValueError(f"Unsupported data source type: {source_type}")


def read_from_csv(data_dir, schema):
    sales_data = pw.io.csv.read(
        data_dir,
        schema=schema,
        mode="streaming",
        autocommit_duration_ms=50,
    )
    return sales_data


def read_from_rainforest_api(schema, params):
    def mapper(msg: bytes) -> bytes:
        parsed_data = json.loads(msg.decode())
        # Extract deals_results
        deals_results = parsed_data["deals_results"]
        json_output = ''
        for deal in deals_results:
            # Map the desired fields for each deal
            mapped_results = {
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
            }
            json_output += json.dumps(mapped_results)

        return json.dumps(json_output).encode()

    table = pw.io.http.read(
        Get_URL(params),
        method="GET",
        response_mapper=mapper,
        schema=schema,
        autocommit_duration_ms=1000,
    )

    pw.debug.compute_and_print(table)

    return table
