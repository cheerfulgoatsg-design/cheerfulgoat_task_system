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

# --- 1. 基础配置 ---
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "Goat2026!")
SECRET_KEY = os.getenv("SECRET_KEY", "cheerful-goat-secret-key-2026")

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 2. 数据库配置（防断线版） ---
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_recycle=300)
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
    if form_data.username == ADMIN_USERNAME and form_data.password == ADMIN_PASSWORD:
        return {"access_token": "cheerful-goat-token-fixed", "token_type": "bearer"}
    raise HTTPException(status_code=400, detail="账号或密码错误")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    if token != "cheerful-goat-token-fixed":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="证件失效")
    return ADMIN_USERNAME

# --- 4. 任务管理接口 ---

@app.get("/tasks/")
def read_tasks(db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    return db.query(TaskModel).all()

@app.post("/tasks/")
def create_task(task: dict, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    deadline_dt = None
    if task.get("deadline"):
        deadline_dt = datetime.fromisoformat(task["deadline"].replace("Z", ""))
    db_task = TaskModel(
        title=task["title"],
        platform=task["platform"],
        description=task.get("description"),
        is_urgent=task.get("is_urgent", False),
        deadline=deadline_dt
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

# 【核心功能更新】：修改整个任务内容
# 【找到这一段，全部替换】
@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_data: dict, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db_task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="未找到任务")
    
    # 这里是重点：大管家开始逐一检查您想修改的内容
    if "title" in updated_data: 
        db_task.title = updated_data["title"]
    if "platform" in updated_data: 
        db_task.platform = updated_data["platform"]
    
    # --- 就是这一行，让描述也能被修改了 ---
    if "description" in updated_data: 
        db_task.description = updated_data["description"]
        
    if "is_urgent" in updated_data: 
        db_task.is_urgent = updated_data["is_urgent"]
    if "status" in updated_data: 
        db_task.status = updated_data["status"]
    
    if "deadline" in updated_data:
        if updated_data["deadline"]:
            # 处理日期格式，防止系统看不懂
            db_task.deadline = datetime.fromisoformat(updated_data["deadline"].replace("Z", ""))
        else:
            db_task.deadline = None
            
    db.commit()      # 存入保险柜
    db.refresh(db_task) # 刷新一下状态
    return db_task

# 快捷更新状态（保留）
@app.put("/tasks/{task_id}/status")
def update_status(task_id: int, new_status: str, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db_task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if not db_task: raise HTTPException(status_code=404, detail="未找到")
    db_task.status = new_status
    db.commit()
    return db_task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db_task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if not db_task: raise HTTPException(status_code=404, detail="未找到")
    db.delete(db_task)
    db.commit()
    return {"message": "已删除"}

@app.get("/")
def home():
    return {"message": "爷爷好！后端大管家正在值班中。"}
