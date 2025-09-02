# 关卡链接: https://www.mashangpa.com/problem-detail/11/
# wasm加密. 使用hook的方式解
# param参数: m 、_ts
import json
import time
from typing import Any, Literal

import requests
import redis

r = redis.Redis()

from Practice.MaShangPa.Const import cookies
from Practice.MaShangPa.Const import submitAnswers

# 使用JsRpc调用 loadPage()
# demo.regAction("execLoadPage", function (resolve, param) {
#     try {
#         loadPage(param);
#         resolve("[+] 执行loadPage(" + param + "); 成功!");
#     } catch (error) {
#         resolve({
#             message: "整体函数执行错误",
#             errorMessage: error.message,
#             stack: error.stack
#         });
#     }
# });
def call_loadPage(page_number):
    try:  # 设置超时为0.001秒，几乎不等待响应
        _ = requests.get(
            f'http://127.0.0.1:12080/go?group=zzz&action=execLoadPage&param=' + str(page_number),
            timeout=0.001
        )
    except requests.exceptions.Timeout:  # 忽略超时异常，无需处理响应
        pass

def get_array_by_get(level, page_number, m, _ts) -> None | int | Literal[0] | Any:
    headers = {
        "Cookie": cookies ,
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
        "Sec-Ch-Ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Accept": "*/*",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": f"https://www.mashangpa.com/problem-detail/{level}/",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Priority": "u=1, i",
        "Connection": "keep-alive",
    }
    response = requests.get(
        f'https://www.mashangpa.com/api/problem-detail/{level}/data/?page={page_number}&m={m}&_ts={_ts}',
        headers=headers)
    if response.status_code != 200:
        print(response.text)
        return 0

    # 响应包解密
    try:
        current_array = response.json()['current_array']
        return sum(current_array)
    except:
        return None


# jsRPC代码:

def get_request_param() -> str:
    response = requests.get(
        f'http://127.0.0.1:12080/go?group=zzz&action=getRequestParam')
    if response.status_code != 200:
        return ''

    return response.json()['data']


def main():
    level = 11
    total_sum = 0
    isBreak = False
    temp_accept_data_by_font = ''

    for page_number in range(20):
        page_number = page_number + 1

        # jsRpc调用 loadPage
        call_loadPage(page_number)
        time.sleep(0.8)

        while True:
            data = r.get("accept_data_by_font")  # 从Redis读取
            data =  data.decode('utf-8')
            if len(data) != 0 and data != temp_accept_data_by_font:
                break

        temp_accept_data_by_font = data
        data_dict = json.loads(data)

        m = data_dict.get('m')
        _ts = data_dict.get('_ts')

        total_sum_by_current_page = get_array_by_get(level, page_number, m, _ts)
        if total_sum_by_current_page == 0 or total_sum_by_current_page is None:
            isBreak = True
            break
        print(f"page:{page_number} - total_sum:{str(total_sum_by_current_page)}")
        total_sum = total_sum + total_sum_by_current_page

    print(f"total_sum : {total_sum}")
    if isBreak:
        print("[-] 访问练习链接遇到非预期错误,请检查代码")
        return

    submitAnswers(level, total_sum)


if __name__ == "__main__":
    main()
