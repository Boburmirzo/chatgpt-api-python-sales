import os

import pathway as pw
from pathway.stdlib.ml.index import KNNIndex

from llm_app.model_wrappers import OpenAIChatGPTModel, OpenAIEmbeddingModel


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

def run(
    *,
    data_dir: str = os.environ.get("PATHWAY_DATA_DIR", "./data/"),
    api_key: str = os.environ.get("OPENAI_API_TOKEN", ""),
    host: str = "0.0.0.0",
    port: int = 8080,
    embedder_locator: str = "text-embedding-ada-002",
    embedding_dimension: int = 1536,
    model_locator: str = "gpt-3.5-turbo",
    max_tokens: int = 200,
    temperature: int = 0.0,
    **kwargs,
):
    embedder = OpenAIEmbeddingModel(api_key=api_key)

    sales_data = pw.io.csv.read(
        data_dir,
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
        data=embedder.apply(text=combined_data.doc, locator=embedder_locator)
    )

    index = KNNIndex(enriched_data, d=embedding_dimension)

    query, response_writer = pw.io.http.rest_connector(
        host=host,
        port=port,
        schema=QueryInputSchema,
        autocommit_duration_ms=50,
    )

    query += query.select(
        data=embedder.apply(text=pw.this.query, locator=embedder_locator),
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

    model = OpenAIChatGPTModel(api_key=api_key)

    responses = prompt.select(
        query_id=pw.this.id,
        result=model.apply(
            pw.this.prompt,
            locator=model_locator,
            temperature=temperature,
            max_tokens=max_tokens,
        ),
    )

    response_writer(responses)

    pw.run()


if __name__ == "__main__":
    run()