document.addEventListener('DOMContentLoaded', () => {
    // Tab switching logic
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const target = btn.dataset.target;
            
            // Remove active class from all
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));
            
            // Add active class to selected
            btn.classList.add('active');
            document.getElementById(target).classList.add('active');
        });
    });

    // Form Submissions
    const scanForm = document.getElementById('scan-form');
    if(scanForm) {
        scanForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const btn = scanForm.querySelector('button[type="submit"]');
            const originalText = btn.innerHTML;
            btn.innerHTML = '<span>Scanning...</span>';
            btn.disabled = true;
            
            const formData = new FormData(scanForm);
            
            try {
                const response = await fetch('/api/scan/', {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken')
                    }
                });
                
                const data = await response.json();
                displayResult(data);
            } catch (error) {
                console.error('Error scanning:', error);
                alert('An error occurred during the scan. Please try again.');
            } finally {
                btn.innerHTML = originalText;
                btn.disabled = false;
            }
        });
    }
});

function displayResult(data) {
    const resultBox = document.getElementById('result-box');
    const resultIcon = document.getElementById('result-icon');
    const resultTitle = document.getElementById('result-title');
    const resultDesc = document.getElementById('result-desc');
    const confidenceText = document.getElementById('confidence-text');
    
    // Reset classes
    resultBox.className = 'result-box glass-card';
    resultBox.classList.add(data.prediction);
    
    if(data.prediction === 'phishing') {
        resultIcon.innerHTML = '🚨';
        resultTitle.textContent = 'Phishing Detected!';
        resultDesc.textContent = 'This message contains elements commonly found in phishing attempts. Do not click any links or share sensitive information.';
    } else {
        resultIcon.innerHTML = '✅';
        resultTitle.textContent = 'Looks Legitimate';
        resultDesc.textContent = 'No obvious signs of phishing were detected. However, always exercise caution with unexpected messages.';
    }
    
    confidenceText.textContent = `Confidence: ${data.confidence}%`;
}

// Utility function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
