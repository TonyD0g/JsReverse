/**
 * 前言:适用于目标检测控制台的情况但绕不过去的情况,利用本方法可将大部分变量瞬间全部导出
 * 使用方法:
 * 1.浏览器下载 Header Editor 插件
 * 2.添加一个规则: 
 *    匹配类型: 目标js的正则表达式
 *    执行: 
 *        请求阶段: 响应
 *        响应头: 先抓个包,把原js的header头copy下来,打开一个AI,问:`请将以下内容转换为json中的键值对`
 *        响应体: 
 *              使用本目录下的`AST注册所有变量到window.js`文件,将原js进行AST处理.
 *              删除AST处理后的console.log,防止因目标的检测而无法生效.
 *              加入本文件的代码,注意替换`定义待导出的对象数据`
 *              进行压缩,防止目标检测格式化(https://www.jijie.ink/tool/js-formatter)
 *              经过以上步骤后,最新的js代码放入`响应体`
 *              点击`保存`按钮
 * 3.浏览器清除下状态防止js缓存导致的失效 + 刷新
 * 4.最好挂上burp等代理软件查看js数据包是否304跳转(如果304跳转了则说明成功替换原js).
 * **/

function safeStringify(obj) {
  const seen = new WeakSet();
  return JSON.stringify(obj, (key, value) => {
    // 检测到循环引用时返回标记
    if (typeof value === 'object' && value !== null) {
      if (seen.has(value)) return '[Circular Reference]';
      seen.add(value);
    }
    return value;
  }, 2); // 缩进2空格美化输出
}

// 1. 定义待导出的对象数据
const outputData = {
  "xxxx": window.xxxx
};

// 2. 将对象转换为格式化JSON字符串
const jsonString = safeStringify(outputData);

// 3. 创建Blob对象并生成下载链接
const blob = new Blob([jsonString], { type: 'application/json' });
const url = URL.createObjectURL(blob);
const a = document.createElement('a');
a.href = url;
a.download = 'window_variables.json'; // 自定义文件名

// 4. 触发下载
document.body.appendChild(a);
a.click();

// 5. 清理资源
setTimeout(() => {
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}, 100);