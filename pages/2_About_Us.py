import streamlit as st

st.set_page_config(page_title="About Us", layout="centered")

st.title("About Eurus - SGI")
st.subheader("Empowering Security Agencies with Grant Intelligence")

st.markdown("---")

st.markdown("### 🧩 Problem Statement")
st.write("""
Security agencies in Singapore face a fragmented landscape when it comes to navigating available government grants. 
These grants—covering areas like technology adoption, workforce upskilling, and digital transformation—are scattered 
across multiple websites and agencies. This makes it difficult for agencies to access relevant, timely, and actionable 
information to support their growth and transformation goals.
""")

st.markdown("### 💡 Proposed Solution")
st.write("""
**Eurus - SGI (Security Grant Intelligence)** is an AI-powered assistant designed to simplify the grant discovery process.

Using Retrieval-Augmented Generation (RAG), Eurus continuously gathers and updates information from official government 
sources through web scraping and manual curation. The assistant can:

- Answer user queries about grants, including **eligibility, objectives, application steps, and more**
- Recommend **complementary or bundled grants** based on the agency's needs
- Offer **human escalation** options when the assistant cannot provide an answer

The goal is to provide an intuitive, always-accessible, and accurate solution for security agencies seeking funding 
opportunities to innovate and grow.
""")

st.markdown("### 🎯 Target Users")
st.write("""
The primary users of Eurus - SGI are **security agencies in Singapore** looking to explore and apply for government 
grants and initiatives relevant to the security sector. These include SMEs and larger firms aiming to upgrade operations, 
digitize services, or enhance manpower capability.

With future iterations, the scope may expand to include grants for related sectors and deeper integration with grant 
application portals.
""")

st.markdown("### 📬 Need Help?")
st.write("""
If Eurus is unable to address your query, don't worry — you will be guided to either:
- Contact a human officer via email, or
- Submit your query through an **online support form**.

We're committed to bridging the gap between agencies and available support, making transformation easier and faster.
""")

st.markdown("---")
st.caption("© 2025 Eurus - SGI | Built for the Security Sector in Singapore")