import streamlit as st

st.set_page_config(page_title="Methodology", layout="wide")

st.title("Bot Methodology")
st.subheader("How Eurus - SGI Was Built and How It Runs")

st.markdown("---")

st.markdown("### 🛠️ Development Stage")
st.write("""
This section describes the step-by-step process used to build the bot's knowledge base and core functions.
""")

st.markdown("#### 1. Compile Relevant URLs and HTMLs")
st.write("""
The process begins with identifying and gathering all the necessary data sources—URLs and manually curated HTML files—that contain the information the bot needs to answer questions. This raw data forms the foundation of the bot's knowledge.
""")

st.markdown("#### 2. Code Web Scraping Function")
st.write("""
A custom function was developed to automatically extract data from the compiled URLs and HTML files. This script parses the raw text from the web pages and structures it into a usable format, filtering out irrelevant elements.
""")

st.markdown("#### 3. Code Vector Store")
st.write("""
The extracted data is then processed to create a vector store (ChromaDB). This involves breaking the text into chunks, converting each chunk into a numerical embedding, and storing these embeddings for fast and efficient similarity searches.
""")

st.markdown("#### 4. Code Retriever")
st.write("""
The retriever function is the bridge between a user's query and the vector store. It takes a user's question, converts it into a vector, and then searches the vector store for the text chunks that are most semantically similar to the query.
""")

st.markdown("#### 5. Code QA Chain")
st.write("""
The QA (Question-Answering) Chain combines the user's original query with the relevant information retrieved from the vector store. This combined context is then sent to a large language model (LLM) to synthesize a clear and accurate answer.
""")

st.markdown("#### 6. Code main.py")
st.write("""
This is the main application file that brings all the components together. It handles user input, orchestrates the calls to the retriever and QA chain, and presents the final response to the user.
""")

st.markdown("---")

st.markdown("### 🔄 User Query Flow")
st.write("""
This section details the journey of a user's query from the moment it is submitted to the final response.
""")

st.image("http://googleusercontent.com/image_collection/image_retrieval/10047254836227734069_0", caption="Eurus-SGI Bot Methodology and User Flow")

st.markdown("""
1.  **User Input:** A user types a question into the bot's interface.
2.  **Query to Retriever:** The main application sends the user's question to the retriever.
3.  **Retriever to Vector Store:** The retriever converts the question into a vector and queries the vector store (ChromaDB) to find the most relevant text chunks from your data.
4.  **Vector Store to QA Chain:** The retrieved text chunks are sent to the QA Chain.
5.  **QA Chain to LLM:** The QA Chain combines the user's original question with the retrieved context and sends it to the Large Language Model.
6.  **LLM Generates Response:** The LLM processes the context and generates a final, synthesized answer.
7.  **Response to User:** The generated answer is sent back through the main application and displayed to the user.
""")

st.markdown("---")
st.caption("© 2025 Eurus - SGI | Built for the Security Sector in Singapore")