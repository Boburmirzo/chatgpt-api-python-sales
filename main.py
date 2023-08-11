import importlib
import os
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":

    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", 8080))

    mode = os.environ.get("APP_VARIANT", "csv")
    app = importlib.import_module(f"example.{mode}.app")

    app.run(host=host, port=port)
