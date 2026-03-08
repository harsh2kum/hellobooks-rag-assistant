import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from pathlib import Path

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

documents = []
embeddings = []

kb_path = Path("knowledge_base")

for file in kb_path.glob("*"):
    text = file.read_text()
    documents.append(text)
    embeddings.append(model.encode(text))

embeddings = np.array(embeddings).astype("float32")

index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)


def search(query, k=3):
    q_embedding = model.encode(query).astype("float32").reshape(1, -1)
    distances, indices = index.search(q_embedding, k)
    return [documents[i] for i in indices[0]]