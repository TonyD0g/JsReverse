import json
from typing import Dict, Union

import redis
import uvicorn
from fastapi import FastAPI, Request, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

r = redis.Redis()

app = FastAPI()

# 配置 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def universal_body_parser(request: Request) -> Union[Dict, str, bytes]:
    """通用请求体解析器，支持多种内容类型"""
    content_type = request.headers.get("Content-Type", "")

    # 处理JSON
    if "application/json" in content_type:
        try:
            return await request.json()
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"JSON解析错误: {str(e)}")

    # 处理表单数据（包括文件上传）
    elif "multipart/form-data" in content_type or "application/x-www-form-urlencoded" in content_type:
        form_data = await request.form()
        parsed_data = {}

        # 处理普通字段
        for key, value in form_data.items():
            if not isinstance(value, UploadFile):
                parsed_data[key] = value

        # 处理文件字段
        files = await request.files()
        for key, file in files.items():
            file_content = await file.read()
            parsed_data[key] = {
                "filename": file.filename,
                "content_type": file.content_type,
                "size": len(file_content),
                "content": file_content.decode("utf-8", errors="ignore")  # 文本文件解码
            }
        return parsed_data

    # 处理纯文本
    elif "text/plain" in content_type:
        return (await request.body()).decode("utf-8")

    # 其他类型按二进制处理
    else:
        return await request.body()


@app.post("/accept")
async def accept(request: Request):
    """通用请求处理端点"""
    try:
        # 使用通用解析器处理请求体[6,7](@ref)
        body = await universal_body_parser(request)

        # 根据不同类型处理存储逻辑
        if isinstance(body, dict):
            # 字典类型存储为JSON字符串
            await r.set("accept_data_by_font", json.dumps(body))
        elif isinstance(body, (str, bytes)):
            # 文本/二进制直接存储
            await r.set("accept_data_by_font", body)
        else:
            # 其他类型转为字符串存储
            await r.set("accept_data_by_font", str(body))

        print(f"Received data: {type(body)} - {body}")
        return {"status": "success", "data_type": type(body).__name__}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"请求处理失败: {str(e)}")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5421)