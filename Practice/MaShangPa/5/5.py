# 关卡链接: https://www.mashangpa.com/problem-detail/5/
# 请求参数加密.post请求
import json
import time

import requests

from MaShangPa.Const import cookies
from MaShangPa.Const import submitAnswers


def get_array_by_get(level, request_body) -> int:
    headers = {
        "Cookie": cookies,
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
        "Connection": "keep-alive"
    }
    response = requests.post(
        f'https://www.mashangpa.com/api/problem-detail/{level}/data/', headers=headers,
        data=request_body)
    if response.status_code != 200 :
        print(response.text)
        return 0

    current_array = response.json()['current_array']
    total_sum = 0
    for num in current_array:
        total_sum += num

    return sum(current_array)

# jsRPC的代码:
# demo.regAction("encrypt", function (resolve,pageNumber) {
#     const timestamp = new Date().getTime();
#     const params = {
#         page: pageNumber,
#         _ts: timestamp,
#     };
#     const jsonString = JSON.stringify(params);
#     var outcome = encrypt(param)
#     resolve(outcome);
# })
def custom_encrypt(page: int) -> str:
    response = requests.get(
        f'http://127.0.0.1:12080/go?group=zzz&action=encrypt&param={page}')
    if response.status_code != 200 :
        return ''

    return response.json()['data']


def load_page(page_number):
    time.sleep(0.5)
    encrypted_query = custom_encrypt(page_number)  # 不扣环境,直接使用jsRPC进行偷懒
    if encrypted_query == {}:
        return None
    return json.dumps({'xl': encrypted_query})


def main():
    level = 5
    total_sum = 0
    isBreak = False

    for page_number in range(20):
        time.sleep(0.5)
        page_number = page_number + 1

        request_body = load_page(page_number)
        if request_body is None:
            print("[-] 访问练习链接遇到非预期错误,请检查代码")
            return

        total_sum_by_current_page = get_array_by_get(level, request_body)
        if total_sum_by_current_page == 0:
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
