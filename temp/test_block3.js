// 单独运行Block 3（站点渲染代码）检查运行时错误
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
            console.log('找到Block 3，长度:', js.length);
            break;
        }
    }
}

// 模拟jQuery
class MockjQuery {
    constructor(selector) {
        this.selector = selector;
        this.element = {
            innerHTML: '',
            style: {},
            classList: { add: () => {}, remove: () => {} },
        };
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
}

const containers = {};
global.$ = function(selector) {
    if (!containers[selector]) {
        containers[selector] = new MockjQuery(selector);
    }
    return containers[selector];
};
global.$.fn = {};
global.$.ready = function(cb) { cb(); };

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
global.setTimeout = (cb, ms) => { cb(); return 0; };
global.lozad = function() { return { observe: () => {} }; };

console.log('\n开始运行Block 3代码...');
try {
    eval(block3JS);
    console.log('Block 3执行完成，无致命错误');
    
    setTimeout(() => {
        console.log('\n=== 结果检查 ===');
        const container = containers['#sites-container'];
        if (container) {
            console.log('sites-container内容长度:', container.element.innerHTML.length);
            const siteCount = (container.element.innerHTML.match(/class="site-item"/g) || []).length;
            console.log('site-item数量:', siteCount);
            if (siteCount > 0) {
                console.log('第一个站点片段:', container.element.innerHTML.substring(0, 150));
            }
        } else {
            console.log('未找到#sites-container容器');
            console.log('所有容器:', Object.keys(containers));
        }
    }, 300);
} catch (e) {
    console.log('Block 3运行时错误:', e.message);
    console.log('错误堆栈:', e.stack);
}
