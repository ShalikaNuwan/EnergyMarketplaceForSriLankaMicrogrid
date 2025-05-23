import os
from dotenv import load_dotenv
from crewai import LLM

load_dotenv()

llm = LLM(
    model="azure/gpt-4.1",
    base_url=os.getenv("AZURE_API_ENDPOINT"),
    api_key=os.getenv("AZURE_API_KEY")
)

__all__ = ['llm']
