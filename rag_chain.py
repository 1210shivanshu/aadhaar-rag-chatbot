import pandas as pd
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA
from groq_config import get_groq_api_key

# Load the data
df = pd.read_csv("all_aadhaar_faqs.csv")

# Combine Q&A into documents
docs = [
    Document(
        page_content=f"Q: {row['Question']}\nA: {row['Answer']}",
        metadata={"source": row['Source URL']}
    ) for _, row in df.iterrows()
]

# No splitting needed – treat each full Q&A as one unit
split_docs = docs

# Embedding model
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Create vector store
vectorstore = FAISS.from_documents(split_docs, embedding_model)
retriever = vectorstore.as_retriever()

# LLM setup (Gemma2 via Groq)
llm = ChatGroq(api_key=get_groq_api_key(), model_name="gemma2-9b-it")

# RAG chain without source documents
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=False
)

# Export retriever and chain for Streamlit
__all__ = ["qa_chain"]
