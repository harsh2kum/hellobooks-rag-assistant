import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from pathlib import Path
from sentence_transformers import SentenceTransformer
from app.vectorstore import get_vector_store
from app.config import EMBEDDING_MODEL

model = SentenceTransformer(EMBEDDING_MODEL)


def load_documents():

    docs = []
    kb_path = Path("knowledge_base")

    for file in kb_path.glob("*"):

        with open(file, "r", encoding="utf-8") as f:
            docs.append({
                "text": f.read(),
                "source": file.name
            })

    return docs


def ingest():

    collection, chroma_client = get_vector_store()

    docs = load_documents()

    for doc in docs:

        embedding = model.encode(doc["text"]).tolist()

        
        collection.add(
            documents=[doc["text"]],
            embeddings=[embedding],
            ids=[doc["source"]],
            metadatas=[{"source": doc["source"]}]
        )
        

    

    print("Knowledge Base Created Successfully")


if __name__ == "__main__":
    ingest()