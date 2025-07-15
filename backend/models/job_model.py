


# reason we need to have job model 
# flow is gonna be here is when request is submitted 
# job is gonna represented intent like progress of job or status of job

# completed or failed or in progress 
# status it is kept on checking 

# when you have longer operations on backend we dont want frontend to wait or backend to wait before we can send response

# flow is 
# frontend - job
# backend  - returns job

# frontend - ask if job is done 
# backed - return status

# if job is done backend can send story 



from sqlalchemy import Column, Integer, String, JSON, ForeignKey,DateTime,Boolean

from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


from db.database import Base

class StoryJob(Base):
    __tablename__ = "story_jobs"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String, index=True,unique=True)
    session_id = Column(String, index=True)
    theme = Column(String)
    status = Column(String)
    story_id = Column(Integer, nullable=True)
    error = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)







    