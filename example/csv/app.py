import pathway as pw
from src.schemas import QueryInputSchema
from src.transform import transform
from src.embedder import embeddings, index_embeddings
from src.prompt import prompt
from src.data_source import connect, DataSourceType


def run(host, port):
    # Real-time data coming from external data sources such as csv file
    sales_data = connect(DataSourceType.CSV)

    # Compute embeddings for each document using the OpenAI Embeddings API
    embedded_data = embeddings(context=sales_data, data_to_embed=sales_data.doc)

    # Construct an index on the generated embeddings in real-time
    index = index_embeddings(embedded_data)

    # Given a user question as a query from your API
    query, response_writer = pw.io.http.rest_connector(
        host=host,
        port=port,
        schema=QueryInputSchema,
        autocommit_duration_ms=50,
    )

    # Generate embeddings for the query from the OpenAI Embeddings API
    embedded_query = embeddings(context=query, data_to_embed=pw.this.query)

    # Build prompt using indexed data
    responses = prompt(index, embedded_query, pw.this.query)

    # Feed the prompt to ChatGPT and obtain the generated answer.
    response_writer(responses)

    # Run the pipeline
    pw.run()
