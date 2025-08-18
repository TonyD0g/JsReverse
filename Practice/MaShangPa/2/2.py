# 关卡链接: https://www.mashangpa.com/problem-detail/2/
# headers请求头验证。有反爬，浏览器相关指纹需处理，适合初级爬虫入门练习。根据返回的数据进行求和并提交答案
import time
import requests
from MaShangPa.Const import cookies

def get_array_by_get(level,page) -> int:
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
    response = requests.get(f'https://www.mashangpa.com/api/problem-detail/{level}/data/?page={page}',headers=headers)
    if response.status_code != 200 or '\\u' in response.json()['current_array']:
        return 0

    current_array = response.json()['current_array']
    return sum(current_array)


def main():
    level = 2
    total_sum = 0
    isBreak = False

    for page in range(20):
        time.sleep(1)
        page = page + 1
        total_sum_by_current_page = get_array_by_get(level,page)
        if total_sum_by_current_page == 0:
            isBreak = True
            break
        print(f"page:{page} - total_sum:{str(total_sum_by_current_page)}")
        total_sum = total_sum + total_sum_by_current_page

    print(f"total_sum : {total_sum}")

    if isBreak:
        print("[-] 访问练习链接遇到非预期错误,请检查代码")
        return




if __name__ == "__main__":
    main()
