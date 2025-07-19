
from typing import List, Optional
from datetime import datetime
import uuid
from fastapi import APIRouter, Depends, HTTPException,Cookie,Response,BackgroundTasks
from sqlalchemy.orm import Session

from db.database import get_db, SessionLocal
from models.story_model import Story,StoryNode
from models.job_model import StoryJob
from schemas.story_schema import CreateStoryRequest,CompleteStoryResponse,CompleteStoryNodeResponse
from schemas.job_schema import StoryJobCreate,StoryJobResponse
from core.story_generator import StoryGenerator

router = APIRouter(
    prefix="/stories",
    tags=["stories"],
)


# a session will identify browser 
# a session can expire after certain amount of time but they cazn store info such that website can remember user 
# we get session id from cookies and identify browser session 
def get_session_id(session_id:Optional[str] = Cookie(None)):
    if not session_id:
        session_id = str(uuid.uuid4())
    return session_id


# what is depends function in fastapi???
# it will grab the value of session id or db and inject into those variables if the route is hit
@router.post("/create",response_model=StoryJobResponse)
def create_story(
    request:CreateStoryRequest,
    background_tasks:BackgroundTasks,
    response:Response,
    session_id:str = Depends(get_session_id),
    db:Session = Depends(get_db)
):
    response.set_cookie(key="session_id",value=session_id,httponly=True)# store our session id to use later 
    # create story -- create job -- 
    job_id = str(uuid.uuid4())
    job = StoryJob(
        job_id=job_id,
        session_id=session_id,
        theme=request.theme,
        status="pending",

    )
    db.add(job)
    db.commit()
    
    #TODO : add background task to generate story 
    background_tasks.add_task(
        generate_story_task,
        job_id=job_id,
        session_id=session_id,
        theme=request.theme,
    )

    return job





def generate_story_task(job_id:str,session_id:str,theme:str):
    db = SessionLocal()
    try:
        job = db.query(StoryJob).filter(StoryJob.job_id == job_id).first()
        if not job:
            return {"error":"Job not found"}
        try:
            job.status = "processing"
            db.commit()
            story = StoryGenerator.generate_story(db,session_id,theme) #TODO : generate story 
            job.story_id = story.id # TODO: update story id 
            job.status = "completed"
            job.completed_at = datetime.now()
            db.commit()
        except Exception as e:
            job.status = "Failed"
            job.completed_at = datetime.now()
            job.error = str(e)
            db.commit()
    finally:
        db.close()


@router.get("/{story_id}/complete",response_model=CompleteStoryResponse)
def get_complete_story(
    story_id:int,
    db:Session = Depends(get_db)
):
    story = db.query(Story).filter(Story.id == story_id).first()
    if not Story:
        raise HTTPException(status_code=404,detail="Story not found")
    

    complete_story = build_complete_story_tree(db,story)
    return complete_story


############### what is this function doing???

def build_complete_story_tree(db: Session, story: Story) -> CompleteStoryResponse:
    nodes = db.query(StoryNode).filter(StoryNode.story_id == story.id).all()

    node_dict = {}
    for node in nodes:
        node_response = CompleteStoryNodeResponse(
            id=node.id,
            content=node.content,
            is_ending=node.is_ending,
            is_winning_ending=node.is_winning_ending,
            options=node.options
        )
        node_dict[node.id] = node_response

    root_node = next((node for node in nodes if node.is_root), None)
    if not root_node:
        raise HTTPException(status_code=500, detail="Story root node not found")

    return CompleteStoryResponse(
        id=story.id,
        title= story.title,
        session_id=story.session_id,
        created_at=story.created_at,
        root_node=node_dict[root_node.id],
        all_nodes=node_dict
    )