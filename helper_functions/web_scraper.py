import os
import requests
from bs4 import BeautifulSoup
from langchain_core.documents import Document

def extract_grant_metadata(text):
    metadata = {}

    # Simple keyword checks for metadata extraction
    if "Enterprise Development Grant" in text:
        metadata = {
            "grant_title": "Enterprise Development Grant",
            "category": "Enterprise Development",
            "objective": "Support upgrading capabilities, innovation, and international expansion",
            "target": "Singapore-registered businesses with at least 30% local equity"
        }
    elif "Productivity Solutions Grant" in text or "PSG" in text:
        metadata = {
            "grant_title": "Productivity Solutions Grant",
            "category": "digitalisation and technology adoption",
            "objective": "Help SMEs adopt digital tools and subsidize adoption of pre-approved IT solutions and equipment",
            "target": "Singapore-registered SMEs with at least 30% local shareholding"
        }
    elif "SkillsFuture Enterprise Credit" in text or "SFEC" in text:
        metadata = {
            "grant_title": "SkillsFuture Enterprise Credit",
            "category": "training",
            "objective": "Subsidize transformation and workforce upgrading",
            "target": "Eligible local employers"
        }
    elif "Career Conversion Programme for Security Officers" in text or "CCP" in text:
        metadata = {
            "grant_title": "Career Conversion Programme for Security Officers",
            "category": "workforce transformation",
            "objective": "Support security employers in reskilling security officers to meet evolving business requirements, such as technology adoption and Outcome-Based Contracts",
            "target": "Singapore-registered security employers and their security officers"
        }
    elif "Career Conversion Programme for Human Capital Professionals" in text or "CCP-HC" in text:
        metadata = {
            "grant_title": "Career Conversion Programme for Human Capital Professionals",
            "category": "workforce transformation",
            "objective": "Support employers in equipping and converting local mid-career PMETs into Human Resource roles",
            "target": "Singapore-registered companies and their potential new hires"
        }
    elif "Job Redesign under Productivity Solutions Grant" in text or "PSG-JR" in text:
        metadata = {
            "grant_title": "Job Redesign under Productivity Solutions Grant",
            "category": "process improvement",
            "objective": "Encourage redesign of work processes to enhance productivity",
            "target": "Singapore-registered enterprises"
        }
    elif "Advanced Digital Solutions Grant" in text or "ADS" in text:
        metadata = {
            "grant_title": "Advanced Digital Solutions Grant",
            "category": "digital transformation",
            "objective": "Support SMEs in adopting advanced and integrated digital solutions to deepen digital capabilities and build resilience",
            "target": "Singapore-registered SMEs"
        }
    elif "Company Training Committee Grant" in text or "CTC" in text:
        metadata = {
            "grant_title": "Company Training Committee Grant",
            "category": "workforce transformation",
            "objective": "Support companies implementing transformation plans to raise productivity, redesign jobs, and upskill workers",
            "target": "Singapore-registered entities with established CTCs"
        }
    elif "SkillsFuture Queen Bee by AETOS" in text or "SFQB" in text:
        metadata = {
            "grant_title": "SkillsFuture Queen Bee by AETOS",
            "category": "skills development",
            "objective": "Leverage industry leaders like AETOS to provide skills training and development for SMEs in security sector",
            "target": "Singapore-registered SMEs in security industry"
        }
    else:
        metadata = {
            "grant_title": "Unknown",
            "category": "general",
            "objective": "Not specified",
            "target": "Not specified"
        }

    return metadata

def extract_filename_from_url(url):
    # Sanitize URL to filename friendly string
    return url.replace("https://", "").replace("http://", "").replace("/", "_").replace("?", "_").replace(":", "_").replace("#", "_")

def scrape_and_clean(url, url_metadata_map=None):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Referer": "https://www.google.com/"
        }

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise if status code is bad
        soup = BeautifulSoup(response.text, "html.parser")

        # Remove unwanted tags to clean text
        for tag in soup(["script", "style", "header", "footer", "nav", "form"]):
            tag.decompose()

        text = soup.get_text(separator="\n")
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        clean_text = "\n".join(lines)

        metadata = extract_grant_metadata(clean_text)
        metadata["source"] = url

        # Override grant_title if url_metadata_map provided and url found
        if url_metadata_map and url in url_metadata_map:
            metadata["grant_title"] = url_metadata_map[url]

        # Save raw scraped content
        os.makedirs("data/scraped_pages", exist_ok=True)
        filename = extract_filename_from_url(url)
        with open(f"data/scraped_pages/{filename}.txt", "w", encoding="utf-8") as f:
            f.write(clean_text)

        print(f"✅ Scraped and saved: {url}")
        return Document(page_content=clean_text, metadata=metadata)

    except Exception as e:
        print(f"❌ Failed to scrape {url}: {e}")
        return None