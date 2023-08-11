import os
from dotenv import load_dotenv
from pathway.stdlib.ml.index import KNNIndex

load_dotenv()
embedding_dimension = int(os.environ.get("EMBEDDING_DIMENSION", 1536))


def Index(embedded_data):
    return KNNIndex(embedded_data, d=embedding_dimension)
