import os
import requests
from typing import Dict

# =========================================================
# CONFIGURATION
# =========================================================

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama")
# allowed values: openai | ollama

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")

CONFIDENCE_THRESHOLD = int(os.getenv("CONFIDENCE_THRESHOLD", 80))


# =========================================================
# PUBLIC API
# =========================================================

def explain_failure(
    category: str,
    stderr: str,
    stdout: str,
    exit_code: int,
    confidence: int
) -> Dict:
    """
    Entry point for AI reasoning.
    Uses LLM only if rule-based confidence is below threshold.
    """

    # High confidence → no LLM needed
    if confidence >= CONFIDENCE_THRESHOLD:
        return _static_explanation(category, exit_code)

    prompt = _build_prompt(category, stderr, stdout, exit_code)

    if LLM_PROVIDER == "openai":
        return _openai_explain(prompt, category, exit_code)

    if LLM_PROVIDER == "ollama":
        return _ollama_explain(prompt, category, exit_code)

    raise ValueError(f"Unsupported LLM provider: {LLM_PROVIDER}")


# =========================================================
# PROMPT ENGINEERING
# =========================================================

def _build_prompt(category: str, stderr: str, stdout: str, exit_code: int) -> str:
    return f"""
You are a senior production support engineer.

Job Exit Code: {exit_code}
Detected Category: {category}

STDERR:
{stderr}

STDOUT:
{stdout}

Tasks:
1. Explain clearly why the job failed
2. Identify the most likely root cause
3. Suggest concrete remediation steps

Respond in a concise, professional tone.
"""


# =========================================================
# OPENAI IMPLEMENTATION
# =========================================================

def _openai_explain(prompt: str, category: str, exit_code: int) -> Dict:
    import openai

    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY is not set")

    openai.api_key = OPENAI_API_KEY

    response = openai.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": "You analyze batch job failures."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )

    content = response.choices[0].message.content

    return _format_response(category, exit_code, content)


# =========================================================
# OLLAMA IMPLEMENTATION (LOCAL LLaMA)
# =========================================================

def _ollama_explain(prompt: str, category: str, exit_code: int) -> Dict:
    response = requests.post(
        f"{OLLAMA_BASE_URL}/api/generate",
        json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
        },
        timeout=60,
    )

    response.raise_for_status()
    content = response.json().get("response", "")

    return _format_response(category, exit_code, content)


# =========================================================
# STATIC FALLBACK (NO LLM)
# =========================================================

def _static_explanation(category: str, exit_code: int) -> Dict:
    return {
        "category": category,
        "exit_code": exit_code,
        "analysis": f"The job failed due to {category}.",
        "remediation": "Review logs and apply standard corrective actions.",
        "llm_used": False
    }


# =========================================================
# RESPONSE NORMALIZER
# =========================================================

def _format_response(category: str, exit_code: int, content: str) -> Dict:
    return {
        "category": category,
        "exit_code": exit_code,
        "analysis": content.strip(),
        "llm_used": True
    }
