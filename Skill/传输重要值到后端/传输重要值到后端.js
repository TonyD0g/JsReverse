// 将 clearSessionStorage 方法放在需要清除状态的位置
function clearSessionStorage() {
  sessionStorage.setItem('isInitialized', 'false');
}

// 将 initializeSession 方法放在你想传输的位置,传参为要发送到后端的值 
function initializeSession(sendValue) {
    // 1. 检查浏览器是否支持 sessionStorage
    if (typeof(Storage) === 'undefined') {
        console.error("浏览器不支持 sessionStorage，初始化跳过");
        return;
    }

    // 2. 检查标记是否存在（避免重复执行）
    if (sessionStorage.getItem('isInitialized') === 'true') return;

    // 3. 立即设置标记（防止并发重复）[1,2](@ref)
    sessionStorage.setItem('isInitialized', 'true');

    try {
        sendInitializationRequest(sendValue);
        console.log("开始阻塞");
        blockMainThread(3000); // 阻塞 3 秒
        console.log("阻塞结束");
    } catch (error) {
        // 5. 失败时清除标记（允许重试）[3](@ref)
        sessionStorage.removeItem('isInitialized');
        console.error("初始化失败：", error);
    }
}

// 阻塞主线程,这段时间内让后端赶紧处理
function blockMainThread(ms) {
        const start = Date.now();
        while (Date.now() - start < ms) {
          // 空循环，持续占用 CPU
        }
      }

// 实际发送到后端的代码
function sendInitializationRequest(sendValue) {
    // 初始化请求配置
    const config = {
        method: 'POST',
        headers: {},
        body: null
    };

    // 根据数据类型设置 Content-Type 和请求体
    if (sendValue instanceof FormData) {
        config.body = sendValue;
        // 不设置 Content-Type，浏览器会自动生成带 boundary 的格式 
    } else if (sendValue instanceof URLSearchParams) {
        config.body = sendValue;
        config.headers['Content-Type'] = 'application/x-www-form-urlencoded';
    } else if (typeof sendValue === 'string' && sendValue.startsWith('<')) {
        config.body = sendValue;
        config.headers['Content-Type'] = 'application/xml; charset=UTF-8';
    } else if (typeof sendValue === 'string') {
        config.body = sendValue;
        config.headers['Content-Type'] = 'text/plain; charset=UTF-8';
    } else if (sendValue instanceof Blob) {
        config.body = sendValue;
        config.headers['Content-Type'] = sendValue.type || 'application/octet-stream';
    } else {
        // 默认 JSON 类型
        config.body = JSON.stringify(sendValue);
        config.headers['Content-Type'] = 'application/json; charset=UTF-8';
    }

    // 发送请求并仅检查状态码
    fetch('http://127.0.0.1:5000/accept', config)
        .then(response => {
            if (response.ok) {
                console.log(`请求成功，状态码: ${response.status}`);
                return Promise.resolve();
            } else {
                throw new Error(`请求失败，状态码: ${response.status}`);
            }
        })
        .catch(error => console.error('错误:', error));
}