
# Shopify AI Assistant (Production-Ready)

A production-grade AI-powered Shopify Assistant built with FastAPI, LangChain, and Gemini LLM, designed to provide:

Conversational customer support

Real-time order tracking

RAG-based knowledge responses

Plug-and-play Shopify storefront integration

# Features
AI Router (Smart Intent Detection)

Classifies user queries into:

GREETING

ORDER

KNOWLEDGE

OUT_OF_SCOPE

Routes requests to the correct service automatically

# Shopify Order Integration
Fetch order details using Shopify Admin API

Supports:

Order financial status

Fulfillment status

# RAG (Retrieval-Augmented Generation)
Uses ChromaDB + Gemini Embeddings

Answers based on your custom knowledge base (/data folder)

Prevents hallucinations with strict context-based prompting

# Chat History Persistence
SQLAlchemy-powered database

Stores:

Chat sessions

Message history

Enables future analytics & personalization

# Embedded Chat Widget
Lightweight JS chatbot

Can be injected into Shopify storefront via ScriptTag API

Floating UI with real-time responses

# FastAPI Backend
High-performance async API

Clean architecture with services layer

CORS enabled for Shopify integration

# Project Structure
app/

│
├── main.py                  # FastAPI entrypoint

├── database.py             # DB connection

├── models.py               # SQLAlchemy models

├── schemas.py              # Pydantic schemas

├── crud.py                 # DB operations

│
├── services/

│   ├── agent_service.py    # AI router (core brain)

│   ├── rag_services.py     # RAG pipeline

│   ├── shopify_services.py # Shopify API integration

│   └── chat_services.py  

│

├── static/

│   └── chatbot.js          # Embeddable chatbot UI

│

templates/
└── index.html              # Test UI

# Environment Variables

Create a .env file:

# Gemini
GEMINI_KEY=your_gemini_api_key

# Shopify
SHOPIFY_STORE=your-store-name
SHOPIFY_STORE_URL=your-store.myshopify.com
SHOPIFY_ACCESS_TOKEN=your_access_token

# Backend
DATABASE_URL=sqlite:///./chat.db
BASE_URL=https://your-domain.com

# CORS
SHOPIFY_DOMAIN=https://your-store.myshopify.com
# How It Works
 User sends message

→ /chat endpoint

 AI Router Classifies Intent
 
"Where is my order #1234?"

→ ORDER

 Routed to Service

ORDER → Shopify API

KNOWLEDGE → RAG pipeline

GREETING → Static response

 Response Stored + Returned


# Author

Kashmala Musarrat Ali
Data Analyst | AI Engineer | LLM & Agentic Systems Builder
