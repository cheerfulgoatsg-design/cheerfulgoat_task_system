from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import schemas, database, models

router = APIRouter(
    prefix="/tasks",
    tags=['Tasks']
)

get_db = database.get_db

@router.post('/', response_model=schemas.Task)
def create_task(request: schemas.TaskCreate, db: Session = Depends(get_db)):
    new_task = models.Task(
        title=request.title,
        description=request.description,
        platform=request.platform,
        is_urgent=request.is_urgent
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task
