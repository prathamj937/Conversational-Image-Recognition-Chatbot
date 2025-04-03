export function renderImagePreview(file) {
    const previewContainer = document.getElementById('imagePreview');
    previewContainer.innerHTML = '';
    
    const img = document.createElement('img');
    img.src = URL.createObjectURL(file);
    img.alt = 'Uploaded preview';
    img.onload = () => URL.revokeObjectURL(img.src);
    
    previewContainer.appendChild(img);
  }
  
  export function renderPrediction(prediction) {
    const resultsContainer = document.getElementById('predictionResults');
    resultsContainer.innerHTML = `
      <div class="prediction-item">
        <strong>Class:</strong> ${prediction.class}
      </div>
      <div class="prediction-item">
        <strong>Confidence:</strong> ${prediction.confidence}%
      </div>
      <div class="prediction-item">
        <strong>Model:</strong> ${prediction.modelType}
      </div>
    `;
  }
  
  export function clearResults() {
    document.getElementById('imagePreview').innerHTML = '';
    document.getElementById('predictionResults').innerHTML = '';
  }
  
  export function showLoading(elementId) {
    const element = document.getElementById(elementId);
    element.classList.add('loading');
  }
  
  export function hideLoading(elementId) {
    const element = document.getElementById(elementId);
    element.classList.remove('loading');
  }