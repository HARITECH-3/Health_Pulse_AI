import requests

url = "http://127.0.0.1:8000/api/v1/chat/send"
payload = {
    "message": "Hello, testing the chatbot",
    "conversation_id": None,
    "user_id": 1
}

print("Sending request to", url)
try:
    r = requests.post(url, json=payload)
    print("Status:", r.status_code)
    print("Response:", r.text)
except Exception as e:
    print("Exception:", e)
