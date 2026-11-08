import requests

url = "https://api.groq.com/openai/v1/chat/completions"

# REPLACE THIS WITH YOUR ACTUAL KEY
API_KEY = "GROQ_API_KEY"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

data = {
    "model": "openai/gpt-oss-120b", 
    "messages": [{"role": "user", "content": "What is 150 * 4?"}]
}

try:
    response = requests.post(url, headers=headers, json=data)
    print("Status Code:", response.status_code)
    print("Response:", response.json())
except Exception as e:
    print("Error:", e)