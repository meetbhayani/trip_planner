# tools/search_tools.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

SERPER_URL = "https://google.serper.dev/search"

def search_internet(query: str, max_results: int = 4, timeout: int = 10) -> str:
    """
    Use serper.dev to run a web search. Returns concatenated title/link/snippet results.
    If SERPER_API_KEY is missing or request fails, returns an explanatory string.
    """
    api_key = os.environ.get("SERPER_API_KEY")
    if not api_key:
        return "Search not available: SERPER_API_KEY not set."

    try:
        headers = {"X-API-KEY": api_key, "Content-Type": "application/json"}
        resp = requests.post(SERPER_URL, headers=headers, json={"q": query}, timeout=timeout)
        resp.raise_for_status()
        data = resp.json()
        organic = data.get("organic", [])[:max_results]
        if not organic:
            return "No search results found."
        out = []
        for r in organic:
            title = r.get("title","No title")
            link = r.get("link","No link")
            snippet = r.get("snippet","")
            out.append(f"Title: {title}\nLink: {link}\nSnippet: {snippet}")
        return "\n\n".join(out)
    except requests.RequestException as e:
        return f"Search error: network issue ({str(e)})"
    except Exception as e:
        return f"Search error: {str(e)}"
