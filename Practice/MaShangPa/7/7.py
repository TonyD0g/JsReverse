# 关卡链接: https://www.mashangpa.com/problem-detail/7/
# js代码轻度混淆,防重放+响应包加密,无限debug
import base64
import json
import time

import requests

from MaShangPa.Const import cookies
from MaShangPa.Const import submitAnswers


def get_array_by_get(level, page_number, M, ts, x) -> int:
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
        "X-Requested-With":"XMLHttpRequest",
        "M": str(M),
        "Ts": str(ts),
    }
    response = requests.get(
        f'https://www.mashangpa.com/api/problem-detail/{level}/data/?page={page_number}&x={str(x)}', headers=headers)
    if response.status_code != 200:
        print(response.text)
        return 0

    # 响应包解密
    decrypt_data = decrypt_response_by_xxxxoooo_func(response.json()['r'])
    if decrypt_data is None:
        print("解密响应包出现问题,请检查")
        return 0

    decrypt_data_json = json.loads(decrypt_data)

    current_array = decrypt_data_json['current_array']
    return sum(current_array)

# jsRPC代码:
# demo.regAction("decryptionByxxxxoooo", function (resolve,r) {
#     let outcome = xxxxoooo(r);
#     resolve(outcome);
# });
def decrypt_response_by_xxxxoooo_func(t):
    response = requests.get(
        f'http://127.0.0.1:12080/go?group=zzz&action=decryptionByxxxxoooo&param={t}')
    if response.status_code != 200:
        return None

    return response.json()['data']

# jsRPC代码:
# demo.regAction("decryption", function (resolve) {
#     try {
#         const yK = OU
#       , yp = OU
#       , yk = R3
#       , yq = R4
#       , W = {
#         'QCqSI': function(B, Y) {
#             return B + Y;
#         },
#         'uSzcs': function(B, Y) {
#             return B(Y);
#         },
#         'KjfHo': yk(0x25f)
#     };
#         let M = new Date().getTime();
#         let O = window['eeee']("xialuo" + M);
#         let MString = M.toString();
#         let encodedStr = encodeURIComponent(MString);
#         let MBase64 = btoa(encodedStr);
#         let OBase64 = btoa(O);
#
#         let generate_x;
#         try {
#             generate_x = W['uSzcs'](encodeURIComponent, dd['a']["SHA256"](O+"xxoo"));
#         } catch (error) {
#             resolve("generate_x 计算错误:"+error.message+error.stack);
#             throw error;
#         }
#
#         let x = btoa(encodeURIComponent(generate_x.toString()));
#         resolve(MBase64 + ' - ' + OBase64 + ' - ' + x);
#     } catch (outerError) {
#         resolve("整体函数执行错误:", outerError.message);
#         resolve("");
#     }
# });
def get_m_and_ts_and_x() -> str:
    response = requests.get(
        f'http://127.0.0.1:12080/go?group=zzz&action=decryption')
    if response.status_code != 200:
        return ''

    return response.json()['data']


def main():
    level = 7
    total_sum = 0
    isBreak = False

    for page_number in range(20):
        time.sleep(0.5)
        page_number = page_number + 1

        m_and_ts_outcome = get_m_and_ts_and_x()
        if m_and_ts_outcome == '{}':
            print("\n[-] 访问jsRPC获取到了非预期结果,请检查代码")
            return

        split_string = m_and_ts_outcome.split('-')
        ts_decoded_bytes = base64.b64decode(split_string[0]).decode('utf-8')
        m_decoded_bytes = base64.b64decode(split_string[1]).decode('utf-8')
        x_decoded_bytes = base64.b64decode(split_string[2]).decode('utf-8')

        time.sleep(0.5)
        total_sum_by_current_page = get_array_by_get(level, page_number, m_decoded_bytes, ts_decoded_bytes, x_decoded_bytes)
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
