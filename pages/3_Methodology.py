import streamlit as st

st.set_page_config(page_title="Methodology", layout="wide")

st.title("Eurus-SGI Bot Development and Operational Methodology")
st.subheader("An AI-Powered Question-Answering Bot")

st.markdown("---")

st.markdown("### I. Development Stage: Building the Eurus-SGI Knowledge Base and Core Functions")
st.write("""
This section provides a detailed overview of the methodology employed in the development of Eurus-SGI. The process involved a systematic, multi-stage approach to ingest, process, and structure information into a usable knowledge base, coupled with the creation of intelligent components for information retrieval and response generation.
""")

st.image("images/development_stage.png", caption="Eurus-SGI Development Stage Workflow", use_container_width=True)

st.markdown("#### 1. Comprehensive Data Acquisition: Identifying and Compiling Relevant Sources")
st.write("""
The initial critical step involved the meticulous identification and compilation of diverse data sources relevant to the bot's domain. This included a curated list of **Targeted URLs** and **Manually Curated HTML Files** for websites where automated scraping was not feasible. This careful selection and organization of raw data formed the foundational layer of Eurus-SGI's knowledge.
""")

st.markdown("#### 2. Intelligent Data Extraction: Development of a Custom Web Scraping Function")
st.write("""
To transform the raw data into a usable format, a custom web scraping function was developed. This script was engineered to automate data retrieval, parse and structure text, and perform crucial data cleaning and pre-processing. The custom nature of this function allowed for fine-tuned control, optimizing the extraction process for the specific content and structure of the chosen data sources.
""")

st.markdown("#### 3. Semantic Indexing: Construction of a Vector Store (ChromaDB)")
st.write("""
The extracted and pre-processed text was then used to build a semantic index using **ChromaDB**, a vector store. This process was designed with a unique and robust approach to ensure the highest quality of data and retrieval accuracy.
""")
st.write("""
- **Hybrid Data Ingestion:** This custom process combines live web scraping from an extensive list of URLs with the loading of local, manually curated HTML files. This ensures a comprehensive dataset that is both current and supplemented by stable, pre-processed documents.
- **Text Chunking:** The text chunking phase utilizes a custom-configured `RecursiveCharacterTextSplitter`. Instead of relying on a simple character limit, this tool intelligently breaks down documents at semantically meaningful separators like paragraphs and sentences, ensuring that each chunk retains a complete idea.
- **Generating Text Embeddings & Storing:** Each chunk is converted into a high-dimensional numerical vector. During this step, a robust metadata pipeline tags each chunk with its corresponding `grant_title` and `source` URL. This enriched metadata is then stored alongside the vectors in the ChromaDB.
""")

st.markdown("#### 4. Intelligent Information Retrieval: Coding the Retriever Function")
st.write("""
The retriever function acts as the intelligent intermediary between a user's query and the knowledge indexed in the vector store. It performs **Query Embedding** to represent the user's question semantically and a **Similarity Search** within ChromaDB to identify the most relevant text chunks. The retriever's efficiency is critical for providing relevant context to the subsequent question-answering process.
""")

st.markdown("#### 5. Contextual Response Generation: Developing the QA Chain")
st.write("""
The **QA (Question-Answering) Chain** synthesizes a coherent and accurate answer based on the retrieved information. It integrates a standard Retrieval-Augmented Generation (RAG) approach with several unique enhancements:
""")
st.write("""
- **Proactive Grant Detection:** The system first employs a multi-stage detection process, including direct keyword matching, fuzzy matching, and intent-based detection, to filter the knowledge base before retrieval.
- **Context-Aware Complementary Grant Suggestion:** After generating the primary answer, the chain can intelligently suggest a complementary grant based on a predefined list or similar objectives.
- **Intelligent Fallback and Proactive Guidance:** The system handles ambiguity gracefully by providing curated lists of grants for specific sectors or a user-friendly fallback message when a direct answer cannot be found.
""")

st.markdown("#### 6. Core Application Logic: Coding the `main.py` File")
st.write("""
The `main.py` file serves as the central orchestrator of all the developed components. It handles user input, manages the flow of information between modules (retriever, QA Chain), and presents the final response to the user. This script ensures the seamless integration and operation of the entire system.
""")

st.markdown("---")

st.markdown("### II. User Query Flow: From Input to Response")
st.write("""
This section illustrates the step-by-step process that occurs when a user interacts with the Eurus-SGI bot by submitting a question.
""")

st.image("images/user_query_flow.png", caption="Eurus-SGI User Query Flow", use_container_width=True)

st.markdown("""
1.  **User Input:** A user types a question into the bot's interface, which is captured by the `main.py` application.
2.  **Query Transmission to Retriever:** The application sends the user's question to the retriever function.
3.  **Vector Store Query:** The retriever converts the question into a vector and queries the **ChromaDB** vector store to find the most relevant text chunks.
4.  **Contextual Data to QA Chain:** The retriever gathers the most relevant text chunks and transmits them to the QA Chain.
5.  **LLM Processing:** The QA Chain combines the user's original question with the retrieved context and sends this augmented prompt to the **Large Language Model**.
6.  **Response Generation:** The Large Language Model processes the provided context and the original question to generate a comprehensive and relevant answer.
7.  **Response Delivery to User:** The generated answer is then passed back to the `main.py` application, which formats and displays the response to the user.
""")

st.markdown("---")
st.caption("© 2025 Eurus - SGI | Built for the Security Sector in Singapore")