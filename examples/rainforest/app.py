import pathway as pw
from common.embedder import embeddings, index_embeddings
from common.transform import transform
from common.prompt import prompt
from examples.rainforest.rainforestapi_helper import send_request


class RainforestDealsInputSchema(pw.Schema):
    position: int
    link: str
    asin: str
    is_lightning_deal: bool
    deal_type: str
    is_prime_exclusive: bool
    starts_at: str
    ends_at: str
    type: str
    title: str
    image: str
    deal_price: float
    old_price: float
    currency: str
    merchant_name: str
    free_shipping: bool
    is_prime: bool
    is_map: bool
    deal_id: str
    seller_id: str
    description: str
    rating: float
    ratings_total: int


class QueryInputSchema(pw.Schema):
    query: str


def run(host, port):
    params = {
      "category_id": "679255011"  # Standard category shoes
      # ... any other params
    }

    data_dir = "./examples/rainforest/data"

    send_request(data_dir, params)

    sales_data = pw.io.jsonlines.read(
        data_dir,
        schema=RainforestDealsInputSchema,
        mode="streaming",
        autocommit_duration_ms=50,
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
