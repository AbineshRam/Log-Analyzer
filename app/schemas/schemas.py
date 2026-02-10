from typing import Optional, List, Dict
from datetime import datetime

from pydantic import BaseModel, Field


# =========================
# REQUEST SCHEMAS
# =========================

class JobLogRequest(BaseModel):
    job_name: str = Field(..., example="daily_etl_job")
    stderr: str = Field("", example="ORA-12541: TNS:no listener")
    stdout: str = Field("", example="Starting job...")
    exit_code: int = Field(..., example=1)


class BulkJobLogRequest(BaseModel):
    jobs: List[JobLogRequest]


# =========================
# AI ANALYSIS SCHEMAS
# =========================

class AnalysisResult(BaseModel):
    category: str
    confidence: int
    exit_code: int
    result: Dict


# =========================
# RESPONSE SCHEMAS
# =========================

class JobLogResponse(BaseModel):
    job_id: str
    job_name: str
    exit_code: int
    created_at: datetime


class JobAnalysisResponse(BaseModel):
    job_id: str
    analysis: AnalysisResult
    created_at: datetime


class FailureSummaryResponse(BaseModel):
    summary: str


# =========================
# GENERIC RESPONSE
# =========================

class MessageResponse(BaseModel):
    message: str
