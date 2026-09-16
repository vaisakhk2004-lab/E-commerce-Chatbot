from urllib import response
from semantic_router import Route
from semantic_router.routers import SemanticRouter
from semantic_router.encoders import HuggingFaceEncoder
import chromadb
import pandas as pd
from groq import Groq
from dotenv import load_dotenv
import os
from pathlib import Path

client=chromadb.PersistentClient(path=r'C:\Users\VYSHAK\Downloads\Project E-commerce Chatbot\app\database')
from chromadb.utils import embedding_functions
load_dotenv()

embedding_function=embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
faq_path=(Path(__file__).parent /'resources'/"faq_data.csv")
def load_data(path):
    df=pd.read_csv(path)
    collection=client.get_or_create_collection(name='faq',embedding_function=embedding_function)
    docs=df['question'].tolist()
    metadatas=[{'answer': answer} for answer in df['answer'].tolist()]
    ids=['id_' + str(i) for i in range(len(docs))]
    collection.add(documents=docs,metadatas=metadatas,ids=ids)

def get_query(query):
    collection=client.get_collection(name='faq')
    results=collection.query(query_texts=[query],n_results=2)
    return results

def chain(query):
    result=get_query(query)
    context='\n'.join([item.get('answer') for item in result['metadatas'][0]])
    prompt=f'''you are given the question and context.you have to answer it based on the context i provided.
    if you don't find the answer from the context,just say 'i don't know
    question: {query}
    context: {context}'''
    client = Groq()
    completion = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
      {
        "role": "user",
        "content": prompt
      }
    ],
    temperature=1,
    max_completion_tokens=2048,
    top_p=1,
    reasoning_effort="medium",
    stream=False,
    stop=None
    )
    return completion.choices[0].message.content


