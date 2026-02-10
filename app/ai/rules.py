import re
from typing import Dict


ERROR_PATTERNS = {
    "Database Error": [
        r"ora-\d+",
        r"sqlstate",
        r"database.*error",
        r"connection.*refused",
        r"could not connect to database"
    ],
    "Memory Error": [
        r"out of memory",
        r"java\.lang\.outofmemoryerror",
        r"killed process",
        r"\boom\b"
    ],
    "File System Error": [
        r"no such file",
        r"permission denied",
        r"read-only file system",
        r"disk quota exceeded"
    ],
    "Network Error": [
        r"connection timed out",
        r"network is unreachable",
        r"temporary failure in name resolution",
        r"host unreachable"
    ],
    "Application Error": [
        r"exception",
        r"traceback",
        r"segmentation fault",
        r"nullpointerexception",
        r"core dumped"
    ]
}


def classify_log(
    stderr: str,
    stdout: str,
    exit_code: int
) -> Dict:
    """
    Classify job failure using deterministic rule-based logic.
    """

    combined_logs = f"{stderr}\n{stdout}".lower()

    # Success case
    if exit_code == 0:
        return {
            "category": "Success",
            "confidence": 100
        }

    # Pattern-based classification
    for category, patterns in ERROR_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, combined_logs):
                return {
                    "category": category,
                    "confidence": 85
                }

    # Exit-code-based fallback rules
    if exit_code == 137:
        return {
            "category": "Memory Error",
            "confidence": 90
        }

    if exit_code == 126 or exit_code == 127:
        return {
            "category": "Permission Error",
            "confidence": 80
        }

    if exit_code == 1:
        return {
            "category": "Application Error",
            "confidence": 70
        }

    # Unknown failure
    return {
        "category": "Unknown Error",
        "confidence": 50
    }
