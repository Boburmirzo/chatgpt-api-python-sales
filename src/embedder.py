import os
from dotenv import load_dotenv
from pathway.stdlib.ml.index import KNNIndex
from src.openaiapi_helper import openai_embedder

load_dotenv()

embedding_dimension = int(os.environ.get("EMBEDDING_DIMENSION", 1536))


def contextful(context, data_to_embed):
    return context + context.select(data=openai_embedder(data_to_embed))


def index_embeddings(embedded_data):
    return KNNIndex(embedded_data, d=embedding_dimension)
