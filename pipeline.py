import os
import sys
import json
from ollama import Ollama

# Initialize Ollama with your quantized Llama2 model
model = Ollama(model='llama2')

# Directory paths
VECTOR_STORE_DIR = 'C:\\Ollama\\VectorStore'
DOCUMENTS_DIR = 'C:\\Ollama\\Documents'

# Initialize vector store
vector_store = model.init_vector_store(directory=VECTOR_STORE_DIR)

def get_embeddings(text):
    """
    Generate embeddings for the given text using Ollama.
    """
    response = model.embed(text)
    return response['embedding']

def librarian_agent(subject):
    """
    Retrieve relevant documents from the vector store based on the subject.
    """
    subject_embedding = get_embeddings(subject)
    # Perform similarity search (top 10 results)
    results = vector_store.search(embedding=subject_embedding, top_k=10)
    
    documents = []
    for result in results:
        doc_id = result['id']
        filepath = os.path.join(DOCUMENTS_DIR, doc_id)
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as file:
                documents.append(file.read())
    return documents

def outliner_agent(documents):
    """
    Generate a detailed outline based on the retrieved documents.
    """
    prompt = (
        "Based on the following information, create a comprehensive and thoughtful outline for a book on the subject.\n\n"
        + "\n\n".join(documents)
    )
    response = model.generate(prompt)
    return response['text']

def technical_writer_agent(outline):
    """
    Expand the outline into detailed book content.
    """
    prompt = (
        "Using the following outline, write a detailed and comprehensive book on the subject.\n\n"
        + outline
    )
    response = model.generate(prompt)
    return response['text']

def main(subject):
    """
    Orchestrate the pipeline to generate a book based on the subject.
    """
    print(f"Starting pipeline for subject: {subject}\n")
    
    # Step 1: Librarian Agent retrieves relevant documents
    print("Librarian Agent: Retrieving relevant documents...")
    documents = librarian_agent(subject)
    if not documents:
        print("No relevant documents found.")
        return
    print(f"Retrieved {len(documents)} documents.\n")
    
    # Step 2: Outliner Agent creates an outline
    print("Outliner Agent: Creating outline...")
    outline = outliner_agent(documents)
    print("Outline created successfully.\n")
    
    # Step 3: Technical Writer Agent fleshes out the outline
    print("Technical Writer Agent: Writing book content...")
    book_content = technical_writer_agent(outline)
    print("Book content generated successfully.\n")
    
    return book_content

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python pipeline.py \"Subject A\"")
        sys.exit(1)
    
    subject = sys.argv[1]
    book = main(subject)
    
    if book:
        # Save the book to a file
        output_dir = 'C:\\Ollama\\GeneratedBooks'
        os.makedirs(output_dir, exist_ok=True)
        book_filename = f"{subject.replace(' ', '_')}_book.txt"
        book_path = os.path.join(output_dir, book_filename)
        with open(book_path, 'w', encoding='utf-8') as f:
            f.write(book)
        print(f"Book saved to {book_path}")
