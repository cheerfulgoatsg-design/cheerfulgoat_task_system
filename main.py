from fastapi import FastAPI, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from typing import List
import models, schemas, database, hashing
from routers import user # 导入我们创建的用户路由

# --- App Initialization ---
app = FastAPI(
    title="CheerfulGoat 任务管理系统",
    description="一个为100岁老爷爷定制的专属任务管理中台",
    version="1.0.0",
)

# --- Database Creation ---
models.Base.metadata.create_all(bind=database.engine)

# --- Include Routers ---
app.include_router(user.router) # 将用户接待处的功能包含进来

# --- Root Endpoint ---
@app.get("/")
def read_root():
    content = '{"message":"欢迎来到 CheerfulGoat 任务管理系统！"}'
    return Response(content=content, media_type="application/json; charset=utf-8")

# --- Task Endpoints (we will add more later) ---
@app.post("/tasks/", response_model=schemas.ShowTask, tags=['Tasks'])
def create_task(request: schemas.TaskCreate, db: Session = Depends(database.get_db)):
    # 在真实场景中，我们应该从登录用户那里获取 creator_id
    # 这里我们暂时硬编码为第一个用户，后续会用登录系统替换
    temp_creator_id = 1 
    
    new_task = models.Task(**request.dict(), creator_id=temp_creator_id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@app.get("/tasks/", response_model=List[schemas.ShowTask], tags=['Tasks'])
def get_all_tasks(db: Session = Depends(database.get_db)):
    tasks = db.query(models.Task).all()
    return tasks
