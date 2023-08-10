import os
from dotenv import load_dotenv
from llm_app.model_wrappers import OpenAIEmbeddingModel

load_dotenv()

embedder_locator = os.environ.get("EMBEDDER_LOCATOR", "text-embedding-ada-002")
api_key = os.environ.get("OPENAI_API_TOKEN", "")


def Contextful(context, data_to_embed):
    embeded_data = context + context.select(data=Embeddings(data_to_embed))

    return embeded_data


def Embeddings(data):

    embedder = OpenAIEmbeddingModel(api_key=api_key)

    return embedder.apply(text=data, locator=embedder_locator)
