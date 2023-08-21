import pathway as pw
import os
from enum import Enum
from dotenv import load_dotenv
from src.rainforestapi_helper import send_request
from src.csv_custom_connector import CsvFileCustomConnector

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
    sales_data = pw.io.python.read(
        CsvFileCustomConnector(data_dir + "/csv"),
        value_columns=["doc"],
        format="json"
    )
    return sales_data


def read_from_rainforest_api(schema, params):

    send_request(data_dir, params)

    sales_data = pw.io.jsonlines.read(
        data_dir + "/rainforest",
        schema=schema,
        mode="streaming",
        autocommit_duration_ms=50,
    )

    return sales_data
