# 关卡链接: https://www.mashangpa.com/problem-detail/8/
# js代码混淆,防重放,无限debug,魔改cookie
import time
import requests
from MaShangPa.Const import cookies
from MaShangPa.Const import submitAnswers


def get_array_by_get(level, page_number, M, T, s) -> int:
    headers = {
        "Cookie": cookies + f's={s}',
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
        "M": str(M),
        "T": str(T),
    }

    post_body = {
        "page": page_number
    }

    response = requests.post(
        f'https://www.mashangpa.com/api/problem-detail/{level}/data/', headers=headers,
        json=post_body)
    if response.status_code != 200:
        print(response.text)
        return 0

    current_array = response.json()['current_array']
    return sum(current_array)


# jsRPC代码:
# demo.regAction("test", function (resolve,param) {
#     try{
#         let timestamp= new Date()["getTime"]();
#         var _0xe8dc6 = a0_0x218b
#           , _0x56df28 = {
#             '\x47\x51\x5a\x65\x44': function(_0x53e7cf, _0x45bf9d) {
#                 return _0x53e7cf + _0x45bf9d;
#             },
#             '\x49\x6c\x43\x47\x79': function(_0x4510fa, _0x3d3320) {
#                 return _0x4510fa + _0x3d3320;
#             },
#             '\x56\x51\x55\x70\x5a': function(_0xf217d6, _0xe4bde6) {
#                 return _0xf217d6(_0xe4bde6);
#             },
#             '\x4b\x54\x52\x5a\x6c': function(_0x597690, _0x39367f, _0x332fa6) {
#                 return _0x597690(_0x39367f, _0x332fa6);
#             },
#             '\x68\x62\x6f\x5a\x44': function(_0x12c1c6, _0x5c00a6) {
#                 return _0x12c1c6 + _0x5c00a6;
#             },
#             '\x47\x7a\x66\x41\x58': function(_0x621f20, _0x30867e) {
#                 return _0x621f20 + _0x30867e;
#             }
#         };
#
#         try{
#              let M = OOOoOo("oooooo"+ timestamp + param, "oooooo")
#              let T = btoa(timestamp);
#              let s = OOOoO("xoxoxoxo" + timestamp);
#              resolve(M + '-' + T + '-' + s);
#         }catch(error){
#             resolve("执行错误1:", error.message+error.stack);
#         }
#
#
#     }catch(error) {
#          resolve("整体函数执行错误:", error.message);
#      }
# });
def get_m_and_ts_and_s(page_num) -> str:
    response = requests.get(
        f'http://127.0.0.1:12080/go?group=zzz&action=test&page={page_num}')
    if response.status_code != 200:
        return ''

    return response.json()['data']


def main():
    level = 8
    total_sum = 0
    isBreak = False

    for page_number in range(20):
        time.sleep(0.5)
        page_number = page_number + 1

        m_and_ts_and_s_outcome = get_m_and_ts_and_s(page_number)
        if m_and_ts_and_s_outcome == '{}':
            print("\n[-] 访问jsRPC获取到了非预期结果,请检查代码")
            return

        split_string = m_and_ts_and_s_outcome.split('-')
        m_decoded_bytes = split_string[0]
        t_decoded_bytes = split_string[1]
        s_decoded_bytes = split_string[2]

        time.sleep(0.5)
        total_sum_by_current_page = get_array_by_get(level, page_number, m_decoded_bytes, t_decoded_bytes,
                                                     s_decoded_bytes)
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
