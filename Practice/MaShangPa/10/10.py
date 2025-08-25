# 关卡链接: https://www.mashangpa.com/problem-detail/10/
# js代码混淆,无限debug,魔改加密算法
import base64
import time
import requests
from Practice.MaShangPa.Const import cookies
from Practice.MaShangPa.Const import submitAnswers


def get_array_by_get(level,page_number, t) -> int:
    headers = {
        "Cookie": cookies,
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
        "Sec-Ch-Ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Accept": "*/*",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Content-Type": "application/json",
        "Origin": "https://www.mashangpa.com",
        "Referer": "https://www.mashangpa.com/problem-detail/8/",
        "X-Requested-With": "XMLHttpRequest",
        "Connection": "keep-alive",
    }
    response = requests.get(
        f'https://www.mashangpa.com/api/problem-detail/{level}/data/?page={page_number}&t={t}', headers=headers)
    if response.status_code != 200:
        print(response.text)
        return 0

    current_array = response.json()['current_array']
    return sum(current_array)


# jsRPC代码,关键代码处:  _pa = _0x27607a[_0x1da480(0x3c8)](OOOO, _0x443686[_0x1da480(0x418)]);
# demo.regAction("getPa", function (resolve, param) {
#     try {
#         let _pa = OOOO("/api/problem-detail/10/data/?page="+param);
#         resolve(_pa);
#     } catch (error) {
#         resolve({
#             message: "整体函数执行错误",
#             errorMessage: error.message,
#             stack: error.stack
#         });
#     }
# });
def get__pa(page) -> str:
    response = requests.get(
        f'http://127.0.0.1:12080/go?group=zzz&action=getPa&param={page}')
    if response.status_code != 200:
        return ''

    return response.json()['data']


def main():
    level = 10
    total_sum = 0
    isBreak = False

    for page_number in range(20):
        time.sleep(0.5)
        page_number = page_number + 1
        t = get__pa(page_number) # _pa 是 t 参数的值
        if t == '{}':
            print("\n[-] 访问jsRPC获取到了非预期结果,请检查代码")
            return

        time.sleep(0.5)
        total_sum_by_current_page = get_array_by_get(level, page_number,t)
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
