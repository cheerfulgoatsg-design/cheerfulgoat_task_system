from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
import schemas, database, models, hashing

router = APIRouter(
    prefix="/user",
    tags=['Users']
)

get_db = database.get_db

# --- 看！我们把 response_model 从 schemas.ShowUser 改回了 schemas.User ---
@router.post('/', response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_user(request: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = models.User(
        username=request.username,
        password=hashing.Hasher.get_password_hash(request.password),
        role=request.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
