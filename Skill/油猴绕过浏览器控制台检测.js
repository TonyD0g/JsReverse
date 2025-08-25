// ==UserScript==
// @name         绕过控制台检测
// @version      v1.1
// @description  高性能且隐蔽的performance.now重写方案
// @author       TonyDog
// @match        *://*/*
// @run-at       document-start
// @grant        none
// @license      MIT
// ==/UserScript==
 
(function() {
    'use strict';
    window.close=function () {
 
    }
    window.history.back=function () {
 
    }
    window.history.forward=function () {
 
    }
    window.history.go=function () {
 
    }
    window.console.clear=function () {
 
    }
    window.console.log=function () {
 
    }
    window.console.table=function () {
 
    }
    setTimeout=function () {
 
    }
    setInterval=function () {
 
    }
})();