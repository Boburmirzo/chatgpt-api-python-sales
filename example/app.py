import os
import pathway as pw

from dotenv import load_dotenv
from datetime import datetime
from pathway.stdlib.ml.index import KNNIndex
from llm_app.model_wrappers import OpenAIChatGPTModel, OpenAIEmbeddingModel
from schemas import DiscountsInputSchema, QueryInputSchema
from transform import transform_data

# Load environment variables from the .env file
load_dotenv()

def run(
    *,
    data_dir: str = os.environ.get("DATA_DIR", "./data/"),
    api_key: str = os.environ.get("OPENAI_API_TOKEN", ""),
    host: str = os.environ.get("HOST", "0.0.0.0"),
    port: int = int(os.environ.get("PORT", 8080)),
    embedder_locator: str = os.environ.get("EMBEDDER_LOCATOR", "text-embedding-ada-002"),
    embedding_dimension: int = int(os.environ.get("EMBEDDING_DIMENSION", 1536)),
    model_locator: str = os.environ.get("MODEL_LOCATOR", "gpt-3.5-turbo"),
    max_tokens: int = int(os.environ.get("MAX_TOKENS", 200)),
    temperature: float = float(os.environ.get("TEMPERATURE", 0.0)),
    **kwargs,
):
    embedder = OpenAIEmbeddingModel(api_key=api_key)

    # Real-time data coming from external data sources such as csv file
    sales_data = pw.io.csv.read(
        data_dir,
        schema=DiscountsInputSchema,
        mode="streaming",
        autocommit_duration_ms=50,
    )

    # Data source rows transformed into structured documents
    documents = transform_data(sales_data)

    # Each section is embedded with the OpenAI Embeddings API and retrieve the embedded result
    enriched_data = documents + documents.select(
        data=embedder.apply(text=documents.doc, locator=embedder_locator)
    )

    # Constructs an index on the generated embeddings in real-time
    index = KNNIndex(enriched_data, d=embedding_dimension)

    # Given a user question as a query from your API
    query, response_writer = pw.io.http.rest_connector(
        host=host,
        port=port,
        schema=QueryInputSchema,
        autocommit_duration_ms=50,
    )

    # Generates an embedding for the query from the OpenAI Embeddings API
    query += query.select(
        data=embedder.apply(text=pw.this.query, locator=embedder_locator),
    )

    # Using the embeddings, retrieve the vector index by relevance to the query
    query_context = index.query(query, k=3).select(
        pw.this.query, local_indexed_data_list=pw.this.result
    )

    # Inserts the question and the most relevant sections into a message to OpenAI Chat Completion API
    @pw.udf
    def build_prompt(local_indexed_data, query):
        docs_str = "\n".join(local_indexed_data)
        prompt = f"Given the following discounts data: \n {docs_str} \nanswer this query: {query}, Assume that current date is: {datetime.now()}. and clean the output"
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

    # Returns ChatGPT's answer
    response_writer(responses)

    pw.run()


if __name__ == "__main__":
    run()