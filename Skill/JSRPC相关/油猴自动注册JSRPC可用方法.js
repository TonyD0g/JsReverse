// ==UserScript==
// @name         jsrpc-register-funciton
// @version      v1
// @description  用于注册jsRPC可以使用的方法
// @author       TonyD0g
// @match        *://*/*
// @include      *://*/*
// @run-at       document-idle
// @grant unsafeWindow
// @license      MIT
// ==/UserScript==

(function(win) {
    'use strict';

    win.addEventListener('load', function() {
        // 要注册jsRPC可以使用的方法填在下方
        // 例如:
        // demo.regAction("getO", function (resolve) {
		//     try {
		//         resolve(win.o_dafsdsf);
		//     } catch (error) {
		//         resolve({
		//             message: "整体函数执行错误",
		//             errorMessage: error.message,
		//             stack: error.stack
		//         });
		//     }
		// });
    });
})(unsafeWindow);