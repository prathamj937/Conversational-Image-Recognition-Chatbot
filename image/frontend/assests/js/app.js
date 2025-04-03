import { analyzeImage } from './api.js';
import { renderImagePreview, renderPrediction, clearResults } from './ui.js';
import chatSystem from './chat.js';

// DOM Elements
const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
const modelType = document.getElementById('modelType');
const chatInput = document.getElementById('chatInput');
const sendButton = document.getElementById('sendButton');

// Event Listeners
dropZone.addEventListener('click', () => fileInput.click());
dropZone.addEventListener('dragover', handleDragOver);
dropZone.addEventListener('drop', handleDrop);
// Debug: Add these console logs to verify event binding
fileInput.addEventListener('change', (e) => {
  console.log('File selected:', e.target.files[0]); // Check browser console
  handleFileSelect(e);
});

dropZone.addEventListener('drop', (e) => {
  e.preventDefault();
  console.log('File dropped:', e.dataTransfer.files[0]); // Check browser console
  handleDrop(e);
});

// Add visual feedback for drag-over
dropZone.addEventListener('dragover', (e) => {
  e.preventDefault();
  dropZone.classList.add('dragover'); // Add CSS class for visual feedback
  console.log('File dragged over'); // Debug
});
// In app.js - Add debug statement
sendButton.addEventListener('click', () => {
  console.log('Send button clicked!'); // Check browser console for this message
  handleSendMessage();
});
chatInput.addEventListener('keypress', (e) => {
  if (e.key === 'Enter') handleSendMessage();
});

// Current state
let currentImage = null;
let currentPrediction = null;

// Handlers
async function handleFileSelect(e) {
  const file = e.target.files[0];
  if (file) processImageFile(file);
}

async function handleDrop(e) {
  e.preventDefault();
  dropZone.classList.remove('drop-zone--over');
  
  const file = e.dataTransfer.files[0];
  if (file && file.type.startsWith('image/')) {
    processImageFile(file);
  }
}

function handleDragOver(e) {
  e.preventDefault();
  dropZone.classList.add('drop-zone--over');
}

async function processImageFile(file) {
  try {
    clearResults();
    currentImage = file;
    
    // Show preview
    renderImagePreview(file);
    
    // Analyze image
    currentPrediction = await analyzeImage(file, modelType.value);
    renderPrediction(currentPrediction);
    
    // Update chat context
    chatSystem.updateImageContext(currentPrediction);
    
  } catch (error) {
    console.error('Error processing image:', error);
    alert('Failed to analyze image. Please try another.');
  }
}

async function handleSendMessage() {
  const message = chatInput.value.trim();
  if (!message) return;
  
  try {
    // Add user message to chat
    renderChatMessage(message, 'user');
    chatInput.value = '';
    
    // Get bot response
    const response = await chatSystem.sendMessage(message, currentPrediction);
    renderChatMessage(response, 'bot');
    
  } catch (error) {
    console.error('Chat error:', error);
    renderChatMessage("Sorry, I'm having trouble responding.", 'bot');
  }
}

function renderChatMessage(message, sender) {
  const chatHistory = document.getElementById('chatHistory');
  const messageElement = document.createElement('div');
  messageElement.classList.add('message', `${sender}-message`);
  messageElement.textContent = message;
  chatHistory.appendChild(messageElement);
  chatHistory.scrollTop = chatHistory.scrollHeight;
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
  console.log('App initialized');
});