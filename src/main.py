import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import SystemMessage
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    model = "llama-3.3-70b-versatile",
    api_key = GROQ_API_KEY,
    temperature = 0.7,
)

prompt_template = """You are a helpful AI assistant. Answer the question based on your knowledge."""

prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content=prompt_template),
        ("human", "{question}"),
    ]
)


parser = StrOutputParser()

chain = prompt | llm | parser

# A fucntion to invoke the chain 

def get_response(question: str) -> str:
    response = chain.invoke({"question": question})
    return response

