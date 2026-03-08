import sys
import os

# allow importing from project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

from app.config import *
from app.vectorstore import get_vector_store
from app.prompts import SYSTEM_PROMPT


# Load embedding model
embedding_model = SentenceTransformer(EMBEDDING_MODEL)

# Load LLM model
tokenizer = AutoTokenizer.from_pretrained(LLM_MODEL)
model = AutoModelForSeq2SeqLM.from_pretrained(LLM_MODEL)


def ask():

    collection, _ = get_vector_store()

    while True:

        question = input("\nAsk a bookkeeping question: ")

        if question.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        # Create embedding for query
        query_embedding = embedding_model.encode(question).tolist()

        # Retrieve relevant documents
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=TOP_K
        )

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]

        context = "\n".join(documents)

        # Build prompt
        prompt = SYSTEM_PROMPT.format(
            context=context,
            question=question
        )

        # Tokenize prompt
        inputs = tokenizer(prompt, return_tensors="pt", truncation=True)

        # Generate answer
        outputs = model.generate(
            **inputs,
            max_new_tokens=200
        )

        # Decode answer
        answer = tokenizer.decode(outputs[0], skip_special_tokens=True)

        print("\nAnswer:\n", answer)

        print("\nSources:")
        for meta in metadatas:
            print("-", meta["source"])


if __name__ == "__main__":
    ask()