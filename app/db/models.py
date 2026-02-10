from datetime import datetime
from typing import Dict, List, Optional

from pymongo.collection import Collection

from app.db.database import get_db


# =========================
# COLLECTION GETTERS
# =========================

def job_logs_collection() -> Collection:
    return get_db()["job_logs"]


def analysis_collection() -> Collection:
    return get_db()["job_analysis"]


# =========================
# JOB LOG OPERATIONS
# =========================

def save_job_log(
    job_name: str,
    stderr: str,
    stdout: str,
    exit_code: int
) -> str:
    """
    Store raw job execution logs
    """
    doc = {
        "job_name": job_name,
        "stderr": stderr,
        "stdout": stdout,
        "exit_code": exit_code,
        "created_at": datetime.utcnow()
    }

    result = job_logs_collection().insert_one(doc)
    return str(result.inserted_id)


def get_job_log(job_id: str) -> Optional[Dict]:
    """
    Fetch a job log by ID
    """
    return job_logs_collection().find_one({"_id": job_id})


# =========================
# AI ANALYSIS OPERATIONS
# =========================

def save_analysis(
    job_id: str,
    analysis_result: Dict
) -> str:
    """
    Store AI analysis output
    """
    doc = {
        "job_id": job_id,
        "analysis": analysis_result,
        "created_at": datetime.utcnow()
    }

    result = analysis_collection().insert_one(doc)
    return str(result.inserted_id)


def get_analysis(job_id: str) -> Optional[Dict]:
    """
    Fetch AI analysis for a job
    """
    return analysis_collection().find_one({"job_id": job_id})


def list_recent_failures(limit: int = 20) -> List[Dict]:
    """
    List recent failed jobs
    """
    cursor = job_logs_collection().find(
        {"exit_code": {"$ne": 0}}
    ).sort("created_at", -1).limit(limit)

    return list(cursor)
