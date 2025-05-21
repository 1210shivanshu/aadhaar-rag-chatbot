import os
print("Current working directory:", os.getcwd())
print("Files in working directory:", os.listdir())
import streamlit as st
from rag_chain import qa_chain

st.set_page_config(page_title="Aadhaar Chatbot", page_icon="🧾")
st.title("🧾 Aadhaar Helpdesk Chatbot")

st.markdown(
    """
    **Tired of endlessly surfing government websites or making *yet another* trip to the Aadhaar office?**  
    Well, you're in luck! This chatbot is trained *only* on official Aadhaar FAQs and info, so you get straight answers without the hassle.  
    No more jumping through bureaucratic hoops — just ask and get the facts.  
    (Yes, even those confusing NRI rules!)  
    \n
    *Built with ❤️ by Shivanshu to save your time and sanity.*
    """
)

query = st.text_input(
    "Go ahead, ask your Aadhaar question here:",
    key="query_input"
)

if query:
    with st.spinner("Let me dig through the official docs for you..."):
        prompt_query = f"Answer the question based only on Aadhaar rules: {query}"
        result = qa_chain.invoke({"query": prompt_query})
        st.success("Here's what I found:")
        st.write(result['result'] if isinstance(result, dict) else result)
