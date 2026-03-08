import streamlit as st
import sys
import os

sys.path.append(os.path.abspath("."))

from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

from app.config import *
from app.vectorstore import search
from app.prompts import SYSTEM_PROMPT


st.title("📊 Hellobooks AI Assistant")
st.write("Ask bookkeeping and accounting questions.")


@st.cache_resource
def load_models():
    embedding_model = SentenceTransformer(EMBEDDING_MODEL)
    tokenizer = AutoTokenizer.from_pretrained(LLM_MODEL)
    model = AutoModelForSeq2SeqLM.from_pretrained(LLM_MODEL)
    return embedding_model, tokenizer, model


embedding_model, tokenizer, model = load_models()

question = st.text_input("Ask a bookkeeping question:")

if question:

    # Retrieve relevant documents using FAISS
    documents = search(question)

    context = "\n".join(documents)

    prompt = SYSTEM_PROMPT.format(
        context=context,
        question=question
    )

    inputs = tokenizer(prompt, return_tensors="pt", truncation=True)

    outputs = model.generate(
        **inputs,
        max_new_tokens=200
    )

    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)

    st.subheader("Answer")
    st.write(answer)

    st.subheader("Sources")

    for doc in documents:
        st.write("Knowledge Base Document")