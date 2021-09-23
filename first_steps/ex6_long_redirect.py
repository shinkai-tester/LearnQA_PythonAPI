import requests

response = requests.post("https://playground.learnqa.ru/api/long_redirect")

for i in response.history:
    print(i.url)

print(len(response.history))
