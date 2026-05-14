/**
 * Retro Alert System
 * Replaces standard window.alert with a stylized in-page modal.
 */

function showRetroAlert(message, callback) {
    // Create overlay if it doesn't exist
    let overlay = document.getElementById('retro-alert-overlay');
    
    if (!overlay) {
        overlay = document.createElement('div');
        overlay.id = 'retro-alert-overlay';
        overlay.className = 'retro-modal-overlay';
        overlay.innerHTML = `
            <div class="retro-modal-window">
                <div class="retro-modal-header">
                    <span>// OLD SCHOOL GAMES — SYS MSG</span>
                    <span>[ESC]</span>
                </div>
                <div class="retro-modal-content">
                    <span id="retro-alert-text"></span><span class="retro-cursor"></span>
                </div>
                <div class="retro-modal-footer">
                    <button id="retro-alert-btn" class="retro-btn">OK</button>
                </div>
            </div>
        `;
        document.body.appendChild(overlay);
    }
    
    const textEl = document.getElementById('retro-alert-text');
    const btn = document.getElementById('retro-alert-btn');
    
    textEl.textContent = message;
    overlay.classList.add('active');
    
    // Focus button
    btn.focus();
    
    const closeAlert = () => {
        overlay.classList.remove('active');
        if (callback && typeof callback === 'function') {
            callback();
        }
        // Clean up listeners
        btn.removeEventListener('click', closeAlert);
        window.removeEventListener('keydown', handleEsc);
    };
    
    const handleEsc = (e) => {
        if (e.key === 'Enter' || e.key === 'Escape') {
            closeAlert();
        }
    };
    
    btn.addEventListener('click', closeAlert);
    window.addEventListener('keydown', handleEsc);
}

// Override global alert (optional, but requested)
window.alert = function(msg) {
    showRetroAlert(msg);
};
