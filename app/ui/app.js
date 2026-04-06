// Application State
const appState = {
  currentPage: 'dashboard',
  sidebarCollapsed: false,
  files: [
    { name: 'voice_sample_01.mp3', size: '2.4 MB', date: '2025-10-28', type: 'audio/mp3' },
    { name: 'presentation_audio.wav', size: '5.1 MB', date: '2025-10-27', type: 'audio/wav' },
    { name: 'podcast_episode_final.m4a', size: '8.7 MB', date: '2025-10-26', type: 'audio/m4a' },
    { name: 'demo_voice.mp3', size: '1.8 MB', date: '2025-10-25', type: 'audio/mp3' }
  ],
  voices: [
    { id: 1, name: 'Natural Male', type: 'instant', language: 'English', style: 'Professional' },
    { id: 2, name: 'Natural Female', type: 'instant', language: 'English', style: 'Friendly' },
    { id: 3, name: 'Premium Voice 1', type: 'premium', language: 'English', style: 'Formal' },
    { id: 4, name: 'Casual Voice', type: 'instant', language: 'English', style: 'Natural' }
  ],
  chatMessages: [
    { role: 'assistant', content: 'Welcome to Voice Cloning Studio! How can I help you today?' },
    { role: 'user', content: 'I want to clone my voice' },
    { role: 'assistant', content: 'Great! You can choose between Instant Clone or Premium Clone. Which would you prefer?' }
  ],
  selectedCloneType: null
};

// Initialize App
function init() {
  setupNavigation();
  setupSidebarToggle();
  setupQuickActions();
  setupVoiceCloning();
  setupTextToSpeech();
  setupFileStorage();
  setupChat();
  setupModal();
  
  // Render initial data
  renderRecentFiles();
  renderVoiceLibrary();
  renderAllFiles();
  renderChatMessages();
}

// Navigation
function setupNavigation() {
  const navItems = document.querySelectorAll('.nav-item');
  const viewAllLinks = document.querySelectorAll('.view-all');
  
  navItems.forEach(item => {
    item.addEventListener('click', (e) => {
      e.preventDefault();
      const page = item.dataset.page;
      navigateToPage(page);
    });
  });
  
  viewAllLinks.forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      const page = link.dataset.page;
      navigateToPage(page);
    });
  });
}

function navigateToPage(page) {
  // Update active nav item
  document.querySelectorAll('.nav-item').forEach(item => {
    item.classList.remove('active');
    if (item.dataset.page === page) {
      item.classList.add('active');
    }
  });
  
  // Hide all pages
  document.querySelectorAll('.page').forEach(p => {
    p.style.display = 'none';
  });
  
  // Show selected page
  const selectedPage = document.getElementById(`${page}-page`);
  if (selectedPage) {
    selectedPage.style.display = 'block';
  }
  
  // Update page title
  const titles = {
    'dashboard': 'Dashboard',
    'voice-cloning': 'Voice Cloning',
    'text-to-speech': 'Text-to-Speech',
    'voice-library': 'Voice Library',
    'file-storage': 'File Storage',
    'chat': 'Chat Assistant',
    'settings': 'Settings',
    'profile': 'Profile'
  };
  
  document.getElementById('pageTitle').textContent = titles[page] || 'Dashboard';
  appState.currentPage = page;
}

// Sidebar Toggle
function setupSidebarToggle() {
  const sidebar = document.getElementById('sidebar');
  const mainContent = document.getElementById('mainContent');
  const toggleBtn = document.getElementById('sidebarToggle');
  
  toggleBtn.addEventListener('click', () => {
    sidebar.classList.toggle('collapsed');
    mainContent.classList.toggle('expanded');
    appState.sidebarCollapsed = !appState.sidebarCollapsed;
  });
}

// Quick Actions
function setupQuickActions() {
  const actionCards = document.querySelectorAll('.action-card');
  
  actionCards.forEach(card => {
    card.addEventListener('click', () => {
      const action = card.dataset.action;
      navigateToPage(action);
    });
  });
}

// Voice Cloning
function setupVoiceCloning() {
  const cloneSelectBtns = document.querySelectorAll('.clone-select-btn');
  const uploadSection = document.getElementById('uploadSection');
  const uploadZone = document.getElementById('uploadZone');
  const browseBtn = document.getElementById('browseBtn');
  const fileInput = document.getElementById('fileInput');
  
  cloneSelectBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const type = btn.dataset.type;
      appState.selectedCloneType = type;
      
      // Update minimum duration based on type
      const minDuration = type === 'instant' ? '30 seconds' : '10 minutes';
      document.getElementById('minDuration').textContent = minDuration;
      
      // Show upload section
      uploadSection.style.display = 'block';
      uploadSection.scrollIntoView({ behavior: 'smooth' });
      
      showToast(`${type === 'instant' ? 'Instant' : 'Premium'} Clone selected!`);
    });
  });
  
  // Drag and drop
  uploadZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadZone.classList.add('drag-over');
  });
  
  uploadZone.addEventListener('dragleave', () => {
    uploadZone.classList.remove('drag-over');
  });
  
  uploadZone.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadZone.classList.remove('drag-over');
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      handleFileUpload(files[0]);
    }
  });
  
  // Browse button
  browseBtn.addEventListener('click', () => {
    fileInput.click();
  });
  
  fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
      handleFileUpload(e.target.files[0]);
    }
  });
}

function handleFileUpload(file) {
  if (!file.type.includes('audio')) {
    showToast('Please upload an audio file', 'error');
    return;
  }
  
  showToast('Uploading file...');
  
  // Simulate upload and processing
  const processingStatus = document.getElementById('processingStatus');
  processingStatus.style.display = 'block';
  
  let progress = 0;
  const interval = setInterval(() => {
    progress += 5;
    document.getElementById('progressFill').style.width = `${progress}%`;
    document.getElementById('progressText').textContent = `${progress}%`;
    
    if (progress >= 100) {
      clearInterval(interval);
      setTimeout(() => {
        showToast('Voice cloning completed successfully!', 'success');
        processingStatus.style.display = 'none';
        document.getElementById('uploadSection').style.display = 'none';
        
        // Add to files
        appState.files.unshift({
          name: file.name,
          size: (file.size / (1024 * 1024)).toFixed(1) + ' MB',
          date: new Date().toISOString().split('T')[0],
          type: file.type
        });
        
        renderRecentFiles();
        renderAllFiles();
      }, 1000);
    }
  }, 100);
}

// Text-to-Speech
function setupTextToSpeech() {
  const ttsInput = document.getElementById('ttsInput');
  const charCount = document.getElementById('charCount');
  const generateBtn = document.getElementById('generateBtn');
  const previewSection = document.getElementById('previewSection');
  const playBtn = document.getElementById('playBtn');
  
  ttsInput.addEventListener('input', () => {
    const length = ttsInput.value.length;
    charCount.textContent = `${length} / 5000`;
  });
  
  generateBtn.addEventListener('click', () => {
    const text = ttsInput.value.trim();
    
    if (!text) {
      showToast('Please enter some text', 'error');
      return;
    }
    
    generateBtn.disabled = true;
    generateBtn.innerHTML = '<span>⏳ Generating...</span>';
    
    // Simulate generation
    setTimeout(() => {
      generateBtn.disabled = false;
      generateBtn.innerHTML = '<span>🔊 Generate Speech</span>';
      previewSection.style.display = 'block';
      previewSection.scrollIntoView({ behavior: 'smooth' });
      showToast('Speech generated successfully!', 'success');
    }, 2000);
  });
  
  // Audio player
  let isPlaying = false;
  playBtn.addEventListener('click', () => {
    isPlaying = !isPlaying;
    
    if (isPlaying) {
      playBtn.innerHTML = `
        <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
          <rect x="6" y="4" width="4" height="16"></rect>
          <rect x="14" y="4" width="4" height="16"></rect>
        </svg>
      `;
      showToast('Playing audio...');
    } else {
      playBtn.innerHTML = `
        <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
          <polygon points="5 3 19 12 5 21 5 3"></polygon>
        </svg>
      `;
    }
  });
  
  // Export formats
  const formatBtns = document.querySelectorAll('.format-btn');
  formatBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const format = btn.textContent.split(' ')[1];
      showToast(`Exporting as ${format}...`, 'success');
    });
  });
}

// File Storage
function setupFileStorage() {
  const viewBtns = document.querySelectorAll('.view-btn');
  const filesContainer = document.getElementById('filesContainer');
  const uploadFileBtn = document.getElementById('uploadFileBtn');
  
  viewBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      viewBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      
      const view = btn.dataset.view;
      filesContainer.classList.remove('grid-view', 'list-view');
      filesContainer.classList.add(`${view}-view`);
    });
  });
  
  uploadFileBtn.addEventListener('click', () => {
    showToast('Upload feature coming soon!');
  });
}

// Chat
function setupChat() {
  const chatInput = document.getElementById('chatInput');
  const sendBtn = document.getElementById('sendBtn');
  const suggestionChips = document.querySelectorAll('.suggestion-chip');
  
  sendBtn.addEventListener('click', () => {
    sendMessage();
  });
  
  chatInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
      sendMessage();
    }
  });
  
  suggestionChips.forEach(chip => {
    chip.addEventListener('click', () => {
      chatInput.value = chip.textContent;
      sendMessage();
    });
  });
}

function sendMessage() {
  const chatInput = document.getElementById('chatInput');
  const message = chatInput.value.trim();
  
  if (!message) return;
  
  // Add user message
  appState.chatMessages.push({ role: 'user', content: message });
  chatInput.value = '';
  
  // Simulate AI response
  setTimeout(() => {
    const responses = [
      'I can help you with that! Let me guide you through the process.',
      'Great question! The main difference is the quality and processing time.',
      'Yes, you can use your cloned voice commercially with our Premium plan.',
      'You have 45 MB used out of 1 GB total storage.',
      'You can export audio in MP3, WAV, OGG, or M4A formats.'
    ];
    
    const randomResponse = responses[Math.floor(Math.random() * responses.length)];
    appState.chatMessages.push({ role: 'assistant', content: randomResponse });
    renderChatMessages();
  }, 1000);
  
  renderChatMessages();
}

// Render Functions
function renderRecentFiles() {
  const container = document.getElementById('recentFiles');
  const recentFiles = appState.files.slice(0, 4);
  
  container.innerHTML = recentFiles.map(file => `
    <div class="file-card">
      <div class="file-icon">
        ${getFileIcon(file.type)}
      </div>
      <div class="file-name">${file.name}</div>
      <div class="file-info">
        <span>${file.size}</span>
        <span>${file.date}</span>
      </div>
      <div class="file-actions">
        <button class="file-action-btn" onclick="playFile('${file.name}')">▶️</button>
        <button class="file-action-btn" onclick="downloadFile('${file.name}')">⬇️</button>
      </div>
    </div>
  `).join('');
}

function renderAllFiles() {
  const container = document.getElementById('filesContainer');
  
  container.innerHTML = appState.files.map(file => `
    <div class="file-card">
      <div class="file-icon">
        ${getFileIcon(file.type)}
      </div>
      <div class="file-details">
        <div class="file-name">${file.name}</div>
        <div class="file-info">
          <span>${file.size}</span>
          <span>${file.date}</span>
        </div>
      </div>
      <div class="file-actions">
        <button class="file-action-btn" onclick="playFile('${file.name}')">▶️</button>
        <button class="file-action-btn" onclick="downloadFile('${file.name}')">⬇️</button>
        <button class="file-action-btn" onclick="deleteFile('${file.name}')">🗑️</button>
      </div>
    </div>
  `).join('');
}

function renderVoiceLibrary() {
  const container = document.getElementById('voicesGrid');
  
  container.innerHTML = appState.voices.map(voice => `
    <div class="voice-card">
      <div class="voice-card-header">
        <div>
          <h4>${voice.name}</h4>
        </div>
        <span class="voice-type-badge ${voice.type}">${voice.type}</span>
      </div>
      <div class="voice-meta">
        <span>🌍 ${voice.language}</span>
        <span>🎭 ${voice.style}</span>
      </div>
      <div class="voice-card-footer">
        <button class="voice-action-btn" onclick="previewVoice(${voice.id})">▶️ Preview</button>
        <button class="voice-action-btn" onclick="selectVoice(${voice.id})">✓ Select</button>
      </div>
    </div>
  `).join('');
  
  // Setup filter buttons
  const filterBtns = document.querySelectorAll('.filter-btn');
  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      filterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      
      const filter = btn.dataset.filter;
      const filtered = filter === 'all' 
        ? appState.voices 
        : appState.voices.filter(v => v.type === filter);
      
      container.innerHTML = filtered.map(voice => `
        <div class="voice-card">
          <div class="voice-card-header">
            <div>
              <h4>${voice.name}</h4>
            </div>
            <span class="voice-type-badge ${voice.type}">${voice.type}</span>
          </div>
          <div class="voice-meta">
            <span>🌍 ${voice.language}</span>
            <span>🎭 ${voice.style}</span>
          </div>
          <div class="voice-card-footer">
            <button class="voice-action-btn" onclick="previewVoice(${voice.id})">▶️ Preview</button>
            <button class="voice-action-btn" onclick="selectVoice(${voice.id})">✓ Select</button>
          </div>
        </div>
      `).join('');
    });
  });
}

function renderChatMessages() {
  const container = document.getElementById('chatMessages');
  
  container.innerHTML = appState.chatMessages.map(msg => `
    <div class="chat-message ${msg.role}">
      <div class="message-avatar">
        ${msg.role === 'user' ? 'JD' : '🤖'}
      </div>
      <div class="message-content">
        ${msg.content}
      </div>
    </div>
  `).join('');
  
  // Scroll to bottom
  container.scrollTop = container.scrollHeight;
}

// Helper Functions
function getFileIcon(type) {
  if (type.includes('mp3')) return '🎵';
  if (type.includes('wav')) return '🎼';
  if (type.includes('m4a')) return '🍎';
  if (type.includes('ogg')) return '🌐';
  return '🎵';
}

function playFile(name) {
  showToast(`Playing ${name}...`);
}

function downloadFile(name) {
  showToast(`Downloading ${name}...`, 'success');
}

function deleteFile(name) {
  const confirmed = confirm(`Are you sure you want to delete ${name}?`);
  if (confirmed) {
    appState.files = appState.files.filter(f => f.name !== name);
    renderRecentFiles();
    renderAllFiles();
    showToast('File deleted successfully', 'success');
  }
}

function previewVoice(id) {
  const voice = appState.voices.find(v => v.id === id);
  showToast(`Previewing ${voice.name}...`);
}

function selectVoice(id) {
  const voice = appState.voices.find(v => v.id === id);
  showToast(`${voice.name} selected!`, 'success');
}

// Modal
function setupModal() {
  const modal = document.getElementById('modal');
  const modalClose = document.getElementById('modalClose');
  
  modalClose.addEventListener('click', () => {
    modal.classList.remove('show');
  });
  
  modal.addEventListener('click', (e) => {
    if (e.target === modal) {
      modal.classList.remove('show');
    }
  });
}

function showModal(title, content) {
  const modal = document.getElementById('modal');
  document.getElementById('modalTitle').textContent = title;
  document.getElementById('modalBody').innerHTML = content;
  modal.classList.add('show');
}

// Toast Notification
function showToast(message, type = 'info') {
  const toast = document.getElementById('toast');
  const toastMessage = document.getElementById('toastMessage');
  
  toastMessage.textContent = message;
  toast.classList.add('show');
  
  setTimeout(() => {
    toast.classList.remove('show');
  }, 3000);
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}