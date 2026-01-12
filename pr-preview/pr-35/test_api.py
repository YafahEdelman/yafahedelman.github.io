import requests
import json

url = "https://text.pollinations.ai/"
headers = {
    "Content-Type": "application/json"
}

# Test 1: No Auth, model 'openai'
print("--- Test 1: No Auth, model 'openai' ---")
data1 = {
    "messages": [{"role": "user", "content": "Say hello"}],
    "model": "openai",
    "jsonMode": False
}
try:
    response = requests.post(url, headers=headers, json=data1, timeout=30)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text[:200]}")
except Exception as e:
    print(f"Error: {e}")

# Test 2: Auth, model 'openai'
print("\n--- Test 2: Auth, model 'openai' ---")
headers_auth = {
    "Content-Type": "application/json",
    "Authorization": "Bearer pk_w1ydtl3pBtnBNHuj"
}
data2 = {
    "messages": [{"role": "user", "content": "Say hello"}],
    "model": "openai",
    "jsonMode": False
}
try:
    response = requests.post(url, headers=headers_auth, json=data2, timeout=30)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text[:200]}")
except Exception as e:
    print(f"Error: {e}")

# Test 3: Auth, model 'gpt-4o-mini' (This failed before, but let's try root url)
print("\n--- Test 3: Auth, model 'gpt-4o-mini' to root url ---")
data3 = {
    "messages": [{"role": "user", "content": "Say hello"}],
    "model": "gpt-4o-mini",
    "jsonMode": False
}
try:
    response = requests.post(url, headers=headers_auth, json=data3, timeout=30)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text[:200]}")
except Exception as e:
    print(f"Error: {e}")
