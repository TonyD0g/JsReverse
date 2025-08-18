# 关卡链接: https://www.mashangpa.com/problem-detail/1/
# 使用爬虫采集详情数据，根据返回的数据进行求和提交答案
import time
import requests
from MaShangPa.Const import cookies

def get_array_by_get(level,page) -> int:
    header = {
        "Cookie": cookies,
        "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
    }
    response = requests.get(f'https://www.mashangpa.com/api/problem-detail/{level}/data/?page={page}', cookies=cookies,headers=header)
    if response.status_code != 200 or '\\u' in response.json()['current_array']:
        return 0

    current_array = response.json()['current_array']
    return sum(current_array)


def main():
    level = 1
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
