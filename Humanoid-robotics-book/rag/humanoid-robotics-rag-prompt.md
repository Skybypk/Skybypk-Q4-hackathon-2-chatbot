# Humanoid Robotics RAG System Prompt

## Overview
This document outlines the Retrieval Augmented Generation (RAG) system for the Humanoid Robotics Book. The RAG system combines vector search with language model generation to provide accurate, context-aware responses based on the book content.

## System Architecture

### 1. Data Ingestion
- Book content from the `docs/` directory is automatically loaded
- Content is chunked into semantic segments (max 500 characters)
- Each chunk is embedded using SentenceTransformer models
- Embeddings are stored in Qdrant vector database

### 2. Query Processing
- User queries are converted to embeddings using the same model
- Vector similarity search retrieves the most relevant content chunks
- Top-k (default 5) most similar chunks are selected as context

### 3. Response Generation
- Retrieved context is combined with the user query in a structured prompt
- A language model generates a response based on the provided context
- Responses are constrained to only use information from the book content
- Multilingual support (English/Urdu) is provided

## Prompt Engineering

### Context Injection Prompt
```
You are an expert assistant for the Humanoid Robotics Book. Answer the user's question based only on the provided book content. Be concise and accurate.

Book Content:
{retrieved_context}

Question: {user_query}

Answer:
```

### Quality Assurance
- Responses are validated against the source material
- Confidence scores are provided based on vector similarity
- Source documents are cited for transparency

## Features

### 1. Select-Text Ask
- Users can select text on any page and ask questions about it
- The selected text is combined with the question for more targeted responses
- Endpoint: `/select-text-ask`

### 2. Multilingual Support
- English and Urdu language support
- Translation service for content and responses
- User preference storage for language selection

### 3. User Analytics
- Query logging for improvement insights
- User preference management
- Response confidence tracking

## Technical Implementation

### Backend Stack
- FastAPI for web framework
- Qdrant for vector database
- SentenceTransformers for embeddings
- Transformers for response generation
- Neon PostgreSQL for metadata

### Frontend Components
- React-based chat interface
- Real-time search functionality
- Language switching capability
- Dynamic favicon updates

## Usage Guidelines

### For Developers
1. When adding new content to the book, ensure it's in the `docs/` directory
2. The system will automatically index new content on startup
3. Configure embedding and model parameters in `config.py`

### For Users
1. Ask specific questions about humanoid robotics
2. Use the text selection feature for contextual questions
3. Switch between English and Urdu as needed
4. Check source citations for reference material

## Performance Considerations

### Free-Tier Optimized
- Lightweight embedding models (all-MiniLM-L6-v2)
- Efficient chunking strategy
- Client-side fallback for offline use
- Minimal GPU usage

### Scalability
- Configurable similarity thresholds
- Adjustable context length
- Modular architecture for feature additions

## Error Handling

- Graceful degradation when backend is unavailable
- Fallback to mock API for development
- Comprehensive logging for debugging
- User-friendly error messages