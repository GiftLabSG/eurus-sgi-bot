import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

import streamlit as st
from helper_functions.utility import check_password 
from helper_functions.qa_chain import get_final_response
from helper_functions.vectorstore import get_embedding, persist_directory, refresh_vectorstore, urls_to_scrape

# --- NEW: Add a top-level try-except block to catch all errors ---
try:
    # The entire app's logic is now inside this block
    if not check_password():
        st.stop()

    # Streamlit page config
    st.set_page_config(page_title="Eurus: Security Grant Initiative", page_icon="💡")
    st.title("💡 Eurus: Security Grant Initiative")
    st.write("Ask any question about government grants for security agencies in Singapore.")
    st.write("👉 Tip: Type **'List of grants for security agencies'** to see all relevant grants.")

    if not os.path.exists(os.path.join(persist_directory, "chroma.sqlite3")):
        st.info("Vector store missing. Building the knowledge base...")
        try:
            embedding = get_embedding()
            refresh_vectorstore(urls_to_scrape, embedding)
            st.success("Vector store built and ready!")
        except Exception as e:
            st.error(f"Error building vector store: {e}")
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
                    "If you're looking for training or workforce upgrading support, "
                    "you might consider grants such as:\n\n"
                    "- **Career Conversion Programme (CCP) for Security Officers**\n"
                    "- **SkillsFuture Enterprise Credit (SFEC)**\n"
                    "- **Productivity Solutions Grant (PSG)**\n\n"
                    "📬 For more help, you can contact **WSG_Biz_Services@wsg.gov.sg** or "
                    "[fill out this form](https://go.gov.sg/contact-form)."
                )

# --- NEW: This block will catch any top-level exceptions and display them ---
except Exception as e:
    st.error("An unhandled error occurred at the top-level of the app.")
    st.exception(e)
# --- END NEW ---