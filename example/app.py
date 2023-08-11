import pathway as pw
from schemas import DiscountsInputSchema, QueryInputSchema
from transform import Transform
from embedder import Contextful
from prompt import Prompt
from data_source import Connect, DataSourceType
from index_embeddings import Index


def run(host, port):
    # Real-time data coming from external data sources such as csv file
    sales_data = Connect(DataSourceType.CSV, DiscountsInputSchema)

    # Data source rows transformed into structured documents
    documents = Transform(sales_data)

    # Compute embeddings for each document using the OpenAI Embeddings API
    embedded_data = Contextful(context=documents, data_to_embed=documents.doc)

    # Construct an index on the generated embeddings in real-time
    index = Index(embedded_data)

    # Given a user question as a query from your API
    query, response_writer = pw.io.http.rest_connector(
        host=host,
        port=port,
        schema=QueryInputSchema,
        autocommit_duration_ms=50,
    )

    # Generate embeddings for the query from the OpenAI Embeddings API
    embedded_query = Contextful(context=query, data_to_embed=pw.this.query)

    # Build prompt using indexed data
    responses = Prompt(index, embedded_query, pw.this.query)

    # Feed the prompt to ChatGPT and obtain the generated answer.
    response_writer(responses)

    # Run the pipeline
    pw.run()
