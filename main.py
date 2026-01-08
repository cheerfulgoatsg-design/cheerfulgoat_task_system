from fastapi import FastAPI
import models, database, hashing
from database import engine
from routers import task, user, login
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

app = FastAPI()

# 自动创建数据库表
models.Base.metadata.create_all(bind=engine)

# --- 自动创建管理员账号的逻辑 ---
def create_admin():
    db = next(database.get_db())
    # 检查是否已经有名为 admin 的用户
    user = db.query(models.User).filter(models.User.username == 'admin').first()
    if not user:
        # 如果没有，就创建一个。账号是 admin，密码是 123456
        admin_user = models.User(
            username='admin', 
            password=hashing.Hasher.get_password_hash('123456'), 
            role='admin'
        )
        db.add(admin_user)
        db.commit()
        print("管理员账号 admin 创建成功！")

# 启动时运行创建逻辑
create_admin()

# 允许所有来源访问
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(login.router)
app.include_router(task.router)
app.include_router(user.router)

@app.get("/")
def index():
    return {"message": "CheerfulGoat Task System API is running"}
