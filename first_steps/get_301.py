import requests

response = requests.post("https://playground.learnqa.ru/api/get_301", allow_redirects=True)
first_response = response.history[0]
second_response = response

print(response.status_code)

print(first_response.url)
print(second_response.url)
