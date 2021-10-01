import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
from datetime import datetime
from faker import Faker


class TestUserRegister(BaseCase):
    def setup(self):
        fake = Faker()
        base_part = "learnqa"
        domain = "example.com"
        random_part = datetime.now().strftime("%m%d%Y%H%M%S")
        self.email = f"{base_part}{random_part}@{domain}"
        self.firstName = fake.first_name()
        self.lastName = fake.last_name()
        self.username = fake.user_name()

    def test_create_user_successfully(self):
        data = {
            'password': '123',
            'username': self.username,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'email': self.email
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_status_code(response, 200)
        Assertions.assert_json_has_key(response, "id")
        print(self.email)

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_status_code(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", \
            f'Unexpected response content {response.content} '
