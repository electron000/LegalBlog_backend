# blog_app/core/llm.py

from .config import GOOGLE_API_KEY
from langchain_google_genai import ChatGoogleGenerativeAI
import os

def get_llm_model() -> ChatGoogleGenerativeAI:
    if not GOOGLE_API_KEY:
        raise ValueError("API Key not found. Please set GOOGLE_API_KEY in your .env file.")

    # Ensure the env var is set for the library to auto-detect
    os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

    return ChatGoogleGenerativeAI( 
        model="gemini-2.5-flash",
        temperature=0.5
    )