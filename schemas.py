from pydantic import BaseModel
from typing import Optional
from datetime import datetime # <--- 我们导入了 datetime 工具

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

# --- 这是任务相关的尺寸定义 ---
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
    # --- 看！这是我们最终的、决定性的修改！---
    # 我们不再要求它是字符串，而是直接接受 datetime 对象
    created_at: datetime 

    class Config:
        # orm_mode = True 在 Pydantic V2 中被重命名为 from_attributes = True
        # 这个配置会自动帮助我们把数据库对象，转换成符合规范的 JSON！
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
