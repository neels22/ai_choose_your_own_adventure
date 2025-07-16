

from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


class StoryJobBase(BaseModel):
    theme:str


class StoryJobResponse(BaseModel):
    job_id:str
    status:str
    created_at:datetime
    story_id:Optional[int] = None
    completed_at:Optional[datetime] = None
    error:Optional[str] = None

    class Config:
        from_attributes = True


# usingg this for specifies this gonna be use for request 
# in code little bit easier to understand meaning of it 
# useing it for ingesting data
class StoryJobCreate(StoryJobBase):
    pass

