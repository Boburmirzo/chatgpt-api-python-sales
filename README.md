# ChatGPT Python API for sales

This is an AI app to find **real-time** discounts/deals/sales prices from various online markets around the world. The project
exposes an HTTP REST endpoint to answer user queries about current sales like [Amazon deals](https://www.amazon.com/gp/goldbox?ref_=nav_cs_gb) in a specific location or from the given any input file such as (CSV, Jsonlines, PDF, Markdown, Txt). It uses Pathway’s [LLM App features](https://github.com/pathwaycom/llm-app) to build real-time LLM(Large Language Model)-enabled data pipeline in Python and join data from multiple input sources, leverages OpenAI API [Embeddings](https://platform.openai.com/docs/api-reference/embeddings) and [Chat Completion](https://platform.openai.com/docs/api-reference/completions) endpoints to generate AI assistant responses.

Currently, the project supports two types of data sources and it is **possible to extend sources** by adding custom input connectors:

- Jsonlines - The Data source expects to have a `doc` object for each line. Make sure that you convert your input data first to Jsonlines. See a sample data in [discounts.jsonl](/examples/csv/data/discounts.jsonl)
- [Rainforest Product API](https://www.rainforestapi.com/docs/product-data-api/overview).

## Features

- Retrieves the latest deals from various sources.
- Provides an API interface to explore these deals.
- Offers user-friendly UI with [Streamlit](https://streamlit.io/).
- Filters and presents deals based on user queries or chosen data sources.
- Data and code reusability for offline evaluation. User has the option to choose to use local (cached) or real data.
- Extend data sources: Using Pathway's built-in connectors for JSONLines, CSV, Kafka, Redpanda, Debezium, streaming APIs, and more.

## Further Improvements

There are more things you can achieve and here are upcoming features:

- Incorporate additional data from external APIs, along with various files (such as Jsonlines, PDF, Doc, HTML, or Text format), databases like PostgreSQL or MySQL, and stream data from platforms like Kafka, Redpanda, or Debedizum.
- Merge data from these sources instantly.
- Maintain a data snapshot to observe variations in sales prices over time, as Pathway provides a built-in feature to compute **differences** between two alterations.
- Beyond making data accessible via API or UI, the LLM App allows you to relay processed data to other downstream connectors, such as BI and analytics tools. For instance, set it up to **receive alerts** upon detecting price shifts.

## Demo

In case you use Rainforest API as a data source for the project, it provides real-time deals for Amazon products.
When the user has the following query in the API request:

```text
Can you find me discounts this week for Adidas men's shoes?
```

You will get the response with some discounts available in Amazon market:

![LLM App responds with discounts from Amazon](/assets/LLM%20App%20v1.gif)

As evident, ChatGPT interface offers general advice on locating discounts but lacks specificity regarding where or what type of discounts, among other details:

![ChatGPT needs custom data](/assets/ChatGPT%20Discounts%20V1.gif)

## Code sample

It requires only few lines of code to build a real-time AI-enabled data pipeline:

```python
# Real-time data coming from external data sources such as jsonlines file
sales_data = pw.io.jsonlines.read(
    "./examples/data",
    schema=DataInputSchema,
    mode="streaming"
)
# Compute embeddings for each document using the OpenAI Embeddings API
embedded_data = embeddings(context=sales_data, data_to_embed=sales_data.doc)
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
```

## Use case

[Open AI GPT](https://openai.com/gpt-4) excels at answering questions, but only on topics it remembers from its training data. If you want GPT to answer questions about unfamiliar topics such as:

- Recent events after Sep 2021.
- Your non-public documents.
- Information from past conversations.
- Real-time data.
- Including discount information.

The model might not answer such queries properly. Because it is not aware of the context or historical data or it needs additional details. In this case, you can use LLM App efficiently to give context to this search or answer process.  See how LLM App [works](https://github.com/pathwaycom/llm-app#how-it-works).

For example, a typical response you can get from the OpenAI [Chat Completion endpoint](https://platform.openai.com/docs/api-reference/chat) or [ChatGPT UI](https://chat.openai.com/) interface without context is:

```text
User: Find discounts in the USA

Assistant: Sure! Here are some ways to find discounts
in the USA :\n\n1. Coupon Websites: Websites like RetailMeNot, 
Coupons.com and Groupon offer a wide range of discounts
and coupon codes for various products and services.\n\n2.
```

As you can see, GPT responds only with suggestions on how to find discounts but it is not specific and does not provide exactly where or what kind of discount and so on.

To help the model, we give knowledge of discount information from any reliable data source (it can be JSON document, APIs, or data stream in Kafka) to get a more accurate answer. Assume that there is a `discounts.csv` file with the following columns of data: *discount_until, country, city, state, postal_code ,region, product_id, category, sub_category, brand, product_name, currency,actual_price ,discount_price, discount_percentage ,address*.

After we give this knowledge to GPT using UI drag and drop, look how it replies:

![ChatGPT needs custom data 2](/assets//Streamlit%20CSV%20File%20uploader.gif)

The app takes `discounts.csv` file and indexed documents into account and uses this data when processing queries. The cool part is, the app is always aware of changes in the discounts. If you add another CSV file or data source, the LLM app does magic and automatically updates the AI model's response.

## How the project works

The sample project does the following procedures to achieve the above output:

1. Prepare search data:
    1. Generate: [discounts-data-generator.py](/examples/csv/discounts-data-generator.py) simulates real-time data coming from external data sources and generates/updates existing `discounts.csv` file with random data. In reality, you can replace it with a database, API, or message broker.
    2. Collect: You upload the CSV file through the UI file-uploader and it maps each row into a jsonline schema for better managing large data sets.
    3. Chunk: Documents are split into short, mostly self-contained sections to be embedded.
    4. Embed: Each section is [embedded](https://platform.openai.com/docs/guides/embeddings) with the OpenAI API and retrieve the embedded result.
    5. Indexing: Constructs an index on the generated embeddings.
2. Search (once per query)
    1. Given a user question, generate an embedding for the query from the OpenAI API.
    2. Using the embeddings, retrieve the vector index by relevance to the query
3. Ask (once per query)
    1. Insert the question and the most relevant sections into a message to GPT
    2. Return GPT's answer

## How to run the project

Example only supports Unix-like systems (such as Linux, macOS, BSD). If you are a Windows user, we highly recommend leveraging Windows Subsystem for Linux (WSL) or Dockerize the app to run as a container.

### Prerequisites

1. Make sure that [Python](https://www.python.org/downloads/) 3.10 or above installed on your machine.
2. Download and Install [Pip](https://pip.pypa.io/en/stable/installation/) to manage project packages.
3. Create an [OpenAI](https://openai.com/) account and generate a new API Key: To access the OpenAI API, you will need to create an API Key. You can do this by logging into the [OpenAI website](https://openai.com/product) and navigating to the API Key management page.
4. (Optional): if you use Rainforest API as a data source, create an [Rainforest](https://www.rainforestapi.com/) account and get a new API Key. Refer to Rainforest API [documentation](https://www.rainforestapi.com/docs).

Then, follow the easy steps to install and get started using the sample app.

### Step 1: Clone the repository

This is done with the `git clone` command followed by the URL of the repository:

```bash
git clone https://github.com/Boburmirzo/chatgpt-api-python-sales.git
```

Next,  navigate to the project folder:

```bash
cd chatgpt-api-python-sales
```

### Step 2: Set environment variables

Create `.env` file in the root directory of the project, copy and paste below config and replace `{OPENAI_API_KEY}` configuration value with your key.
Optionally, you change other values. `APP_VARIANT=csv.api` means the app uses csv file as a data source and exposes API endpoint to query this data.
If you change it to `APP_VARIANT=rainforest` it uses Rainforest API as a data source. In this case, you need to specify also `{RAINFOREST_BASE_URL}` and `{RAINFOREST_API_KEY}`. By default the app uses [Mock API response](https://run.mocky.io/v3/f17d8811-09ff-4ba6-8d14-31ef972ce6cd/request).

```bash
APP_VARIANT=csv.api
OPENAI_API_TOKEN={OPENAI_API_KEY}
RAINFOREST_BASE_URL={RAINFOREST_BASE_URL}
RAINFOREST_API_KEY={RAINFOREST_API_KEY}
HOST=0.0.0.0
PORT=8080
EMBEDDER_LOCATOR=text-embedding-ada-002
EMBEDDING_DIMENSION=1536
MODEL_LOCATOR=gpt-3.5-turbo
MAX_TOKENS=200
TEMPERATURE=0.0
```

### Step 3: Install the app dependencies

Install the required packages:

```bash
pip install --upgrade -r requirements.txt
```

### Step 4: Run and start to use it

You start the application by navigating to `llm_app` folder and run `main.py`:

```bash
python main.py
```

When the application runs successfully, you should see output something like this:

![pathway_progress_dashboard](/assets/pathway_progress_dashboard.png)

### Step 5: Run Streamlit UI for file upload

You can run the UI seperately by navigating to `cd examples/csv/ui` and running Streamlit app
`streamlit run app.py` command. It connects to the backend API automatically and you will see UI frontend is running on your browser:

![screenshot_ui_streamlit](/assets/screenshot_ui_streamlit.png)

## Test the sample app

Assume that we have this entry on the CSV file (this can be any CSV file where the first raw has column names separated by commas):

| discount_until | country | city | state | postal_code | region | product_id | category | sub_category | brand | product_name | currency | actual_price | discount_price | discount_percentage | address |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2024-08-09 | USA | Los Angeles | IL | 22658 | Central | 7849 | Footwear | Men Shoes | Nike | Formal Shoes | USD | 130.67 | 117.60 | 10 | 321 Oak St |

When the user uploads this file to the file uploader and asks questions:

```text
Can you find me discounts this month for Nikes men shoes?
```

You will get the response as its expected on the UI.

```text
"Based on the given data, there is one discount available this month for Nike's men shoes. Here are the details::

Discounts this week for Nike's men shoes:

City: Los Angeles
Ship Mode: Second Class
Postal Code: 22658
Category: Footwear
Sub-category: Men Shoes
Brand: Nike
Product Name: Formal Shoes
Formal Shoes
Actual Price: $130.67
Discounted Price: $117.60
Discount Percentage: 10%
Ship Date: 2024-08-09
```
