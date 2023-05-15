import requests

url = "http://localhost:5000/login"
# url = "http://localhost:8000/login"
payload = {"username": "admin", "password": "password"}
response = requests.post(url, data=payload)

print(response.text)