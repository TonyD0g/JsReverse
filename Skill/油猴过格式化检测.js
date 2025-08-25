// ==UserScript==
// @name         过格式化检测
// @version      v1.1
// @description  绕过js检测代码是否被格式化过
// @author       0xsdeo
// @match        *://*/*
// @run-at       document-start
// @grant        none
// @license      MIT
// ==/UserScript==

(function() {
    'use strict';

    let temp_toString = Function.prototype.toString;

    Function.prototype.toString = function () {
        let toString_result = temp_toString.apply(this, arguments);
        if (this === Function.prototype.toString) {
            return 'function toString() { [native code] }';
        } else {
            if (typeof toString_result == "string") {
                toString_result = toString_result.replace(/\s/g, '');
                if (toString_result.slice(0, 8) === 'function') {
                    toString_result = toString_result.slice(0, 8) + ' ' + toString_result.slice(8);
                }
            }
            return toString_result;
        }
    }
})();