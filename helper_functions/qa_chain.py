from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from helper_functions.retriever import get_retriever
from langchain_openai import ChatOpenAI
from difflib import get_close_matches

# Load the LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Step 1: Detect grant type from user input
def detect_grant_from_question(question: str) -> str | None:
    normalized = " ".join(question.lower().split())
    keywords = {
        "sfec": "SkillsFuture Enterprise Credit",
        "skillsfuture enterprise credit": "SkillsFuture Enterprise Credit",
        "skills future enterprise credit": "SkillsFuture Enterprise Credit",

        "sfqb": "SkillsFuture Queen Bee by AETOS",
        "skillsfuture queen bee": "SkillsFuture Queen Bee by AETOS",
        "skills future queen bee": "SkillsFuture Queen Bee by AETOS",

        "psg": "Productivity Solutions Grant",
        "productivity solutions grant": "Productivity Solutions Grant",

        "edg": "Enterprise Development Grant",
        "enterprise development grant": "Enterprise Development Grant",

        "ads": "Advanced Digital Solutions Grant",
        "advanced digital solution": "Advanced Digital Solutions Grant",
        "advanced digital solution grant": "Advanced Digital Solutions Grant",
        "advanced digital solutions grant": "Advanced Digital Solutions Grant",

        "ccp so": "Career Conversion Programme for Security Officers",
        "ccp sos": "Career Conversion Programme for Security Officers",
        "ccp for so": "Career Conversion Programme for Security Officers",
        "ccp for sos": "Career Conversion Programme for Security Officers",
        "ccp for security officers": "Career Conversion Programme for Security Officers",
        "career conversion programme for security officers": "Career Conversion Programme for Security Officers",

        "ccp hc": "Career Conversion Programme for Human Capital Professionals",
        "ccp for hc": "Career Conversion Programme for Human Capital Professionals",
        "ccp hcp": "Career Conversion Programme for Human Capital Professionals",
        "ccp for hcp": "Career Conversion Programme for Human Capital Professionals",
        "career conversion programme for human capital": "Career Conversion Programme for Human Capital Professionals",
        "career conversion programme for human capital professionals": "Career Conversion Programme for Human Capital Professionals",

        "ctc": "Company Training Committee Grant",
        "ctc grant": "Company Training Committee Grant",
        "company training committee": "Company Training Committee Grant",
        "company training committee grant": "Company Training Committee Grant"
    }

    # 🔍 Step 1: Direct match
    for key, grant in keywords.items():
        if key in normalized:
            return grant

    # 🔍 Step 2: Fuzzy match
    possible_keys = list(keywords.keys())
    close_matches = get_close_matches(normalized, possible_keys, n=1, cutoff=0.8)
    if close_matches:
        return keywords[close_matches[0]]

    # 🧠 Step 3: Intent-based detection
    if any(term in normalized for term in [
        "reskill hr", "reskill my hr", "upskill my hr", "upskill hr", "train hr", "train my hr", "hr transformation", "upskill my staff", "train human resource"
    ]):
        return "Career Conversion Programme for Human Capital Professionals"
    
    if any(term in normalized for term in [
        "reskill my security officer", "reskill my security officers", "upskill my security officer", "upskill my security officers", "security upskill", "train my security officer", "train my security officers", "security training"
    ]):
        return "Career Conversion Programme for Security Officers"

    return None

grant_to_keywords = {
    "SkillsFuture Enterprise Credit": ["sfec", "skillsfuture enterprise credit", "skills future enterprise credit"],
    "SkillsFuture Queen Bee by AETOS": ["sfqb", "skillsfuture queen bee", "skills future queen bee"],
    "Productivity Solutions Grant": ["psg", "productivity solutions grant"],
    "Enterprise Development Grant": ["edg", "enterprise development grant"],
    "Advanced Digital Solutions Grant": [
        "ads", "advanced digital solution", "advanced digital solution grant", "advanced digital solutions grant"
    ],
    "Career Conversion Programme for Security Officers": [
        "ccp so", "ccp sos", "ccp for so", "ccp for sos",
        "ccp for security officers", "career conversion programme for security officers"
    ],
    "Career Conversion Programme for Human Capital Professionals": [
        "ccp hc", "ccp for hc", "ccp hcp", "ccp for hcp",
        "career conversion programme for human capital",
        "career conversion programme for human capital professionals"
    ],
    "Company Training Committee Grant": [
        "ctc", "ctc grant", "company training committee", "company training committee grant"
    ]
}

# Step 2: Define the prompt
prompt_template = """You are a knowledgeable grant advisor.

Answer based ONLY on the context below. Use ONLY the provided documents to answer the question.
Do not hallucinate or include unrelated grant details.

If the user does not specify a grant but asks about workforce upgrading, upskilling, reskilling, or HR development, you may suggest a relevant grant such as the Career Conversion Programme for Human Capital Professionals or Security Officers, based on context.

Format your answer clearly:

Grant Description:
{{Brief summary}}

Eligibility Criteria:
{{Who is eligible (use bullet points)}}

Application Steps:
{{Extract any relevant process, eligibility requirements, funding procedures, or contact details for applying, even if not explicitly labeled as "application steps". (use bullet points). If truly no process is mentioned, say "Not found in documents."}}

Context:
{context}

Question:
{question}

Answer:"""

prompt = PromptTemplate(
    template=prompt_template,
    input_variables=["context", "question"]
)

abbr_to_full = {
    "ads": "Advanced Digital Solutions Grant",
    "advanced digital solution": "Advanced Digital Solutions Grant",
    "advanced digital solutions grant": "Advanced Digital Solutions Grant",
    
    "ctc": "Company Training Committee Grant",
    "company training committee grant": "Company Training Committee Grant",
    
    "psg": "Productivity Solutions Grant",
    "productivity solutions grant": "Productivity Solutions Grant",
    
    "edg": "Enterprise Development Grant",
    "enterprise development grant": "Enterprise Development Grant",
    
    "sfqb": "SkillsFuture Queen Bee by AETOS",
    "skillsfuture queen bee": "SkillsFuture Queen Bee by AETOS",
    "skills future queen bee": "SkillsFuture Queen Bee by AETOS",
    
    "sfec": "SkillsFuture Enterprise Credit",
    "skillsfuture enterprise credit": "SkillsFuture Enterprise Credit",
    "skills future enterprise credit": "SkillsFuture Enterprise Credit",
}

def normalize_and_map(grant_name):
    normalized = " ".join(grant_name.lower().split())
    return abbr_to_full.get(normalized, grant_name)

def find_complementary_grant(docs, detected_grant):
    detected_grant_full = normalize_and_map(detected_grant)

    complements = {
        "Advanced Digital Solutions Grant": "Career Conversion Programme for Security Officers",
        "Company Training Committee Grant": "Career Conversion Programme for Security Officers",
        "Productivity Solutions Grant": "Career Conversion Programme for Security Officers",
        "Enterprise Development Grant": "SkillsFuture Enterprise Credit",
        "SkillsFuture Queen Bee by AETOS": "Career Conversion Programme for Security Officers",
        "Career Conversion Programme for Security Officers": "Company Training Committee Grant",
        "SkillsFuture Enterprise Credit": "Productivity Solutions Grant",
        "Career Conversion Programme for Human Capital Professionals": "SkillsFuture Enterprise Credit"
    }

    if detected_grant_full in complements:
        paired = complements[detected_grant_full]
        reason = f"This grant complements the objectives of the {detected_grant_full}."
        return f"\n\n### 🔄 Complementary Grant Suggestion:\n- **{paired}**: {reason}"

    # 🔄 Fallback to category/objective matching
    detected_metadata = next((doc.metadata for doc in docs if doc.metadata.get("title", "").lower() == detected_grant_full.lower()), {})
    for doc in docs:
        title = doc.metadata.get("title", "")
        if title.lower() == detected_grant_full.lower():
            continue

        category = doc.metadata.get("category", "").lower()
        objective = doc.metadata.get("objective", "").lower()

        if (detected_metadata.get("category", "").lower() in category) or \
           (detected_metadata.get("objective", "").lower() in objective):

            reason = f"Complementary grant related to {category or objective}."
            return f"\n\n### 💡 Complementary Grant Suggestion:\n- **{title}**: {reason}"

    return complements.get(detected_grant_full, "")  # Returns "" if no complement found

# Step 3: Build QA chain with metadata filter
def build_qa_chain(question: str):
    grant_title = detect_grant_from_question(question)
    retriever = get_retriever(grant_filter=grant_title if grant_title else None)
    
    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt}
    )

# Step 4: Query and format response
def get_final_response(question: str) -> str:
    detected_grant = detect_grant_from_question(question)
    normalized = question.lower()

    if not detected_grant and any(word in normalized for word in [
        "security agency", "security agencies", "security firm", "security company",
        "security officer", "security offiers", "security", "list of grants"
    ]):
        return (
            "Based on your interest in grants for security agencies, here are some relevant options:\n\n"
            "- **Career Conversion Programme (CCP) for Security Officers** - Reskills security officers for tech-driven roles.\n"
            "- **Productivity Solutions Grant (PSG)** - Funds security-related tech like surveillance, smart dashboards, etc.\n"
            "- **Company Training Committee (CTC) Grant** - Supports structured job redesign and training initiatives.\n\n"
            "- **SkillsFuture Enterprise Credit (SFEC)** - Offsets enterprise and workforce transformation costs with up to $10,000 in credits.\n"
            "- **SkillsFuture Queen Bee (SFQB) by AETOS** - Provides industry-led support to upskill security SMEs and drive digital adoption.\n"
            "- **Enterprise Development Grant (EDG)** - Funds projects in innovation, productivity improvement, and business expansion.\n"
            "- **Advanced Digital Solutions (ADS) Grant)** - Supports adoption of integrated digital solutions for enhanced operations.\n"
            "- **Career Conversion Programme (CCP) for Human Capital Professionals** - Equips mid-career professionals to take on HR roles within sectors like security.\n\n"
            "You can ask about any of these grants specifically to get full details including eligibility and how to apply."
        )

    try:
        qa_chain = build_qa_chain(question)
        result = qa_chain({"query": question})
        final_answer = result.get("result", "").strip()
        docs = result.get("source_documents", [])

        fallback_phrases = [
            "i don't know", "not found in documents", "no relevant",
            "sorry", "cannot answer", "unable to find"
        ]

        # 🔧 NEW: Trigger fallback if poor result
        if not final_answer or any(phrase in final_answer.lower() for phrase in fallback_phrases) or not docs:
            return (
                "❗ Sorry, I couldn't find a suitable answer to your question.\n\n"
                "If you're looking for training or workforce upgrading support, "
                "you might consider grants such as:\n\n"
                "- **Career Conversion Programme (CCP) for Security Officers**\n"
                "- **Company Training Committee Grant (CTC)**\n"
                "- **Productivity Solutions Grant (PSG)**\n\n"
                "📬 For more help, you can contact **WSG_Biz_Services@wsg.gov.sg** or "
                "[fill out this form](https://go.gov.sg/contact-form)."
            )

        sources = sorted({
            src for doc in docs if (src := doc.metadata.get("source", "")).startswith("http")
        })
        sources_str = "\n".join(f"- {src}" for src in sources)

        suggestion = find_complementary_grant(docs, detected_grant) if detected_grant else ""

        return f"{final_answer}{suggestion}\n\n### 🔗 Sources:\n{sources_str or 'No sources found.'}"

    # 🛠️ Catch-all error handler
    except Exception:
        return (
            "❗ Sorry, I couldn't find a suitable answer to your question.\n\n"
            "If you're looking for training or workforce upgrading support, "
            "you might consider grants such as:\n\n"
            "- **Career Conversion Programme (CCP) for Security Officers**\n"
            "- **Company Training Committee Grant (CTC)**\n"
            "- **Productivity Solutions Grant (PSG)**\n\n"
            "📬 For more help, you can contact **WSG_Biz_Services@wsg.gov.sg** or "
            "[fill out this form](https://go.gov.sg/contact-form)."
        )