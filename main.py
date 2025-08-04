import os
from dotenv import load_dotenv
# Load environment variables
load_dotenv()

import streamlit as st
from helper_functions.utility import check_password 
# Check if the password is correct.  
if not check_password():
    st.stop()

from helper_functions.qa_chain import get_final_response

# Streamlit page config
st.set_page_config(page_title="Eurus: Security Grant Initiative", page_icon="💡")
st.title("💡 Eurus: Security Grant Initiative")
st.write("Ask any question about government grants for security agencies in Singapore.")
st.write("👉 Tip: Type **'List of grants for security agencies'** to see all relevant grants.")

#NEW
from helper_functions.vectorstore import refresh_vectorstore, urls_to_scrape, get_embedding, persist_directory
embedding = get_embedding()
if not os.path.exists(persist_directory) or not os.listdir(persist_directory):
    st.write("Vectorstore missing or empty, refreshing...")
    refresh_vectorstore(urls_to_scrape, embedding)
    st.write("Vectorstore refreshed!")
    #REVIEW THE ABOVE

# Input field
query = st.text_input("Enter your question")

if query:
    with st.spinner("Thinking..."):
        try:
            response = get_final_response(query)
            st.markdown(response)
        except Exception:
            st.warning("❗ Sorry, I couldn't find a suitable answer to your question.")
            st.info(
                "If you're looking for training or workforce upgrading support, "
                "you might consider grants such as:\n\n"
                "- **Career Conversion Programme (CCP) for Security Officers**\n"
                "- **SkillsFuture Enterprise Credit (SFEC)**\n"
                "- **Productivity Solutions Grant (PSG)**\n\n"
                "📬 For more help, you can contact **WSG_Biz_Services@wsg.gov.sg** or "
                "[fill out this form](https://go.gov.sg/contact-form)."
            )