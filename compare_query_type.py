import requests

# http-запрос любого типа без параметра method
response = requests.delete("https://playground.learnqa.ru/ajax/api/compare_query_type")
print(response.text)
print(response.status_code)

print("----------------------------------------")

# http-запрос не из списка
response = requests.head("https://playground.learnqa.ru/ajax/api/compare_query_type")
print(response.text)
print(response.status_code)

print("----------------------------------------")

# запрос с правильным значением method
response = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method": "POST"})
print(response.text)
print(response.status_code)

"""
С помощью цикла проверяет все возможные сочетания реальных типов запроса и значений параметра method. 
Например, с GET-запросом передает значения параметра method равное ‘GET’, затем ‘POST’, ‘PUT’, ‘DELETE’ и так далее. 
И так для всех типов запроса. Найти такое сочетание, когда реальный тип запроса не совпадает со значением параметра, 
но сервер отвечает так, словно все ок. Или же наоборот, когда типы совпадают, но сервер считает, что это не так.
"""
requestTypes = ['GET', 'POST', 'PUT', 'DELETE']

for i in requestTypes:
    responseForGETReq = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", params={"method": i})
    responseForPOSTReq = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method": i})
    responseForPUTReq = requests.put("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method": i})
    responseForDELETEReq = requests.delete("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method": i})
    if responseForGETReq:
        print('Type of the request is GET, method is %s\n'
              'Response text: %s, status code is %s' % (i, responseForGETReq.text, responseForGETReq.status_code))
        print('===========================================')
    if responseForPOSTReq:
        print('Type of the request is POST, method is %s\n'
              'Response text: %s, status code is %s' % (i, responseForPOSTReq.text, responseForPOSTReq.status_code))
        print('===========================================')
    if responseForPUTReq:
        print('Type of the request is PUT, method is %s\n'
              'Response text: %s, status code is %s' % (i, responseForPUTReq.text, responseForPUTReq.status_code))
        print('===========================================')
    if responseForDELETEReq:
        print('Type of the request is DELETE, method is %s\n'
              'Response text: %s, status code is %s' % (i, responseForDELETEReq.text, responseForDELETEReq.status_code))
        print('===========================================')