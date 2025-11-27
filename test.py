import requests
import json

BASE_URL = "http://127.0.0.1:5000/api"

def test_tier2():
    #Reset
    print("Resetting conversation...")
    resp = requests.post(f"{BASE_URL}/reset")
    data = resp.json()
    conv_id = data['conversation_id']
    print(f"Conversation ID: {conv_id}")
    
    #Send Negative Message
    print("\nSending negative message...")
    resp = requests.post(f"{BASE_URL}/chat", json={
        "message": "I am very angry with your service!",
        "conversation_id": conv_id
    })
    data = resp.json()
    print(f"User Sentiment: {data.get('user_sentiment')}")
    if data.get('user_sentiment') == 'Negative':
        print("PASS: Negative sentiment detected.")
    else:
        print(f"FAIL: Expected Negative, got {data.get('user_sentiment')}")
        
    #Send Positive Message
    print("\nSending positive message...")
    resp = requests.post(f"{BASE_URL}/chat", json={
        "message": "But the support agent was very kind and helpful.",
        "conversation_id": conv_id
    })
    data = resp.json()
    print(f"User Sentiment: {data.get('user_sentiment')}")
    if data.get('user_sentiment') == 'Positive':
        print("PASS: Positive sentiment detected.")
    else:
        print(f"FAIL: Expected Positive, got {data.get('user_sentiment')}")
        
    #Analyzing Trend
    print("\nAnalyzing trend...")
    resp = requests.get(f"{BASE_URL}/analyze?conversation_id={conv_id}")
    data = resp.json()
    print(f"Summary: {data.get('summary')}")
    if data.get('summary'):
        print("PASS: Summary received.")
    else:
        print("FAIL: No summary received.")

if __name__ == "__main__":
    test_tier2()
