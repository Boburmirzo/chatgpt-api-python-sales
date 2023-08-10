import app
import os
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":

    data_dir = os.environ.get("DATA_DIR", "./data/")
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", 8080))
    embedding_dimension = int(os.environ.get("EMBEDDING_DIMENSION", 1536))

    app.run(data_dir=data_dir,
            host=host,
            port=port,
            embedding_dimension=embedding_dimension)
