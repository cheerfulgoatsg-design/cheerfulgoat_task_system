from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import models
from database import engine
from routers import user, task # <--- 看！我们在这里导入了新的 task 路由！

# 创建数据库表
models.Base.metadata.create_all(bind=engine)

# 创建 FastAPI 应用实例
app = FastAPI()

# “白名单”配置
origins = [
    "https://cheerfulgoat-frontend.onrender.com",
    "https://cheerfulgoat-task-panel.onrender.com", # <--- 这是您的新网址
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
 )

# 包含用户路由和任务路由
app.include_router(user.router)
app.include_router(task.router) # <--- 看！我们在这里把“任务处理台”正式挂牌营业！

# 根路由
@app.get("/")
def read_root():
    return {"message": "欢迎来到 CheerfulGoat 任务管理系统！"}
