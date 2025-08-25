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
    fetch('http://127.0.0.1:5000/accept', {
        method: 'POST',
        headers: { 'Content-Type': 'text/plain' },
        body: sendValue
    })
    .then(response => {
        if (!response.ok) throw new Error('请求失败');
        return response.json();
    })
    .then(data => console.log('成功:', data))
    .catch(error => console.error('错误:', error));
}