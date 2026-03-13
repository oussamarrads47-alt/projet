/* =====================================================
   TRANS-GEST — UI Scripts
   ===================================================== */

// ── Sidebar toggle (mobile) ──
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebar-overlay');
    sidebar.classList.toggle('open');
    overlay.classList.toggle('open');
}

document.addEventListener('DOMContentLoaded', function () {

    // ── Auto-close overlay on click ──
    const overlay = document.getElementById('sidebar-overlay');
    if (overlay) {
        overlay.addEventListener('click', toggleSidebar);
    }

    // ── Auto-dismiss flash messages after 4s ──
    document.querySelectorAll('.alert[data-auto-dismiss]').forEach(function (el) {
        setTimeout(function () {
            el.style.transition = 'opacity 0.4s';
            el.style.opacity = '0';
            setTimeout(function () { el.remove(); }, 400);
        }, 4000);
    });

    // ── Animate page content on load ──
    document.querySelectorAll('.animate-in').forEach(function (el, i) {
        el.style.animationDelay = (i * 60) + 'ms';
    });

});
