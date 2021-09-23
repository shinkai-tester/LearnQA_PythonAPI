import requests


class TestHomeworkHeader:

    def test_hw_header(self):
        url = "https://playground.learnqa.ru/api/homework_header"
        response = requests.get(url)

        headers = response.headers
        print(headers)

        header_name = 'x-secret-homework-header'
        header_value = 'Some secret value'

        assert response.status_code == 200, "Wrong response code"
        assert header_name in headers, f"There is no header '{header_name}' in the response"
        assert headers.get(header_name) == header_value, f"The value of the header '{header_name}' " \
                                                         f"is not equal to '{header_value}'"
