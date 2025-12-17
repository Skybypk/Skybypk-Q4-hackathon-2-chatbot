# Humanoid Robotics Book with Chatbot

This project combines a Docusaurus-based documentation site with an AI-powered chatbot that can answer questions about the humanoid robotics content using a RAG (Retrieval-Augmented Generation) system.

## Features

- Interactive chatbot that understands the humanoid robotics book content
- Multi-language support (English and Urdu)
- Text selection feature to ask questions about selected content
- Responsive Docusaurus-based interface

## Prerequisites

- Python 3.8+
- Node.js 16+
- Docker (for running Qdrant vector database)
- Git

## Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Start the complete system using the startup script**
   ```bash
   # On Windows
   start_system.bat
   ```

3. **Access the applications**
   - Book: http://localhost:3000
   - Chat: http://localhost:3000/chat
   - Backend API: http://localhost:8000
   - Backend API Docs: http://localhost:8000/docs

## Manual Setup

### Backend (RAG System)

1. Navigate to the backend directory:
   ```bash
   cd docusaurus-book/backend
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Ensure Qdrant is running (using Docker):
   ```bash
   docker run -d --name qdrant -p 6333:6333 -p 6334:6334 qdrant/qdrant
   ```

4. Run the setup script to create the collection:
   ```bash
   python setup_qdrant.py
   ```

5. Start the backend server:
   ```bash
   python start_rag_system.py
   ```

### Frontend (Docusaurus)

1. Navigate to the docusaurus directory:
   ```bash
   cd docusaurus-book
   ```

2. Install Node dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npx docusaurus start
   ```

## Troubleshooting

### Common Issues

1. **Port already in use**: Make sure ports 3000 (frontend) and 8000 (backend) are available.

2. **Qdrant connection issues**: Ensure Qdrant is running on port 6333:
   ```bash
   docker ps
   ```
   If not running, start it with:
   ```bash
   docker run -d --name qdrant -p 6333:6333 -p 6334:6334 qdrant/qdrant
   ```

3. **PyTorch/SentenceTransformer DLL errors**: The system will work with limited functionality. For full embedding support, ensure your Python environment has the correct PyTorch installation for your system.

4. **Database connection errors**: The system will work without database features. For full functionality, set up a PostgreSQL database and update the .env file.

### API Endpoints

- `POST /query` - Query the RAG system with a question
- `POST /select-text-ask` - Ask about selected text
- `GET /health` - Health check
- `POST /translate-book` - Translate book content
- `GET/POST /user/preferences` - User preferences management

## Architecture

- **Frontend**: Docusaurus site with React components
- **Backend**: FastAPI server with RAG functionality
- **Vector Store**: Qdrant for document embeddings
- **Database**: PostgreSQL for user data and analytics (optional)
- **ML Models**: SentenceTransformer for embeddings, transformers for text generation

## Development

To contribute to this project:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

[Specify your license here]