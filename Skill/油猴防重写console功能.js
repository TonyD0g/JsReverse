// ==UserScript==
// @name         绕过无法使用Console
// @version      v1.1
// @description  彻底防止页面篡改 console 对象及其方法
// @author       TonyDog
// @match        *://*/*
// @run-at       document-start
// @grant        none
// @license      MIT
// ==/UserScript==

(function() {
    'use strict';

    // 深度冻结函数（防止嵌套对象被修改）
    const deepFreeze = (obj) => {
        Object.freeze(obj);
        Object.keys(obj).forEach(key => {
            if (obj[key] && typeof obj[key] === 'object') {
                deepFreeze(obj[key]);  // 递归冻结嵌套对象
            }
        });
        return obj;
    };

    // 主保护逻辑
    try {
        // 优先使用深度冻结（比 defineProperty 更彻底）
        deepFreeze(window.console);

        // 额外防止控制台被整体替换
        Object.defineProperty(window, 'console', {
            value: window.console,
            writable: false,
            configurable: false
        });

        console.debug("[Lock Console Pro] 控制台已深度冻结");
    } catch (e) {
        console.warn("[Lock Console Pro] 初始化失败", e);
    }
})();