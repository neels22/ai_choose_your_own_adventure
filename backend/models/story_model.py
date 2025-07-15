from sqlalchemy import Column, Integer, String, JSON, ForeignKey,DateTime,Boolean

from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


from db.database import Base

class Story(Base):
    __tablename__ = "stories"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    session_id = Column(String, index=True) # every user has unique session id to track their seesions
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    nodes = relationship("StoryNode", back_populates="story")
    
    # relationship to story node one story connected to multiple nodes
    # one to many relationship
    # back populates to related all story so that we know to which story node belongs to 


class StoryNode(Base):
    __tablename__ = "story_nodes"

    id = Column(Integer, primary_key=True, index=True)
    story_id = Column(Integer, ForeignKey("stories.id"),index=True)
    content = Column(String, index=True)
    is_root = Column(Boolean, default=False)
    is_ending = Column(Boolean, default=False)
    is_winning_ending = Column(Boolean, default=False)
    options = Column(JSON,default=list)

    story = relationship("Story", back_populates="nodes")




    
    
    
    



