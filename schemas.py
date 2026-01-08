from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# --- 用户相关的定义 ---
class UserBase(BaseModel):
    username: str
    role: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    class Config:
        from_attributes = True

# --- 任务相关的定义 ---
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    platform: str
    is_urgent: bool = False
    # --- 看！我们在这里加了截止日期这一行 ---
    deadline: Optional[datetime] = None 

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    status: str
    created_at: datetime
    class Config:
        from_attributes = True

# --- 登录相关的定义 ---
class Login(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
