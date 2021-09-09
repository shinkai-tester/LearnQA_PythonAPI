import requests

nameParam = {'name': 'Sasha'}
response = requests.get("https://playground.learnqa.ru/api/hello", params=nameParam)
print(response.text)
