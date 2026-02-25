// ============================================
//  THEME TOGGLE — Dark / Light Mode
// ============================================

(function () {
    const STORAGE_KEY = 'studsafe-theme';

    // Apply saved theme ASAP to prevent flash
    function applySavedTheme() {
        const saved = localStorage.getItem(STORAGE_KEY);
        // Default to light if nothing saved
        const theme = saved || 'light';
        document.documentElement.setAttribute('data-theme', theme);
        return theme;
    }

    const currentTheme = applySavedTheme();

    document.addEventListener('DOMContentLoaded', function () {
        const toggleBtn = document.getElementById('theme-toggle');
        if (!toggleBtn) return;

        const icon = toggleBtn.querySelector('.theme-toggle-icon');

        // Set initial icon
        updateIcon(icon, currentTheme);

        toggleBtn.addEventListener('click', function () {
            const html = document.documentElement;
            const current = html.getAttribute('data-theme') || 'light';
            const next = current === 'dark' ? 'light' : 'dark';

            html.setAttribute('data-theme', next);
            localStorage.setItem(STORAGE_KEY, next);
            updateIcon(icon, next);
        });
    });

    function updateIcon(iconEl, theme) {
        if (!iconEl) return;
        // Show moon in light mode (click to go dark), sun in dark mode (click to go light)
        iconEl.textContent = theme === 'dark' ? '🌞' : '🌚';
        iconEl.parentElement.setAttribute(
            'title',
            theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'
        );
    }
})();

// ============================================
//  AUTO-DISMISS ALERT MESSAGES
// ============================================
document.addEventListener('DOMContentLoaded', function () {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function (alert) {
        // Fade out after 4 seconds
        setTimeout(function () {
            alert.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            alert.style.opacity = '0';
            alert.style.transform = 'translateX(30px)';
            // Remove from DOM after animation
            setTimeout(function () {
                alert.remove();
            }, 500);
        }, 4000);
    });
});
