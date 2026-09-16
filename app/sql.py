import sqlite3
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv
import re
from groq import Groq
sql_path=(Path(__file__).parent /'db.sqlite')
load_dotenv()

def run_the_query(query):
    if query.strip().upper().startswith('SELECT'):
        with sqlite3.connect(sql_path) as connection:
            df=pd.read_sql_query(query, connection)
            return df.head(10)
    return None
prompt='''you are an expert in SQL and providing accurate SQL queries based on the natural language provided by the user .
the overall structure of the schema is given below.
Table:product                       
fields:
product_link(string( website link for the product)
title(string(name of  the product))
brand(string(brand of the product)
price(integer(price for the product in rupees))
discount(float(discount on the product in percentage .for example,10% is represented as 0.1,20% as 0.2 etc..))
avg_rating(float(average rating provided by the users for the product))
total_ratings(integer(total number reviews provided by users on the product))
so now you know the overall structure. you need to generate accurate SQL queries based on the users input. 
you will be punished if you don't give correct query. 
note that the case for letters will be not same. convert the fields to lower case using lower() in the sql query.
generate only a single query with respect to the input.nver use 'ILIKE'.
use '*' instead of  mentioning each and every fields.also give tags '<SQL>' at the beginning and end of query.'''
def sql_query_generator(query):
    client = Groq()
    completion = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
        {
            "role": "system",
            "content":prompt
        },
      {
        "role": "user",
        "content": query
      }
    ],
    temperature=0.2,
    max_completion_tokens=2048,
    top_p=1,
    reasoning_effort="medium",
    stream=False,
    stop=None
    )
    return completion.choices[0].message.content
def sql_chain(question):
    answer=sql_query_generator(question)
    print(answer)
    pattern=r'<SQL>(.*?)</SQL>'
    matches=re.findall(pattern,answer, re.DOTALL)
    if len(matches)==0:
        return'LLm does not know the answer'
    reply=run_the_query(matches[0].strip())
    if reply is None:
        return 'there is no such query!'
    data=reply.to_dict(orient='records')
    reply=response_for_df(question,data)
    return reply



data_frame_prompt='''you are an expert in reading datasets based on the question provided. the dataset may be in the form of array, dictionary or a pandas data frame. the dataset contain contents such as index,product_link,title,brand,price,discount,avg_rating,total_rating.provide answer only for the question provided. answer the questions based on the example format i am providing you.

nike running shoes :-,rating :-4.7 , price:-2200 (20% discount) , link:-link to the product
sparx running shoes  rating :-4.0 , price:-2200 (5% discount) , link:-link to the product
sparx sneaker shoes  rating :-3.8 , price:-999 (10% discount) , link:-link to the product
.you will be  provided with QUESTION and DATA.'''
def response_for_df(question,context):

    client = Groq()
    completion = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": data_frame_prompt
            },
            {
                "role": "user",
                "content": f'question:-{question},data:{context}'
            }
        ],
        temperature=0.2,
        max_completion_tokens=2048,
        top_p=1,
        reasoning_effort="medium",
        stream=False,
        stop=None
    )
    return completion.choices[0].message.content
resp=sql_chain('give me items more than 20% discount')
print(resp)