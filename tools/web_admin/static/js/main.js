// 009tg管理后台通用JS

$(document).ready(function() {
    // 导航栏当前页高亮
    var path = window.location.pathname;
    $('.nav.navbar-nav > li').removeClass('active');
    if (path === '/' || path === '/dashboard') {
        $('.nav.navbar-nav > li:eq(0)').addClass('active');
    } else if (path.indexOf('/crawl') >= 0) {
        $('.nav.navbar-nav > li:eq(1)').addClass('active');
    } else if (path.indexOf('/merge') >= 0) {
        $('.nav.navbar-nav > li:eq(2)').addClass('active');
    } else if (path.indexOf('/manage') >= 0) {
        $('.nav.navbar-nav > li:eq(3)').addClass('active');
    }
});

// 通用工具函数
var AdminUtil = {
    // 格式化数字
    formatNumber: function(num) {
        return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    },

    // 显示提示
    showToast: function(message, type) {
        type = type || 'info';
        var icon = {
            success: 'fa-check-circle',
            error: 'fa-exclamation-circle',
            warning: 'fa-exclamation-triangle',
            info: 'fa-info-circle'
        }[type] || 'fa-info-circle';

        var bgColor = {
            success: '#5cb85c',
            error: '#d9534f',
            warning: '#f0ad4e',
            info: '#5bc0de'
        }[type] || '#5bc0de';

        var toast = $('<div>').css({
            position: 'fixed',
            top: '80px',
            right: '20px',
            background: bgColor,
            color: '#fff',
            padding: '15px 20px',
            borderRadius: '6px',
            boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
            zIndex: 9999,
            maxWidth: '400px',
            fontSize: '14px'
        }).html('<i class="fa ' + icon + '"></i> ' + message);

        $('body').append(toast);
        toast.fadeIn(300);

        setTimeout(function() {
            toast.fadeOut(300, function() {
                $(this).remove();
            });
        }, 3000);
    },

    // 确认对话框
    confirm: function(message, callback) {
        if (confirm(message)) {
            callback();
        }
    },

    // 复制到剪贴板
    copyToClipboard: function(text) {
        var textarea = $('<textarea>').val(text).css({position: 'fixed', opacity: 0});
        $('body').append(textarea);
        textarea.select();
        try {
            document.execCommand('copy');
            this.showToast('已复制到剪贴板', 'success');
        } catch (e) {
            this.showToast('复制失败', 'error');
        }
        textarea.remove();
    }
};
