// 模拟jQuery基本功能，运行分类页JS代码检查运行时错误
const fs = require('fs');

// 读取分类页
const html = fs.readFileSync('cn/category/2.html', 'utf8');

// 提取所有script块
const scriptRegex = /<script[^>]*>([\s\S]*?)<\/script>/g;
let match;
let allJS = '';
while ((match = scriptRegex.exec(html)) !== null) {
    const js = match[1].trim();
    if (js.length > 0 && !js.includes('src=')) {
        allJS += '\n// --- Script Block ---\n' + js;
    }
}

// 模拟jQuery
const mockElements = [];
class MockjQuery {
    constructor(selector) {
        this.selector = selector;
        this.element = {
            innerHTML: '',
            style: {},
            classList: { add: () => {}, remove: () => {} },
            appendChild: (child) => { this.element.innerHTML += child; },
        };
        mockElements.push({ selector, element: this.element });
    }
    empty() { this.element.innerHTML = ''; return this; }
    css(prop, val) { 
        if (typeof prop === 'object') {
            Object.assign(this.element.style, prop);
        } else {
            this.element.style[prop] = val;
        }
        return this; 
    }
    append(html) { 
        if (typeof html === 'string') {
            this.element.innerHTML += html;
        }
        return this; 
    }
    text(val) { return this; }
    prop(prop, val) { return this; }
    click(handler) { return this; }
    width() { return 1200; }
    on(event, handler) { return this; }
}

global.$ = function(selector) {
    return new MockjQuery(selector);
};
global.$.fn = {};

// 模拟document
global.document = {
    getElementById: (id) => {
        return { innerHTML: '', style: {} };
    },
    documentElement: { style: {} },
};
global.window = {
    scrollY: 0,
    addEventListener: () => {},
    matchMedia: () => ({ matches: false }),
    localStorage: { getItem: () => null, setItem: () => {} },
};
global.performance = { now: () => Date.now() };
global.requestAnimationFrame = (cb) => setTimeout(cb, 16);
global.setTimeout = (cb, ms) => { cb(); return 0; }; // 立即执行
global.localStorage = { getItem: () => null, setItem: () => {} };

console.log('开始运行分类页JS代码...');
console.log('JS代码长度:', allJS.length);

try {
    eval(allJS);
    console.log('JS代码执行完成，无致命错误');
    
    // 等待一下让setTimeout执行
    setTimeout(() => {
        console.log('\n=== 执行结果检查 ===');
        console.log('模拟的jQuery元素数量:', mockElements.length);
        mockElements.forEach((m, i) => {
            if (m.selector === '#sites-container') {
                console.log(`sites-container内容长度: ${m.element.innerHTML.length}`);
                const siteCount = (m.element.innerHTML.match(/class="site-item"/g) || []).length;
                console.log(`site-item数量: ${siteCount}`);
                if (siteCount > 0) {
                    console.log('第一个站点HTML片段:', m.element.innerHTML.substring(0, 200));
                }
            }
        });
    }, 500);
} catch (e) {
    console.log('JS运行时错误:', e.message);
    console.log('错误堆栈:', e.stack);
}
