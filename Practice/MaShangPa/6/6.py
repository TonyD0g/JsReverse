# 关卡链接: https://www.mashangpa.com/problem-detail/6/
# 防重放 + 响应包加密
import json
import time

import requests

from Practice.MaShangPa.Const import cookies
from Practice.MaShangPa.Const import submitAnswers


def get_array_by_get(level, page_number, Tt, S) -> int:
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
        "Connection": "keep-alive",
        "Tt": str(Tt),
        "S": S,
    }
    response = requests.get(
        f'https://www.mashangpa.com/api/problem-detail/{level}/data/?page={page_number}', headers=headers)
    if response.status_code != 200:
        print(response.text)
        return 0

    # 响应包解密
    decrypt_data = decrypt_response_by_xxxxoooo_func(response.json()['t'])
    if decrypt_data is None:
        print("解密响应包出现问题,请检查")
        return 0

    decrypt_data_json = json.loads(decrypt_data)

    current_array = decrypt_data_json['current_array']
    return sum(current_array)

# jsRPC代码:
# demo.regAction("xxxxoooo", function (resolve,encryptedHex) {
#     var outcome = updatePageContent(JSON.parse(xxxxoooo(encryptedHex)))
#     resolve(outcome);
# })
def decrypt_response_by_xxxxoooo_func(t):
    response = requests.get(
        f'http://127.0.0.1:12080/go?group=zzz&action=xxxxoooo&param={t}')
    if response.status_code != 200:
        return None

    return response.json()['data']

# jsRPC代码:
# demo.regAction("s", function (resolve) {
#     s()
#     var outcome = window.hhh
#     resolve(outcome);
# })
def get_hhh_by_s_func() -> str:
    response = requests.get(
        f'http://127.0.0.1:12080/go?group=zzz&action=s')
    if response.status_code != 200:
        return ''

    return response.json()['data']


def main():
    level = 6
    total_sum = 0
    isBreak = False

    for page_number in range(20):
        time.sleep(0.5)
        page_number = page_number + 1

        hhh_outcome = get_hhh_by_s_func()
        hhh_outcome_by_json = json.loads(hhh_outcome)
        Tt = hhh_outcome_by_json['tt']
        S = hhh_outcome_by_json['s']

        total_sum_by_current_page = get_array_by_get(level, page_number, Tt, S)
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
