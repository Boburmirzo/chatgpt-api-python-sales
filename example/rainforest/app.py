import pathway as pw
from src.schemas import RainforestDealsInputSchema
from src.data_source import connect, DataSourceType


def run(host, port):
    params = {
      "category_id": "679442011"
      # ... any other params
    }

    # Real-time data coming from external data sources such as Rainforest Deals API
    sales_data = connect(DataSourceType.RAINFOREST_API, RainforestDealsInputSchema, params)
