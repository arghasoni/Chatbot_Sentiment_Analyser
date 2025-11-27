import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv
from database import init_db, create_conversation, save_message, get_conversation_history, get_all_conversations
from sentiment_analysis import analyze_conversation_llm, analyze_message

load_dotenv()

app = Flask(__name__)

# Configuring Google GenAI
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-flash-latest')
else:
    print("WARNING: GOOGLE_API_KEY not found in .env file. LLM features will not work.")
    model = None

# Initializing DB
init_db()
    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message')
    conversation_id = data.get('conversation_id')
    
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    
    if not conversation_id:
        conversation_id = create_conversation()
    
    user_sentiment = "Neutral"
    if model:
        user_sentiment = analyze_message(model, user_message)
    
    # Save user message with sentiment
    save_message(conversation_id, 'user', user_message, user_sentiment)
    
    # Generating response using LLM
    if model:
        try:
            history = get_conversation_history(conversation_id)
            
            gemini_history = []
            for msg in history:
                role = "user" if msg['sender'] == 'user' else "model"
                gemini_history.append({"role": role, "parts": [msg['text']]})
            
            
            current_msg = gemini_history.pop()
            
            chat = model.start_chat(history=gemini_history)
            response = chat.send_message(current_msg['parts'][0])
            bot_response = response.text
            
        except Exception as e:
            print(f"LLM Error: {e}")
            bot_response = "I'm having trouble connecting to my brain right now. Please check my API key."
    else:
        bot_response = "I am not connected to the LLM. Please configure the API key."
    
    save_message(conversation_id, 'bot', bot_response)
    
    return jsonify({
        'response': bot_response, 
        'conversation_id': conversation_id,
        'user_sentiment': user_sentiment
    })

@app.route('/api/analyze', methods=['GET'])
def analyze():
    conversation_id = request.args.get('conversation_id')
    if not conversation_id:
        return jsonify({'error': 'No conversation ID provided'}), 400
        
    history = get_conversation_history(conversation_id)
    messages = [msg['text'] for msg in history]
    
    if model:
        result = analyze_conversation_llm(model, messages)
    else:
        result = {"score": 0, "label": "Neutral (No LLM)", "summary": "LLM not available."}
        
    return jsonify(result)

@app.route('/api/history', methods=['GET'])
def get_history():
    conversations = get_all_conversations()
    return jsonify(conversations)

@app.route('/api/history/<conversation_id>', methods=['GET'])
def get_conversation(conversation_id):
    messages = get_conversation_history(conversation_id)
    return jsonify(messages)

@app.route('/api/reset', methods=['POST'])
def reset():
    
    new_id = create_conversation()
    return jsonify({'status': 'New conversation started', 'conversation_id': new_id})

if __name__ == '__main__':
    app.run(debug=True)
