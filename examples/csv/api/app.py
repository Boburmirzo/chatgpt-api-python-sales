import pathway as pw
from common.transform import transform
from common.embedder import embeddings, index_embeddings
from common.prompt import prompt


class CsvDiscountsInputSchema(pw.Schema):
    discount_until: str
    country: str
    city: str
    state: str
    postal_code: str
    region: str
    product_id: str
    category: str
    sub_category: str
    brand: str
    product_name: str
    currency: str
    actual_price: str
    discount_price: str
    discount_percentage: str
    address: str


class QueryInputSchema(pw.Schema):
    query: str


def run(host, port):
    # Real-time data coming from external data sources such as csv file
    sales_data = pw.io.csv.read(
        "./examples/csv/data",
        schema=CsvDiscountsInputSchema,
        mode="streaming"
    )

    # Data source rows transformed into structured documents
    documents = transform(sales_data)

    # Compute embeddings for each document using the OpenAI Embeddings API
    embedded_data = embeddings(context=documents, data_to_embed=documents.doc)

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
