from pydantic import BaseModel
from typing import Optional, List

# --- User Schemas ---
class UserBase(BaseModel):
    username: str
    role: str

class UserCreate(UserBase):
    password: str

class ShowUser(UserBase):
    id: int
    is_active: bool
    tasks: List["ShowTask"] = []

    class Config():
        orm_mode = True

# --- Task Schemas ---
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    platform: str
    is_urgent: bool = False

class TaskCreate(TaskBase):
    pass

class ShowTask(TaskBase):
    id: int
    status: str
    creator_id: int
    creator: ShowUser

    class Config():
        orm_mode = True
        
# --- Token Schemas for Login ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class Login(BaseModel):
    username: str
    password: str
