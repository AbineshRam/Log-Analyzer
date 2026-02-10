from typing import Dict


def read_log_file(file_path: str) -> str:
    """
    Safely read a log file.
    Returns empty string if file cannot be read.
    """

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except Exception:
        return ""


def parse_logs(
    stdout_path: str | None = None,
    stderr_path: str | None = None
) -> Dict:
    """
    Parse stdout and stderr logs.

    Returns:
    {
        "stdout": str,
        "stderr": str
    }
    """

    stdout = read_log_file(stdout_path) if stdout_path else ""
    stderr = read_log_file(stderr_path) if stderr_path else ""

    return {
        "stdout": stdout.strip(),
        "stderr": stderr.strip()
    }
