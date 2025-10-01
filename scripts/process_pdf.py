import os
import fitz
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
from dotenv import load_dotenv
import hashlib

load_dotenv()

class PDFProcessor:
    def __init__(self):
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.chroma_client = chromadb.PersistentClient(path="./data/chroma_db")
        self.collection = self.chroma_client.get_or_create_collection("rust_docs")
        
    def extract_text_from_pdf(self, pdf_path):
        doc = fitz.open(pdf_path)
        chunks = []
        
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text = page.get_text()
            
            paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
            for para in paragraphs:
                if len(para) > 50:
                    chunks.append({
                        'text': para,
                        'page': page_num + 1,
                        'source': os.path.basename(pdf_path)
                    })
        
        doc.close()
        return chunks
    
    def generate_id(self, text):
        return hashlib.md5(text.encode()).hexdigest()
    
    def process_and_store(self, pdf_path):
        print("Extracting text from PDF...")
        chunks = self.extract_text_from_pdf(pdf_path)
        print(f"Extracted {len(chunks)} chunks")
        
        documents = []
        metadatas = []
        ids = []
        
        for chunk in chunks:
            documents.append(chunk['text'])
            metadatas.append({
                'page': chunk['page'],
                'source': chunk['source']
            })
            ids.append(self.generate_id(chunk['text']))
        
        print("Adding to ChromaDB...")
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        print("PDF processing complete!")

if __name__ == "__main__":
    processor = PDFProcessor()
    processor.process_and_store("./data/raw_docs/rust_documentation.pdf")
