import importlib
import os
from dotenv import load_dotenv
from crontab import CronTab

load_dotenv()

cron = CronTab(user=True)
job = cron.new(command='python3 examples/rainforest/data_ingestion_cron_job.py')
job.minute.every(1)
cron.write()

if __name__ == "__main__":
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", 8080))

    app = importlib.import_module("examples.api.app")

    app.run(host=host, port=port)
