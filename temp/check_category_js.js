
// --- Script Block 4 ---

        function initTheme() {
            var savedTheme = localStorage.getItem('theme');
            if (savedTheme) {
                document.documentElement.setAttribute('data-theme', savedTheme);
                updateThemeIcon(savedTheme);
            } else {
                if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
                    document.documentElement.setAttribute('data-theme', 'dark');
                    updateThemeIcon('dark');
                }
            }
        }
        function toggleTheme() {
            var currentTheme = document.documentElement.getAttribute('data-theme');
            var newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            updateThemeIcon(newTheme);
        }
        function updateThemeIcon(theme) {
            var icon = document.getElementById('theme-icon');
            if (icon) {
                if (theme === 'dark') {
                    icon.className = 'fa-sun-o';
                    icon.parentElement.title = '切换到浅色模式';
                } else {
                    icon.className = 'fa-moon-o';
                    icon.parentElement.title = '切换到深色模式';
                }
            }
        }
        initTheme();
        if (window.matchMedia) {
            window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function(e) {
                if (!localStorage.getItem('theme')) {
                    if (e.matches) {
                        document.documentElement.setAttribute('data-theme', 'dark');
                        updateThemeIcon('dark');
                    } else {
                        document.documentElement.removeAttribute('data-theme');
                        updateThemeIcon('light');
                    }
                }
            });
        }
    
// --- Script Block 12 ---

        function backToTop(){var s={p:window.scrollY||document.documentElement.scrollTop},t=performance.now();function a(n){var e=Math.min((n-t)/300,1);window.scrollTo(0,s.p*(1-Math.pow(1-e,3)));e<1&&requestAnimationFrame(a)}requestAnimationFrame(a)}
        window.addEventListener('scroll',function(){var b=document.querySelector('.back-to-top');if(b){window.scrollY>300?b.classList.add('show'):b.classList.remove('show')}});
    
