from pydantic import BaseModel
from typing import Optional

# --- 这是用户相关的尺寸定义 ---
class UserBase(BaseModel):
    username: str
    role: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        from_attributes = True

# --- 这是我们新补上的、任务相关的尺寸定义！ ---
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    platform: str
    is_urgent: bool = False

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    status: str
    created_at: str # 我们让它返回字符串，前端处理更简单

    class Config:
        from_attributes = True

# --- 登录相关的尺寸定义 ---
class Login(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
