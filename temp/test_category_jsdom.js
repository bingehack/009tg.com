const { JSDOM } = require('jsdom');
const fs = require('fs');
const html = fs.readFileSync('cn/category/2.html', 'utf8');
try {
    const dom = new JSDOM(html, { runScripts: 'dangerously', resources: 'usable' });
    console.log('JS执行完成，无致命错误');
    console.log('sites-container内容长度:', dom.window.document.getElementById('sites-container')?.innerHTML?.length || 0);
    setTimeout(() => {
        const content = dom.window.document.getElementById('sites-container')?.innerHTML || '';
        console.log('2秒后sites-container内容长度:', content.length);
        console.log('site-item数量:', (content.match(/class="site-item"/g) || []).length);
    }, 2000);
} catch(e) {
    console.log('JS运行时错误:', e.message);
}
