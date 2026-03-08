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

    with st.spinner("Thinking..."):

        # Retrieve documents from FAISS
        results = search(question)

        documents = [r["document"] for r in results]
        sources = [r["source"] for r in results]

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
    st.success(answer)

    st.subheader("Sources")

    for source in sources:
        st.write(source)