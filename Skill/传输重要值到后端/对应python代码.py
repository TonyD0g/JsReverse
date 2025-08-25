from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware  # 引入中间件

app = FastAPI()

# 配置 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有源（生产环境应替换为具体前端域名）
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有 HTTP 方法（包括 OPTIONS）
    allow_headers=["*"],  # 允许所有请求头
)

@app.post("/accept")
async def accept_data(body: str = Body(..., media_type="text/plain")):
    print(f"Received string: {body}")
    return {}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000)