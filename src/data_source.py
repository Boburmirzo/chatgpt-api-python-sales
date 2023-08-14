import pathway as pw
import os
import json
from enum import Enum
from dotenv import load_dotenv
from src.rainforestapi_helper import Get_URL

load_dotenv()

data_dir = os.environ.get("DATA_DIR", "./data/")


class DataSourceType(Enum):
    CSV = "CSV"
    RAINFOREST_API = "RAINFOREST_API"


def connect(source_type, schema=None, params=None):
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
        mode="streaming"
    )
    return sales_data


def read_from_rainforest_api(schema, params):
    def mapper(data: bytes) -> bytes:
        parsed_data = json.loads(data)
        deals_results = parsed_data["deals_results"]
        output = ''
        for deal in deals_results:
            line = json.dumps(deal)
            output += line + '\n'
        return json.dumps({"deals_results": output}).encode()

    table = pw.io.http.read(
        Get_URL(params),
        method="GET",
        response_mapper=mapper,
        schema=schema
    )

    return table
