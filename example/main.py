import app
import os
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":

    data_dir = os.environ.get("DATA_DIR", "./data/")
    api_key = os.environ.get("OPENAI_API_TOKEN", "")
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", 8080))
    embedder_locator = os.environ.get("EMBEDDER_LOCATOR", "text-embedding-ada-002")
    embedding_dimension = int(os.environ.get("EMBEDDING_DIMENSION", 1536))
    model_locator = os.environ.get("MODEL_LOCATOR", "gpt-3.5-turbo")
    max_tokens = int(os.environ.get("MAX_TOKENS", 200))
    temperature = float(os.environ.get("TEMPERATURE", 0.0))

    app.run(data_dir=data_dir,
            api_key=api_key,
            host=host,
            port=port,
            embedder_locator=embedder_locator,
            embedding_dimension=embedding_dimension,
            model_locator=model_locator,
            max_tokens=max_tokens,
            temperature=temperature)
