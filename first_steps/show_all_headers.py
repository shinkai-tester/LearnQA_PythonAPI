import requests

headers = {"some_header": "123"}
response = requests.get("https://playground.learnqa.ru/api/show_all_headers", headers=headers)

print(response.text)
print(response.headers)
