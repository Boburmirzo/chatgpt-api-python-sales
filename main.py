import importlib
import os
from dotenv import load_dotenv
import subprocess

load_dotenv()

if __name__ == "__main__":
    # Fetch data from Rainforest API
    try:
        cmd = ["python3", "examples/rainforest/data_ingestion_cron_job.py"]

        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError:
        print("Script execution failed.")
    except FileNotFoundError:
        print("Python interpreter or the script was not found.")

    # Run Discounts API
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", 8080))
    app_api = importlib.import_module("examples.api.app")
    app_api.run(host=host, port=port)
