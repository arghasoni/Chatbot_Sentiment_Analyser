def analyze_message(model, text):
    """
    Analyzes the sentiment of a single message.
    """
    if not text:
        return "Neutral"
        
    prompt = f"""
    Analyze the sentiment of this single message.
    Message: "{text}"
    
    Return ONLY one word: Positive, Negative, or Neutral.
    """
    
    try:
        response = model.generate_content(prompt)
        sentiment = response.text.strip()
        # Clean up
        for s in ["Positive", "Negative", "Neutral"]:
            if s in sentiment:
                return s
        return "Neutral"
    except Exception as e:
        print(f"Message Analysis Error: {e}")
        return "Neutral"

def analyze_conversation_llm(model, messages):
    """
    Analyzes the sentiment of a conversation using Google GenAI.
    """
    if not messages:
        return {"score": 0, "label": "Neutral", "summary": "No conversation."}
    
    combined_text = "\n".join(messages)
    prompt = f"""
    Analyze the sentiment of the following conversation with high precision.
    
    Instructions:
    1. Focus heavily on specific positive and negative keywords (e.g., "happy", "sad", "angry", "great", "terrible", "problem", "issue").
    2. Pay attention to the user's emotional state and the bot's ability to resolve or address it.
    3. Even if the conversation is polite, if the user expresses a problem that isn't resolved, the sentiment might lean negative or neutral.
    4. If the user expresses joy, gratitude, or satisfaction, the sentiment is positive.
    
    Conversation:
    {combined_text}
    
    Provide:
    1. A sentiment score between -1.0 (very negative) and 1.0 (very positive).
    2. A label (Positive, Negative, Neutral).
    3. A brief summary of the sentiment trend (e.g., "Started negative but ended positive").
    
    Return the result in JSON format like this:
    {{
        "score": 0.5,
        "label": "Positive",
        "summary": "The user started with a problem but was satisfied with the help."
    }}
    """
    
    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        
        # Debug logging
        print(f"Raw Sentiment Response: {text}")
        
        import re
        import json
        
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            json_str = match.group(0)
            result = json.loads(json_str)
            return result
        else:
            print("No JSON found in response")
            return {"score": 0, "label": "Error (No JSON)", "summary": "Could not analyze."}
            
    except Exception as e:
        print(f"Sentiment Analysis Error: {e}")
        return {"score": 0, "label": "Error", "summary": "Error during analysis."}
