import requests


class TestHomeworkCookie:

    def test_hw_cookie(self):
        url = "https://playground.learnqa.ru/api/homework_cookie"
        response = requests.get(url)

        cookies = dict(response.cookies)
        print(cookies)

        cookie_name = 'HomeWork'
        cookie_value = 'hw_value'

        assert response.status_code == 200, "Wrong response code"
        assert cookie_name in cookies, f"There is no cookie '{cookie_name}' in the response"
        assert cookies.get(cookie_name) == cookie_value, f"The value of the cookie '{cookie_name}' " \
                                                         f"is not equal to '{cookie_value}'"
