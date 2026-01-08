from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import models
from database import engine
from routers import user

# 创建数据库表
models.Base.metadata.create_all(bind=engine)

# 创建 FastAPI 应用实例
app = FastAPI()

# --- 这是我们新添加的“白名单”配置！ ---
origins = [
    "https://cheerfulgoat-frontend.onrender.com", # 允许我们的前端地址访问
    "http://localhost", # 为了以后本地测试方便
    "http://localhost:8080", # 为了以后本地测试方便
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # 告诉“保安” ，只允许这些地址的人进来
    allow_credentials=True,
    allow_methods=["*"], # 允许他们使用任何方法 (GET, POST, etc.)
    allow_headers=["*"], # 允许他们携带任何类型的“信封”
)
# --- “白名单”配置结束 ---


# 包含用户路由
app.include_router(user.router)

# 根路由
@app.get("/")
def read_root():
    return {"message": "欢迎来到 CheerfulGoat 任务管理系统！"}

