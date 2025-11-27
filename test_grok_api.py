import requests
import os
from dotenv import load_dotenv

load_dotenv("Gurukul_new-main/Backend/.env")

# Test the Grok API endpoint
base_url = "https://43956d08ec05.ngrok-free.app"
api_url = f"{base_url}/v1/chat/completions"

headers = {
    "Content-Type": "application/json",
    "ngrok-skip-browser-warning": "true"
}

payload = {
    "model": "llama3.1:latest",
    "messages": [{"role": "user", "content": "Hello, say hi back!"}],
    "temperature": 0.7,
    "max_tokens": 100
}

print(f"Testing: {api_url}")
print(f"Model: {payload['model']}")

try:
    response = requests.post(api_url, headers=headers, json=payload, timeout=30)
    print(f"\nStatus: {response.status_code}")
    print(f"Response: {response.text[:500]}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"\n✅ SUCCESS!")
        print(f"Content: {result['choices'][0]['message']['content']}")
    else:
        print(f"\n❌ FAILED: {response.status_code}")
        
except Exception as e:
    print(f"\n❌ ERROR: {e}")
