

# app/services/agent_service.py

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from .rag_service import rag_answer
from .shopify_service import get_order_status

load_dotenv()

api_key = os.getenv("GEMINI_KEY")

router_llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    google_api_key=api_key
)


ROUTER_PROMPT = """
You are an AI router for an ecommerce assistant.

Your job is to classify the user message into ONE of these categories:

1. GREETING → hello, hi, how are you, etc.
2. ORDER → user asking about order status or referencing order number
3. KNOWLEDGE → product info, company info, FAQs (use RAG)
4. OUT_OF_SCOPE → anything unrelated to ecommerce or company

Return ONLY one word:
GREETING
ORDER
KNOWLEDGE
OUT_OF_SCOPE

User message:
"""


def classify_message(message: str) -> str:
    response = router_llm.invoke(ROUTER_PROMPT + message)
    return response.content.strip()

def handle_message(message: str):

    try:
        category = classify_message(message)

        if category == "GREETING":
            return "Hello 👋 How can I help you today?"

        elif category == "ORDER":
            return get_order_status(message)

        elif category == "KNOWLEDGE":
            return rag_answer(message)

        elif category == "OUT_OF_SCOPE":
            return "I can only help with product information and order related questions."

        else:
            return "I'm not sure how to help with that."

    except Exception as e:
        return f"Error: {str(e)}"