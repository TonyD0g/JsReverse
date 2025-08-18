# 关卡链接: https://www.mashangpa.com/problem-detail/9/
# js代码混淆,防重放,无限debug,魔改cookie
import base64
import time
import requests
from MaShangPa.Const import cookies
from MaShangPa.Const import submitAnswers


def get_array_by_get(level, page_number, m, timestamp) -> int:
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

    timestamp_bytes = str(timestamp).encode('utf-8')
    base64_timestamp = base64.b64encode(timestamp_bytes).decode('utf-8')

    post_body =  {
        "page": page_number,
        "m": m,
        "tt": str(base64_timestamp)
    }
    response = requests.post(
        f'https://www.mashangpa.com/api/problem-detail/{level}/data/', headers=headers,
        json=post_body)
    if response.status_code != 200:
        print(response.text)
        return 0

    current_array = response.json()['current_array']
    return sum(current_array)


# jsRPC代码,关键代码处: n.data.m = t.MqmaW(c, t[r(1881)](t[r(489)], f))
# demo.regAction("getM", function (resolve, param) {
#     try {
#         function c(n) {
#                 var r = i
#                   , t = {
#                     RjdKj: function(n, r) {
#                         return n % r
#                     },
#                     DBjOO: function(n, r) {
#                         return n + r
#                     },
#                     BByPb: function(n, r) {
#                         return n ^ r
#                     },
#                     KIZHi: function(n, r) {
#                         return n | r
#                     },
#                     HAGBT: function(n, r) {
#                         return n >>> r
#                     },
#                     pUtQl: function(n, r) {
#                         return n < r
#                     },
#                     UwUnt: function(n, r) {
#                         return n * r
#                     },
#                     WdUAe: function(n, r) {
#                         return n + r
#                     },
#                     VDcvU: "debu",
#                     PwEDm: r(2874),
#                     KWaPS: r(1672),
#                     BjniW: r(488),
#                     ztPZi: function(n, r) {
#                         return n === r
#                     },
#                     RaGFx: r(894),
#                     bnqLR: r(2645)
#                 };
#                 if (n) {
#                     if (t[r(2257)] !== t[r(697)])
#                         return dd.aa[r(2897)](n, "xxxooo")[r(1049)]();
#                     var u = _0x17006a[t[r(2743)](t[r(1811)](_0x219937, 4), 5)]
#                       , e = _0x388b65[t[r(2743)](_0x416ac4 + 1, 5)]
#                       , c = e[r(2756)]
#                       , f = e[r(487)];
#                     for (_0x1e7dc0 = t[r(2767)](u[r(2756)], t.KIZHi(c << 1, f >>> 31)),
#                     _0x4d8156 = u[r(487)] ^ t.KIZHi(f << 1, t.HAGBT(c, 31)),
#                     _0x680b88 = 0; t[r(2417)](_0x2a74ec, 5); _0xba8375++)
#                         (_0x1c98da = _0x410975[t[r(1811)](_0x106157, t[r(1454)](5, _0x94eeb7))])[r(2756)] ^= _0x336535,
#                         _0x26218e[r(487)] ^= _0x2ba16c
#                 } else {
#                     if (t.ztPZi(t[r(1938)], t.RaGFx))
#                         return t[r(2406)];
#                     (function() {
#                         return !1
#                     }
#                     )[r(2726)](lnDKWR[r(1703)](lnDKWR[r(882)], "gger"))[r(2173)](lnDKWR[r(2933)])
#                 }
#             }
#
#         let outcome = c("9527"+param);
#         resolve(outcome);
#     } catch (error) {
#         resolve({
#             message: "整体函数执行错误",
#             errorMessage: error.message,
#             stack: error.stack
#         });
#     }
# });
def get_m(timestamp) -> str:
    response = requests.get(
        f'http://127.0.0.1:12080/go?group=zzz&action=getM&param={timestamp}')
    if response.status_code != 200:
        return ''

    return response.json()['data']


def main():
    level = 9
    total_sum = 0
    isBreak = False

    for page_number in range(20):
        time.sleep(0.5)
        page_number = page_number + 1
        timestamp = int(time.time())
        timestamp = int(str(timestamp) + '830')

        m = get_m(timestamp)
        if m == '{}':
            print("\n[-] 访问jsRPC获取到了非预期结果,请检查代码")
            return

        time.sleep(0.5)
        total_sum_by_current_page = get_array_by_get(level, page_number, m, timestamp)
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
