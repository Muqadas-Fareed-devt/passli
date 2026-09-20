/**
 * Passli — Clean Human-Crafted Interactive Elements
 */

document.addEventListener('DOMContentLoaded', () => {
    initSharePassSimulator();
});

function initSharePassSimulator() {
    const docCheckboxes = document.querySelectorAll('.sim-doc-checkbox');
    const expirySelect = document.getElementById('sim-expiry-select');
    const generateBtn = document.getElementById('sim-generate-btn');
    const keyDisplay = document.getElementById('sim-key-text');
    const expiryBadge = document.getElementById('sim-expiry-text');

    if (!generateBtn) return;

    docCheckboxes.forEach(cb => {
        cb.addEventListener('change', (e) => {
            const row = e.target.closest('.mockup-doc-row');
            if (row) {
                if (e.target.checked) {
                    row.classList.add('active');
                } else {
                    row.classList.remove('active');
                }
            }
        });
    });

    generateBtn.addEventListener('click', () => {
        // Generate random 8-character key
        const chars = '23456789ABCDEFGHJKLMNPQRSTUVWXYZ';
        let key = '';
        for (let i = 0; i < 8; i++) {
            if (i === 4) key += '-';
            key += chars.charAt(Math.floor(Math.random() * chars.length));
        }

        if (keyDisplay) {
            keyDisplay.textContent = key;
        }

        if (expiryBadge && expirySelect) {
            expiryBadge.textContent = expirySelect.options[expirySelect.selectedIndex].text;
        }

        const originalText = generateBtn.textContent;
        generateBtn.textContent = 'Pass Generated';
        generateBtn.disabled = true;

        setTimeout(() => {
            generateBtn.textContent = originalText;
            generateBtn.disabled = false;
        }, 1200);
    });
}
