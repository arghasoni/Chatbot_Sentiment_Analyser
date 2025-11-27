import sqlite3
import datetime
import uuid

DB_NAME = "chatbot.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    
    # Create conversations table
    c.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id TEXT PRIMARY KEY,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create messages table
    c.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id TEXT NOT NULL,
            sender TEXT NOT NULL,
            text TEXT NOT NULL,
            sentiment TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (conversation_id) REFERENCES conversations (id)
        )
    ''')
    
    try:
        c.execute('ALTER TABLE messages ADD COLUMN sentiment TEXT')
    except sqlite3.OperationalError:
        pass
    
    conn.commit()
    conn.close()

def create_conversation():
    conversation_id = str(uuid.uuid4())
    conn = get_db_connection()
    conn.execute('INSERT INTO conversations (id) VALUES (?)', (conversation_id,))
    conn.commit()
    conn.close()
    return conversation_id

def save_message(conversation_id, sender, text, sentiment=None):
    conn = get_db_connection()
    conn.execute('INSERT INTO messages (conversation_id, sender, text, sentiment) VALUES (?, ?, ?, ?)',
                 (conversation_id, sender, text, sentiment))
    conn.commit()
    conn.close()

def get_conversation_history(conversation_id):
    conn = get_db_connection()
    messages = conn.execute('SELECT * FROM messages WHERE conversation_id = ? ORDER BY timestamp ASC',
                            (conversation_id,)).fetchall()
    conn.close()
    return [dict(msg) for msg in messages]

def get_all_conversations():
    conn = get_db_connection()
    conversations = conn.execute('''
        SELECT c.id, c.created_at, 
               (SELECT text FROM messages WHERE conversation_id = c.id ORDER BY timestamp DESC LIMIT 1) as last_message
        FROM conversations c
        ORDER BY c.created_at DESC
    ''').fetchall()
    conn.close()
    return [dict(conv) for conv in conversations]
