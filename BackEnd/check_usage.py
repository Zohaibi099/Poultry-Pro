import requests
import json

# Your xAI Grok API key
API_KEY = "xai-TH5bwqSgBHz3qBVgFZ9YOxLMRBlYENOzlVouTqjaoosCc0gMAFvFLNmKi46Gnrnq11tqavPY09eJia7d"

# API endpoint for Grok
url = "https://api.x.ai/v1/chat/completions"

# JSON body (similar to your cURL command)
data = {
    "messages": [
        {"role": "system", "content": "You are a test assistant."},
        {"role": "user", "content": "Testing. Just say hi and hello world and nothing else."}
    ],
    "model": "grok-4-latest",
    "stream": False,
    "temperature": 0
}

# Headers
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

# Send POST request
response = requests.post(url, headers=headers, data=json.dumps(data))

print("\n=== API Response ===")
print(response.json())
