/**
 * Passli — Interactive UI Engine
 */

document.addEventListener('DOMContentLoaded', () => {
    initSharePassSimulator();
});

function initSharePassSimulator() {
    const docCheckboxes = document.querySelectorAll('.sim-doc-checkbox');
    const expirySelect = document.getElementById('sim-expiry-select');
    const viewPerm = document.getElementById('sim-perm-view');
    const downloadPerm = document.getElementById('sim-perm-download');
    const generateBtn = document.getElementById('sim-generate-btn');
    const keyDisplay = document.getElementById('sim-key-text');
    const expiryBadge = document.getElementById('sim-expiry-text');
    const docCountBadge = document.getElementById('sim-selected-count');
    const qrContainer = document.getElementById('sim-qr-preview');

    if (!generateBtn) return;

    function updateSelectedCount() {
        let count = 0;
        docCheckboxes.forEach(cb => {
            if (cb.checked) count++;
        });
        if (docCountBadge) {
            docCountBadge.textContent = `${count} Selected`;
        }
    }

    docCheckboxes.forEach(cb => {
        cb.addEventListener('change', updateSelectedCount);
    });

    generateBtn.addEventListener('click', () => {
        // Generate random key formatted like: 8K7P-42XM
        const chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
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

        // Animate button feedback
        const originalText = generateBtn.innerHTML;
        generateBtn.innerHTML = '<span>⚡ Generated!</span>';
        generateBtn.style.background = 'linear-gradient(135deg, #10b981, #059669)';
        
        setTimeout(() => {
            generateBtn.innerHTML = originalText;
            generateBtn.style.background = '';
        }, 1500);
    });
}
