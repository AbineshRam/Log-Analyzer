from typing import List, Dict

from app.ai.llm import explain_failure


def summarize_failures(failures: List[Dict]) -> Dict:
    """
    Summarize multiple job failures using LLM reasoning.

    Each failure dict is expected to contain:
    - stderr
    - stdout
    - exit_code
    """

    if not failures:
        return {
            "summary": "No failures available for summarization.",
            "llm_used": False
        }

    analyses = []

    for failure in failures:
        stderr = failure.get("stderr", "")
        stdout = failure.get("stdout", "")
        exit_code = failure.get("exit_code", -1)

        # Force LLM usage by passing low confidence
        explanation = explain_failure(
            category="Multiple Job Failures",
            stderr=stderr,
            stdout=stdout,
            exit_code=exit_code,
            confidence=0
        )

        analysis_text = explanation.get("analysis")
        if analysis_text:
            analyses.append(analysis_text)

    if not analyses:
        return {
            "summary": "Failures detected but no meaningful analysis could be generated.",
            "llm_used": True
        }

    combined_summary = "\n\n---\n\n".join(analyses)

    return {
        "summary": combined_summary,
        "llm_used": True
    }
