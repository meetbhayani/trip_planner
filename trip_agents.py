# agents.py
from langchain_community.llms import Ollama
import os

# Create a single LLM factory function so we can change model or params centrally.
def create_llm(model_name: str = "gemma:2b", temperature: float = 0.7, max_tokens: int = 512):
    """
    Returns an Ollama LLM wrapper instance.
    NOTE: depending on your installed langchain_community version, you might need to
    call .generate(...) or .predict(...) instead of calling the object directly.
    """
    llm = Ollama(model=model_name, temperature=temperature, num_predict=max_tokens)
    return llm

def call_llm(prompt: str, model_name: str = "gemma:2b", temperature: float = 0.7, max_tokens: int = 512) -> str:
    llm = create_llm(model_name=model_name, temperature=temperature, max_tokens=max_tokens)
    # Many LLM wrappers support calling the instance to get a result:
    try:
        # Preferred: call the llm like a function
        resp = llm(prompt)
        # If the wrapper returns an object, convert to string explicitly
        if isinstance(resp, str):
            return resp
        try:
            return str(resp)
        except Exception:
            return resp.__repr__()
    except TypeError:
        # Fallback: many wrappers implement `.generate` or `.predict`
        if hasattr(llm, "generate"):
            out = llm.generate([prompt])
            # try to extract text
            try:
                return out.generations[0][0].text
            except Exception:
                return str(out)
        if hasattr(llm, "predict"):
            return llm.predict(prompt)
        raise
