// ==UserScript==
// @name         Leave-debugger
// @namespace    https://github.com/SherryBX/Leave-debugger
// @version      v2.2.0
// @description  用于破解网页无限debugger，支持多种调试方式拦截
// @author       Sherry
// @match        *://*/*
// @include      *://*/*
// @run-at       document-start
// @license      MIT
// @icon         https://mms0.baidu.com/it/u=2886239489,318124131&fm=253&app=138&f=JPEG?w=800&h=800
// @downloadURL  https://update.greasyfork.org/scripts/524858/Leave-debugger.user.js
// @updateURL    https://update.greasyfork.org/scripts/524858/Leave-debugger.meta.js
// ==/UserScript==

(function() {  // 立即执行函数，创建独立作用域
    'use strict';  // 启用严格模式，防止一些不规范的代码写法

    // 调试配置对象
    //按0开启日志，默认关闭
    const DEBUG = {
        enable: 1,    // 控制是否输出日志信息的开关
        deb: 1       // 控制是否在关键位置设置断点的开关
    };

//作者：Dexter
//公众号：我不是蜘蛛

    // 定义日志输出函数，根据 DEBUG.enable 决定是否输出日志
    const log = function(...args) {
        if (DEBUG.enable==0) {
            console.log(...args);
        }
    };

        // 保存原始的 setInterval 函数
        var originalSetInterval = window.setInterval;

        // 用新的函数替换原始的 setInterval
        window.setInterval = function(callback, delay) {
            // 获取除了 callback 和 delay 的其他额外参数
            var args = Array.prototype.slice.call(arguments, 2);

            // 如果 callback 是字符串，则删除其中的 debugger 语句
            if (typeof callback === 'string') {
                callback = callback.replace(/debugger;/g, '');
            } else if (typeof callback === 'function') {
                // 如果 callback 是函数，替换包含 debugger 的回调
                var originalCallback = callback;
                callback = function() {
                    // 获取原始回调函数的源码
                    var callbackSource = originalCallback.toString();

                    // 如果源码包含 debugger，将其删除并创建新的函数
                    if (callbackSource.indexOf('debugger') !== -1) {
                        callbackSource = callbackSource.replace(/debugger;/g, '');
                        originalCallback = new Function('return ' + callbackSource)();
                    }

                    // 调用修改后的回调函数，并传入参数
                    originalCallback.apply(this, arguments);
                };
            }

            // 调用原始的 setInterval 函数，并传入修改后的 callback、delay 和其他参数
            return originalSetInterval.apply(window, [callback, delay].concat(args));
        }
    //============ toString 相关防护 ============
    var temp_eval = eval;                      // 保存原始的 eval 函数
    var temp_toString = Function.prototype.toString;  // 保存原始的 toString 方法



    // 改进toString方法的处理
    Function.prototype.toString = function () {
        if (this === eval) {
            return 'function eval() { [native code] }';
        } else if (this === Function) {
            return 'function Function() { [native code] }';
        } else if (this === Function.prototype.toString) {
            return 'function toString() { [native code] }';
        } else if(this===window.setInterval){
            return 'function setInterval() { [native code] }';
        }
        return temp_toString.apply(this, arguments);
    }

    //============ eval 相关hook ============
    window.eval = function () {  // 重写全局 eval 函数
        const stackTrace = new Error().stack;  // 获取调用栈
        const callLocation = stackTrace;       // 保存调用位置
        log(callLocation);                     // 输出调用信息
        if (DEBUG.deb==0) {                       // 根据配置决定是否断点
            debugger;
        }
        log("=============== eval end ===============");

        // 处理传入的字符串参数，移除 debugger 语句
        if (typeof arguments[0] == "string") {
            var temp_length = arguments[0].match(/debugger/g);
            if (temp_length != null) {
                temp_length = temp_length.length;
                var reg = /debugger/;
                while (temp_length) {
                    arguments[0] = arguments[0].replace(reg, "");
                    temp_length--;
                }
            }
        }
        return temp_eval(...arguments);  // 使用原始 eval 执行处理后的代码
    }

    //============ Function 相关hook ============
    var _debugger = Function;  // 保存原始 Function 构造函数

    Function = function () {  // 重写 Function 构造函数
        const stackTrace = new Error().stack;  // 获取调用栈
        const callLocation = stackTrace;       // 保存调用位置
        log(callLocation);                     // 输出调用信息
        if (DEBUG.deb==0) {                       // 根据配置决定是否断点
            debugger;
        }
        log("=============== Function end ===============");

        // 处理所有参数中的 debugger 语句
        var reg = /debugger/;
        for (var i = 0; i < arguments.length; i++) {
            if (typeof arguments[i] == "string") {
                var temp_length = arguments[i].match(/debugger/g);
                if (temp_length != null) {
                    temp_length = temp_length.length;
                    while (temp_length) {
                        arguments[i] = arguments[i].replace(reg, "");
                        temp_length--;
                    }
                }
            }
        }
        return _debugger(...arguments);  // 使用原始 Function 构造函数创建函数
    }

    // 保持原型链的完整性
    Function.prototype = _debugger.prototype;

    // 重写 Function 构造函数的 constructor
    Function.prototype.constructor = function () {
        const stackTrace = new Error().stack;  // 获取调用栈
        const callLocation = stackTrace;       // 保存调用位置
        log(callLocation);                     // 输出调用信息
        if (DEBUG.deb==0) {                       // 根据配置决定是否断点
            debugger;
        }
        log("=============== Function constructor end ===============");

        // 处理所有参数中的 debugger 语句
        var reg = /debugger/;
        for (var i = 0; i < arguments.length; i++) {
            if (typeof arguments[i] == "string") {
                var temp_length = arguments[i].match(/debugger/g);
                if (temp_length != null) {
                    temp_length = temp_length.length;
                    while (temp_length) {
                        arguments[i] = arguments[i].replace(reg, "");
                        temp_length--;
                    }
                }
            }
        }
        return _debugger(...arguments);  // 使用原始 Function 构造函数
    }

    // 确保构造函数的原型链正确
    Function.prototype.constructor.prototype = Function.prototype;
})();