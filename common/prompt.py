import pathway as pw
from datetime import datetime
from common.openaiapi_helper import openai_chat_completion


def prompt(index, embedded_query, user_query):

    @pw.udf
    def build_prompt(local_indexed_data, query):
        docs_str = "\n".join(local_indexed_data)
        prompt = f"Given the following discounts data: \n {docs_str} \nanswer this query: {query}, Assume that current date is: {datetime.now()}. and clean the output"
        return prompt

    query_context = index.query(embedded_query, k=3).select(
        user_query, local_indexed_data_list=pw.this.result
    )

    prompt = query_context.select(
        prompt=build_prompt(pw.this.local_indexed_data_list, user_query)
    )

    return prompt.select(
        query_id=pw.this.id,
        result=openai_chat_completion(pw.this.prompt),
    )
