import pathway as pw

from pathway.stdlib.ml.index import KNNIndex
from schemas import DiscountsInputSchema, QueryInputSchema
from transform import Transform
from embedder import Contextful
from prompt import Prompt


def run(
    data_dir,
    host,
    port,
    embedding_dimension
):
    # Real-time data coming from external data sources such as csv file
    sales_data = pw.io.csv.read(
        data_dir,
        schema=DiscountsInputSchema,
        mode="streaming",
        autocommit_duration_ms=50,
    )

    # Data source rows transformed into structured documents
    documents = Transform(sales_data)

    # Each section is embedded with the OpenAI Embeddings API and retrieve the embedded result
    embedded_data = Contextful(context=documents, data_to_embed=documents.doc)

    # Constructs an index on the generated embeddings in real-time
    index = KNNIndex(embedded_data, d=embedding_dimension)

    # Given a user question as a query from your API
    query, response_writer = pw.io.http.rest_connector(
        host=host,
        port=port,
        schema=QueryInputSchema,
        autocommit_duration_ms=50,
    )

    # Generates an embedding for the query from the OpenAI Embeddings API
    embedded_query = Contextful(context=query, data_to_embed=pw.this.query)

    # Using the embeddings, retrieve the vector index by relevance to the query
    query_context = index.query(embedded_query, k=3).select(
        pw.this.query, local_indexed_data_list=pw.this.result
    )

    # Inserts the question and the most relevant sections into a message to OpenAI Chat Completion API
    responses = Prompt(query_context)

    # Returns ChatGPT's answer
    response_writer(responses)

    pw.run()
