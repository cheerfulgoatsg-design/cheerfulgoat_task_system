from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List
import schemas, database, models

router = APIRouter(
    prefix="/tasks",
    tags=['Tasks']
)

get_db = database.get_db

# 提交新任务
@router.post('/', response_model=schemas.Task, status_code=status.HTTP_201_CREATED)
def create_task(request: schemas.TaskCreate, db: Session = Depends(get_db)):
    new_task = models.Task(
        title=request.title,
        description=request.description,
        platform=request.platform,
        is_urgent=request.is_urgent,
        # --- 看！这里把截止日期也存进数据库了 ---
        deadline=request.deadline, 
        status="待处理"
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

# 获取所有任务列表
@router.get('/', response_model=List[schemas.Task])
def get_all_tasks(db: Session = Depends(get_db)):
    tasks = db.query(models.Task).order_by(models.Task.created_at.desc()).all()
    return tasks

# 修改任务状态
@router.put('/{id}/status')
def update_status(id: int, new_status: str, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == id)
    if not task.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="任务不存在")
    task.update({'status': new_status})
    db.commit()
    return {"message": "状态更新成功"}
