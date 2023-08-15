import pathway as pw
from src.schemas import RainforestDealsInputSchema, QueryInputSchema
from src.data_source import connect, DataSourceType
from src.embedder import contextful, index_embeddings
from src.transform import transform
from src.prompt import prompt


def run(host, port):
    params = {
      "category_id": "679255011"  # Standard category shoes
      # ... any other params
    }

    # Real-time data coming from external data sources such as Rainforest Deals API
    sales_data = connect(DataSourceType.RAINFOREST_API,
                         RainforestDealsInputSchema,
                         params)

    # Data source rows transformed into structured documents
    documents = transform(sales_data)

    # Compute embeddings for each document using the OpenAI Embeddings API
    embedded_data = contextful(context=documents, data_to_embed=documents.doc)

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
    embedded_query = contextful(context=query, data_to_embed=pw.this.query)

    # Build prompt using indexed data
    responses = prompt(index, embedded_query, pw.this.query)

    # Feed the prompt to ChatGPT and obtain the generated answer.
    response_writer(responses)

    # Run the pipeline
    pw.run()
