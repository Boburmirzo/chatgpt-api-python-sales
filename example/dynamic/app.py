import pathway as pw
from src.schemas import RainforestDealsInputSchema, QueryInputSchema, CsvDiscountsInputSchema
from src.data_source import connect, DataSourceType
from src.embedder import embeddings, index_embeddings
from src.transform import transform
from src.prompt import prompt


def run(host, port):
    params = {
      "category_id": "679255011"  # Standard category shoes from Amazon
      # ... any other params
    }

    # Real-time data coming from external data sources
    csv_data = connect(DataSourceType.CSV, CsvDiscountsInputSchema)
    rainforest_data = connect(DataSourceType.RAINFOREST_API,
                              RainforestDealsInputSchema,
                              params)

    # Given a user question as a query from your API
    query, response_writer = pw.io.http.rest_connector(
        host=host,
        port=port,
        schema=QueryInputSchema,
        route="/endpoint",
        autocommit_duration_ms=50,
    )

    query, response_writer = pw.io.http.rest_connector(
        host=host,
        port=port,
        schema=QueryInputSchema,
        route="/csv",
        autocommit_duration_ms=50,
    )

    # Retrieve embeddings for input data and index
    index = index_embedded_data(csv_data)

    # Generate embeddings for the query from the OpenAI Embeddings API
    embedded_query = embeddings(context=query, data_to_embed=pw.this.query)

    # Build prompt using indexed data
    responses = prompt(index, embedded_query, pw.this.query)

    # Feed the prompt to ChatGPT and obtain the generated answer.
    response_writer(responses)

    # Run the pipeline
    pw.run()


def index_embedded_data(data):
    # Data source rows transformed into structured documents
    documents = transform(data)

    # Compute embeddings for each document using the OpenAI Embeddings API
    embedded_data = embeddings(context=documents, data_to_embed=documents.doc)

    # Construct an index on the generated embeddings in real-time
    return index_embeddings(embedded_data)
