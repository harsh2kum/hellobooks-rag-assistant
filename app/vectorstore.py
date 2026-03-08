import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from pathlib import Path

# Load embedding model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

documents = []
sources = []
embeddings = []

kb_path = Path("knowledge_base")

# Load documents
for file in kb_path.glob("*"):
    text = file.read_text(encoding="utf-8")
    documents.append(text)
    sources.append(file.name)
    embeddings.append(model.encode(text))

# Convert to numpy
embeddings = np.array(embeddings).astype("float32")

# Build FAISS index
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)


def search(query, k=3):

    query_embedding = model.encode(query).astype("float32").reshape(1, -1)

    distances, indices = index.search(query_embedding, k)

    results = []

    for i in indices[0]:
        results.append({
            "document": documents[i],
            "source": sources[i]
        })

    return results