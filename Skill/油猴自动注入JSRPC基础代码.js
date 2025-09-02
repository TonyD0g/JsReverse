// ==UserScript==
// @name         jsrpc-auto-inject
// @version      v1
// @description  用于自动注入JSRPC基础代码,从而为注入自定义function做准备,减少人的使用操作(需要开启JSRPC)
// @author       TonyD0g
// @match        *://*/*
// @include      *://*/*
// @run-at       document-start
// @license      MIT
// ==/UserScript==

(function() {  // 立即执行函数，创建独立作用域
   // 创建提示框元素
const toast = document.createElement('div');
toast.id = 'custom-toast-notification';
toast.style.cssText = `
        position: fixed;
        top: 20px;
        left: 50%;
        transform: translateX(-50%);
        background-color: rgba(144, 238, 144, 1); /* 亮黄色背景 */
        color: #333; /* 深灰色文字 */
        padding: 12px 24px;
        border-radius: 6px;
        font-family: Arial, sans-serif;
        font-size: 16px; /* 增大字体大小 */
        z-index: 9999;
        opacity: 0;
        transition: opacity 0.5s ease-in-out;
        text-align: center;
        max-width: 80%;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25); /* 更深的阴影 */
        pointer-events: none;
    `;

// 添加到页面
document.body.appendChild(toast);

// 显示消息的函数
function showMessage(message) {
    // 设置消息内容
    toast.textContent = message;
    toast.style.opacity = '1';

    // 3秒后隐藏
    setTimeout(() => {
        toast.style.opacity = '0';

        // 动画完成后移除元素（可选）
        setTimeout(() => {
            toast.remove();
        }, 500);
    }, 3000);
}

// 将函数暴露到全局，以便在其他地方调用
window.showToastMessage = showMessage;

var rpc_client_id, Hlclient = function(wsURL) {
    this.wsURL = wsURL;
    this.handlers = {
        _execjs: function(resolve, param) {
            var res = eval(param)
            if (!res) {
                resolve("没有返回值")
            } else {
                resolve(res)
            }
        }
    };
    this.socket = undefined;
    if (!wsURL) {
        throw new Error('wsURL can not be empty!!')
    }
    this.connect()
}
Hlclient.prototype.connect = function() {
    if (this.wsURL.indexOf("clientId=") === -1 && rpc_client_id) {
        this.wsURL += "&clientId=" + rpc_client_id
    }
    console.log('begin of connect to wsURL: ' + this.wsURL);
    var _this = this;
    try {
        this.socket = new WebSocket(this.wsURL);
        this.socket.onmessage = function(e) {
            _this.handlerRequest(e.data)
        }
    } catch (e) {
        console.log("connection failed,reconnect after 10s");
        setTimeout(function() {
            _this.connect()
        }, 10000)
    }
    this.socket.onclose = function() {
        console.log('rpc已关闭');
        setTimeout(function() {
            _this.connect()
        }, 10000)
    }
    this.socket.addEventListener('open', (event) => {
        console.log("rpc连接成功");
    });
    this.socket.addEventListener('error', (event) => {
        console.error('rpc连接出错,请检查是否打开服务端:', event.error);
    })
};
Hlclient.prototype.send = function(msg) {
    this.socket.send(msg)
}
Hlclient.prototype.regAction = function(func_name, func) {
    if (typeof func_name !== 'string') {
        throw new Error("an func_name must be string");
    }
    if (typeof func !== 'function') {
        throw new Error("must be function");
    }
    console.log("register func_name: " + func_name);
    this.handlers[func_name] = func;
    return true
}
Hlclient.prototype.handlerRequest = function(requestJson) {
    var _this = this;
    try {
        var result = JSON.parse(requestJson)
    } catch (error) {
        console.log("请求信息解析错误", requestJson);
        return
    }
    if (result["registerId"]) {
        rpc_client_id = result['registerId']
        return
    }
    if (!result['action'] || !result["message_id"]) {
        console.warn('没有方法或者消息id,不处理');
        return
    }
    var action = result["action"],
        message_id = result["message_id"]
    var theHandler = this.handlers[action];
    if (!theHandler) {
        this.sendResult(action, message_id, 'action没找到');
        return
    }
    try {
        if (!result["param"]) {
            theHandler(function(response) {
                _this.sendResult(action, message_id, response);
            })
            return
        }
        var param = result["param"]
        try {
            param = JSON.parse(param)
        } catch (e) {}
        theHandler(function(response) {
            _this.sendResult(action, message_id, response);
        }, param)
    } catch (e) {
        console.log("error: " + e);
        _this.sendResult(action, message_id, e);
    }
}
Hlclient.prototype.sendResult = function(action, message_id, e) {
    if (typeof e === 'object' && e !== null) {
        try {
            e = JSON.stringify(e)
        } catch (v) {
            console.log(v) //不是json无需操作
        }
    }
    this.send(JSON.stringify({
        "action": action,
        "message_id": message_id,
        "response_data": e
    }));
}

window.Hlclient = Hlclient;
var demo = new Hlclient("ws://127.0.0.1:12080/ws?group=zzz");
showMessage('JSRPC已成功注入!');
})();