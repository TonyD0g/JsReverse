# 关卡链接: https://www.mashangpa.com/problem-detail/4/
# 有一个sign经过加密处理，适合初级JS逆向模拟分析(即防重放)
import hashlib
import time
import requests
from MaShangPa.Const import cookies
from MaShangPa.Const import submitAnswers


def get_array_by_get(level, page, sign, ts) -> int:
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
    response = requests.get(
        f'https://www.mashangpa.com/api/problem-detail/{level}/data/?page={page}&sign={sign}&_ts={ts}', headers=headers)
    if response.status_code != 200 or '\\u' in response.json()['current_array']:
        return 0

    current_array = response.json()['current_array']

    return sum(current_array)

#  对应算法:
# function loadPage(pageNumber) {
#     const timestamp = new Date().getTime()
#     window.token = window.md5("tuling" + timestamp + pageNumber)
#     const params = {
#         page: pageNumber,
#         sign: window.token,
#         _ts: timestamp,
#     };
#     const queryString = new URLSearchParams(params).toString();
#     fetch(`/api/problem-detail/${problemId}/data/?${queryString}`)
#         .then(response => response.json())
#         .then(data => updatePageContent(data))
#         .catch(error => console.error('Error fetching problem details:', error));
# }
def getSignAndTs(page_number):
    timestamp = int(time.time() * 1000)
    token_str = f"tuling{timestamp}{page_number}"
    sign = hashlib.md5(token_str.encode()).hexdigest()

    return sign, timestamp


def main():
    level = 4
    total_sum = 0
    isBreak = False

    for page_number in range(20):
        time.sleep(0.5)
        page_number = page_number + 1

        sign, ts = getSignAndTs(page_number)

        total_sum_by_current_page = get_array_by_get(level, page_number, sign, ts)
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
