from openai_helper import Embeddings


def Contextful(context, data_to_embed):
    return context + context.select(data=Embeddings(data_to_embed))
