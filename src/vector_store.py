import chromadb
from sentence_transformers import SentenceTransformer
from chromadb.config import Settings

class VectorStore:
    def __init__(self):
        self.client = chromadb.PersistentClient(path="./data/chroma_db")
        self.collection = self.client.get_collection("rust_docs")
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    
    def search(self, query, n_results=5):
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results,
            include=['documents', 'metadatas', 'distances']
        )
        return results
    
    def get_collection_info(self):
        return self.collection.count()
