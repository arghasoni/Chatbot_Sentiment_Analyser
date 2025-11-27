# 🤖 Chatbot_Sentiment_Analyser

A simple LLM-powered chatbot with conversation-level and message-level sentiment analysis. It keeps full chat history, evaluates the overall emotional direction of the conversation, and assigns sentiment to each user message.  

---

## Features

- **Interactive Chatbot UI** - Clean, responsive interface for natural conversations
- **Dual-Tier Sentiment Analysis :**
  - **Tier 1**: Real-time message-level sentiment scoring
  - **Tier 2**: AI-powered conversation-level insights and behavioral patterns
- **Conversation Management** - Store, view, analyze, and delete conversation histories
- **Google Gemini Integration** - Powered by advanced AI for intelligent responses  
- **Web-based chatbot interface** (via a Flask app).  

---

## Technology Stack Used

- **Python** — core programming language  
- **Flask** — for web server / chatbot UI (`app.py`, templates & static folders)  
- **SQLite** (or lightweight DB) — for storing conversation history (`chatbot.db`, `database.py`)  
- **Sentiment analysis module** — custom logic in `sentiment_analysis.py`  
- **Requirements**: see `requirements.txt` (external libraries, e.g., for NLP or LLM integration)  
- **Tests** — provided test scripts (`test.py`, `test_api.py`)  

---

## Sentiment Logic — How It Works

1. **Message-level sentiment**: Each user message is passed through the sentiment analysis logic (in `sentiment_analysis.py`) to classify its sentiment (e.g. positive / neutral / negative).  
2. **History tracking**: All messages from both ends (user + bot) are stored in a conversation log (database).  
3. **Conversation-level sentiment**: At the end of interaction, the system aggregates message-level sentiments (e.g., by counting or averaging) and determines the overall emotional direction of the full conversation.  
4. **Output**: The analysis result — overall mood (e.g., “ Positive”, “Neutral”, “Negative”) — is presented to the user.  

---

## Tier 2 Implementation Status

- ✅ **Statement-level sentiment analysis** — Implemented Successfully
- ✅ **Conversation-level sentiment summary** — Implemented Successfully

---
## Prerequisites

- Python 3.8 or higher
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))
- Git
  
---
## How to Run

1. **Clone the Repository**
   ```bash
   git clone https://github.com/arghasoni/Chatbot_Sentiment_Analyser.git
   cd ChatBot_Sentiment_Analyser
   ```

2. **Create a Virtual Environment**
   ```bash
   # macOS/Linux
   python -m venv venv
   source venv/bin/activate

   # Windows
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**
   
   Create a `.env` file in the root directory:
   ```env
   GOOGLE_API_KEY=your_gemini_api_key_here
   ```

5. **Run the Application**
   ```bash
   python app.py
   ```

6. **Access the Application**
   
   Open your browser and navigate to:
   ```
   http://localhost:5000
   ```
---
##  Project Structure

```
ChatBot_Sentiment_Analyser/
├── app.py                 # Main Flask application
├── database.py            # Database models and operations
├── sentiment_analysis.py  # Sentiment analysis logic
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (added to .gitignore)
├── test.py                # Unit & Functional Tests
├── test_api.py            # API Endpoint Tests
├── static/
│   ├── css/               # Stylesheets File
│   └── js/                # JavaScript File
├── templates/
│   └── index.html         # Main UI template
└── README.md
```
---

##  Key Innovations

1. **Two-Layer Sentiment Engine** – Utilizes both heuristic rules and AI-driven evaluation for stronger accuracy.
2. **Highly Modular System** – Components are clearly separated, making updates, debugging, and testing straightforward.
3. **Rich Conversation Logging** – Each stored message includes:
   - Complete message text
   - User/bot identifier
   - Calculated sentiment value
   - Exact timestamp for ordering
4. **LLM-Enhanced Interpretation** – Provides deeper contextual understanding rather than basic polarity detection.
5. **Scalable Framework** – Built to support future additions like visual analytics, ML upgrades, and detailed dashboards.
---

## Author

**Argha Biswas**
- GitHub: [@arghasoni](https://github.com/arghasoni)
- Linked In: [Argha Biswas](https://www.linkedin.com/in/arghabiswas2004/)
