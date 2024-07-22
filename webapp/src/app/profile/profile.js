// script.js
document.addEventListener('DOMContentLoaded', function() {
    const descriptionDiv = document.querySelector('.description');
    const placeholderText = 'Description';
    
    descriptionDiv.setAttribute('data-placeholder', placeholderText);
    
    descriptionDiv.addEventListener('focus', function() {
        const placeholder = this.querySelector('.placeholder');
        if (placeholder) {
            placeholder.remove();
        }
    });
    
    descriptionDiv.addEventListener('blur', function() {
        if (this.textContent.trim() === '') {
            this.innerHTML = `<span class="placeholder">${placeholderText}</span>`;
        }
    });
});
