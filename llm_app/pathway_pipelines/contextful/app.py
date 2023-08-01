import os

import pathway as pw
from model_wrappers import OpenAIChatGPTModel, OpenAIEmbeddingModel
from pathway.stdlib.ml.index import KNNIndex


class DiscountsInputSchema(pw.Schema):
    ship_date: str
    ship_mode: str
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
    user: str


HTTP_HOST = os.environ.get("PATHWAY_REST_CONNECTOR_HOST", "127.0.0.1")
HTTP_PORT = os.environ.get("PATHWAY_REST_CONNECTOR_PORT", "8080")

API_KEY = os.environ.get("OPENAI_API_TOKEN")
EMBEDDER_LOCATOR = "text-embedding-ada-002"
EMBEDDING_DIMENSION = 1536

MODEL_LOCATOR = "gpt-3.5-turbo" # Change to 'gpt-4' if you have access.
TEMPERATURE = 0.0
MAX_TOKENS = 200

def concat_with_titles(*args) -> str:
    titles = [
        "country",
        "city",
        "ship_mode",
        "state",
        "product_id",
        "postal_code",
        "region",
        "category",
        "sub_category",
        "brand",
        "product_name",
        "actual_price",
        "discount_price",
        "discount_percentage",
        "address",
        "currency",
        "ship_date",
    ]
    combined = [f"{title}: {value}" for title, value in zip(titles, args)]
    return ', '.join(combined)

def run():
    embedder = OpenAIEmbeddingModel(api_key=API_KEY)

    sales_data = pw.io.csv.read(
        "../data/",
        schema=DiscountsInputSchema,
        mode="streaming",
        autocommit_duration_ms=50,
    )

    combined_data = sales_data.select(
        doc=pw.apply(concat_with_titles,
                           pw.this.country,
                           pw.this.city,
                           pw.this.ship_mode,
                           pw.this.state,
                           pw.this.product_id,
                           pw.this.postal_code,
                           pw.this.region,
                           pw.this.category,
                           pw.this.sub_category,
                           pw.this.brand,
                           pw.this.product_name,
                           pw.this.actual_price,
                           pw.this.discount_price,
                           pw.this.discount_percentage,
                           pw.this.address,
                           pw.this.currency,
                           pw.this.ship_date),
    )

    enriched_data = combined_data + combined_data.select(
        data=embedder.apply(text=combined_data.doc, locator=EMBEDDER_LOCATOR)
    )

    index = KNNIndex(enriched_data, d=EMBEDDING_DIMENSION)

    query, response_writer = pw.io.http.rest_connector(
        host=HTTP_HOST,
        port=int(HTTP_PORT),
        schema=QueryInputSchema,
        autocommit_duration_ms=50,
    )

    query += query.select(
        data=embedder.apply(text=pw.this.query, locator=EMBEDDER_LOCATOR),
    )

    query_context = index.query(query, k=3).select(
        pw.this.query, local_indexed_data_list=pw.this.result
    )

    @pw.udf
    def build_prompt(local_indexed_data, query):
        docs_str = "\n".join(local_indexed_data)
        prompt = f"Given the following discounts data: \n {docs_str} \nanswer this query: {query} and clean the output"
        return prompt

    prompt = query_context.select(
        prompt=build_prompt(pw.this.local_indexed_data_list, pw.this.query)
    )

    model = OpenAIChatGPTModel(api_key=API_KEY)

    responses = prompt.select(
        query_id=pw.this.id,
        result=model.apply(
            pw.this.prompt,
            locator=MODEL_LOCATOR,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
        ),
    )

    response_writer(responses)

    pw.run()

if __name__ == "__main__":
    run()