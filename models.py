from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean, func
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default='colleague', nullable=False) # admin, leader, colleague
    tasks_created = relationship("Task", back_populates="creator")

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    platform = Column(String, nullable=False) # 亚马逊, tiktok, 独立站, 虾皮, 国内, b端, 杂项
    is_urgent = Column(Boolean, default=False)
    status = Column(String, default='pending', nullable=False) # pending, in_progress, completed, archived, rejected
    created_at = Column(DateTime, server_default=func.now())
    deadline = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, onupdate=func.now())
    creator_id = Column(Integer, ForeignKey('users.id'))
    creator = relationship("User", back_populates="tasks_created")
    approval_comment = Column(Text)
