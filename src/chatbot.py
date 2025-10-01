import os
from openai import OpenAI
from dotenv import load_dotenv
from vector_store import VectorStore

load_dotenv()

class RAGChatbot:
    def __init__(self):
        self.vector_store = VectorStore()
        self.client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=os.getenv('OPENROUTER_API_KEY')
        )
    
    def generate_response(self, query):
        try:
            results = self.vector_store.search(query)
            if not results or 'documents' not in results or not results['documents'] or not results['documents'][0]:
                return "Sorry, I couldn't find any relevant context in the Rust documentation. Please try rephrasing your question."

            context = "\n\n".join(results['documents'][0])

            try:
                response = self.client.chat.completions.create(
                    model="deepseek/deepseek-chat-v3.1:free",
                    messages=[
                        {"role": "system", "content": "You are a helpful Rust programming expert. Use the provided context to answer questions about Rust. If the context doesn't contain relevant information, say so."},
                        {"role": "user", "content": query}
                    ],
                    temperature=0.1,
                    max_tokens=500
                )
            except Exception as api_err:
                return f"Error communicating with the language model: {str(api_err)}"

            if not response or not hasattr(response, 'choices') or not response.choices:
                return "Sorry, I couldn't generate a response. Please try again later."

            return response.choices[0].message.content
        except Exception as e:
            return f"An error occurred while processing your request: {str(e)}"

def main():
    chatbot = RAGChatbot()
    print("Rust Doc RAG Chatbot ready! Type 'quit' to exit.")
    
    while True:
        query = input("\nQuestion: ")
        if query.lower() == 'quit':
            break
        
        response = chatbot.generate_response(query)
        print(f"\nAnswer: {response}")

if __name__ == "__main__":
    main()
