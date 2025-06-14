// TDS Virtual TA Frontend JavaScript
document.addEventListener('DOMContentLoaded', function() {
    const questionForm = document.getElementById('questionForm');
    const questionInput = document.getElementById('questionInput');
    const imageInput = document.getElementById('imageInput');
    const submitBtn = document.getElementById('submitBtn');
    const loadingIndicator = document.getElementById('loadingIndicator');
    const responseCard = document.getElementById('responseCard');
    const answerContent = document.getElementById('answerContent');
    const linksSection = document.getElementById('linksSection');
    const linksList = document.getElementById('linksList');
    const errorAlert = document.getElementById('errorAlert');
    const errorMessage = document.getElementById('errorMessage');

    // Handle form submission
    questionForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const question = questionInput.value.trim();
        if (!question) {
            showError('Please enter a question');
            return;
        }

        // Prepare request data
        const requestData = { question: question };
        
        // Handle image upload
        if (imageInput.files.length > 0) {
            try {
                const imageBase64 = await fileToBase64(imageInput.files[0]);
                requestData.image = imageBase64;
            } catch (error) {
                showError('Error processing image file');
                return;
            }
        }

        // Show loading state
        showLoading();
        
        try {
            const response = await fetch('/api/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(requestData)
            });

            const data = await response.json();
            
            if (response.ok) {
                showResponse(data);
            } else {
                showError(data.error || 'An error occurred while processing your question');
            }
        } catch (error) {
            console.error('API Error:', error);
            showError('Network error. Please check your connection and try again.');
        } finally {
            hideLoading();
        }
    });

    // Convert file to base64
    function fileToBase64(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.readAsDataURL(file);
            reader.onload = () => {
                // Remove the data URL prefix to get just the base64 string
                const base64 = reader.result.split(',')[1];
                resolve(base64);
            };
            reader.onerror = error => reject(error);
        });
    }

    // Show loading state
    function showLoading() {
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
        loadingIndicator.style.display = 'block';
        responseCard.style.display = 'none';
        errorAlert.style.display = 'none';
    }

    // Hide loading state
    function hideLoading() {
        submitBtn.disabled = false;
        submitBtn.innerHTML = '<i class="fas fa-paper-plane me-2"></i>Ask Question';
        loadingIndicator.style.display = 'none';
    }

    // Show response
    function showResponse(data) {
        answerContent.textContent = data.answer;
        
        // Show links if available
        if (data.links && data.links.length > 0) {
            linksList.innerHTML = '';
            data.links.forEach(link => {
                const linkElement = document.createElement('a');
                linkElement.href = link.url;
                linkElement.target = '_blank';
                linkElement.className = 'link-item';
                linkElement.innerHTML = `
                    <i class="fas fa-external-link-alt me-2"></i>
                    ${escapeHtml(link.text)}
                `;
                linksList.appendChild(linkElement);
            });
            linksSection.style.display = 'block';
        } else {
            linksSection.style.display = 'none';
        }
        
        responseCard.style.display = 'block';
        
        // Scroll to response
        responseCard.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    // Show error message
    function showError(message) {
        errorMessage.textContent = message;
        errorAlert.style.display = 'block';
        responseCard.style.display = 'none';
        
        // Scroll to error
        errorAlert.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    // Escape HTML to prevent XSS
    function escapeHtml(text) {
        const map = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#039;'
        };
        return text.replace(/[&<>"']/g, function(m) { return map[m]; });
    }

    // Add some example questions for better UX
    const exampleQuestions = [
        "How do I use pandas DataFrames?",
        "What's the difference between list and tuple in Python?",
        "How do I create visualizations with matplotlib?",
        "What are the best practices for Git version control?",
        "How do I set up a virtual environment in Python?"
    ];

    // Add click handlers for example questions
    const placeholderElement = questionInput;
    let currentExample = 0;
    
    // Cycle through examples as placeholder
    function cyclePlaceholder() {
        if (questionInput.value === '') {
            questionInput.placeholder = `e.g., ${exampleQuestions[currentExample]}`;
            currentExample = (currentExample + 1) % exampleQuestions.length;
        }
    }
    
    // Change placeholder every 3 seconds
    setInterval(cyclePlaceholder, 3000);
});