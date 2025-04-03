const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:3000/api';

export async function analyzeImage(file, modelType = 'auto') {
  try {
    // Convert image to base64
    const base64 = await convertToBase64(file);
    
    const response = await fetch(`${API_BASE}/predict`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        imageBase64: base64,
        modelType
      })
    });

    if (!response.ok) {
      throw new Error(`API Error: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error('API call failed:', error);
    throw error;
  }
}

function convertToBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result);
    reader.onerror = reject;
    reader.readAsDataURL(file);
  });
}

// Chat API (if using your own backend)
export async function sendChatMessage(message, context = '') {
  const response = await fetch(`${API_BASE}/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      message,
      context
    })
  });
  return await response.json();
}