import requests
import time

# Test chat speed
base_url = "http://localhost:8001"

print("Testing chat response speed...")
print("=" * 50)

# Step 1: Send message
start = time.time()
response1 = requests.post(
    f"{base_url}/chatpost",
    params={"user_id": "test-user"},
    json={"message": "Hello", "llm": "grok", "type": "chat_message"}
)
post_time = time.time() - start
print(f"1. POST /chatpost: {post_time:.2f}s - Status: {response1.status_code}")

# Step 2: Get response
start = time.time()
response2 = requests.get(
    f"{base_url}/chatbot",
    params={"user_id": "test-user"}
)
get_time = time.time() - start
print(f"2. GET /chatbot: {get_time:.2f}s - Status: {response2.status_code}")

if response2.status_code == 200:
    data = response2.json()
    if 'response' in data:
        print(f"\n✅ Response: {data['response']['message'][:100]}...")
    else:
        print(f"\n❌ No response in data: {data}")
else:
    print(f"\n❌ Error: {response2.text}")

print(f"\nTotal time: {post_time + get_time:.2f}s")
