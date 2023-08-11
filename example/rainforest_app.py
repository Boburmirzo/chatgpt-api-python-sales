import pathway as pw
from schemas import RainforestDealsInputSchema
from transform import Transform
from embedder import Contextful
from prompt import Prompt
from data_source import Connect, DataSourceType
from index_embeddings import Index


def run(host, port):
    params = {
      "category_id": "679442011"
      # ... any other params
    }

    # Real-time data coming from external data sources such as Rainforest Deals API
    sales_data = Connect(DataSourceType.RAINFOREST_API, RainforestDealsInputSchema, params)
