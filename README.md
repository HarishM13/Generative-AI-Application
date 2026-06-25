# Generative-AI-Application
Overview
Enterprise GenAI Platform is an Agentic Retrieval-Augmented Generation (RAG) application that enables users to upload enterprise documents and interact with them using natural language.

The platform supports ingestion of PDF, Excel, CSV, and Text documents, converts them into vector embeddings, stores them in ChromaDB, and uses Google's Gemini 3.1 Flash Lite Preview model to generate contextual responses based on retrieved document content.

The solution is built using FastAPI, Streamlit, ChromaDB, HuggingFaceEmbeddings, Gemini, Docker, and  Crew AI Agents.

Key Features

Document Ingestion
Removing the junk text and chunking the raw text
Vector Embeddings

Supports multiple file formats:

PDF
Excel
CSV
Text

Retrieval-Augmented Generation (RAG)
Semantic Search
Context Retrieval
Context-Aware Response Generation

Agent-Based Architecture
Planner Agent
Retrieval Agent
Reasoning Agent
validatorAgent

API Layer
FastAPI REST Endpoints


User Interface
Streamlit Web Application
File Upload
Question Answering

Deployment

Docker
Docker Compose

Solution Architecture
  User
    ↓
Streamlit UI
    ↓
FastAPI API Layer
    ↓
Crew Agent Manager
    ↓
Planner Agent Manager  
    ↓
Retrieval Agent
    ↓
ChromaDB
    ↓
Reasoning Agent
    ↓
Gemini 3.1 Flash Lite Preview
    ↓
Grounded Response(Answer)


└── README.md
