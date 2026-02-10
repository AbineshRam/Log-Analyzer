from typing import Dict

from app.ai.rules import classify_log
from app.ai.llm import explain_failure


def analyze_job(
    stderr: str,
    stdout: str,
    exit_code: int
) -> Dict:
    """
    Main AI entry point for analyzing a single job failure.
    """

    # Step 1: Rule-based classification
    rule_result = classify_log(stderr, stdout, exit_code)

    category = rule_result["category"]
    confidence = rule_result["confidence"]

    # Step 2: LLM / static reasoning
    explanation = explain_failure(
        category=category,
        stderr=stderr,
        stdout=stdout,
        exit_code=exit_code,
        confidence=confidence
    )

    # Step 3: Unified response
    return {
        "category": category,
        "confidence": confidence,
        "exit_code": exit_code,
        "result": explanation
    }
