import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter

from helper_functions.web_scraper import scrape_and_clean

# Load environment variables
load_dotenv()

persist_directory = "data/chroma_db"
manual_scrape_dir = "data/manual_scrapes"

def get_embedding():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is missing!")
    return OpenAIEmbeddings(openai_api_key=api_key)

# Improved splitter to chunk on paragraphs and smaller units
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=150,
    separators=["\n\n", "\n", ".", " "]
)

# URL to grant title mapping dictionary
url_metadata_map = {
    "https://www.enterprisesg.gov.sg/financial-support/enterprise-development-grant": "Enterprise Development Grant",
    "https://www.enterprisesg.gov.sg/resources/all-faqs/enterprise-development-grant": "Enterprise Development Grant",
    "https://www.enterprisesg.gov.sg/financial-support/productivity-solutions-grant": "Productivity Solutions Grant",
    "https://www.gobusiness.gov.sg/productivity-solutions-grant/#type-of-psg-soln": "Productivity Solutions Grant",
    "https://www.gobusiness.gov.sg/business-grants-portal-faq/psg-general/": "Productivity Solutions Grant",
    "https://www.gobusiness.gov.sg/productivity-solutions-grant/all-psg-solutions/": "Productivity Solutions Grant",
    "https://www.gobusiness.gov.sg/browse-all-solutions-security/automated-visitor-management": "Productivity Solutions Grant",
    "https://www.enterprisesg.gov.sg/financial-support/skillsfuture-enterprise-credit": "SkillsFuture Enterprise Credit",
    "https://www.enterprisesg.gov.sg/resources/all-faqs/skillsfuture-enterprise-credit": "SkillsFuture Enterprise Credit",
    "https://snef.org.sg/grants/ccp-so/": "Career Conversion Programme for Security Officers",
    "https://conversion.mycareersfuture.gov.sg/Portal/ProgramDetails.aspx?ProgID=P00003120": "Career Conversion Programme for Security Officers",
    "https://www.wsg.gov.sg/home/employers-industry-partners/workforce-development-job-redesign/security-productivity-initiative": "Security Productivity Initiative",
    "https://www.sbf.org.sg/what-we-do/skills-empowered/career-conversion-programme/CCP-HC": "Career Conversion Programme for Human Capital Professionals",
    "https://snef.org.sg/grants/ccp-hcp/": "Career Conversion Programme for Human Capital Professionals",
    "https://www.wsg.gov.sg/home/employers-industry-partners/workforce-development-job-redesign/support-for-job-redesign-under-productivity-solutions-grant": "Job Redesign under Productivity Solutions Grant",
    "https://snef.org.sg/grants/psgjr/": "Job Redesign under Productivity Solutions Grant",
    "https://www.imda.gov.sg/how-we-can-help/smes-go-digital/advanced-digital-solutions": "Advanced Digital Solutions Grant",
    "https://services2.imda.gov.sg/ctoaas/Category/ads_15/integrated-security-management--ism-": "Advanced Digital Solutions Grant",
    "https://www.e2i.com.sg/ctc/": "Company Training Committee Grant",
    "https://skillsfuture.gobusiness.gov.sg/support-and-programmes/skillsfuture-queen-bee-networks": "SkillsFuture Queen Bee by AETOS",
    "https://skillsfuture.gobusiness.gov.sg/support-and-programmes/skillsfuture-queen-bee-networks/sfqb-aetos": "SkillsFuture Queen Bee by AETOS",
    "https://www.aetos.com.sg/SFQB": "SkillsFuture Queen Bee by AETOS"
}

def load_manual_documents(directory_path):
    """
    Load manual .html documents from a directory and convert them to Document objects.
    """
    manual_docs = []
    for filename in os.listdir(directory_path):
        if filename.endswith(".html"):
            file_path = os.path.join(directory_path, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                soup = BeautifulSoup(f, "html.parser")
                content = soup.get_text(separator="\n", strip=True)

            normalized_name = filename.replace(".html", "").lower()

            if normalized_name.startswith("company_training_committee_grant"):
                grant_title = "Company Training Committee Grant"
            elif normalized_name.startswith("skillsfuture_queen_bee"):
                grant_title = "SkillsFuture Queen Bee by AETOS"
            elif normalized_name.startswith("career_conversion_programme_for_human_capital_professionals"):
                grant_title = "Career Conversion Programme for Human Capital Professionals"
            else:
                grant_title = normalized_name.replace("_", " ").title()

            metadata = {
                "grant_title": grant_title,
                "source": f"manual_html::{filename}"
            }
            print(f"✅ Parsed manual grant title: {grant_title}")

            manual_docs.append(Document(page_content=content, metadata=metadata))
            print(f"📄 Loaded HTML file: {filename}")
    return manual_docs

def refresh_vectorstore(urls):
    print("🚀 Starting vectorstore refresh...")

    # 1. Scrape live URLs
    docs = []
    for url in urls:
        doc = scrape_and_clean(url, url_metadata_map)
        if doc:
            docs.append(doc)
    print(f"✅ Scraped {len(docs)} documents from URLs.")

    # 2. Load manual .html documents
    manual_docs = load_manual_documents(manual_scrape_dir)
    docs.extend(manual_docs)
    print(f"📄 Total documents after adding manual HTMLs: {len(docs)}")
    
    # 3. Chunk documents with improved splitter
    all_chunks = []
    for doc in docs:
        chunks = splitter.split_text(doc.page_content)
        for chunk in chunks:
            all_chunks.append(Document(page_content=chunk, metadata=doc.metadata))
    print(f"📚 Split into {len(all_chunks)} chunks.")

    # 4. Check for empty chunks
    if len(all_chunks) == 0:
        print("⚠️ No chunks to add to vectorstore. Aborting.")
        return

    # 5. Save chunks to vectorstore
    db = Chroma.from_documents(
        documents=all_chunks,
        embedding=embedding,
        persist_directory=persist_directory
    )
    
    print("✅ Vectorstore refresh complete.")

urls_to_scrape = [
    "https://www.enterprisesg.gov.sg/financial-support/enterprise-development-grant",
    "https://www.enterprisesg.gov.sg/resources/all-faqs/enterprise-development-grant",
    "https://www.enterprisesg.gov.sg/financial-support/productivity-solutions-grant",
    "https://www.gobusiness.gov.sg/productivity-solutions-grant/#type-of-psg-soln",
    "https://www.gobusiness.gov.sg/business-grants-portal-faq/psg-general/",
    "https://www.gobusiness.gov.sg/productivity-solutions-grant/all-psg-solutions/",
    "https://www.gobusiness.gov.sg/browse-all-solutions-security/automated-visitor-management",
    "https://www.enterprisesg.gov.sg/financial-support/skillsfuture-enterprise-credit",
    "https://www.enterprisesg.gov.sg/resources/all-faqs/skillsfuture-enterprise-credit",
    "https://snef.org.sg/grants/ccp-so/",
    "https://conversion.mycareersfuture.gov.sg/Portal/ProgramDetails.aspx?ProgID=P00003120",
    "https://www.wsg.gov.sg/home/employers-industry-partners/workforce-development-job-redesign/security-productivity-initiative",
    "https://www.sbf.org.sg/what-we-do/skills-empowered/career-conversion-programme/CCP-HC",
    "https://snef.org.sg/grants/ccp-hcp/",
    "https://www.wsg.gov.sg/home/employers-industry-partners/workforce-development-job-redesign/support-for-job-redesign-under-productivity-solutions-grant",
    "https://snef.org.sg/grants/psgjr/",
    "https://www.imda.gov.sg/how-we-can-help/smes-go-digital/advanced-digital-solutions",
    "https://services2.imda.gov.sg/ctoaas/Category/ads_15/integrated-security-management--ism-",
    "https://www.e2i.com.sg/ctc/",
    "https://skillsfuture.gobusiness.gov.sg/support-and-programmes/skillsfuture-queen-bee-networks",
    "https://skillsfuture.gobusiness.gov.sg/support-and-programmes/skillsfuture-queen-bee-networks/sfqb-aetos",
    "https://www.aetos.com.sg/SFQB"
]

if __name__ == "__main__":
    embedding = get_embedding()
    refresh_vectorstore(urls_to_scrape)