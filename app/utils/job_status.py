from typing import Dict


def get_job_status(exit_code: int) -> Dict:
    """
    Normalize job status based on exit code.
    """

    if exit_code == 0:
        return {
            "status": "SUCCESS",
            "exit_code": 0
        }

    return {
        "status": "FAILED",
        "exit_code": exit_code
    }
