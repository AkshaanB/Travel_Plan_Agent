import requests
import json

url = "http://localhost:8000/chat"
headers = {"Content-Type": "application/json"}
data = {"text": "Plan a 3-day trip to Paris"}

response = requests.post(url, headers=headers, json=data)
print(json.dumps(response.json(), indent=2))
