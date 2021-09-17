import requests

payload = {"name": "Sasha"}
response = requests.get("https://playground.learnqa.ru/api/hello", params=payload)
print(response.text)
