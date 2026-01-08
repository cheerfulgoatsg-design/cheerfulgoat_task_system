from fastapi import FastAPI
import models
from database import engine
from routers import task, user, login # <--- 增加了 login
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 自动创建数据库表
models.Base.metadata.create_all(bind=engine)

# 允许所有来源访问 (终极绝招)
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(login.router) # <--- 登录柜台开张
app.include_router(task.router)
app.include_router(user.router)

@app.get("/")
def index():
    return {"message": "CheerfulGoat Task System API is running"}
