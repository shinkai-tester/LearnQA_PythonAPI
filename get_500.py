import requests

response = requests.post("https://playground.learnqa.ru/api/get_500")
print(response.status_code)
print(response.text)
