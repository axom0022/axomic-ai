const chatArea = document.getElementById('chatArea');
const promptInput = document.getElementById('promptInput');
const sendBtn = document.getElementById('sendBtn');
const modeSelect = document.getElementById('modeSelect');
const themeToggle = document.getElementById('themeToggle');
const undoBtn = document.getElementById('undoBtn');
const redoBtn = document.getElementById('redoBtn');
const exportBtn = document.getElementById('exportBtn');
const importBtn = document.getElementById('importBtn');
const fileInput = document.getElementById('fileInput');
const urlInput = document.getElementById('urlInput');
const trainurlBtn = document.getElementById('trainurlBtn');
const trainurlstreamBtn = document.getElementById('trainurlstreamBtn');

function addMessage(text, type, ishtml=false) {
    const div = document.createElement('div');
    div.className = `message ${type}`;
    if (ishtml) {
        div.innerHTML = text;
    } else {
        div.textContent = text;
    }
    chatArea.appendChild(div);
    chatArea.scrollTop = chatArea.scrollHeight;
}

function sendMessage() {
    const prompt = promptInput.value.trim();
    if (!prompt) return;
    addMessage(prompt, 'user');
    promptInput.value = '';
    const mode = modeSelect.value;
    let endpoint = '/chat';
    if (mode === 'code') endpoint = '/generate/code';
    else if (mode === 'image') endpoint = '/generate/image';
    else if (mode === 'audio') endpoint = '/generate/audio';
    else if (mode === 'video') endpoint = '/generate/video';

    fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: prompt })
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) {
            addMessage('Error: ' + data.error, 'assistant');
            return;
        }
        let response = data.response || data.result || 'No response';
        addMessage(response, 'assistant');
    })
    .catch(err => {
        addMessage('Error: ' + err.message, 'assistant');
    });
}

sendBtn.addEventListener('click', sendMessage);
promptInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});

themeToggle.addEventListener('click', () => {
    document.body.classList.toggle('light');
    themeToggle.textContent = document.body.classList.contains('light') ? '☀️' : '🌙';
});

undoBtn.addEventListener('click', () => {
    fetch('/undo', { method: 'POST' })
    .then(res => res.json())
    .then(data => {
        addMessage(data.status || data.error, 'assistant');
    });
});

redoBtn.addEventListener('click', () => {
    fetch('/redo', { method: 'POST' })
    .then(res => res.json())
    .then(data => {
        addMessage(data.status || data.error, 'assistant');
    });
});

exportBtn.addEventListener('click', () => {
    const path = prompt('Export filename:', 'exported_model.pt');
    if (path) {
        fetch('/export', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ path: path })
        })
        .then(res => res.json())
        .then(data => {
            addMessage('Exported to ' + data.path, 'assistant');
        });
    }
});

importBtn.addEventListener('click', () => {
    fileInput.click();
});

fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (!file) return;
    const path = file.name;
    fetch('/import', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ path: path })
    })
    .then(res => res.json())
    .then(data => {
        addMessage(data.status || data.error, 'assistant');
    });
    fileInput.value = '';
});

function trainFromUrl(streaming) {
    const url = urlInput.value.trim();
    if (!url) return;
    const endpoint = streaming ? '/trainurlstream' : '/trainurl';
    addMessage('Training from URL (stream=' + streaming + '): ' + url, 'assistant');
    fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: url, epochs: 1, chunksize: 200 })
    })
    .then(res => res.json())
    .then(data => {
        addMessage(data.status || data.error, 'assistant');
    });
}

trainurlBtn.addEventListener('click', () => trainFromUrl(false));
trainurlstreamBtn.addEventListener('click', () => trainFromUrl(true));
