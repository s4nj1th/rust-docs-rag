<div align="center">
    <img src="src/favicon.ico" width="128"/>
    <h1>Rust Docs RAG Chatbot</h1>
    <p>A Retrieval-Augmented Generation (RAG) chatbot that answers questions about Rust programming using the official Rust documentation. Get accurate, context-aware answers powered by semantic search and large language models.</p>
</div>

## Features

- **Documentation-Powered Answers**: Uses actual Rust documentation as knowledge base
- **Semantic Search**: Finds relevant documentation snippets using vector embeddings
- **Multiple Interfaces**: Choose between terminal or web-based chat
- **Local Processing**: ChromaDB vector storage runs entirely locally
- **Flexible LLM Support**: Compatible with OpenAI, OpenRouter models.

## Quick Start

### Prerequisites

- Python 3.8+
- Rust documentation PDF (optional - can use any Rust docs)

### Installation

1. **Clone and setup environment**:
```bash
git clone https://github.com/s4nj1th/rust-docs-rag.git
cd rust-docs-rag
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Set up your Rust documentation**:
```bash
# Place your Rust documentation PDF in:
mkdir -p data/raw_docs
# Add your rust-docs.pdf to data/raw_docs/
```

4. **Build the knowledge base**:
```bash
python scripts/process_pdf.py
```

5. **Configure API keys** (optional for local models):
```bash
cp .env.example .env
# Edit .env and add your OpenRouter API key if using cloud LLMs
```

## Usage

### Terminal Interface
```bash
python src/chatbot.py
```

### Web Interface (Streamlit)
```bash
streamlit run src/streamlit_app.py
```

## Architecture

```
rust-docs-rag/
├── data/
│   ├── raw_docs/          # Source PDF documentation
│   └── chroma_db/         # Vector database (auto-generated)
├── src/
│   ├── chatbot.py         # Terminal chat interface
│   ├── streamlit_app.py   # Web interface
│   ├── vector_store.py    # ChromaDB management
│   └── document_loader.py # PDF processing
├── scripts/
│   └── process_pdf.py     # Knowledge base builder
└── config/
    └── settings.yaml      # Configuration
```

## How It Works

1. **Document Processing**: PDFs are chunked and converted to vector embeddings
2. **Semantic Search**: User queries are matched against documentation vectors
3. **Context Augmentation**: Relevant doc snippets are injected into LLM prompts
4. **Answer Generation**: LLM produces accurate answers based on Rust documentation

## Development

### Adding New Documentation
```bash
# Add new PDFs to data/raw_docs/
python scripts/process_pdf.py  # Rebuilds vector database
```

### Customizing Embeddings
Edit `src/vector_store.py` to use different embedding models:
- `all-MiniLM-L6-v2` (default, fast)
- `all-mpnet-base-v2` (higher quality)

### Using Local Models
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull a model
ollama pull llama2:7b

# Update chatbot.py to use local endpoint
```

## Performance

- **Embedding Model**: SentenceTransformers `all-MiniLM-L6-v2`
- **Vector Database**: ChromaDB (local persistence)
- **Retrieval**: Top-5 most relevant chunks
- **Response Time**: 2-5 seconds typical

## Contributing

Contributions welcome! Please feel free to submit pull requests or open issues for:
- Additional LLM integrations
- Improved chunking strategies
- UI enhancements
- Performance optimizations

## License

This project is distributed under the [MIT License](./LICENSE).

## Acknowledgments

- Built with ChromaDB for vector storage
- SentenceTransformers for embeddings
- Streamlit for web interface
- Rust community for excellent documentation
