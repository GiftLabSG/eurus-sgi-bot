import os
import sys
from dotenv import load_dotenv

# --- NEW: Fix for sqlite3 version incompatibility on Streamlit Cloud ---
try:
    __import__('pysqlite3')
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except ImportError:
    pass
# --- END NEW ---

# Load environment variables from .env file (for local development)
load_dotenv()

import streamlit as st
from helper_functions.utility import check_password 
from helper_functions.qa_chain import get_final_response
from helper_functions.vectorstore import get_embedding, persist_directory, refresh_vectorstore, urls_to_scrape

# Check for password
if not check_password():
    st.stop()

# Streamlit page config
st.set_page_config(page_title="Eurus: Security Grant Initiative", page_icon="💡")
st.title("💡 Eurus: Security Grant Initiative")
st.write("Ask any question about government grants for security agencies in Singapore.")
st.write("👉 Tip: Type **'List of grants for security agencies'** to see all relevant grants.")

# --- Check and refresh vector store with proper feedback ---
if not os.path.exists(os.path.join(persist_directory, "chroma.sqlite3")):
    st.info("Vector store missing. Building the knowledge base...")
    try:
        embedding = get_embedding()
        refresh_vectorstore(urls_to_scrape, embedding)
        st.success("Vector store built and ready!")
    except Exception as e:
        st.error(f"Error building vector store. Please check logs. Error: {e}")
        st.exception(e)
        st.stop()

# Input field
query = st.text_input("Enter your question")

if query:
    with st.spinner("Thinking..."):
        try:
            response = get_final_response(query)
            st.markdown(response)
        except Exception as e:
            st.warning("❗ Sorry, an error occurred. The bot could not process your query.")
            st.exception(e)
            st.info(
"""If you're looking for training or workforce upgrading support, you might consider grants such as:
- **Career Conversion Programme (CCP) for Security Officers**
- **Company Training Committee Grant (CTC)**
- **Productivity Solutions Grant (PSG)**
📬 For more help, you can contact **WSG_Biz_Services@wsg.gov.sg** or [fill out this form](https://go.gov.sg/contact-form)."""
            )