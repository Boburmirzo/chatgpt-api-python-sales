# Find discounts using LLM App

This repo demonstrates Pathway’s [LLM App features](https://github.com/pathwaycom/llm-app) with an example project that processes discount data in real-time like [Amazon Products Sales Dataset](https://www.kaggle.com/datasets/lokeshparab/amazon-products-dataset?select=Shoes.csv) as input and exposes an HTTP REST endpoint to answer user queries about current discounts from different markets in a specific location.

## Use case

[Open AI GPT](https://openai.com/gpt-4) excels at answering questions, but only on topics it remembers from its training data. If you want GPT to answer questions about unfamiliar topics such as:

- Recent events after Sep 2021.
- Your non-public documents.
- Information from past conversations.
- Including discounts information.

the models cannot answer such queries. Because it is not aware of the context or historical data or it needs additional details. In this case, you can use LLM App efficiently to give context to this search or answer process.  See how LLM App [works](https://github.com/pathwaycom/llm-app#how-it-works). 

For example, a typical response you can get from OpenAI [Chat Completion endpoint](https://platform.openai.com/docs/api-reference/chat) or [ChatGPT UI](https://chat.openai.com/) interface without context is:

```text
User: Find discounts in USA

Assistant: Sure! Here are some ways to find discounts
in the USA:\n\n1. Coupon Websites: Websites like RetailMeNot, 
Coupons.com, and Groupon offer a wide range of discounts
and coupon codes for various products and services.\n\n2.
```

As you can see, GPT responds only with suggestion how to find discounts but it is not specific and does not provide exactly where or what kind of discount and so on.

To help the model, we give knowledge of discounts information from any reliable data source (it can be Json document, APIs, data stream in Kafka) to get a more accurate answer. Assume that there is a `future_discounts.csv` file with the following columns of data: *ship_date, ship_mode, country, city, state, postal_code ,region, product_id, category, sub_category, brand, product_name, currency,actual_price ,discount_price, discount_percentage ,address*. 

After we give this knowledge to GPT, look how it replies:

```text
User: Find discounts in USA

Assistant: 

"Based on the given data, the shipment dates are as follows:
 
Shipment Date: 2024-03-25  
Country: UK
City: London
Ship Mode: Standard Class
State: ON
Product ID: 9464
Postal Code: 43505
Region: East   
Category: Footwear  
Sub-category: Men Shoes
Product: Nike Running Shoes
Actual Price: 344.58
Discounted Price: 312.65   
...
```

The cool part is, the app is always aware of changes in the discounts. If you add another csv file or data source, LLM app does a magic and automatically updates AI models response.

## How the project works

Sample project does the following procedures to achieve above output:

1. Prepare search data:
    1. Generate: [discounts-data-generator.py](http://discounts-data-generator.py) simulates real-time data coming from external data sources and generates/updates existing `future_discounts.csv` file with random data. In reality, you can replace it with database, API or message broker.
    2. Collect: The app reads CSV file and its rows in real-time (when streaming mode is enabled) and maps each row into a structured document schema for better managing large data sets.
    3. Chunk: Documents are split into short, mostly self-contained sections to be embedded.
    4. Embed: Each section is [embedded](https://platform.openai.com/docs/guides/embeddings) with the OpenAI API and retrieve embedded result.
    5. Indexing: Constructs an index on the generated embeddings.
2. Search (once per query)
    1. Given a user question, generate an embedding for the query from the OpenAI API.
    2. Using the embeddings, retrieve vector index by relevance to the query
3. Ask (once per query)
    1. Insert the question and the most relevant sections into a message to GPT
    2. Return GPT's answer

## How to run the project

Assume that we have this entry on the CSV file:

| ship_date | ship_mode | country | city | state | postal_code | region | product_id | category | sub_category | brand | product_name | currency | actual_price | discount_price | discount_percentage | address |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2024-08-09 | Second Class | USA | Los Angeles | IL | 22658 | Central | 7849 | Footwear | Men Shoes | Nike | Formal Shoes | USD | 130.67 | 117.60 | 10 | 321 Oak St |

When user has the following query:

```bash
curl --data '{"user": "user", "query": "Can you find me discounts this week for Nikes men shoes?. Now is 19th of August, 2023 year"}' http://localhost:8080/
```

You will get the response as its expected (even if GPT is refusing it that data is not real).

```text
"I'm sorry, but I cannot provide real-time data or search for discounts. 
However, I can help you clean the output by removing unnecessary information. 
Here is the cleaned output for the given data:

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

Please note that this is a fictional example and the data provided is not real."
```