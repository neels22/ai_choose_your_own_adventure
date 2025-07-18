

from typing import List, Optional
from datetime import datetime
import uuid
from fastapi import APIRouter, Depends, HTTPException,Cookie,Response,BackgroundTasks
from sqlalchemy.orm import Session

from db.database import get_db
from models.job_model import StoryJob
from schemas.job_schema import StoryJobCreate,StoryJobResponse

router = APIRouter(
    prefix="/jobs",
    tags=["jobs"],
)


@router.get("/{job_id}",response_model=StoryJobResponse)
def get_job_status(
    job_id:str,
    db:Session = Depends(get_db)
):
    job = db.query(StoryJob).filter(StoryJob.job_id == job_id).first()
    if not job:
        raise HTTPException(status_code=404,detail="Job not found")
    return job
