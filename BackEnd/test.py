import requests

response = requests.post(
    "http://127.0.0.1:8000/chat",
    json={"message": "Meri murghi anday nahi de rahi"},
)

print("Bot Reply:", response.json())
