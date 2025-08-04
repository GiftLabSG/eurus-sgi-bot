from langchain.vectorstores import Chroma
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_openai import ChatOpenAI
from helper_functions.vectorstore import get_embedding, persist_directory

embedding = get_embedding()

# Load the LLM used for multi-query expansion
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def get_retriever(grant_filter=None):
    """
    Returns a retriever with optional grant-specific filtering.
    Uses MultiQueryRetriever to expand the query semantically.
    """
    db = Chroma(
        persist_directory=persist_directory,
        embedding_function=embedding
    )

    # Base retrieval setup
    search_kwargs = {
        "k": 7,
        "fetch_k": 30
    }

    # Apply metadata filter if provided
    if isinstance(grant_filter, list) and grant_filter:
        # Apply OR logic for multiple grant titles
        search_kwargs["filter"] = {
            "$or": [{"grant_title": title} for title in grant_filter]
        }
    elif isinstance(grant_filter, str) and grant_filter.strip():
        # Single string case
        search_kwargs["filter"] = {"grant_title": grant_filter}

    retriever = db.as_retriever(
        search_type="mmr",
        search_kwargs=search_kwargs
    )

    # Multi-query expansion
    multi_retriever = MultiQueryRetriever.from_llm(
        retriever=retriever,
        llm=llm
    )

    return multi_retriever