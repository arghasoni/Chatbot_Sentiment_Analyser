document.addEventListener('DOMContentLoaded', () => {
    const chatWindow = document.getElementById('chat-window');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const endBtn = document.getElementById('end-btn');
    const newChatBtn = document.getElementById('new-chat-btn');
    const themeToggle = document.getElementById('theme-toggle');
    const sentimentResult = document.getElementById('sentiment-result');
    const sentimentLabel = document.getElementById('sentiment-label');
    const sentimentScore = document.getElementById('sentiment-score');
    const sentimentSummary = document.getElementById('sentiment-summary');
    const historyList = document.getElementById('history-list');

    let currentConversationId = null;

    // Theme Toggle Functionality
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'light') {
        document.body.classList.add('light-mode');
    }

    themeToggle.addEventListener('click', () => {
        document.body.classList.toggle('light-mode');
        const isLightMode = document.body.classList.contains('light-mode');
        localStorage.setItem('theme', isLightMode ? 'light' : 'dark');
    });

    // Format bot messages with markdown-like formatting
    function formatBotMessage(text) {
        // Escape HTML to prevent XSS
        let formatted = text
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;');

        // Convert markdown formatting to HTML
        // Bold: **text** or __text__
        formatted = formatted.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
        formatted = formatted.replace(/__(.+?)__/g, '<strong>$1</strong>');

        // Italic: *text* or _text_
        formatted = formatted.replace(/\*(.+?)\*/g, '<em>$1</em>');
        formatted = formatted.replace(/_(.+?)_/g, '<em>$1</em>');

        // Line breaks: Convert double newlines to paragraphs
        formatted = formatted.replace(/\n\n/g, '</p><p>');

        // Single line breaks
        formatted = formatted.replace(/\n/g, '<br>');

        // Wrap in paragraph tags
        formatted = '<p>' + formatted + '</p>';

        // Bullet points: lines starting with •, -, or *
        formatted = formatted.replace(/<p>([•\-\*])\s(.+?)<\/p>/g, '<p class="bullet-point">• $2</p>');

        return formatted;
    }

    function appendMessage(sender, text, sentiment = null) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', sender === 'user' ? 'user-message' : 'bot-message');

        const contentDiv = document.createElement('div');
        contentDiv.classList.add('message-content');

        // Text wrapper
        const textSpan = document.createElement('span');
        textSpan.classList.add('message-text');

        // Format bot messages with markdown-like formatting
        if (sender === 'bot') {
            const formattedText = formatBotMessage(text);
            textSpan.innerHTML = formattedText;
        } else {
            textSpan.textContent = text;
        }

        contentDiv.appendChild(textSpan);

        if (sender === 'user' && sentiment) {
            const sentimentSpan = document.createElement('span');
            sentimentSpan.classList.add('sentiment-tag');

            if (sentiment === 'Positive') sentimentSpan.classList.add('sentiment-positive');
            else if (sentiment === 'Negative') sentimentSpan.classList.add('sentiment-negative');
            else sentimentSpan.classList.add('sentiment-neutral');

            sentimentSpan.textContent = sentiment;
            contentDiv.appendChild(sentimentSpan);
        }

        messageDiv.appendChild(contentDiv);
        chatWindow.appendChild(messageDiv);

        chatWindow.scrollTop = chatWindow.scrollHeight;
    }

    async function sendMessage() {
        const text = userInput.value.trim();
        if (!text) return;

        // Clear input
        userInput.value = '';

        appendMessage('user', text);

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message: text,
                    conversation_id: currentConversationId
                })
            });

            const data = await response.json();

            if (data.conversation_id && data.conversation_id !== currentConversationId) {
                currentConversationId = data.conversation_id;
                loadHistoryList();
            }

            const userMessages = document.querySelectorAll('.user-message .message-content');
            if (userMessages.length > 0) {
                const lastUserMsg = userMessages[userMessages.length - 1];
                // Check if it already has a sentiment tag (it shouldn't)
                if (!lastUserMsg.querySelector('.sentiment-tag') && data.user_sentiment) {
                    const sentimentSpan = document.createElement('span');
                    sentimentSpan.classList.add('sentiment-tag');
                    if (data.user_sentiment === 'Positive') sentimentSpan.classList.add('sentiment-positive');
                    else if (data.user_sentiment === 'Negative') sentimentSpan.classList.add('sentiment-negative');
                    else sentimentSpan.classList.add('sentiment-neutral');
                    sentimentSpan.textContent = data.user_sentiment;
                    lastUserMsg.appendChild(sentimentSpan);
                }
            }

            // Adding bot response to UI
            appendMessage('bot', data.response);

        } catch (error) {
            console.error('Error sending message:', error);
            appendMessage('bot', 'Sorry, something went wrong.');
        }
    }

    async function endConversation() {
        if (!currentConversationId) return;

        try {
            const response = await fetch(`/api/analyze?conversation_id=${currentConversationId}`);
            const data = await response.json();

            sentimentLabel.textContent = data.label;
            sentimentScore.textContent = data.score.toFixed(4);
            if (sentimentSummary) {
                sentimentSummary.textContent = data.summary || "No summary available.";
            }

            if (data.label === 'Positive') {
                sentimentLabel.style.color = '#10b981';
            } else if (data.label === 'Negative') {
                sentimentLabel.style.color = '#ef4444';
            } else {
                sentimentLabel.style.color = '#f59e0b';
            }

            sentimentResult.classList.remove('hidden');
            setTimeout(() => {
                chatWindow.scrollTop = chatWindow.scrollHeight;
            }, 100);

        } catch (error) {
            console.error('Error analyzing sentiment:', error);
        }
    }

    async function resetConversation() {
        try {
            const response = await fetch('/api/reset', { method: 'POST' });
            const data = await response.json();

            currentConversationId = data.conversation_id;

            // Clear UI
            chatWindow.innerHTML = `
                <div class="message bot-message">
                    <div class="message-content">Hello! I'm ready to chat. I'll analyze our conversation sentiment when you're done.</div>
                </div>
            `;
            sentimentResult.classList.add('hidden');

            loadHistoryList();

        } catch (error) {
            console.error('Error resetting conversation:', error);
        }
    }

    async function loadHistoryList() {
        try {
            const response = await fetch('/api/history');
            const conversations = await response.json();

            historyList.innerHTML = '';

            conversations.forEach(conv => {
                const item = document.createElement('div');
                item.classList.add('history-item');
                if (conv.id === currentConversationId) {
                    item.classList.add('active');
                }

                const date = new Date(conv.created_at).toLocaleDateString();
                const preview = conv.last_message || 'New Conversation';

                item.innerHTML = `
                    <div class="history-date">${date}</div>
                    <div class="history-preview">${preview}</div>
                `;

                item.addEventListener('click', () => loadConversation(conv.id));
                historyList.appendChild(item);
            });

        } catch (error) {
            console.error('Error loading history:', error);
        }
    }

    async function loadConversation(id) {
        if (id === currentConversationId) return;

        try {
            const response = await fetch(`/api/history/${id}`);
            const messages = await response.json();

            currentConversationId = id;

            // Clear UI
            chatWindow.innerHTML = '';
            sentimentResult.classList.add('hidden');

            messages.forEach(msg => {
                appendMessage(msg.sender, msg.text, msg.sentiment);
            });

            document.querySelectorAll('.history-item').forEach(item => {
                item.classList.remove('active');
            });
            loadHistoryList();

        } catch (error) {
            console.error('Error loading conversation:', error);
        }
    }

    sendBtn.addEventListener('click', sendMessage);

    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    endBtn.addEventListener('click', endConversation);
    newChatBtn.addEventListener('click', resetConversation);

    loadHistoryList();
});
