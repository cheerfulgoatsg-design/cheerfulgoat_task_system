from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# --- 1. 基础配置与安全设置 ---
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "Goat2026!")
SECRET_KEY = os.getenv("SECRET_KEY", "cheerful-goat-secret-key-2026")

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# 允许跨域访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 2. 数据库配置 ---
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class TaskModel(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    platform = Column(String)
    description = Column(String, nullable=True)
    is_urgent = Column(Boolean, default=False)
    status = Column(String, default="待处理")
    deadline = Column(DateTime, nullable=True)

# 这里是系统自动在数据库里建表的地方
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- 3. 登录逻辑 ---
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # 检查用户名和密码
    if form_data.username == ADMIN_USERNAME and form_data.password == ADMIN_PASSWORD:
        return {"access_token": "cheerful-goat-token-fixed", "token_type": "bearer"}
    raise HTTPException(status_code=400, detail="用户名或密码错误")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    if token != "cheerful-goat-token-fixed":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="无效证件")
    return ADMIN_USERNAME

# --- 4. 任务管理接口 ---
class TaskCreate(BaseModel):
    title: str
    platform: str
    description: Optional[str] = None
    is_urgent: bool = False
    deadline: Optional[datetime] = None

@app.get("/tasks/")
def read_tasks(db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    return db.query(TaskModel).all()

@app.post("/tasks/")
def create_task(task: TaskCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db_task = TaskModel(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@app.put("/tasks/{task_id}/status")
def update_status(task_id: int, new_status: str, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db_task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="任务未找到")
    db_task.status = new_status
    db.commit()
    return db_task
# --- 在代码最末尾添加这个“删除”接口 ---

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db_task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="任务未找到")
    db.delete(db_task)
    db.commit()
    return {"message": "任务已成功删除"}
