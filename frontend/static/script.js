document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('predict-form');
    const messageInput = document.getElementById('message');
    const submitBtn = document.getElementById('submit-btn');
    const resultDiv = document.getElementById('result');
    const resultBadge = document.getElementById('result-badge');
    const errorDiv = document.getElementById('error');

    form.addEventListener('submit', async function (e) {
        e.preventDefault();

        const message = messageInput.value.trim();
        if (!message) {
            showError('Please enter a message to analyze.');
            return;
        }

        // Disable button and show loading state
        submitBtn.disabled = true;
        submitBtn.textContent = 'Analyzing...';
        resultDiv.classList.add('hidden');
        errorDiv.classList.add('hidden');

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message }),
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'An error occurred.');
            }

            // Display result
            resultBadge.textContent = data.prediction;
            resultBadge.className = 'badge ' + data.prediction.toLowerCase();
            resultDiv.classList.remove('hidden');
        } catch (err) {
            showError(err.message);
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = 'Analyze Message';
        }
    });

    function showError(msg) {
        errorDiv.textContent = msg;
        errorDiv.classList.remove('hidden');
    }
});