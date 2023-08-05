import importlib
from dotenv import load_dotenv


load_dotenv()


if __name__ == "__main__":

    scenario_module = importlib.import_module("discounts.app")

    scenario_module.run()
