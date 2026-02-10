from fastapi import APIRouter, HTTPException
from datetime import datetime
from typing import List

from app.ai.engine import analyze_job
from app.ai.summarizer import summarize_failures
from app.schemas.schemas import (
    JobLogRequest,
    BulkJobLogRequest,
    JobAnalysisResponse,
    FailureSummaryResponse,
)

router = APIRouter(prefix="/api", tags=["Log Analyzer"])


# =========================
# HEALTH CHECK
# =========================

@router.get("/health")
def health_check():
    return {"status": "ok", "timestamp": datetime.utcnow()}


# =========================
# SINGLE JOB ANALYSIS
# =========================

@router.post("/analyze", response_model=JobAnalysisResponse)
def analyze_job_log(payload: JobLogRequest):
    """
    Analyze a single job failure log.
    """

    try:
        analysis = analyze_job(
            stderr=payload.stderr,
            stdout=payload.stdout,
            exit_code=payload.exit_code
        )

        return {
            "job_id": f"{payload.job_name}-{int(datetime.utcnow().timestamp())}",
            "analysis": analysis,
            "created_at": datetime.utcnow()
        }

    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


# =========================
# BULK FAILURE SUMMARY
# =========================

@router.post("/summarize", response_model=FailureSummaryResponse)
def summarize_job_failures(payload: BulkJobLogRequest):
    """
    Summarize multiple job failures using LLM.
    """

    try:
        failures = [
            {
                "stderr": job.stderr,
                "stdout": job.stdout,
                "exit_code": job.exit_code
            }
            for job in payload.jobs
        ]

        summary = summarize_failures(failures)

        return summary

    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
