// 修复模拟，正确处理$(document).ready
const fs = require('fs');

const html = fs.readFileSync('cn/category/2.html', 'utf8');
const scriptRegex = /<script[^>]*>([\s\S]*?)<\/script>/g;
let match;
let blockIndex = 0;
let block3JS = '';

while ((match = scriptRegex.exec(html)) !== null) {
    const js = match[1].trim();
    if (js.length > 0 && !js.includes('src=')) {
        blockIndex++;
        if (blockIndex === 3) {
            block3JS = js;
            break;
        }
    }
}

console.log('Block 3长度:', block3JS.length);

// 模拟jQuery - 正确处理$(document).ready
const containers = {};
class MockjQuery {
    constructor(selector) {
        this.selector = selector;
        this.element = {
            innerHTML: '',
            style: {},
            classList: { add: () => {}, remove: () => {} },
        };
        containers[selector] = this;
    }
    empty() { this.element.innerHTML = ''; return this; }
    css(prop, val) { 
        if (typeof prop === 'object') Object.assign(this.element.style, prop);
        else this.element.style[prop] = val;
        return this; 
    }
    append(html) { 
        if (typeof html === 'string') this.element.innerHTML += html;
        return this; 
    }
    text(val) { return this; }
    prop(prop, val) { return this; }
    click(handler) { return this; }
    width() { return 1200; }
    on(event, handler) { return this; }
    ready(cb) { 
        console.log('$(document).ready被调用，立即执行回调');
        cb(); 
        return this; 
    }
    resize(handler) { return this; }
}

global.$ = function(selector) {
    return new MockjQuery(selector);
};
global.$.fn = {};

global.document = {
    getElementById: (id) => containers['#' + id]?.element || { innerHTML: '', style: {} },
    documentElement: { style: {} },
    querySelector: () => null,
};
global.window = {
    scrollY: 0,
    addEventListener: () => {},
    matchMedia: () => ({ matches: false, addEventListener: () => {} }),
    localStorage: { getItem: () => null, setItem: () => {} },
};
global.performance = { now: () => Date.now() };
global.requestAnimationFrame = (cb) => setTimeout(cb, 16);
global.setTimeout = (cb, ms) => { 
    console.log(`setTimeout被调用，延迟${ms}ms，立即执行`);
    cb(); 
    return 0; 
};
global.lozad = function() { return { observe: () => {} }; };

console.log('\n开始运行Block 3代码...');
try {
    eval(block3JS);
    console.log('Block 3执行完成');
    
    console.log('\n=== 结果检查 ===');
    console.log('所有容器:', Object.keys(containers));
    const container = containers['#sites-container'];
    if (container) {
        console.log('sites-container内容长度:', container.element.innerHTML.length);
        const siteCount = (container.element.innerHTML.match(/class="site-item"/g) || []).length;
        console.log('site-item数量:', siteCount);
        if (siteCount > 0) {
            console.log('第一个站点片段:', container.element.innerHTML.substring(0, 200));
        }
    }
} catch (e) {
    console.log('Block 3运行时错误:', e.message);
    console.log('错误堆栈:', e.stack);
}
