// Add Quill fonts and size whitelist (optional)
const Font = Quill.import('formats/font');
Font.whitelist = ['sans-serif', 'serif', 'monospace'];
Quill.register(Font, true);

const Size = Quill.import('formats/size');
Size.whitelist = ['small', 'normal', 'large', 'huge'];
Quill.register(Size, true);

// Initialize Quill with toolbar options
const quill = new Quill('#editor-container', {
    theme: 'snow',
    modules: {
        toolbar: '#toolbar'
    },
    placeholder: 'Start typing...'
});

const docId = window.location.pathname.split('/').slice(-2, -1)[0];
const socket = new WebSocket(
    'ws://' + window.location.host + '/ws/edit/' + docId + '/'
);

let isRemoteUpdate = false;
let saveTimeout = null;

// Send changes through WebSocket + debounce DB save
quill.on('text-change', () => {
    if (isRemoteUpdate) return;
    const html = quill.root.innerHTML;

    // Broadcast to other users
    socket.send(JSON.stringify({ content: html }));

    // Debounce DB save (every 2 seconds)
    if (saveTimeout) clearTimeout(saveTimeout);
    saveTimeout = setTimeout(() => {
        socket.send(JSON.stringify({ content: html, save: true }));
    }, 2000);
});

// Receive changes from other users
socket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    if (data.content !== quill.root.innerHTML) {
        isRemoteUpdate = true;
        quill.root.innerHTML = data.content;
        isRemoteUpdate = false;
    }
};

// Grammar check using LanguageTool API
function getGrammarSuggestions() {
    document.getElementById('suggestions').innerText = "Checking grammar...";
    const content = quill.root.innerHTML;

    fetch(`/editor/${docId}/grammar/`, {
        method: 'POST',
        body: JSON.stringify({ content }),
        headers: { 'Content-Type': 'application/json' }
    })
    .then(res => res.json())
    .then(data => {
        const suggestionsDiv = document.getElementById('suggestions');
        if (data.error) {
            suggestionsDiv.innerText = `Error: ${data.error}`;
        } else if (data.matches && data.matches.length > 0) {
            suggestionsDiv.innerText = JSON.stringify(data.matches, null, 2);
        } else {
            suggestionsDiv.innerText = "No grammar issues found.";
        }
    })
    .catch(err => {
        document.getElementById('suggestions').innerText = `Error: ${err.message}`;
    });
}

// AI suggestion using OpenAI
function getOpenAISuggestion() {
    document.getElementById('suggestions').innerText = "Improving text...";

    fetch(`/editor/${docId}/openai/`, {
        method: 'POST',
        body: JSON.stringify({ content: quill.root.innerHTML }),
        headers: { 'Content-Type': 'application/json' }
    })
    .then(res => res.json())
    .then(data => {
        const suggestionsDiv = document.getElementById('suggestions');

        if (data.error) {
            suggestionsDiv.innerText = `Error: ${data.error}`;
        } else {
            // Handle both string or object type for `data.suggested`
            let suggestion = "";

            if (typeof data.suggested === 'string') {
                suggestion = data.suggested;
            } else if (typeof data.suggested === 'object') {
                suggestion = data.suggested.text || JSON.stringify(data.suggested, null, 2);
            }

            suggestionsDiv.innerHTML = `
                <div><strong>Suggested:</strong></div>
                <div class="mt-2 p-2 border bg-white rounded">${suggestion}</div>
                ${data.tokens_used ? `<div class="mt-2 text-gray-500 text-xs">Tokens used: ${data.tokens_used}</div>` : ''}
            `;
        }
    })
    .catch(err => {
        document.getElementById('suggestions').innerText = `Error: ${err.message}`;
    });
}
