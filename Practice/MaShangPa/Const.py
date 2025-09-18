import requests

cookies = ""

# 用于提交答案,形参为关卡数,比如1
def submitAnswers(level,answer):
    url = f"https://www.mashangpa.com/problem/{level}/submit/"
    headers = {
        "Host": "www.mashangpa.com",
        "Cookie": cookies,
        "Sec-Ch-Ua-Platform": "\"macOS\"",
        "X-Csrftoken": "PmdMuVqFkD9BWOkHGxvCHVRPudcxLIL3pMpbXi3PClBlSOhiAS8iXYRK0ywrszFg",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
        "Sec-Ch-Ua": "\"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"138\", \"Google Chrome\";v=\"138\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Accept": "*/*",
        "Origin": "https://www.mashangpa.com",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": f"https://www.mashangpa.com/problem-detail/{level}/",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Priority": "u=1, i",
        "Connection": "keep-alive"
    }

    # 构建multipart/form-data请求体
    boundary = "----WebKitFormBoundarySIsNdpNTGwHnmqlm"
    body = (
        f"--{boundary}\r\n"
        'Content-Disposition: form-data; name="csrfmiddlewaretoken"\r\n\r\n'
        "PmdMuVqFkD9BWOkHGxvCHVRPudcxLIL3pMpbXi3PClBlSOhiAS8iXYRK0ywrszFg\r\n"
        f"--{boundary}\r\n"
        'Content-Disposition: form-data; name="user_answer"\r\n\r\n'
        f"{answer}\r\n"
        f"--{boundary}--\r\n"
    )

    # 添加动态Content-Type头
    headers["Content-Type"] = f"multipart/form-data; boundary={boundary}"

    # 发送请求
    response = requests.post(
        url,
        headers=headers,
        data=body.encode("utf-8")  # 手动编码为字节流
    )

    # 输出响应结果
    print("\n\n正在提交答案...")
    print(f"状态码: {response.status_code}")
    try:
        responseJson = response.json()
        print(f"响应状态码: {responseJson['status']}")
        print(f"响应内容: {responseJson['message']}")
    except:
        pass
